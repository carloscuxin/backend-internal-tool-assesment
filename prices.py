from flask import request
from faker import Faker
from flask_restx import Resource, Api
from constants import ERROR_CODES
from redis_client import RedisClient
from utils import daterange
from datetime import datetime, timedelta
from hotels import Hotels

client = RedisClient()
fake = Faker()


api = Api()


class Prices(Resource):
    @api.doc(
        params={
            "start_date": {"description": "Start date in dd/mm/yyyy format"},
            "end_date": {"description": "End date in dd/mm/yyyy format"},
        },
        responses={
            400: "Date range cannot be more than 30 days",
            401: "Invalid date format dd/mm/yyyy",
            401: "Unexpected error",
            404: "Hotel not found",
        },
    )
    def get(self, hotel_id):
        try:
            if self.valid_hotel(hotel_id):
                return ({"error": ERROR_CODES["prices"]["not_found"]}, 404)
            try:
                [start_date, end_date] = self.set_dates(request.args)
            except KeyError:
                return ({"error": ERROR_CODES["prices"]["invalid_date"]}, 400)

            if end_date - start_date > timedelta(days=30):
                return ({"error": ERROR_CODES["prices"]["invalid_date_range"]}, 401)

            if start_date.month != end_date.month:
                return ({"error": ERROR_CODES["prices"]["invalid_date_range"]}, 401)

            prices = self.get_price_from_cache(hotel_id, start_date.month)
            if prices is None:
                prices = self.generate_room_prices(hotel_id, start_date, end_date)
                self.set_price_from_cache(hotel_id, prices, start_date.month)

            return {"hotel_id": hotel_id, "prices": prices}
        except Exception as e:
            return ({"error": str(e)}, 402)

    @staticmethod
    def get_price_from_cache(hotel_id, month):
        redis_hotel_price_id = "hotel:{}:prices:{}".format(hotel_id, month)
        return client.easy_get(redis_hotel_price_id)

    @staticmethod
    def set_price_from_cache(hotel_id, prices, month):
        redis_hotel_price_id = "hotel:{}:prices:{}".format(hotel_id, month)
        client.easy_set(redis_hotel_price_id, prices)

    def generate_room_prices(self, hotel_id, start_date, end_date):
        hotel = Hotels.get_hotel_from_cache(hotel_id)
        rooms_with_prices = {}
        for room in hotel["rooms"]:
            rooms_with_prices[room["room_id"]] = (
                self.generate_prices(start_date, end_date),
            )

        return rooms_with_prices

    def get_rooms(self, hotel):
        return hotel["rooms"]

    def generate_prices(self, start_date, end_date):
        prices = []
        for day in daterange(start_date, end_date):
            prices.append(
                {
                    "date": day.strftime("%d/%m/%Y"),
                    "booking": {
                        "price": fake.random_int(min=100, max=1000),
                        "currency": "USD",
                        "tax": fake.random_int(min=0, max=10),
                    },
                    "expedia": {
                        "price": fake.random_int(min=100, max=1000),
                        "currency": "USD",
                        "tax": fake.random_int(min=0, max=10),
                    },
                    "travel_com": {
                        "price": fake.random_int(min=100, max=1000),
                        "currency": "USD",
                        "tax": fake.random_int(min=0, max=10),
                    },
                    "guruhotel": {
                        "price": fake.random_int(min=100, max=1000),
                        "currency": "USD",
                        "tax": fake.random_int(min=0, max=10),
                    },
                }
            )

        return prices

    def set_dates(self, args):
        query_params = args
        start_date = query_params.get("start_date")
        end_date = query_params.get("end_date")
        start_date = datetime.strptime(start_date, "%d/%m/%Y")
        end_date = datetime.strptime(end_date, "%d/%m/%Y")
        return [start_date, end_date]

    def valid_hotel(self, hotel_id):
        redis_hotel_id = "hotel:{}".format(hotel_id)
        hotel = client.easy_get(redis_hotel_id)
        if hotel is None:
            return True
        return False
