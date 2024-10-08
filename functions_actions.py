#openai functions call - actions
import openai
import json, os
from dotenv import load_dotenv
load_dotenv()
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

    #organic_results = results["organic_results"]

    # Extrair resultados orgânicos
    organic_results = results.get("organic_results", [])

    # Inicializar uma lista para armazenar todos os snippets
    snippets = []

    # Iterar sobre os resultados e coletar os snippets
    for index, result in enumerate(organic_results):
        if index >= 3:  # Limitar a apenas os três primeiros resultados
            break
        snippet = result.get("snippet", "")
        if snippet:  # Se o snippet não estiver vazio, adicioná-lo à lista
            snippets.append(snippet)

    # Combinar todos os snippets em um único texto e adicionar separadores
    combined_snippets = " | ".join(snippets)

    return combined_snippets



def websearch(query):
    return search_serpapi(query)

