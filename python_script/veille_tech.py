import requests
import feedparser
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

BASE_URL = "http://spring-boot:8080/api/resources"

session = requests.Session()
retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
session.mount("http://", HTTPAdapter(max_retries=retries))

def wait_for_spring_boot():
    for _ in range(30):  # Attendre jusqu'à 5 minutes
        try:
            response = session.get("http://spring-boot:8080/")
            print(f"Healthcheck response: {response.status_code} - {response.text}")
            if response.status_code == 200:
                print("Spring Boot is ready!")
                return
        except requests.exceptions.RequestException as e:
            print(f"Waiting for Spring Boot... Error: {e}")
            time.sleep(10)
    raise Exception("Spring Boot did not start in time")

def fetch_nvd_feed():
    try:
        print("Fetching NVD feed...")
        feed = feedparser.parse("https://nvd.nist.gov/feeds/xml/cve/misc/nvd-rss.xml")
        print(f"Feed status: {feed.get('status', 'No status')}, Entries: {len(feed.entries)}")
        if not feed.entries:
            print("No entries found in the feed.")
        for entry in feed.entries:
            print(f"Processing entry: {entry.title}")
            resource = {
                "title": entry.title,
                "link": entry.link,
                "description": entry.summary
            }
            print(f"Sending POST request with payload: {resource}")
            response = session.post(BASE_URL, json=resource)
            print(f"POST response: {response.status_code} - {response.text}")
            response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Erreur NVD: {e}")
    except Exception as e:
        print(f"Unexpected error in fetch_nvd_feed: {e}")

def test_xss():
    try:
        payload = {"title": "<script>alert(1)</script>", "link": "http://test.com", "description": "XSS test"}
        print(f"Sending XSS test payload: {payload}")
        response = session.post(BASE_URL, json=payload)
        print(f"XSS test response: {response.status_code} - {response.text}")
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Erreur XSS: {e}")

def test_sqli():
    try:
        payload = {"title": "' UNION SELECT 1, current_database()--", "link": "http://test.com", "description": "SQLi test"}
        print(f"Sending SQLi test payload: {payload}")
        response = session.post(BASE_URL, json=payload)
        print(f"SQLi test response: {response.status_code} - {response.text}")
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Erreur SQLi: {e}")

if __name__ == "__main__":
    print("Starting Python script...")
    wait_for_spring_boot()
    fetch_nvd_feed()
    test_xss()
    test_sqli()