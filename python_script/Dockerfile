FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY veille_tech.py .
CMD ["sh", "-c", "while true; do python veille_tech.py; sleep 86400; done"]