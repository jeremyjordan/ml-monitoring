import numpy as np
from fastapi import FastAPI, Response

from joblib import load
from .schemas import Wine, Rating
from .monitoring import instrumentator

app = FastAPI()
scaler = load("artifacts/scaler.joblib")
model = load("artifacts/model.joblib")
feature_names = [
    "fixed_acidity",
    "volatile_acidity",
    "citric_acid",
    "residual_sugar",
    "chlorides",
    "free_sulfur_dioxide",
    "total_sulfur_dioxide",
    "density",
    "ph",
    "sulphates",
    "alcohol_pct_vol",
]
instrumentator.instrument(app).expose(app, include_in_schema=False, should_gzip=True)


@app.get("/")
async def root():
    return "Wine Quality Ratings"


@app.post("/predict", response_model=Rating)
def predict(response: Response, sample: Wine):
    sample = sample.dict()
    features = np.array([sample[f] for f in feature_names]).reshape(1, -1)
    features_scaled = scaler.transform(features)
    prediction = model.predict(features_scaled)[0]
    response.headers["X-model-score"] = str(prediction)
    return Rating(quality=prediction)


@app.get("/healthcheck")
async def healthcheck():
    return {"staus": "ok"}
