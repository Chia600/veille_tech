import requests
import time
from datetime import datetime, timedelta
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

BASE_URL = "http://spring-boot:8080/api/resources"
NVD_API_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"

session = requests.Session()
retries = Retry(total=5, backoff_factor=1, status_forcelist=[429, 502, 503, 504])
session.mount("http://", HTTPAdapter(max_retries=retries))
session.mount("https://", HTTPAdapter(max_retries=retries))

def wait_for_spring_boot():
    print("Checking if Spring Boot is ready...")
    for _ in range(30):  # Attendre jusqu'à 5 minutes
        try:
            response = session.get("http://spring-boot:8080/health")
            print(f"Healthcheck response: {response.status_code} - {response.text}")
            if response.status_code == 200:
                print("Spring Boot is ready!")
                return
        except requests.exceptions.RequestException as e:
            print(f"Waiting for Spring Boot... Error: {e}")
            time.sleep(10)
    raise Exception("Spring Boot did not start in time")

def fetch_nvd_cves():
    try:
        print("Fetching NVD CVE data...")
        # Calculer les dates pour les 3 derniers mois
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=90)  # 3 mois = 90 jours
        params = {
            "resultsPerPage": 10,
            "startIndex": 0,
            "pubStartDate": start_date.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
            "pubEndDate": end_date.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        }
        print(f"Fetching CVEs from {params['pubStartDate']} to {params['pubEndDate']}")
        response = session.get(NVD_API_URL, params=params, timeout=10)
        print(f"HTTP status: {response.status_code}, URL: {response.url}")
        if response.status_code != 200:
            print(f"Failed to fetch CVE data: {response.status_code} - {response.text}")
            return
        data = response.json()
        vulnerabilities = data.get("vulnerabilities", [])
        print(f"Found {len(vulnerabilities)} CVE entries")
        if not vulnerabilities:
            print("No CVE entries found. Check API URL or parameters.")
            return
        for vuln in vulnerabilities:
            cve = vuln.get("cve", {})
            cve_id = cve.get("id", "")
            description = ""
            for desc in cve.get("descriptions", []):
                if desc.get("lang") == "en":
                    description = desc.get("value", "")
                    break
            cve_link = f"https://nvd.nist.gov/vuln/detail/{cve_id}"
            resource = {
                "title": cve_id,
                "link": cve_link,
                "description": description
            }
            print(f"Sending POST request with payload: {resource}")
            response = session.post(BASE_URL, json=resource)
            print(f"POST response: {response.status_code} - {response.text}")
            response.raise_for_status()
            print(f"Successfully posted CVE: {cve_id}")
    except requests.exceptions.RequestException as e:
        print(f"Erreur NVD: {e}")
    except Exception as e:
        print(f"Unexpected error in fetch_nvd_cves: {e}")

def test_xss():
    try:
        payload = {"title": "<script>alert(1)</script>", "link": "http://test.com", "description": "XSS test"}
        print(f"Sending XSS test payload: {payload}")
        response = session.post(BASE_URL, json=payload)
        print(f"XSS test response: {response.status_code} - {response.text}")
        response.raise_for_status()
        print("XSS test completed successfully")
    except requests.exceptions.RequestException as e:
        print(f"Erreur XSS: {e}")

def test_sqli():
    try:
        payload = {"title": "' UNION SELECT 1, current_database()--", "link": "http://test.com", "description": "SQLi test"}
        print(f"Sending SQLi test payload: {payload}")
        response = session.post(BASE_URL, json=payload)
        print(f"SQLi test response: {response.status_code} - {response.text}")
        response.raise_for_status()
        print("SQLi test completed successfully")
    except requests.exceptions.RequestException as e:
        print(f"Erreur SQLi: {e}")

if __name__ == "__main__":
    print("Starting Python script...")
    wait_for_spring_boot()
    # Exécuter les tests XSS et SQLi une seule fois au démarrage
    test_xss()
    test_sqli()
    while True:
        print(f"Starting CVE fetch cycle at {datetime.utcnow()}")
        fetch_nvd_cves()
        print("CVE fetch cycle completed. Sleeping for 7 days...")
        time.sleep(604800)  # 7 jours = 604 800 secondes