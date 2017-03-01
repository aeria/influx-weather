import configparser
import requests
#import urllib2
from urllib.request import urlopen
from datetime import datetime
import json
import time
import datetime
from influxdb import InfluxDBClient
from influxdb.exceptions import InfluxDBClientError, InfluxDBServerError
from requests.exceptions import ConnectionError

config = configparser.ConfigParser()
config.read('wu-config.ini')

cityid = config['WEATHERUNDERGROUND']['Location']
weatherapikey = config['WEATHERUNDERGROUND']['APIKey']

#print(type(influxPort))

#influx_client = InfluxDBClient(influxAddress, influxPort, influxUser, influxPassword, influxDatabase)

def getWeatherData(cityid):

    requestURL = 'http://api.wunderground.com/api/' + weatherapikey + '/conditions/q/' + str(cityid)+ '.json'

    response = requests.get(requestURL)

    #print(type(json_data))
    data = json.loads(response.text)
    #print(data['main']['temp'])

    json_data = formatData(data)

    return json_data

def formatData(data):

    #print(type(data))
    #print(data)
    relative_humidity = data['current_observation']['relative_humidity'].split( )

    json_data = [
        {
            "measurement": "weatherunderground",
            "tags": {
                "city": data['current_observation']['display_location']['city'],
                "location_id": data['current_observation']['display_location']['wmo'],
                'station_id': data['current_observation']['station_id']
            },

            "fields":
            {
                'pressure_mb': data['current_observation']['pressure_mb'],
                'dewpoint_c': data['current_observation']['dewpoint_c'],
                'precip_today_metric':data['current_observation']['precip_today_metric'],
                'temp_c':data['current_observation']['temp_c'],
                'wind_gust_kph':data['current_observation']['wind_gust_kph'],
                'relative_humidity':relative_humidity[0],
                'wind_kph':data['current_observation']['wind_kph'],
                'wind_degrees':data['current_observation']['wind_degrees'],
                'windchill_c':data['current_observation']['windchill_c'],
                'feelslike_c':data['current_observation']['feelslike_c'],
                'visibility_km':data['current_observation']['visibility_km'],
                'heat_index_c':data['current_observation']['heat_index_c'],
                'UV':data['current_observation']['UV'],
             }
        }
    ]


    #print(type(json_data))
    #print(json_data)

    return json_data

def main():
    weatherdata = getWeatherData(cityid)
    #sendInfluxData(weatherdata)

    #time.sleep(delay)
    return weatherdata

if __name__ == '__main__':
    main()