"""
Fiddler's expected model wrapper class.
https://docs.fiddler.ai/api-reference/package-py/
"""

from pathlib import Path
from joblib import load

import pandas as pd

from wine_quality_model.app.schemas import feature_names

ROOT_DIR = Path(__file__).parent
MODEL_PATH = ROOT_DIR / "artifacts" / "model.joblib"
SCALER_PATH = ROOT_DIR / "artifacts" / "scaler.joblib"


class MyModel:
    def __init__(self, model_path=MODEL_PATH, scaler_path=SCALER_PATH):
        self.scaler = load(scaler_path)
        self.model = load(model_path)

    def transform_input(self, input_df):
        return input_df[feature_names]

    def predict(self, input_df):
        features_scaled = self.scaler.transform(input_df)
        predictions = self.model.predict(features_scaled)
        return pd.DataFrame({"predicted_quality": predictions})


def get_model():
    return MyModel()
