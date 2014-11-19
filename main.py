# -*- coding: utf-8 -*-
"""
Yo single tap bar recommendation
Yo Docs: http://docs.justyo.co
Yo Keys: http://dev.justyo.co
Yelp code from https://github.com/Yelp/yelp-api/blob/master/v2/python/sample.py
Yelp Docs: http://www.yelp.com/developers/documentation
Yelp Keys: http://www.yelp.com/developers/manage_api_keys
"""
import json
import sys
import requests
from flask import request, Flask
import os


YO_API_TOKEN = '42d7af4f-7d2c-4396-b768-188d10fcb27c'




app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello world!"

@app.route("/yo/")
def yo():

    # extract and parse query parameters
    username = request.args.get('username')
    location = request.args.get('location')
    splitted = location.split(';')
    latitude = splitted[0]
    longitude = splitted[1]

    print "We got a Yo from " + username

    # get the city name since Yelp api must be provided with at least a city even though we give it accurate coordinates
    url = 'https://api.parse.com/1/functions/checkBathroom'
    appID = 'SJzvb7dpPUIzlPa9wtWsqasByPeZtI8PZBdKJYPB'
    apiKEY = 'HDCp31PgE4UpTL8PZIbBh5KbpkHXcGmD3fh7YDof'
    geopoint = {"__type":"GeoPoint", "latitude":round(float(latitude),2), "longitude":round(float(longitude),2)}
    header = {'X-Parse-Application-Id':appID, 'X-Parse-REST-API-Key':apiKEY, 'Content-Type':'application/json'}
    data = {'location':geopoint, 'limit':5}
    print data
    response = requests.post(url, data=json.dumps(data), headers=header)
    r = response.json()
    print r

    #requests.post("http://api.justyo.co/yo/", data={'api_token': YO_API_TOKEN, 'username': username, 'link': bar_url})

   # requests.post('http://response_object')

    # OK!
    rLocation = str(r['result'][0]['geoPoint']['latitude']) + "," + str(r['result'][0]['geoPoint']['longitude'])
    e = {'api_token': YO_API_TOKEN, 'username': username, 'location':rLocation}
    print e
    requests.post("http://api.justyo.co/yo/", data={'api_token': YO_API_TOKEN, 'username': username, 'location':rLocation})
    return 'OK'


if __name__ == "__main__":
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
