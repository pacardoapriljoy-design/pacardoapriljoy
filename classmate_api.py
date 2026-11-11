
import requests

# ===================================
# CLASSMATE API CONFIGURATION
# ===================================

CLASSMATE_BASE_URL = "https://francineescultura-4.onrender.com"
ENDPOINT = "/api/students"

# Complete API URL
url = f"{CLASSMATE_BASE_URL}{ENDPOINT}"


# ===================================
# RETRIEVE CLASSMATE RECORDS
# ===================================

def get_classmate_records():

    try:

        response = requests.get(url, timeout=20)

        response.raise_for_status()

        data = response.json()

        # Accept either a list or a dictionary response
        if isinstance(data, list):
            records = data

        elif isinstance(data, dict):
            records = data.get(
                "students",
                data.get("records", [])
            )

        else:
            raise ValueError("Invalid API response format")

        if not isinstance(records, list):
            raise ValueError("Student records must be a list")

        return {
            "success": True,
            "records": records,
            "total": len(records)
        }

    except requests.exceptions.Timeout:

        return {
            "success": False,
            "error": "Classmate API request timed out"
        }

    except requests.exceptions.RequestException as e:

        return {
            "success": False,
            "error": str(e)
        }

    except ValueError as e:

        return {
            "success": False,
            "error": str(e)
        }


# ===================================
# TEST CLASSMATE API
# ===================================

if __name__ == "__main__":

    result = get_classmate_records()

    if result["success"]:

        print("Classmate API connected successfully!")

        print("Total Records:", result["total"])

        for student in result["records"]:
            print(student)

    else:

        print("API Connection Failed:")
        print(result["error"])
