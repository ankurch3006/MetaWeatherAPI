import requests
import concurrent.futures


class Weather:
    def __init__(self, city_name, meta_weather_api_url):
        self.city_name = city_name
        self.meta_weather_api_url = meta_weather_api_url

    def get_avg_max_tmp(self):
        try:
            response = requests.get(self.meta_weather_api_url)
        except requests.exceptions.HTTPError as e:
            return "Error: " + str(e)

        res = response.json()
        weather = res['consolidated_weather']

        max_temps = [weather[i]['max_temp'] for i in range(len(weather))]

        if len(max_temps) > 0:
            avg_max_temps = round(sum(max_temps) / len(max_temps), 2)
            return f"{self.city_name} Average Max Temp: {avg_max_temps}"

# Make a list with name of the city and the url of metaweather api
list_cities = [["Salt Lake City", "https://www.metaweather.com/api/location/2487610/"] \
    , ["Los Angeles", "https://www.metaweather.com/api/location/2442047/"] \
    , ["Boise", "https://www.metaweather.com/api/location/2366355/"]]

with concurrent.futures.ThreadPoolExecutor() as executor:
    results = [executor.submit(Weather(list_cities[i][0], list_cities[i][1]).get_avg_max_tmp) for i in
               range(len(list_cities))]

    for max_temp in concurrent.futures.as_completed(results):
        print(max_temp.result())
