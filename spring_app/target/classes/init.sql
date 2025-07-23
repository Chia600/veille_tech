CREATE TABLE resource (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    link VARCHAR(255) NOT NULL,
    description TEXT,
    source VARCHAR(50)
);