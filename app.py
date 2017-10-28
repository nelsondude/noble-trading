from project.common.urls import URLsRegistry
from project.settings import settings
from tornado.ioloop import IOLoop
from tornado.web import Application as BaseApplication

# from tornado_sqlalchemy import make_session_factory
import tornado
import os



# factory = make_session_factory('sqlite:///noblesqlite.db')
#
class Application(BaseApplication):

    def __init__(self, **kwargs):
        kwargs['debug'] = settings.DEBUG
        super(Application, self).__init__(handlers=URLsRegistry.get(), **kwargs)


if __name__ == '__main__':

    application = Application(
        template_path = os.path.join(os.path.dirname(__file__), "templates"),
        static_path = os.path.join(os.path.dirname(__file__), "static"),
        cookie_secret = settings.COOKIE_SECRET,
        login_url = "/login",
        xsrf_cookies = False,
    )
    application.listen(port=settings.PORT)

    IOLoop.instance().start()