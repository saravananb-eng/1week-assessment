import csv
import json
import os

import requests
from dotenv import load_dotenv

BASE_URL = "https://jsonplaceholder.typicode.com"
TIMEOUT = 5



def process_employees(path="employees.csv"):
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    for row in rows:
        row["salary"] = int(row["salary"])

    with open("employees.json", "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2)

    high = [r for r in rows if r["salary"] > 50000]
    with open("high_earners.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(high)

    print(f"Rows read: {len(rows)} | High earners: {len(high)}")



def load_api_key():
    load_dotenv()
    key = os.getenv("API_KEY")
    if not key:
        print("Warning: API_KEY not found in .env")
    return key



def fetch_users(headers):
    try:
        resp = requests.get(f"{BASE_URL}/users", headers=headers, timeout=TIMEOUT)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.Timeout:
        print("Error: request timed out")
    except requests.exceptions.ConnectionError:
        print("Error: could not connect to the server")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")
    return []


def check_missing_user(headers):
    try:
        resp = requests.get(f"{BASE_URL}/users/9999", headers=headers, timeout=TIMEOUT)
        if resp.status_code == 404:
            print("/users/9999 -> 404 Not found")
        else:
            print(f"/users/9999 -> {resp.status_code}")
    except requests.exceptions.Timeout:
        print("Error: request timed out")
    except requests.exceptions.ConnectionError:
        print("Error: could not connect to the server")



def save_users(users):
    cleaned = []
    for u in users:
        cleaned.append({
            "id": u.get("id"),
            "name": u.get("name"),
            "email": u.get("email"),
            "city": u.get("address", {}).get("city"),
            "lat": u.get("address", {}).get("geo", {}).get("lat"),
            "company": u.get("company", {}).get("name"),
        })
    with open("users.json", "w", encoding="utf-8") as f:
        json.dump(cleaned, f, indent=2)


def main():
    process_employees()
    api_key = load_api_key()
    headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}

    users = fetch_users(headers)
    for u in users[:3]:
        print(f"{u['id']} - {u['name']} - {u['email']}")

    check_missing_user(headers)

    if users:
        save_users(users)


if __name__ == "__main__":
    main()
