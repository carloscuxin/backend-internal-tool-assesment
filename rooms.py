from faker import Faker
from flask_restx import Resource, Api
from constants import AMENITIES, ROOM_TYPES
from redis_client import RedisClient
from hotels import Hotels

client = RedisClient()
fake = Faker()


class Rooms(Resource):
    def get(self, hotel_id):
        return Hotels.get_rooms_from_cache(hotel_id)
