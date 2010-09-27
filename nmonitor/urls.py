from torneira.core.dispatcher import url
from controller.home import HomeController
from controller.site import SiteController
from controller.server import ServerController

urls = (
    url("/", HomeController, action="", name="home"),    

    url("/login", HomeController, action="login", name="login"),
    
    url("/site", SiteController, action="", name="new_site"),    
    url("/site/{site_id}/edit", SiteController, action="", name="update_site"),    
    url("/site/{site_id}", SiteController, action="view_site", name="view_site"),

    url("/server", ServerController, action="", name="new_server"),    
    url("/server/{server_id}/edit", ServerController, action="", name="update_server"),    

)
