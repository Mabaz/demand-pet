CREATE TABLE IF NOT EXISTS raw_sales (
    id         SERIAL PRIMARY KEY,
    day_number INTEGER NOT NULL,
    sales      FLOAT   NOT NULL
);

CREATE TABLE IF NOT EXISTS predictions (
    id              SERIAL PRIMARY KEY,
    created_at      TIMESTAMP DEFAULT NOW(),
    day_number      INTEGER NOT NULL,
    predicted_sales FLOAT   NOT NULL
);

CREATE TABLE IF NOT EXISTS pipeline_logs (
    id         SERIAL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT NOW(),
    level      VARCHAR(10),
    message    TEXT
);