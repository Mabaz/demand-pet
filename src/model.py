import joblib
from sklearn.linear_model import LinearRegression
from src.config import MODEL_PATH

def train(X, y) -> LinearRegression:
    model = LinearRegression()
    model.fit(X, y)
    MODEL_PATH.parent.mkdir(exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    return model

def load() -> LinearRegression:
    return joblib.load(MODEL_PATH)