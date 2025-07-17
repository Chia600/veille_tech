import requests
import feedparser
import uuid
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

BASE_URL = "http://spring-boot:8080/api/resources"

session = requests.Session()
retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
session.mount("http://", HTTPAdapter(max_retries=retries))

def fetch_nvd_feed():
    try:
        feed = feedparser.parse("https://nvd.nist.gov/feeds/xml/cve/misc/nvd-rss.xml")
        for entry in feed.entries:
            resource = {
                "id": str(uuid.uuid4()),
                "title": entry.title,
                "link": entry.link,
                "description": entry.summary
            }
            response = session.post(BASE_URL, json=resource)
            response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Erreur NVD: {e}")

def test_xss():
    try:
        payload = {"title": "<script>alert(1)</script>", "link": "http://test.com", "description": "XSS test"}
        response = session.post(BASE_URL, json=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Erreur XSS: {e}")

def test_sqli():
    try:
        payload = {"title": "' UNION SELECT 1, current_database()--", "link": "http://test.com", "description": "SQLi test"}
        response = session.post(BASE_URL, json=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Erreur SQLi: {e}")

if __name__ == "__main__":
    time.sleep(10)  # Wait for Spring Boot to start
    fetch_nvd_feed()
    test_xss()
    test_sqli()