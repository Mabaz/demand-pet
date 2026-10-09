from loguru import logger
import pandas as pd

from src.db import read_sales, write_predictions, write_log
from src import model

def run() -> None:
    try:
        logger.info("Pipeline started")
        write_log("INFO", "Pipeline started")

        # 1. Читаем данные
        df = read_sales()
        logger.info(f"Read {len(df)} rows from raw_sales")
        if df.empty:
            raise ValueError("raw_sales is empty")

        # 2. Обучаем
        X, y = df[["day_number"]], df["sales"]
        m = model.train(X, y)
        logger.info(f"Trained: coef={m.coef_[0]:.4f}, intercept={m.intercept_:.4f}")
        write_log("INFO", f"Trained coef={m.coef_[0]:.4f}")

        # 3. Прогноз на 7 дней вперёд
        last_day = int(df["day_number"].max())
        future = pd.DataFrame({"day_number": range(last_day + 1, last_day + 8)})
        preds = m.predict(future)

        out = pd.DataFrame({
            "day_number": future["day_number"],
            "predicted_sales": preds,
        })
        write_predictions(out)
        logger.info(f"Wrote {len(out)} predictions")
        write_log("INFO", f"Wrote {len(out)} predictions")

    except Exception as e:
        logger.exception("Pipeline failed")
        write_log("ERROR", str(e))
        raise

if __name__ == "__main__":
    run()