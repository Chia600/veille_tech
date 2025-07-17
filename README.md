# Veille Technologique - Cybersécurité (Dockerisé avec PostgreSQL)

Site Spring Boot avec un script Python pour collecter des ressources de veille technologique en cybersécurité, conteneurisé avec Docker.

## Fonctionnalités
- **API REST** : Gère des ressources (titre, lien, description) via `/api/resources`.
- **Frontend Thymeleaf** : Affiche les ressources avec Bootstrap.
- **Base PostgreSQL** : Stockage des données.
- **Script Python** : Scrape RSS (The Hacker News) et API NVD (CVE).
- **Tests de sécurité** : Vérification XSS et SQLi (bloqués par OWASP Sanitizer et JPA).

## Prérequis
- Docker et Docker Compose.

## Installation
1. Clonez le dépôt :
   ```bash
   git clone <votre-repo>
   cd veilletech-project