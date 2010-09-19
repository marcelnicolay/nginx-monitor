# coding: utf-8
#!/usr/bin/env python

from torneira.controller import BaseController, render_to_extension
from tornado.web import HTTPError
from api.models.usuario import Usuario
from api.models.usuarioChave import UsuarioChave
from api.models.videocanal import VideoCanal
from api.models.video import Video
from api.models.playlist import Playlist
from torneira.core.meta import TorneiraSession
from api.controller import tokenizer, authenticated

from datetime import datetime
import math
import settings, uuid, simplexml, simplejson
from util import signature

class UsuarioController(BaseController):
	
    @tokenizer
    @render_to_extension
    def videos(self, usuario_id, extension, pagina=1, **kw):

        usuario_id = int(usuario_id)
        pagina = int(pagina)

        usuario = Usuario().get(usuario_id)
        
        if not usuario:
            raise HTTPError(404)

        response = {"usuario":usuario.as_dict()}

        response['usuario']['paginas'] = int(math.ceil(usuario.videos.count() / settings.PAGE_SIZE)) + 1

        limit = int((pagina -1) * settings.PAGE_SIZE)

        response['usuario']['videos'] = []
        for video in usuario.videos.order_by(Video.criacao)[limit:limit+settings.PAGE_SIZE]:
            video.setUri(extension)
            response['usuario']['videos'].append(video.as_dict())

        return response

    @tokenizer
    @render_to_extension
    def favoritos(self, usuario_id, extension, pagina=1, **kw):

        usuario_id = int(usuario_id)
        pagina = int(pagina)

        usuario = Usuario().get(usuario_id)

        if not usuario:
            raise HTTPError(404)

        response = {"usuario":usuario.as_dict()}

        response['usuario']['paginas'] = int(math.ceil(usuario.favoritos.count() / settings.PAGE_SIZE)) + 1

        limit = int((pagina -1) * settings.PAGE_SIZE)

        response['usuario']['videos'] = []
        for favorito in usuario.favoritos.order_by(Playlist.ordenacao)[limit:limit+settings.PAGE_SIZE]:
            favorito.video.setUri(extension)
            response['usuario']['videos'].append(favorito.video.as_dict())

        return response

    @tokenizer
    @authenticated
    def favorito(self, usuario, **kw):
        favorito_data = simplexml.loads(self.handler.request.body)
        
        playlist = Playlist()
        playlist.id_usuario = usuario.id
        playlist.id_video = int(favorito_data['video'].get('id'))
        playlist.data_cadastro = datetime.now()
        playlist.ordenacao = 0
        playlist.save()
        
    def login(self, login, senha):

        usuario = Usuario().doLogin(login, senha)
        if usuario:
            auth = signature.set_secure_value(str(usuario.id), 1)
            return "Autenticacao=%s" % auth
        
        return 'LOGIN OU SENHA INCORRETOS'

    def chave(self, *args, **kargs):
        if self.handler.request.method == 'GET':
            return self.render_to_template('chave.html')
        else:
            
            if kargs.get('login') and kargs.get('senha'):
                usuario = Usuario().doLogin(kargs.get('login'), kargs.get('senha'))
                if usuario :
                    usuario_chave = TorneiraSession().query(UsuarioChave).filter(UsuarioChave.id_usuario == usuario.id).first()
                    if not usuario_chave:
                        usuario_chave = UsuarioChave()
                        usuario_chave.id_usuario = usuario.id
                        usuario_chave.chave = uuid.uuid4()
                        
                        TorneiraSession().add(usuario_chave)
                        TorneiraSession().flush()
                        
                    return self.render_to_template('chave_view.html', usuario_chave=usuario_chave)
                    
                else:
                    return self.render_to_template('chave.html', erro='login ou senha incorretos')
            else:
                return self.render_to_template('chave.html', erro='por favor informe seu login e senha no videolog.tv')