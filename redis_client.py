import redis
from redis.commands.json.path import Path


class Singleton(type):
    """
    An metaclass for singleton purpose. Every singleton class should inherit from this class by 'metaclass=Singleton'.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class RedisClient(object):
    def __init__(self):
        self.pool = redis.ConnectionPool(host="redis", port="6379", db=0)

    @property
    def conn(self):
        if not hasattr(self, "_conn"):
            self.get_connection()
        return self._conn

    def get_connection(self):
        self._conn = redis.Redis(connection_pool=self.pool)

    def easy_set(self, id, obj):
        self.conn.json().set(id, Path.rootPath(), obj)

    def easy_get(self, id):
        return self.conn.json().get(id)
