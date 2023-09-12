# ChatBot with AI using OpenAI Function Calling Structure

This is a Python ChatBot application that leverages the OpenAI GPT-3.5 Turbo model for conversation. It allows users to interact with the ChatBot, which can perform various functions based on user queries and recent internet events.

## Table of Contents
1. [Getting Started](#getting-started)
2. [Usage](#usage)
3. [Modules](#modules)
    - [ChatBotBrain.py](#chatbotbrainpy)
    - [functions_actions.py](#functionsactionspy)
4. [API Keys](#api-keys)
5. [License](#license)

## Getting Started

1. Clone this repository to your local machine.
2. Install the required Python packages using `pip install -r requirements.txt`.
3. Set up the necessary API keys (see [API Keys](#api-keys)).
4. Run the `AppChatBot.py` script to start the ChatBot.

## Usage

1. Start the ChatBot by running `AppChatBot.py`.
2. Enter your queries as a user.
3. The ChatBot will respond based on your input and may perform functions using OpenAI.

## Modules

### ChatBotBrain.py

This module contains the main ChatBot logic. It reads user input, manages conversation history, and communicates with the OpenAI model.

#### Functions:

- `run_conversation(prompt)`: Main function to run the conversation with the ChatBot. It interacts with the OpenAI GPT-3.5 Turbo model.

### functions_actions.py

This module defines actions that the ChatBot can perform based on user queries.

#### Functions:

- `get_weather_forecast(location, cnt=1)`: Get weather forecasts or current weather for a given location using the OpenWeather API.

- `websearch(query)`: Perform web searches and answer questions about recent events using DuckDuckGo and SERPAPI

### API Keys

To use this ChatBot, you need to set up the following API keys:

- `OPENAI_API_KEY`: Your OpenAI API key for accessing the GPT-3.5 Turbo model.
- `OPENWEATHER_API_KEY`: Your OpenWeather API key for weather forecasts.
- `apikey_search`: Your API key for web searches using SERPAPI.

https://platform.openai.com/account/api-keys
https://home.openweathermap.org/api_keys
https://serpapi.com/dashboard


You should store these keys securely and add them to your environment variables or a `.env` file.

.env file
OPENAI_API_KEY=your_openai_api_key
OPENWEATHER_API_KEY=your_openweather_api_key
apikey_search=your_serpapi_api_key

#Important Note:

I only test it on Raspiberry Pi 4B 8G OS 64bit

#MIT License

Copyright (c) 2023 PeriniDev

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
