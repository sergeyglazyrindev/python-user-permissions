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
        '''
        Accepts dictionary with keys needed to connect to the redis: host, post, db
        Args:
            :param connection: dictionary with keys: host, port, db
            :type connection: dict
        Returns: None
        '''
        cls.connection = connection
