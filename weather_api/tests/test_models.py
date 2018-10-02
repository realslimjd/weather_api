from django.test import SimpleTestCase, RequestFactory
from django.http import JsonResponse
from weather_api import weather

# Note that these tests can't test too many inputs because of the mock API
# This should also include tests of all the failure cases as well
class WeatherAPITests(SimpleTestCase):

    def test_noaa(self):
        expected_reponse = (True, {'fahrenheit' : 55,
            'celsius' : 12})
        
        temp = weather.get_noaa(44, 33)
        self.assertEqual(temp, expected_reponse)

    def test_weather_dot_com(self):
        expected_reponse = (True, {'fahrenheit' : 37,
            'celsius' : None})

        temp = weather.get_weather_dot_com(33.3, 44.4)
        self.assertEqual(temp, expected_reponse)

    def get_accuweather(self):
        expected_reponse = (True, {'fahrenheit' : 55,
            'celsius' : 12})

        temp = get_accuweather(44, 33)
        self.assertEqual(temp, expected_reponse)


# This could be expanded to include all combinations of services
# We'd also want to test more lat/long inputs in the future
class WeatherHandlersTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def get_avg_temp_no_filter(self):
        expected_reponse = (True, 49)

        results = get_avg_temp(44, 33)
        self.assertEqual(results, expected_reponse)

    def get_avg_temp_bad_filter(self):
        expected_reponse = (False, 'An invalid service was requested. The available services are: noaa, weather.com, accuweather')

        results = get_avg_temp(44, 33)
        self.assertEqual(results, expected_reponse)

    def get_avg_temp_noaa(self):
        expected_reponse = (True, 55)

        results = get_avg_temp(44, 33, 'noaa')
        self.assertEqual(results, expected_reponse)

    def get_avg_temp_weatherdotcom(self):
        expected_reponse = (True, 37)

        results = get_avg_temp(33.3, 44.4, 'weather.com')
        self.assertEqual(results, expected_reponse)

    def get_avg_temp_accuweather(self):
        expected_reponse = (True, 55)

        results = get_avg_temp(44, 33, 'accuweather')
        self.assertEqual(results, expected_reponse)

    def get_avg_temp_allfilters(self):
        expected_reponse = (True, 49)

        results = get_avg_temp(44, 33, ['noaa', 'weather.com', 'accuweather'])
        self.assertEqual(results, expected_reponse)

    def get_weather_good_request(self):
        expected_reponse = JsonResponse({'Data' : {'Temperature' : {'Fahrenheit' : 37}}})

        request = self.factory.get('/weather?latitude=44&longitude=33&filters=weather.com')
        results = get_weather(request)
        self.assertEqual(results, expected_reponse)

    def get_weather_no_latlong(self):
        expected_reponse =  JsonResponse({'Error' :'Please include latitude and longitude'})

        request = self.factory.get('/weather?filters=weather.com')
        results = get_weather(request)
        self.assertEqual(results, request)
