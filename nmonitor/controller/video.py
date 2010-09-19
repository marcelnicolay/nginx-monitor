# coding: utf-8
#!/usr/bin/env python

from torneira.controller import BaseController, render_to_extension
from torneira.cache import get_cache
from torneira.core.meta import TorneiraSession
from api.models.video import Video
from api.models.tag import Tag
from api.controller import authenticated, tokenizer
from tornado.web import HTTPError
from api.models.videoqueue import VideoQueue
import uuid, re, os
import settings
import simplexml
import logging

from datetime import datetime

class VideoController(BaseController):

    @tokenizer
    @render_to_extension
    def index(self, videos_id, extension, **kw):

        videos_id = videos_id.split(',')

        if len(videos_id) == 1:
            video_id = int(videos_id[0])
            video = Video().get(video_id)
        
            if not video:
                raise HTTPError(404)

            video.tags = video.getTags()
            video.setUri(extension)
            return {'video':video.as_dict()}

        videos = []
        for video_id in videos_id:
            video_id = int(video_id)
            video = Video().get(video_id)

            video.tags = video.getTags()
            video.setUri(extension)
            videos.append(video.as_dict())
        
        return {'videos': {'total':len(videos), 'videos': videos}}

    @tokenizer    
    @authenticated
    @render_to_extension
    def create(self, usuario, extension, **kw):
        video_data = simplexml.loads(self.handler.request.body.replace('\n',''))['video']
        videoqueue = VideoQueue()

        tags = []
        if video_data.get('tags'):
            if isinstance(video_data.get('tags'), list):
                tags = [t['tag'] for t in video_data.get('tags')]
            else:
                tags = [video_data.get('tags')['tag']]

        # campos obrigatorios
        videoqueue.id_usuario = usuario.id
        videoqueue.titulo = video_data['titulo']
        videoqueue.criacao = datetime.now()
        videoqueue.descricao = video_data['descricao']
        videoqueue.tags = ",".join([str(t._id) for t in Tag.getTags(tags)])
        videoqueue.id_canal = video_data.get('canal')

        # nao obrigatorios
        videoqueue.thread_idioma = video_data.get('idioma') or 99
        videoqueue.privacidade = video_data.get('privacidade') or '0'
        videoqueue.download = video_data.get('download') or '0'
        videoqueue.uso_comercial = video_data.get('uso_comercial') or '1'
        videoqueue.alteracao_obra = video_data.get('alteracao_obra') or '1'
        videoqueue.divulgar_video = video_data.get('divulgar_video') or '0'
        videoqueue.indicar = video_data.get('indicar') or '0'
        videoqueue.censura = video_data.get('censura') or '0'
        videoqueue.indicar = video_data.get('indicar') or '0'

        videoqueue.uuid = str(uuid.uuid4())
        
        cache = get_cache()
        cache.set(key=videoqueue.uuid, value=videoqueue, timeout=60*30)
        
        return {'video':{'uuid':videoqueue.uuid}}
    
    @tokenizer
    @authenticated
    def upload(self, usuario, uuid, **kargs):

        cache = get_cache()
        video = cache.get(uuid)

        if not video:
            raise HTTPError(404)
        
        video_data = self.handler.request.files.get('video')

        if not video_data: raise HTTPError(500)

        video_data = video_data[0]
        
        try:
            return video.publicar(video_data)
        except Exception, e:
            logging.exception("Erro ao publicar o video")
            raise HTTPError(500)
    
    @tokenizer
    @authenticated   
    def delete(self, usuario, video_id, **kw):
        
        video_id = int(video_id)
        video = Video().get(video_id)
        
        if not video:
            raise HTTPError(404)
            
        if not video.usuario_id == usuario.id:
            raise HTTPError(401)
                
        try:
            session = TorneiraSession()
            session.begin()
            session.execute(" DELETE FROM video where id_video = %s " % video.id)
            
            os.remove("/dados/nfs/videolog/videos/" + video.getFLV())
            
            #remove todos os comentarios do video
            session.execute("DELETE FROM video_comentario WHERE id_video = %s" % video.id);
            #remove dos favoritos
            session.execute("DELETE FROM playlist WHERE id_video = %s" % video.id);
            #remove dos destaques
            session.execute("DELETE FROM video_destaque WHERE id_video = %s" % video.id);
            #remove da busca
            session.execute("DELETE FROM video_titulo WHERE id_video = %s" % video.id);
            
            session.commit()
        except Exception, e:
            session.rollback()
            logging.exception("erro ao remover video %s" % video.id)
            raise HTTPError(500)
    
    @authenticated
    def update(self, video_id, usuario, **kw):
        pass
    
    @tokenizer
    @render_to_extension
    def comentarios(self, video_id, extension, **kw):

        video_id = int(video_id)
        video = Video().get(video_id)
        
        if not video:
            raise HTTPError(404)

        video.comentarios = video._comentarios[:]

        return {'video':video.as_dict()}

    @tokenizer
    @render_to_extension
    def relacionados(self, video_id, extension, **kw):
        video = Video().get(int(video_id))
        
        if not video:
            raise HTTPError(404)
            
        video.relacionados = video.getRelacionados()

        return {'video':video.as_dict()}

    @tokenizer
    @render_to_extension
    def busca(self, extension, *args, **kargs):
        
        inicio = kargs.get('inicio')
        itens = kargs.get('itens')
        q = kargs.get('q')
        orderby = kargs.get("orderby")
        canal = kargs.get('canal')
        usuario = kargs.get('usuario')
        
        videos, total = Video().busca(q, canal, usuario, orderby, inicio, itens)
        
        return {'busca':{'videos':[video.as_dict() for video in videos], 'total':total}}
