import requests
import time
from datetime import datetime, timedelta
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import feedparser
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

BASE_URL = "http://spring-boot:8080/api/resources"
NVD_API_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"
CERT_FR_RSS = "https://www.cert.ssi.gouv.fr/feed/"
CISA_KEV_RSS = "https://www.cisa.gov/uscert/ncas/alerts.xml"
HACKER_NEWS_RSS = "https://feeds.feedburner.com/TheHackersNews?format=xml"

session = requests.Session()
retries = Retry(total=5, backoff_factor=1, status_forcelist=[429, 502, 503, 504])
session.mount("http://", HTTPAdapter(max_retries=retries))
session.mount("https://", HTTPAdapter(max_retries=retries))

def wait_for_spring_boot():
    logger.info("Vérification de la disponibilité de Spring Boot...")
    for _ in range(30):  # Attendre jusqu'à 5 minutes
        try:
            response = session.get("http://spring-boot:8080/health", timeout=10)
            logger.info(f"Réponse du healthcheck : {response.status_code} - {response.text}")
            if response.status_code == 200:
                logger.info("Spring Boot est prêt !")
                return
        except requests.exceptions.RequestException as e:
            logger.warning(f"En attente de Spring Boot... Erreur : {e}")
            time.sleep(10)
    raise Exception("Spring Boot n'a pas démarré à temps")

def fetch_nvd_cves():
    try:
        logger.info("Récupération des données CVE de NVD...")
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=90)
        params = {
            "resultsPerPage": 10,
            "startIndex": 0,
            "pubStartDate": start_date.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
            "pubEndDate": end_date.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        }
        logger.info(f"Récupération des CVE de {params['pubStartDate']} à {params['pubEndDate']}")
        response = session.get(NVD_API_URL, params=params, timeout=10)
        logger.info(f"Statut HTTP : {response.status_code}, URL : {response.url}")
        response.raise_for_status()
        data = response.json()
        vulnerabilities = data.get("vulnerabilities", [])
        logger.info(f"{len(vulnerabilities)} entrées CVE trouvées")
        if not vulnerabilities:
            logger.warning("Aucune entrée CVE trouvée. Vérifiez l'URL de l'API ou les paramètres.")
            return
        for vuln in vulnerabilities:
            cve = vuln.get("cve", {})
            cve_id = cve.get("id", "")
            description = next((desc.get("value", "") for desc in cve.get("descriptions", []) if desc.get("lang") == "en"), "")
            cve_link = f"https://nvd.nist.gov/vuln/detail/{cve_id}"
            resource = {
                "title": cve_id,
                "link": cve_link,
                "description": description,
                "source": "NVD"
            }
            logger.info(f"Envoi de la requête POST avec le payload : {resource}")
            response = session.post(BASE_URL, json=resource, timeout=10)
            response.raise_for_status()
            logger.info(f"CVE posté avec succès : {cve_id}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Erreur NVD : {e}")
    except Exception as e:
        logger.error(f"Erreur inattendue dans fetch_nvd_cves : {e}")

def fetch_cert_fr():
    try:
        logger.info("Récupération des alertes CERT-FR...")
        feed = feedparser.parse(CERT_FR_RSS)
        logger.info(f"Statut du flux RSS CERT-FR : {feed.get('status', 'N/A')}")
        logger.info(f"{len(feed.entries)} alertes trouvées dans le flux RSS")
        if not feed.entries:
            logger.warning("Aucune alerte trouvée dans le flux RSS.")
            return
        for entry in feed.entries[:10]:
            resource = {
                "title": entry.get("title", "Sans titre"),
                "link": entry.get("link", ""),
                "description": entry.get("summary", "Aucune description disponible"),
                "source": "CERT-FR"
            }
            logger.info(f"Envoi de la requête POST avec le payload : {resource}")
            response = session.post(BASE_URL, json=resource, timeout=10)
            response.raise_for_status()
            logger.info(f"Alerte postée avec succès : {resource['title']}")
    except Exception as e:
        logger.error(f"Erreur lors de la récupération de CERT-FR : {e}")

def fetch_cisa_kev():
    try:
        logger.info("Récupération des alertes CISA KEV...")
        response = session.get(CISA_KEV_RSS, timeout=10)
        logger.info(f"Statut HTTP brut : {response.status_code}, URL : {response.url}")
        response.raise_for_status()
        feed = feedparser.parse(response.content)
        logger.info(f"Statut du flux RSS CISA KEV : {feed.get('status', 'N/A')}")
        logger.info(f"Contenu brut du flux (premiers 500 caractères) : {response.text[:500]}")
        logger.info(f"{len(feed.entries)} alertes trouvées dans le flux RSS")
        if not feed.entries:
            logger.warning("Aucune alerte trouvée dans le flux RSS CISA KEV. Vérifiez si le flux est vide ou mal formé.")
            return
        for entry in feed.entries[:10]:
            resource = {
                "title": entry.get("title", "Sans titre"),
                "link": entry.get("link", ""),
                "description": entry.get("summary", "Aucune description disponible"),
                "source": "NVD-RSS"
            }
            logger.info(f"Envoi de la requête POST avec le payload : {resource}")
            response = session.post(BASE_URL, json=resource, timeout=10)
            response.raise_for_status()
            logger.info(f"Alerte postée avec succès : {resource['title']}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Erreur réseau lors de la récupération de CISA KEV : {e}")
    except Exception as e:
        logger.error(f"Erreur inattendue dans fetch_cisa_kev : {e}")

def fetch_hacker_news():
    try:
        logger.info("Récupération des articles de The Hacker News...")
        feed = feedparser.parse(HACKER_NEWS_RSS)
        logger.info(f"Statut du flux RSS The Hacker News : {feed.get('status', 'N/A')}")
        logger.info(f"{len(feed.entries)} articles trouvés")
        if not feed.entries:
            logger.warning("Aucun article trouvé dans le flux RSS The Hacker News.")
            return
        for entry in feed.entries[:10]:
            resource = {
                "title": entry.get("title", "Sans titre"),
                "link": entry.get("link", ""),
                "description": entry.get("summary", "Aucune description"),
                "source": "TheHackerNews"
            }
            logger.info(f"Envoi de la requête POST avec le payload : {resource}")
            response = session.post(BASE_URL, json=resource, timeout=10)
            response.raise_for_status()
            logger.info(f"Article posté avec succès : {resource['title']}")
    except Exception as e:
        logger.error(f"Erreur lors de la récupération de The Hacker News : {e}")

def test_xss():
    try:
        payload = {"title": "<script>alert(1)</script>", "link": "http://test.com", "description": "Test XSS", "source": "Test"}
        logger.info(f"Envoi du payload de test XSS : {payload}")
        response = session.post(BASE_URL, json=payload, timeout=10)
        response.raise_for_status()
        logger.info("Test XSS terminé avec succès")
    except requests.exceptions.RequestException as e:
        logger.error(f"Erreur XSS : {e}")

def test_sqli():
    try:
        payload = {"title": "' UNION SELECT 1, current_database()--", "link": "http://test.com", "description": "Test SQLi", "source": "Test"}
        logger.info(f"Envoi du payload de test SQLi : {payload}")
        response = session.post(BASE_URL, json=payload, timeout=10)
        response.raise_for_status()
        logger.info("Test SQLi terminé avec succès")
    except requests.exceptions.RequestException as e:
        logger.error(f"Erreur SQLi : {e}")

if __name__ == "__main__":
    logger.info("Démarrage du script Python...")
    wait_for_spring_boot()
    test_xss()
    test_sqli()
    while True:
        logger.info(f"Démarrage du cycle de récupération à {datetime.utcnow()}")
        fetch_nvd_cves()
        fetch_cert_fr()
        fetch_cisa_kev()
        fetch_hacker_news()
        logger.info("Cycle de récupération terminé. Pause de 7 jours...")
        time.sleep(604800)  # 7 jours