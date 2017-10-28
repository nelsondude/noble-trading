from tornado.web import url

from .handlers import (
    LoginHandler,
    HomeHandler,
    TradeHandler,
    RegisterHandler
)


__all__ = ('URLsRegistry',)


class URLsRegistry(object):

    _urls = []

    @classmethod
    def register(cls, urls):
        cls._urls.extend(urls)

    @classmethod
    def get(cls):
        return tuple(cls._urls)


URLS = (
    url(r'/login', LoginHandler),
    url(r'/trade', TradeHandler),
    url(r'/register', RegisterHandler),
    url(r'/', HomeHandler),
)


URLsRegistry.register(urls=URLS)
