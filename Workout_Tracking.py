import requests
from datetime import datetime as dt
import os

# Datetime .............................................................................................
today = dt.now()
DATE = today.strftime("%d/%m/%Y")
TIME = today.strftime("%H:%M:%S")

# API_CONSTANTS ........................................................................................
APP_ID: str = os.environ["APP_ID"]
API_KEY: str = os.environ["API_KEY"]
HEADERS: dict = {"x-app-id": APP_ID,
                 "x-app-key": API_KEY,
                 }
exercise_endpoint: str = "https://trackapi.nutritionix.com/v2/natural/exercise"

# BODY_CONSTANTS ........................................................................................
GENDER = "male"
WEIGHT_KG = 75
HEIGHT_CM = 177
AGE = 38

exercise_done: str = input("What did you do today?")
# exercise_done = "Today I did 2 hours of brazilian jiujitsu and 2 hours of wrestling and came back home running 6 hour"

request: dict = {
    "query": exercise_done,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

response1 = requests.post(url=exercise_endpoint, json=request, headers=HEADERS)

# print(f"""
# Testing response1 .......................................................................................
# {type(response1) = }
# {response1 = }
# {response1.json() = }
# """)

dict_list: list = []
response1_data = response1.json()

for index1, element1 in enumerate(response1_data):
    #     print(f"""
    # {type(response1_data) = }
    # {index1 = }: {element1 = } {type(element1) = }
    # {type(response1_data[element1]) = }{response1_data[element1] = }
    # """)
    element1_data = response1_data[element1]
    for index2, element2 in enumerate(element1_data):
        # print(f"""{index2}: {element2}""")
        activity_dict = {"date": DATE,
                         "time": TIME,
                         "exercise": element2["user_input"],
                         "duration": element2['duration_min'],
                         "calories": element2['nf_calories']
                         }
        dict_list.append(activity_dict)

# print(f"""
# {dict_list = }
# {len(dict_list) = }
# """)

SHEET_ENDPOINT = os.environ["SHEET_ENDPOINT"]

# Bearer Token ...............................................................................................
TOKEN = os.environ["TOKEN"]
headers = {'Authorization': TOKEN}

for workout_dict in dict_list:
    body = {"workout": workout_dict}
    response2 = requests.post(url=SHEET_ENDPOINT, json=body, headers=headers)

    # print(f"""
    # Testing response1 ..........................................................................................
    # {type(response2) = }
    # {response2 = }
    # {response2.json() = }
    # """)
