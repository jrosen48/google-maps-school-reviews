# source .venv/bin/acticate

from serpapi import GoogleSearch
import pandas as pd
import time
import datetime
import timestring
from datetime import date, datetime
import os.path
from os import path
import warnings

warnings.filterwarnings("ignore")
    
today = date.today()

log_filename = 'logs/' + str(today) + '-log.txt'

schools = pd.read_csv("all-schools-2021.csv")
schools = schools.loc[schools['state_name'] == "North Carolina"]

df = pd.DataFrame()

for school in schools.index:
  
  try:
    
    time.sleep(5)
  
    name = schools[schools.index == school]['school_name'].values[0]
    zipcode = schools[schools.index == school]['zip'].values[0]
    
    print('processing: ', str(name) + ' ' + str(zipcode))
  
    params = {
      "api_key": "xx",
      "device": "desktop",
      "engine": "google_maps",
      "type": "search",
      "google_domain": "google.com",
      "q": str(name) + str(zipcode),
      "hl": "en"
    }
    
    search = GoogleSearch(params)
    results = search.get_dict()
    
    tmp = pd.DataFrame(columns = ['nces_name', 'zipcode'], index = [0])
    # tmp = pd.json_normalize(results['place_results']['user_reviews']['most_relevant'])
    tmp['nces_name'] = name
    tmp['zipcode'] = zipcode
    
    try:
      
      tmp['title'] = results['place_results']['title']
      tmp['address'] = results['place_results']['address']
      tmp['data_id'] = results['place_results']['data_id']
      tmp['rating'] = results['place_results']['rating']
      tmp['n_reviews'] = results['place_results']['reviews']
    
      df = df.append(tmp)
      
      log_file = open(log_filename, "a")
      log_file.writelines(name + ' ' + str(zipcode) + ' - succeeded as a place result')
      log_file.writelines('\n')
      log_file.close()
      
      print('first success for: ', str(name) + ' ' + str(zipcode) + '\n')
      
    except BaseException as e:
      
      print('first error for: ', name + ' ' + str(zipcode))

      tmp['title'] = results['local_results'][0]['title']
      tmp['address'] = results['local_results'][0]['address']
      tmp['data_id'] = results['local_results'][0]['data_id']
      tmp['rating'] = results['local_results'][0]['rating']
      tmp['n_reviews'] = results['local_results'][0]['reviews']
      
      df = df.append(tmp)
      
      log_file = open(log_filename, "a")
      log_file.writelines(name + ' ' + str(zipcode) + ' - succeeded as a local result')
      log_file.writelines('\n')
      log_file.close()
      
      print('second success for: ', str(name) + ' ' + str(zipcode) + '\n')
      
  except BaseException as e:
    
    print('still an error for: ', name + ' ' + str(zipcode))
  
    # logging errors
    log_file = open(log_filename, "a")
    log_file.writelines(name + ' ' + str(zipcode) + ' FAILED ' + str(e))
    log_file.writelines('\n')
    log_file.close()

df.to_csv("output-for-all.csv")
