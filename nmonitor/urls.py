from torneira.core.dispatcher import url
from controller.home import HomeController
from controller.site import SiteController

urls = (
    url("/", HomeController, action="", name="home"),    
    url("/site/{site_id}", SiteController, action="", name="site"),    
)
