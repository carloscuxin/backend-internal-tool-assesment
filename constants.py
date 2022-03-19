AMENITIES = [
    "wifi",
    "kitchen",
    "parking",
    "air conditioning",
    "heating",
    "iron",
    "hair_dryer",
    "bathtub",
    "free_parking",
]

ROOM_TYPES = ["residential", "business"]

ERROR_CODES = {
    "prices": {
        "not_found": "Hotel has no data previously fetched, please use /hotels/:hotel_id endpoint",
        "invalid_date": "Invalid date format, please use DD/MM/YYYY",
        "invalid_date_range": "Date range cannot be more than 30 days",
    }
}
