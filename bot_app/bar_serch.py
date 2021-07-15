import googlemaps
import bot_data
import pandas as pd

class Bar_serch:
    def __init__(self):
        self.gmaps = googlemaps.Client(key = bot_data.google_token)
        self.i = 0
        self.view_list = []

    def serch(self, location_lat = 60, location_lng = 30):
        self.location = (location_lat, location_lng)
        data = self.gmaps.places(type = "bar",
                                 location = self.location,
                                 min_price = 0, max_price = 3, # Вилка цены
                                 open_now = True, # Открыто сейчас
                                 radius = 250, language='ru')
        self.df = pd.json_normalize(data['results'])[['name', 'formatted_address',
                                                 'rating', 'types', 'user_ratings_total',
                                                 'opening_hours.open_now',
                                                 'geometry.location.lat', 'geometry.location.lng', 'place_id']][:5]
        # Сортировка
        # Работает как-то не очень
        # self.df = self.df.sort_values(by = 'user_ratings_total', ignore_index = True, ascending = False)
        self.i_max = self.df.index[-1]
        self.get_bar()

        return self

    # Добавляем последний худший коментарий
    def get_bar(self):
        if self.i + 1 >= self.i_max: return None
        # Проверка на дубликаты
        while self.df.place_id[self.i] in self.view_list:
            self.i += 1
        place_id = self.df.place_id[self.i]
        self.i += 1
        bar_info_df = self.gmaps.place(place_id = place_id, language = 'ru')
        reviews_df = pd.json_normalize(bar_info_df['result']['reviews'])
        review = reviews_df[reviews_df.rating == reviews_df.rating.min()].text.values[0]
        self.df.loc[self.df.place_id == place_id, 'review'] = review
        # Сохранить последние 100 баров
        self.view_list.append(place_id)
        self.view_list = self.view_list[-100:]
        return self.df.loc[self.df.place_id == place_id].squeeze()
