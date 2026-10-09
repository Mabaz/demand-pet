import pandas as pd
from sqlalchemy import create_engine, text
from src.config import DB_URL

engine = create_engine(DB_URL)

def read_sales() -> pd.DataFrame:
    with engine.connect() as conn:
        return pd.read_sql("SELECT day_number, sales FROM raw_sales ORDER BY day_number", conn)

def write_predictions(df: pd.DataFrame) -> None:
    df.to_sql("predictions", engine, if_exists="append", index=False)

def write_log(level: str, message: str) -> None:
    with engine.begin() as conn:
        conn.execute(
            text("INSERT INTO pipeline_logs (level, message) VALUES (:l, :m)"),
            {"l": level, "m": message},
        )