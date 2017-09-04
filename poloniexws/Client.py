import json
import logging
import tornado.gen
import tornado.websocket
from datetime import datetime
from dppy.behavioral import pubsub
from time import time


#from .models import Stream


logger = logging.getLogger('poloniexws')


class Client(pubsub.AbsPublisher):

    def __init__(self, channels):
        self._conn = None
        self._url = 'wss://api2.poloniex.com'
        self._channels = channels

    @tornado.gen.coroutine
    def connect(self):
        logger.info("connecting")
        try:
            websocket_connect = tornado.websocket.websocket_connect
            self._conn = yield websocket_connect(self._url)
            self.subscribe()
        except:
            logger.exception("failed to connect")
        else:
            logger.info("connected")
            self.listen()

    @tornado.gen.coroutine
    def listen(self):
        while True:
            try:
                msg = yield self._conn.read_message()
                if msg is None:
                    logger.info("connection closed")
                    self._conn = None
                    break
                else:
                    data = json.loads(msg)
                    timestamp = time()
                    params = {
                        'timestamp': timestamp,
                        'datetime': datetime.fromtimestamp(timestamp),
                        'data': data
                    }
                    self.notify(params)
            except:
                logger.exception("failed on listen")
                raise

    def subscribe(self):
        for channel in self._channels:
            logger.info("subscribing(channel=%s)" % channel)
            self._conn.write_message(json.dumps({
                'command': 'subscribe',
                'channel': channel
            }))

