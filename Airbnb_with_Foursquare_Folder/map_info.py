#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 07:45:29 2020

@author: minghuishen
"""

import pandas as pd
# library for data analsysis
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

from bs4 import BeautifulSoup
import requests
import numpy as np # library to handle data in a vectorized manner
import json # library to handle JSON files
#!conda install -c conda-forge geopy --yes # uncomment this line if you haven't completed the Foursquare API lab
from geopy.geocoders import Nominatim # convert an address into latitude and longitude values
import requests # library to handle requests
from pandas.io.json import json_normalize # tranform JSON file into a pandas dataframe
# Matplotlib and associated plotting modules
import matplotlib.cm as cm
import matplotlib.colors as colors
# import k-means from clustering stage
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

CLIENT_ID = '4ZDZSCQUDW0AFZAZNXCYKUFXSP5PJTBUQRV4RHJ1SKYLZB4S' # your Foursquare ID
CLIENT_SECRET = '5KQCUGJXPBYDZP4L5BGSGYSZCNVDSCKSTVLXAEGSFE2AOKB0' # your Foursquare Secret
VERSION = '20180605' # Foursquare API version

print('Your credentails:')
print('CLIENT_ID: ' + CLIENT_ID)
print('CLIENT_SECRET:' + CLIENT_SECRET)

def getNearbyVenues(names, latitudes, longitudes, radius=500, limit=100):
    venues_list=[]
    for name, lat, lng in zip(names, latitudes, longitudes):
            
        # create the API request URL
        url = 'https://api.foursquare.com/v2/venues/search?categoryId=4bf58dd8d48988d181941735,507c8c4091d498d9fc8c67a9,4bf58dd8d48988d184941735,4d4b7105d754a06372d81259,4bf58dd8d48988d1f9941735,4d4b7105d754a06379d81259,4bf58dd8d48988d1fa931735&intent=browse&&client_id={}&client_secret={}&v={}&ll={},{}&radius={}&limit={}'.format(
                    CLIENT_ID, 
                    CLIENT_SECRET, 
                    VERSION, 
                    lat, 
                    lng, 
                    radius, 
                    limit)
        results = requests.get(url).json()["response"]
        result_summary = {'Museum':0,'Public Art':0,'Stadium':0,'College':0,'Food Shop':0,'Transport':0,'Hotel':0}
        for v in results['venues']:
            if v['categories'][0]['id'] == '4bf58dd8d48988d181941735':
                result_summary['Museum'] += 1
            elif v['categories'][0]['id'] == '507c8c4091d498d9fc8c67a9':
                result_summary['Public Art'] += 1
            elif v['categories'][0]['id'] == '4bf58dd8d48988d184941735':
                result_summary['Stadium'] += 1
            elif v['categories'][0]['id'] == '4d4b7105d754a06372d81259':
                result_summary['College'] += 1
            elif v['categories'][0]['id'] == '4bf58dd8d48988d1f9941735':
                result_summary['Food Shop'] += 1
            elif v['categories'][0]['id'] == '4d4b7105d754a06379d81259':
                result_summary['Transport'] += 1
            elif v['categories'][0]['id'] == '4bf58dd8d48988d1fa931735':
                result_summary['Hotel'] += 1
        # return only relevant information for each nearby venue
        venues_list.append([name,lat,lng,
                            result_summary['Museum'],
                            result_summary['Public Art'],
                            result_summary['Stadium'],
                            result_summary['College'],
                            result_summary['Food Shop'],
                            result_summary['Transport'],
                            result_summary['Hotel']])

    nearby_venues = pd.DataFrame(venues_list)
    nearby_venues.columns = ['Neighborhood', 
                  'Latitude', 
                  'Longitude', 
                  'Museum',
                  'Public Art',
                  'Stadium',
                  'College',
                  'Food Shop',
                  'Transport',
                  'Hotel']
    
    return(nearby_venues)




d = {'Neighborhood': ['Parkwoods'], 'Latitude': [43.753259], 'Longitude':[-79.329656]}
input_df = pd.DataFrame(data=d)
output = getNearbyVenues(input_df['Neighborhood'],input_df['Latitude'],input_df['Longitude'])




