import logging, os

DEBUG = True
PROFILING = False

DATABASE_ENGINE = "mysql://root:@localhost:3306/nginx_monitor?charset=utf8&use_unicode=0"
DATABASE_POOL_SIZE = 50

logging.basicConfig(
    level = logging.INFO,
#    format = '%(asctime)s %(levelname)s %(message)s',
#    filename = "/opt/logs/apivideolog/python/api.log",
#    filemode = 'a'
)
logging.getLogger('sqlalchemy').setLevel(logging.ERROR)

ROOT_URLS = 'server.urls'

# make this unique and secret
COOKIE_SECRET = "29NbhyfgaA092ZkjMbNvCx06789jdA8iIlLqz7d1D9c8"
TEMPLATE_DIRS = (
    "%s/templates" % os.path.abspath(os.path.dirname(__file__))
)

CACHE_BACKEND = "memcached"
CACHE_BACKEND_OPTS = { 'memcached': ['localhost:11211']}
CACHE_TIMEOUT = 60*60