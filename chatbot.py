import re
import math
import datetime
import requests
import os
from google import genai
from dotenv import load_dotenv
import sqlite3

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)

#----------------------DATABASE SECTION--------------------------------#

def init_db():
    conn = sqlite3.connect("chat_memory.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   session_id TEXT,
                   role TEXT,
                   content TEXT,
                   timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                   )
               """)
    conn.commit()
    conn.close()

init_db()


def save_message(session_id, role, content):
    conn = sqlite3.connect("chat_memory.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO messages (session_id, role, content, timestamp)
        VALUES (?, ?, ?, ?)
    """, (session_id, role, content, datetime.datetime.now().isoformat()))
    conn.commit()
    conn.close()

def load_recent_messages(session_id, limit=10):
    conn = sqlite3.connect("chat_memory.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT role, content FROM messages
        WHERE session_id = ?
        ORDER BY id DESC
        LIMIT ?
    """, (session_id, limit))

    rows = cursor.fetchall()
    conn.close()
    return list(reversed(rows))


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

QA_DICT = {"How are you?": "I'm doing well, what about you?",
           "Who are you?": "I'm a friendly Python bot who is waiting to be educate with AI. I am here to help you :)", #o
           "Exit": "Good Bye!",
           "What time is it?": f"{current_time}",
           "What day is it today?": f"{current_day}",
           "What's the full date of today?": f"{today}",
           "What's the Pi number?": f"{pi_number}",
           }

normalized_dict = {normalize(k): v for k, v in QA_DICT.items()}


#----------------------GEMINI API SECTION--------------------------------#

SESSION_ID = "deafult_user"

def get_response(user_command):
    cleaned_command = normalize(user_command)

    #JOKE API
    if cleaned_command == "tell me a joke":
        r = requests.get("https://v2.jokeapi.dev/joke/Any")
        data = r.json()
        if data["type"] == "single":
            bot_reply = data['joke']
        elif data["type"] == "twopart":
            bot_reply = f"{data['setup']} - {data['delivery']}"
        else:
            bot_reply = "Coulnd't fetch a joke"
    
    #DICTIONARY PART
    elif cleaned_command in normalized_dict:
        bot_reply = normalized_dict[cleaned_command]
        
    
    #GEMINI API
    else:
        recent_messages = load_recent_messages(SESSION_ID)

        conversation_context  = ""
        for role, content in recent_messages:
            conversation_context += f"{role}: {content}\n"
        
        conversation_context += f"user: {user_command}"

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents = conversation_context
        )
        bot_reply = response.text
    
    save_message(SESSION_ID, "user", user_command)
    save_message(SESSION_ID, "bot", bot_reply)

    return bot_reply




