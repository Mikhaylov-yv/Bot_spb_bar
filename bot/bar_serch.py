import googlemaps
import bot_data
import pandas as pd

class Bar_serch:
    def __init__(self, location_lat = 60, location_lng = 30):
        self.location = (location_lat, location_lng)
        self.gmaps = googlemaps.Client(key = bot_data.google_token)

    def serch(self):
        data = self.gmaps.places(type = "bar",
                                 location = self.location,
                                 radius = 500, language='ru')
        df = pd.json_normalize(data['results'])[['name', 'formatted_address',
                                                 'rating', 'types', 'user_ratings_total',
                                                 'opening_hours.open_now',
                                                 'geometry.location.lat', 'geometry.location.lng', 'place_id']]

        return df