
import requests

PARTNER_API = "https://francineescultura-4.onrender.com/api/students"

record = {
    "student_id": "EXT-001",
    "name": "Sample Exchange Record",
    "program": "BSIT",
    "year": 1,
    "section": "A",
    "source": "Partner API"
}

try:
    response = requests.post(
        PARTNER_API,
        json=record,
        timeout=15
    )

    print("Status Code:", response.status_code)
    print("Partner Response:", response.text)

except requests.RequestException as error:
    print("Connection Error:", error)
