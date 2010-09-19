# coding: utf-8
#!/usr/bin/env python

from api.util import signature 
from api.models.usuario import Usuario
from tornado.web import HTTPError
from torneira.core.meta import TorneiraSession
from api.models.usuarioChave import UsuarioChave

import logging

def authenticated(fn):
    def authenticated_fn(self, *args, **kwargs):
        
        auth = self.handler.request.headers.get('Autenticacao')
        usuario = None
        
        if auth:
            usuario_id = signature.get_secure_value(auth)
            if usuario_id:
                usuario = Usuario().get(int(usuario_id))
        
        if usuario:
            return fn(self, usuario, *args, **kwargs)
        else:
            raise HTTPError(401)
    return authenticated_fn

def tokenizer(fn):
    def tokenizer_fn(self, *args, **kwargs):
        
        # valida o token para toda requisicao que n seja jsonp
        if not (kwargs and kwargs.get('extension') and kwargs.get('extension') == 'jsonp'):
            token = self.handler.request.headers.get('Token') or kwargs.get('token')
            usuario_chave = None

            if token:
                usuario_chave = TorneiraSession().query(UsuarioChave).filter(UsuarioChave.chave == token).first()
            
            if not usuario_chave:
                raise HTTPError(401)
            
            logging.info("Acesso liberado! token: %s " % token)
            
        return fn(self, *args, **kwargs)
    
    return tokenizer_fn