import googlemaps
import bot_data
import pandas as pd

class Bar_serch:
    def __init__(self, location_lat = 60, location_lng = 30):
        self.location = (location_lat, location_lng)
        self.gmaps = googlemaps.Client(key = bot_data.google_token)
        self.i = 0

    def serch(self):
        data = self.gmaps.places(type = "bar",
                                 location = self.location,
                                 radius = 600, language='ru')
        self.df = pd.json_normalize(data['results'])[['name', 'formatted_address',
                                                 'rating', 'types', 'user_ratings_total',
                                                 'opening_hours.open_now',
                                                 'geometry.location.lat', 'geometry.location.lng', 'place_id']]
        self.df = self.df.sort_values(by = 'user_ratings_total', ignore_index = True, ascending = False)
        self.i_max = self.df.index[-1]
        self.get_bar()

        return self

    # Добавляем последний худший коментарий
    def get_bar(self):
        if self.i + 1 >= self.i_max: return False
        place_id = self.df.place_id[self.i]
        self.i += 1
        bar_info_df = self.gmaps.place(place_id = place_id, language = 'ru')
        reviews_df = pd.json_normalize(bar_info_df['result']['reviews'])
        review = reviews_df[reviews_df.rating == reviews_df.rating.min()].text.values[0]
        self.df.loc[self.df.place_id == place_id, 'review'] = review
        return self.df.loc[self.df.place_id == place_id].squeeze()
