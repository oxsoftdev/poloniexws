import asyncio
import logging
from autobahn.asyncio.wamp import ApplicationRunner
from autobahn.asyncio.wamp import ApplicationSession
from datetime import datetime
from dppy.creational import singleton
from dppy.behavioral import pubsub
from time import time

#from .models import Stream


logger = logging.getLogger('poloniexws')


class _Proxy(metaclass=singleton.MetaSingleton):

    def run(self):
        params = ('wss://api.poloniex.com:443', 'realm1')
        runner = ApplicationRunner(*params)
        runner.run(_Component)

    @property
    def books(self):
        return self.__books

    @books.setter
    def books(self, books):
        self.__books = books

    @property
    def publisher(self):
        return self.__publisher

    @publisher.setter
    def publisher(self, publisher):
        self.__publisher = publisher


class _Component(ApplicationSession):

    def onConnect(self):
        logger.info("transport connected")
        self.join(self.config.realm)

    def onChallenge(self, challenge):
        logger.info("authentication challenge received")

    def onLeave(self, details):
        logger.info("session left")

    def onDisconnect(self):
        logger.info("transport disconnected")
        asyncio.get_event_loop().stop()

    async def onJoin(self, details):
        logger.info("session joined")

        def onTicker(*args):
            _Proxy().publisher.notify(args)
        await self.subscribe(onTicker, 'ticker')

        def onMarket(book):
            def onTrade(*args, **kwargs):
                _Proxy().publisher.notify(book, args, kwargs)
        for book in _Proxy().books:
            await self.subscribe(onMarket(book), book)


class Client(pubsub.AbsPublisher):

    def __init__(self, books):
        self.proxy = _Proxy()
        self.proxy.books = books
        self.proxy.publisher = self
        self.proxy.run()

