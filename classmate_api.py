
import requests

CLASSMATE_BASE_URL = "https://francineescultura.onrender.com"
ENDPOINT = "/api/students"

url = f"{CLASSMATE_BASE_URL}{ENDPOINT}"

try:
    response = requests.get(url, timeout=20)

    if response.status_code == 200:

        data = response.json()

        print("--- Classmate's API Response ---")

        for student in data:
            print(student)

    else:
        print("Request failed.")
        print("Status Code:", response.status_code)
        print("Response:", response.text)

except requests.exceptions.RequestException as e:
    print("Connection error:", e)
