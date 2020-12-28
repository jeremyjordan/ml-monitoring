"""
Train a scikit-learn model on UCI Wine Quality Dataset
https://archive.ics.uci.edu/ml/datasets/wine+quality
"""

import logging
from pathlib import Path

import pandas as pd
from joblib import dump
from sklearn import preprocessing
from sklearn.experimental import enable_hist_gradient_boosting  # noqa
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

logger = logging.getLogger(__name__)


def train():
    logger.info("Preparing dataset...")
    dataset = pd.read_csv(
        "https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv",
        delimiter=";",
    )
    target = dataset["quality"]
    features = dataset.drop("quality", axis=1)
    X_train, X_test, y_train, y_test = train_test_split(
        features, target, test_size=0.20, random_state=1
    )

    logger.info("Training model...")
    scaler = preprocessing.StandardScaler().fit(X_train)
    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)
    model = HistGradientBoostingRegressor(max_iter=50).fit(X_train, y_train)

    y_pred = model.predict(X_test)
    error = mean_squared_error(y_test, y_pred)
    logger.info(f"Test MSE: {error}")

    logger.info("Saving artifacts...")
    Path("artifacts").mkdir(exist_ok=True)
    dump(model, "artifacts/model.joblib")
    dump(scaler, "artifacts/scaler.joblib")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    train()
