from pathlib import Path

import numpy as np
from fastapi import FastAPI, Response

from joblib import load
from .schemas import Wine, Rating, feature_names
from .monitoring import instrumentator

ROOT_DIR = Path(__file__).parent.parent

app = FastAPI()
scaler = load(ROOT_DIR / "artifacts/scaler.joblib")
model = load(ROOT_DIR / "artifacts/model.joblib")
instrumentator.instrument(app).expose(app, include_in_schema=False, should_gzip=True)


@app.get("/")
async def root():
    return "Wine Quality Ratings"


@app.post("/predict", response_model=Rating)
def predict(response: Response, sample: Wine):
    sample_dict = sample.dict()
    features = np.array([sample_dict[f] for f in feature_names]).reshape(1, -1)
    features_scaled = scaler.transform(features)
    prediction = model.predict(features_scaled)[0]
    response.headers["X-model-score"] = str(prediction)
    return Rating(quality=prediction)


@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}
