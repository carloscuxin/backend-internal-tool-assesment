from faker import Faker
from flask_restx import Resource, Api
from constants import AMENITIES, ROOM_TYPES
from redis_client import RedisClient

client = RedisClient()
fake = Faker()


class Ping(Resource):
    def get(self):
        health = True
        try:
            redis_ping = client.conn.ping()
        except Exception as e:
            health = False

        return {"healthy": health}
