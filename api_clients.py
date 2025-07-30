# api_clients.py

import os
import pickle
import datetime
import random
import requests
from bs4 import BeautifulSoup
import sys
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from appdirs import user_data_dir

# --- Google Calendar API Configuration ---
SCOPES = ['https://www.googleapis.com/auth/calendar.events.readonly']
APP_NAME = "PersonalDashboard"
APP_AUTHOR = "YourName"

# --- Path Setup ---
if getattr(sys, 'frozen', False):
    bundle_dir = sys._MEIPASS
else:
    bundle_dir = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_FILE = os.path.join(bundle_dir, 'credentials.json')

APP_DATA_DIR = user_data_dir(APP_NAME, APP_AUTHOR)
os.makedirs(APP_DATA_DIR, exist_ok=True)
TOKEN_FILE = os.path.join(APP_DATA_DIR, 'token.json')


def authenticate_google_calendar():
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_FILE):
                print("Error: credentials.json not found.")
                return None
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
    return creds


def get_google_calendar_service():
    creds = authenticate_google_calendar()
    if creds:
        try:
            return build('calendar', 'v3', credentials=creds)
        except Exception as e:
            print(f"Error building calendar service: {e}")
    return None


def fetch_upcoming_events(num_events=2):
    service = get_google_calendar_service()
    if not service: return ["Google Calendar service not available."]
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    try:
        events_result = service.events().list(calendarId='primary', timeMin=now, maxResults=num_events,
                                              singleEvents=True, orderBy='startTime').execute()
        events = events_result.get('items', [])
        if not events: return ['No upcoming events found.']
        events_list = []
        for event in events:
            start_str = event['start'].get('dateTime', event['start'].get('date'))
            if 'T' in start_str:
                dt_obj = datetime.datetime.fromisoformat(start_str.replace('Z', '+00:00')).astimezone()
                formatted_start = dt_obj.strftime('%a, %b %d at %I:%M %p')
            else:
                dt_obj = datetime.datetime.strptime(start_str, '%Y-%m-%d')
                formatted_start = dt_obj.strftime('%a, %b %d (All-day)')
            events_list.append(f"{formatted_start}<br>- {event['summary']}")
        return events_list
    except Exception as e:
        return [f"Error fetching events: {e}"]


def fetch_trending_meme_url():
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get("https://imgflip.com/tag/memes", headers=headers, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, 'html.parser')
        img = soup.find('img', class_='base-img')
        return "https:" + img['src'] if img and img.has_attr('src') else None
    except Exception as e:
        print(f"Error fetching meme: {e}")
        return None


def fetch_wisdom_quote():
    """Scrapes quotes.toscrape.com for a random quote."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get("https://quotes.toscrape.com/", headers=headers, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, 'html.parser')
        quotes = soup.find_all('div', class_='quote')
        if not quotes: return "No quotes found."
        q = random.choice(quotes)
        text = q.find('span', class_='text').get_text(strip=True)
        author = q.find('small', class_='author').get_text(strip=True)

        # --- THIS IS THE KEY FIX ---
        # The scraped 'text' already contains quotes, so we don't add our own.
        return f'{text}\n- {author}'
        # --- END OF FIX ---

    except Exception as e:
        print(f"Error fetching quote: {e}")
        return "Failed to fetch wisdom quote."


def fetch_recipe_of_the_day():
    """Fetches a random recipe from TheMealDB API, including instructions."""
    try:
        url = "https://www.themealdb.com/api/json/v1/1/random.php"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        meal = data['meals'][0]
        title = meal['strMeal']
        ingredients = []
        for i in range(1, 21):
            ingredient = meal[f'strIngredient{i}']
            measure = meal[f'strMeasure{i}']
            if ingredient and ingredient.strip():
                ingredients.append(f"{measure} {ingredient}")
        instructions = meal['strInstructions']
        return {
            "title": title,
            "ingredients": ingredients,
            "instructions": instructions
        }
    except Exception as e:
        print(f"An error occurred in the recipe API process: {e}")
        return None