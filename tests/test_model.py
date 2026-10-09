import pandas as pd
from pathlib import Path
from unittest.mock import patch
from src import model

def test_train_and_load(tmp_path):
    """
    Тест проверяет, что модель обучается, сохраняется и загружается корректно.
    tmp_path — это временная папка, которую pytest создает автоматически.
    """
    # 1. Подменяем путь к модели на временный файл, чтобы не засорять папку models/
    model_path = tmp_path / "test_model.pkl"
    
    with patch("src.model.MODEL_PATH", model_path):
        # 2. Создаем простые данные: y = 2*x + 1
        # При x=[1,2,3,4,5], y должен быть [3,5,7,9,11]
        X = pd.DataFrame({"day_number": [1, 2, 3, 4, 5]})
        y = pd.Series([3, 5, 7, 9, 11])
        
        # 3. Обучаем модель
        m = model.train(X, y)
        
        # 4. Проверяем, что коэффициенты правильные (с округлением)
        assert round(m.coef_[0], 2) == 2.0, "Наклон (coef) должен быть 2.0"
        assert round(m.intercept_, 2) == 1.0, "Сдвиг (intercept) должен быть 1.0"
        
        # 5. Проверяем, что модель загружается из файла
        loaded_m = model.load()
        assert round(loaded_m.coef_[0], 2) == 2.0, "Загруженная модель должна иметь тот же наклон"