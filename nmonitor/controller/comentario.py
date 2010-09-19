# coding: utf-8
#!/usr/bin/env python

from torneira.controller import BaseController, render_to_extension
from tornado.web import HTTPError
from api.controller import authenticated, tokenizer
from api.models.comentario import Comentario
from datetime import datetime
import settings
import simplejson
import simplexml

class ComentarioController(BaseController):

    @tokenizer
    @authenticated
    @render_to_extension
    def create(self, usuario, video_id, extension, **kw):
        
        if extension == 'xml':
            comentario_data = simplexml.loads(self.handler.request.body)
        else:
            comentario_data = simplejson.loads(self.handler.request.body)
        
        video = Video().get(int(video_id))
        if not video:
            raise HTTPError(404)
        
        comentario = Comentario()    
        comentario._id_video = video.id_video
        comentario.id_usuario = usuario.id
        comentario.texto = comentario_data['comentario']['texto']
        comentario.data = datetime.now()
        comentario.save()
        
        return {'comentario':comentario.as_dict()}

    @tokenizer
    @authenticated
    def delete(self ,usuario, comentario_id, extension, **kw):
        comentario = Comentario().get(int(comentario_id))
        
        if not comentario:
            raise HTTPError(404)
        
        if not comentario.id_ususario == usuario.id:
            raise HTTPError(401)
            
        comentario.delete()
    
    @tokenizer
    @render_to_extension
    def index(self, comentario_id, extension, **kw):
        
        comentario = Comentario().get(int(comentario_id))
        
        if not comentario:
            raise HTTPError(404)
            
        comentario.id_video = comentario._id_video
        
        return {'comentario':comentario.as_dict()}
