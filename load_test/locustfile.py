"""
Run load tests:

locust -f load_test/locustfile.py --host http://127.0.0.1:3000
"""

from locust import HttpUser, task
import pandas as pd
import random

feature_columns = {
    "fixed acidity": "fixed_acidity",
    "volatile acidity": "volatile_acidity",
    "citric acid": "citric_acid",
    "residual sugar": "residual_sugar",
    "chlorides": "chlorides",
    "free sulfur dioxide": "free_sulfur_dioxide",
    "total sulfur dioxide": "total_sulfur_dioxide",
    "density": "density",
    "pH": "ph",
    "sulphates": "sulphates",
    "alcohol": "alcohol_pct_vol",
}
dataset = (
    pd.read_csv(
        "https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv",
        delimiter=";",
    )
    .rename(columns=feature_columns)
    .drop("quality", axis=1)
    .to_dict(orient="records")
)


class WinePredictionUser(HttpUser):
    @task(1)
    def healthcheck(self):
        self.client.get("/healthcheck")

    @task(10)
    def prediction(self):
        record = random.choice(dataset).copy()
        self.client.post("/predict", json=record)

    @task(2)
    def prediction_bad_value(self):
        record = random.choice(dataset).copy()
        corrupt_key = random.choice(list(record.keys()))
        record[corrupt_key] = "bad data"
        self.client.post("/predict", json=record)
