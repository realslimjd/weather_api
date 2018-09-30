import requests

def get_weather(latitude_in, longitude_in, filters):
    '''
    Returns a tuple containing:
    1. True or false to indicate whether or not the API calls were successful
    2. The average temperature at the requested address if successful
    2 (cont). or an error message if not
    '''
    successes = 0
    errors = 0
    apis = {'noaa' : {'temp' : 0.0, 'func' : get_noaa},
            'weather.com' : {'temp' : 0.0, 'func' : get_weather_dot_com},
            'accuweather' : {'temp' : 0.0, 'func' : get_accuweather}}
    
    # Make sure the lat and long values we'e been passed are actually numbers
    try:
        latitude, longitude = float(latitude_in), float(longitude_in)
    except:
        return (False, 'Please include latitude and longitude')

    # If there aren't any services in filters, then we'll add all of them
    # That makes the next step pretty cool
    if not filters:
        filters = ['noaa', 'weather.com', 'accuweather']

    # Find the temperature for each requested service
    for service in filters:
        try:
            result = apis[service][func](latitude, longitude)
            # Check if the result was actually returned
            if result[0]:
                # We could add celsius pretty easily here too
                apis[service]['temp'] += result[1]['fahrenheit']
                successes += 1
            else:
                errors += 1
                # log error message so we know what's happening

        # This should only happen if an invalid service is requested
        except Exception as ex:
            # log exception
            return (False, 'An invalid service was requested.\
                The available services are: noaa, weather.com, accuweather')

    # If no API calls were successful
    if successes == 0:
        return (False, 'We were unable to get any results. Sorry!')
    # If at least one of the requested services returned a value,
    # we'll return a temp
    else:
        # Add up all the temps and divide by the number that gave us a result
        avg_temp = 0
        for api in apis:
            avg_temp += apis[api]['temp']
        # This should be a float already
        avg_temp = avg_temp / successes

    # In the future consider returning any error messages, too
    return (True, avg_temp)


def get_noaa(latitude, longitude):
    '''
    Returns a tuple containing:
    1. True or false to indicate whether or not the API call was successful
    2. A dict containing the temperature in f and c, or an error string
    '''

    url = 'http://127.0.0.1:5000/noaa?'
    # Oh cruel irony
    lat_long = ','.join([str(latitude), str(longitude)])
    params = {'latlon' : lat_long}

    try:
        r = requests.get(url, params)
        response = r.json()

        current_temp_f = response['today']['current']['fahrenheit']
        current_temp_c = response['today']['current']['celsius']
    except Exception as ex:
        # log exception
        return (False, 'Could not connect to NOAA API')
    
    return (True, {'fahrenheit' : float(current_temp_f),
            'celsius' : float(current_temp_c)})


def get_weather_dot_com(latitude, longitude):
    '''
    Returns a tuple containing:
    1. True or false to indicate whether or not the API call was successful
    2. A dict containing the temperature in f, or an error string

    Note: This API does not return the temp in c, but we're including the key
    in the dict to match the other results in case it's added in the future
    '''

    url = 'http://127.0.0.1:5000/weatherdotcom'
    params = {'lat' : latitude,
            'lon' : longitude}

    try:
        r = requests.post(url, json=params)
        response = r.json()

        current_temp_f = response['query']['results']['channel']['condition']['temp']
    except Exception as ex:
        # log exception
        return (False, 'Could not connect to Accuweather API')

    return (True, {'fahrenheit' : float(current_temp_f),
            'celsius' : None})


def get_accuweather(latitude, longitude):
    '''
    Returns a tuple containing:
    1. True or false to indicate whether or not the API call was successful
    2. A dict containing the temperature in f and c, or an error string
    '''

    url = 'http://127.0.0.1:5000/accuweather'
    params = {'latitude' : latitude,
            'longitude' : longitude}
    
    try:
        r = requests.get(url, params)
        response = r.json()

        current_temp_f = response['simpleforecast']['forecastday'][0]['current']['fahrenheit']
        current_temp_c = response['simpleforecast']['forecastday'][0]['current']['celsius']
    except Exception as ex:
        # log exception
        return (False, 'Could not connect to Accuweather API')

    return (True, {'fahrenheit' : float(current_temp_f),
            'celsius' : float(current_temp_c)})
