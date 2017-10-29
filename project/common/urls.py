from tornado.web import url

from .handlers import (
    LoginHandler,
    HomeHandler,
    TradeHandler,
    RegisterHandler,
    CompleteTradeHandler
)

from .api.handlers import (
    TradesAPIHandler,
    UsersAPIHandler
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
    url(r'/trade/complete', CompleteTradeHandler),
    url(r'/register', RegisterHandler),
    url(r'/', HomeHandler),
)

API_URLS = (
    url(r'/api/trades', TradesAPIHandler),
    url(r'/api/users', UsersAPIHandler)
)


URLsRegistry.register(urls=URLS)

URLsRegistry.register(urls=API_URLS)
