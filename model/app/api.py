import os
from pathlib import Path

import numpy as np
from fastapi import FastAPI, Response, BackgroundTasks

from joblib import load
from .schemas import Wine, Rating, feature_names
from .monitoring import instrumentator
from model.fiddler_monitoring import client


FIDDLER_PROJECT = os.environ.get("FIDDLER_PROJECT", "jj_wine_quality")
FIDDLER_MODEL_ID = os.environ.get("FIDDLER_MODEL_ID", "sklearn_model")
ROOT_DIR = Path(__file__).parent.parent

app = FastAPI()
scaler = load(ROOT_DIR / "artifacts/scaler.joblib")
model = load(ROOT_DIR / "artifacts/model.joblib")
instrumentator.instrument(app).expose(app, include_in_schema=False, should_gzip=True)


def log_prediction(sample: Wine, prediction: Rating):
    event_dict = sample.dict()
    event_dict["predicted_quality"] = prediction.quality
    client.publish_event(
        project_id=FIDDLER_PROJECT, model_id=FIDDLER_MODEL_ID, event=event_dict,
    )


@app.get("/")
async def root():
    return "Wine Quality Ratings"


@app.post("/predict", response_model=Rating)
def predict(response: Response, sample: Wine, background_tasks: BackgroundTasks):
    sample_dict = sample.dict()
    features = np.array([sample_dict[f] for f in feature_names]).reshape(1, -1)
    features_scaled = scaler.transform(features)
    prediction = model.predict(features_scaled)[0]
    response.headers["X-model-score"] = str(prediction)
    response = Rating(quality=prediction)
    background_tasks.add_task(log_prediction, sample, response)
    return response


@app.get("/healthcheck")
async def healthcheck():
    return {"staus": "ok"}
