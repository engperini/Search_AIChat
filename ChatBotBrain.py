
import openai
import json, os
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
from functions_actions import get_weather_forecast, websearch

#define main chatcompletion - Chatbot whit functions call
def run_conversation(prompt):
    # Step 1: send the conversation and available functions to GPT
    
    messages = [
        {"role": "system", "content": "You are a helpfull assistant. Only use the functions provided to you"},
        {"role": "user", "content": f"{prompt}?"}, ]
    
    functions = [
        {
            "name": "get_weather_forecast",
            "description": "Get the weather forecast up to 5 days with data every 3 hours or the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    },
                    "cnt": {"type": "integer", 
                    "description": "Choice the timestamp 1 up to 40 for forecast each 3 hours to return or timestamp 0 for the current weather. Forecast Default is 1, which returns one forecast timestamp availiable. Current weather Default is 0, wich returns the current wheather"},
                },
                "required": ["location", "cnt"],
            },
        },

        {
            "name": "websearch",
            "description": "Usefull to aswer questions about recent events. Do not use it to general questions",
            "parameters": {
                "type": "object",
                "properties": {
                    "query":{
                        "type":"string",
                        "description": "query to search tools, e.g. who won the us open this year?, recent news about this subject"
                    },
                    
                },
                "required": ["query"],
            },
        },
    ]
    

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        functions=functions,
        function_call="auto", 
    )
    response_message = response["choices"][0]["message"]

    # Step 2: check if GPT wanted to call a function
    if response_message.get("function_call"):
        # Step 3: call the function
        
        available_functions = {
            "get_weather_forecast": get_weather_forecast, 
            "websearch":websearch,

        }  # can have multiple functions

        function_name = response_message["function_call"]["name"]
        fuction_to_call = available_functions[function_name]
        function_args = json.loads(response_message["function_call"]["arguments"])
        

        #I got this solution because first I put all args togheter and-> TypeError: websearch() got an unexpected keyword argument 'location'
        if function_name == "get_weather_forecast":
            function_response = fuction_to_call(
                location=function_args.get("location"),
                cnt=function_args.get("cnt"),
            )
        
        elif function_name == "websearch":
            function_response = fuction_to_call(
                query=function_args.get("query"),
            )

        else:
            function_response = None

        # Step 4: send the info on the function call and function response to GPT
        messages.append(response_message)  # extend conversation with assistant's reply
        messages.append(
            {
                "role": "function",
                "name": function_name,
                "content": function_response,
            }
        )  # extend conversation with function response

        second_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=messages,
        )  # get a new response from GPT where it can see the function response

        #print(second_response)
        return second_response
    
    else:
        return response
