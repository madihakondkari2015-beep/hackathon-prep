import os
import requests
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])


def calculator_tool(expression):
    try:
        return str(eval(expression))
    except:
        return "Invalid calculation"


def text_tool(command, text):
    if command == "count":
        return f"Word Count: {len(text.split())}"

    if command == "reverse":
        return text[::-1]

    if command == "uppercase":
        return text.upper()

    return "Unknown text operation"


def weather_tool():
    try:
        url = "https://api.open-meteo.com/v1/forecast?latitude=19.99&longitude=73.31&current_weather=true"

        data = requests.get(url).json()

        temp = data["current_weather"]["temperature"]

        wind = data["current_weather"]["windspeed"]

        return f"Temperature: {temp}°C, Wind Speed: {wind} km/h"

    except:
        return "Weather service unavailable"


def wikipedia_tool(topic):
    try:

        topic = topic.strip()
        topic = topic.replace("what is", "")
        topic = topic.replace("tell me about", "")
        topic = topic.strip()

        topic = topic.replace(" ", "_")

        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic}"

        response = requests.get(
            url,
            headers={"User-Agent": "PlexiAgent/1.0"}
        )

        data = response.json()

        if "extract" in data:
            return data["extract"]

        return "No information found"

    except Exception as e:
        return str(e)


def decide_tool(user_input):

    try:

        prompt = f"""
You are an AI Agent.

Choose ONLY ONE tool.

Available tools:

calculator
weather
text_count
text_reverse
text_uppercase
wikipedia

User Request:
{user_input}

Respond with ONLY the tool name.
"""

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        return response.text.strip().lower()

    except Exception as e:

        text = user_input.lower()

        if any(op in text for op in ["+", "-", "*", "/"]):
            return "calculator"

        if "weather" in text:
            return "weather"

        if "uppercase" in text:
            return "text_uppercase"

        if "reverse" in text:
            return "text_reverse"

        if "count" in text:
            return "text_count"

        return "wikipedia"