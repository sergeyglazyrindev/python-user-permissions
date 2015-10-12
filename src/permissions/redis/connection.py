from redisext import (
    ConnectionHandler as RedisConnectionHandler,
)


class ConnectionHandler(RedisConnectionHandler):
    connection = {
        'host': 'localhost',
        'port': 6379,
        'db': 0
    }

    @classmethod
    def configure_connection(cls, connection):
        cls.connection = connection
