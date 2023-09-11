#openai functions call - actions
import openai
import json, os
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
wheather_api_key = os.getenv("OPENWEATHER_API_KEY")
search_api = os.getenv("apikey_search")
import requests

#define function weather
def get_weather_forecast(location, cnt=1, api_key = wheather_api_key):
    """Get the weather forecast or current weather in a given location"""

    if cnt>=1:

        url = "http://api.openweathermap.org/data/2.5/forecast" # 5 days 3 to 3 hours

        params = {
            "q": location,
            "cnt": cnt, #number of timestamp
            "appid": api_key,
            "units": "metric",}

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raise an exception for non-2xx responses
            data = response.json()
            print(data)

            cnt = cnt-1
            
            # Extract relevant forecast information
            temperature = data["list"][cnt]["main"]["temp"]
            weather_description = data["list"][cnt]["weather"][0]["description"]
            humidity = data["list"][cnt]["main"]["humidity"]
            timestamp = data["list"][cnt]["dt_txt"]
        
            forecast_info = {
            "location": location,
            "temperature": temperature,
            "humidity": humidity,
            "forecast_description": weather_description,
            "timestamp": timestamp,
            "type" : "forecast data, all units in metric",
            }

            return json.dumps(forecast_info)
        
        except requests.exceptions.RequestException as e:
            print("Error occurred during API request:", e)
            return None
        
    else: #current weather
        
        url = "http://api.openweathermap.org/data/2.5/weather" 
        
        params = {
            "q": location,
            "appid": api_key,
            "units": "metric",}

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raise an exception for non-2xx responses
            data = response.json()
                   
            # Extract relevant current weather information
            temperature = data["main"]["temp"]
            weather_description = data["weather"][0]["description"]
            humidity = data["main"]["humidity"]
            wind = data["wind"]["speed"]
        
            forecast_info = {
            "location": location,
            "temperature": temperature,
            "humidity": humidity,
            "weather_description": weather_description,
            "wind_speed": wind,
            "type" : "current weather data, all units in metric",
            }

            return json.dumps(forecast_info)
        
        except requests.exceptions.RequestException as e:
            print("Error occurred during API request:", e)
            return None

from duckduckgo_search import DDGS

def search_duckduckgo(query):
   
    with DDGS() as ddgs:
        results = list(ddgs.answers(query))
        if results:
            first_result = results[0]
            first_text = first_result.get('text')
            return first_text

        else:
            return None
    
#def function to serpapi search engine
from serpapi import GoogleSearch
def search_serpapi(query):
    params = {
        "engine": "google", #"duckduckgo"
        "q": query,
        "hl": "pt-br",
        "api_key": search_api 
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    organic_results = results["organic_results"]
    return organic_results[0]['title']

def websearch(query):
    r = search_duckduckgo(query)
    if r is not None:
        return r
    else:
        print("No results found for the Duckduckgo search query.")
        return search_serpapi(query)

