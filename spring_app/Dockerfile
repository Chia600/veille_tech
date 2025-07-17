# Étape de build
FROM maven:latest AS builder
WORKDIR /app
COPY pom.xml .
COPY src ./src
RUN mvn clean package -DskipTests

# Étape finale
FROM openjdk:17-jdk-slim
WORKDIR /app
# Installer curl
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
COPY --from=builder /app/target/veilletech-0.0.1-SNAPSHOT.jar app.jar
CMD ["java", "-jar", "app.jar"]