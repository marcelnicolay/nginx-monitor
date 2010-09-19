# coding: utf-8
#!/usr/bin/env python

from torneira.controller import BaseController, render_to_extension
from api.models.canal import Canal
from api.models.videocanal import VideoCanal
from api.models.video import Video
from tornado.web import HTTPError
from api.controller import tokenizer

import math
import settings

class CanalController(BaseController):
	
    @tokenizer
    @render_to_extension
    def videos(self, canal_id, extension, pagina=1, **kw):

        canal_id = int(canal_id)
        pagina = int(pagina)

        canal = Canal().get(canal_id)

        if not canal:
            raise HTTPError(404)

        response = {"canal":canal.as_dict()}

        page_size = kw.get("itens") or settings.PAGE_SIZE
        page_size = int(page_size) if int(page_size) < 100 else 100
        
        response['canal']['paginas'] = int(math.ceil(canal.videos.count() / page_size)) + 1

        limit = int((pagina -1) * page_size)

        response['canal']['videos'] = []

        for video in canal.videos.order_by(Video.criacao.desc())[limit:limit+page_size]:
            video.setUri(extension)
            response['canal']['videos'].append(video.as_dict())

        return response
