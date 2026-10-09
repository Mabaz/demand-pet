import numpy as np
import pandas as pd
from sqlalchemy import text
from src.db import engine

# 1. Очищаем таблицу перед вставкой (чтобы seed был идемпотентным)
with engine.begin() as conn:
    conn.execute(text("TRUNCATE TABLE raw_sales RESTART IDENTITY;"))

# 2. Генерируем данные
np.random.seed(42)
days = np.arange(1, 101)
sales = 2 * days + 10 + np.random.normal(0, 5, size=len(days))

df = pd.DataFrame({"day_number": days, "sales": sales})

# 3. Записываем
df.to_sql("raw_sales", engine, if_exists="append", index=False)
print(f"✅ Seeded {len(df)} rows into raw_sales")