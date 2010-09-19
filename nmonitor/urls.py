from torneira.core.dispatcher import url
from controller.canal import CanalController
from controller.usuario import UsuarioController
from controller.video import VideoController
from controller.comentario import ComentarioController

urls = (
    url("/comentario/{comentario_id}.{extension}", ComentarioController, action="", name="comentario"),    
)
