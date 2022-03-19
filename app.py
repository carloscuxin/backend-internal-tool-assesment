from flask import Flask
from flask_restx import Api
from redis_client import RedisClient
from hotels import Hotels
from ping import Ping
from prices import Prices
from rooms import Rooms

client = RedisClient()

app = Flask(__name__)

api = Api(
    app,
    version="1.0.0",
    title="Hotel API",
    description="A simple hotel API",
    default="Hotel",
    default_label="Hotel and Historic Rates API",
)

api.add_resource(Hotels, "/hotels/<int:hotel_id>")
api.add_resource(Prices, "/hotels/<int:hotel_id>/prices")
api.add_resource(Rooms, "/hotels/<int:hotel_id>/rooms")
api.add_resource(Ping, "/ping")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
