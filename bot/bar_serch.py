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
        mes = 'Вот 5 баров рядом:\n'
        for i, ind in enumerate(df.sort_values('user_ratings_total', ascending=False)[:5].index):
            name = df.loc[ind, 'name']
            place_id = df.loc[ind, 'place_id']
            # geo:37.786971,-122.399677
            mes += f"{i}. [{name}](geo:37.786971,122.399677)\n"
            # mes += f"{i}. [{name}](https://www.google.com/maps/search/?api=1&query={name}&query_place_id={place_id}\n"
        print(mes)
        return mes