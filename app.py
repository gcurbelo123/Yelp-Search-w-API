from __future__ import print_function 
import requests
import pprint
import argparse
import datetime
import json
import sys
import urllib
import urllib2
import re
import pyowm
from pyowm import OWM
import rauth
import time
import cgi
import flask
from flask import request
import os
app = flask.Flask(__name__)

#Everything works, except sometimes it will return a city with an apostraphe, or an error in
#the address which aren't allowed by Yelp, so it won't work

app_id = 'RqqxitLGWZRExd8_vTeiCg'
app_secret = 'CCLbZTkrxIDIzFPXoXPt1sLzeLO6fQuuRNXnwdJOPm04BdsFgD2Bz76fSl5NoaxE'
data = {'grant_type': 'client_credentials',
        'client_id': app_id,
        'client_secret': app_secret}
token = requests.post('https://api.yelp.com/oauth2/token', data=data)
access_token = token.json()['access_token']
url = 'https://api.yelp.com/v3/businesses/search'
headers = {'Authorization': 'bearer %s' % access_token}
@app.route('/', methods = ["GET","POST"])  
def index():
    return flask.render_template("website.html")
    
@app.route('/result', methods = ['POST'])
def result():
    API_key = 'd04e4c4a1f8c6a72c99bd508d1dba5b5'
    owm = OWM(API_key)
    city = request.form['city']
    #################
    hotelNames = []
    hotelPhones = []
    hotelAddress = []
    num = 0
    params = {'location': city,
              'term': 'hotels',
              'pricing_filter': '1,2',
              'sort_by': 'rating'
             }
    resp = requests.get(url = url, params = params, headers = headers)
    num = resp.json()['total']
    if(num > 10):
        num = 10
    elif(num == 0):
        hotelNames = "None"
        hotelPhones = "None"
        hotelAddress = "None"
    if(num > 0):
        for i in range(num):
            hotelNames.append(str(resp.json()['businesses'][i]['name']))
            hotelPhones.append(str(resp.json()['businesses'][i]['display_phone']))
            hotelAddress.append(str(resp.json()['businesses'][i]['location']['display_address'][0])+" "+(str(resp.json()['businesses'][i]['location']['display_address'][1])))
    hotelName = hotelNames[:]
    hotelPhone = hotelPhones[:]
    hotelAdd = hotelAddress[:]
    bound1 = num
    #################
    num = 0
    resNames = []
    resPhones = []
    resAddress = []
    params = {'location': city,
              'term': 'restaurant',
              'pricing_filter': '1,2',
              'sort_by': 'rating'
             }
    resp = requests.get(url = url, params = params, headers = headers)
    num = resp.json()['total']
    if(num > 10):
        num = 10
    elif(num == 0):
        resNames = "None"
        resPhones = "None"
        resAddress = "None"
    if(num > 0):
        for i in range(num):
            resNames.append(str(resp.json()['businesses'][i]['name']))
            resPhones.append(str(resp.json()['businesses'][i]['display_phone']))
            resAddress.append(str(resp.json()['businesses'][i]['location']['display_address'][0])+" "+(str(resp.json()['businesses'][i]['location']['display_address'][1])))
    resName = resNames[:]
    resPhone = resPhones[:]
    resAdd = resAddress[:]
    bound2 = num
    ##################
    num = 0
    spaNames = []
    spaPhones = []
    spaAddress = []
    params = {'location': city,
              'term': 'clubs',
              'pricing_filter': '1,2',
              'sort_by': 'rating'
             }
    resp = requests.get(url = url, params = params, headers = headers)
    num = resp.json()['total']
    if(num > 10):
        num = 10
    elif(num == 0):
        spaNames = "None"
        spaPhones = "None"
        spaAddress = "None"
    if(num > 0):
        for i in range(num):
            spaNames.append(str(resp.json()['businesses'][i]['name']))
            spaPhones.append(str(resp.json()['businesses'][i]['display_phone']))
            spaAddress.append(str(resp.json()['businesses'][i]['location']['display_address'][0])+" "+(str(resp.json()['businesses'][i]['location']['display_address'][1])))
    spaName = spaNames[:]
    spaPhone = spaPhones[:]
    spaAdd = spaAddress[:]
    bound3 = num
    ###################
    return flask.render_template("result.html", hotelName = hotelName[:], hotelPhone = hotelPhone[:], hotelAdd = hotelAdd[:], bound1 = bound1, resName = resNames[:], resPhone = resPhones[:], resAdd = resAddress[:], bound2 = bound2, spaName = spaNames[:], spaPhone = spaPhones[:], spaAdd = spaAddress[:], bound3 = bound3)


app.run(
    port=int(os.getenv('PORT', 8080)),
    host=os.getenv('IP', '0.0.0.0'),
    debug=True
)