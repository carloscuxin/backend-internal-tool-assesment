from faker import Faker
from flask_restx import Resource, Namespace
from constants import AMENITIES, ROOM_TYPES
from redis_client import RedisClient

client = RedisClient()
fake = Faker()


class Hotels(Resource):
    def get(self, hotel_id):
        redis_hotel_id = "hotel:{}".format(hotel_id)
        hotel = client.easy_get(redis_hotel_id)
        if hotel is None:
            hotel = self.generate_hotel()
            client.easy_set(redis_hotel_id, hotel)
        return hotel

    @staticmethod
    def get_hotel_from_cache(hotel_id):
        redis_hotel_id = "hotel:{}".format(hotel_id)
        return client.easy_get(redis_hotel_id)

    @staticmethod
    def get_rooms_from_cache(hotel_id):
        redis_hotel_id = "hotel:{}".format(hotel_id)
        return client.easy_get(redis_hotel_id)["rooms"]

    def generate_hotel(self):
        return {
            "name": fake.company(),
            "city": fake.city(),
            "state": fake.state(),
            "rooms": self.generate_rooms(),
        }

    def generate_rooms(self):
        rooms = []
        rooms_to_generate = fake.random_int(min=1, max=100)
        for room in range(rooms_to_generate):
            rooms.append(
                {
                    "room_id": fake.uuid4(),
                    "room_name": fake.word(),
                    "room_type": fake.random_element(elements=(ROOM_TYPES)),
                    "bed_count": fake.random_int(min=1, max=5),
                    "amenities": [fake.random_element(elements=(AMENITIES))],
                }
            )
        return rooms
