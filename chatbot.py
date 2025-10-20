import re
import math
import datetime
import requests
import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)

#----------------------DATE--------------------------------------#
date = datetime.datetime.today()
today = date.strftime('%d.%m.%Y')
current_time = date.strftime('%H:%M')
current_day = date.strftime('%A')

#----------------------MATH--------------------------------------#
pi_number = math.pi

#--------------------DICTIONARY & NORMALIZATION----------------------------------#
def normalize(text):
    text = text.lower().strip()
    text = re.sub(r"[^\w\s]", '', text)
    return text

QA_DICT = {"How are you?": "I'm doing well, what about you?", #x #o
           "Who are you?": "I'm a friendly Python bot who is waiting to be educate with AI. I am here to help you :)", #o
           "Exit": "Good Bye!",#x
           "What time is it?": f"{current_time}",#x #o
           "What day is it today?": f"{current_day}", #x #o
           "What's the full date of today?": f"{today}",#x #o
           "What's the Pi number?": f"{pi_number}",#x #o
           }

normalized_dict = {normalize(k): v for k, v in QA_DICT.items()}


#----------------------GEMINI API SECTION--------------------------------#


def get_response(user_command):
    cleaned_command = normalize(user_command)

    if cleaned_command == "tell me a joke":
        r = requests.get("https://v2.jokeapi.dev/joke/Any")
        data = r.json()
        if data["type"] == "single":
            joke = data['joke']
        elif data["type"] == "twopart":
            joke = f"{data['setup']} - {data['delivery']}"
        else:
            joke = "Coulnd't fetch a joke"
        return joke

    elif cleaned_command in normalized_dict:
        dict_answer = normalized_dict[cleaned_command]
        return dict_answer
    else:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"{user_command}"
        )
        return response.text

