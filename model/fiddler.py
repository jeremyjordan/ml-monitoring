import os
from pathlib import Path

import fiddler

from .train import prepare_dataset

ROOT_DIR = Path(__file__).parent

FIDDLER_URL = os.environ.get("FIDDLER_URL")
FIDDLER_ORG_ID = os.environ.get("FIDDLER_ORG_ID")
FIDDLER_AUTH_TOKEN = os.environ.get("FIDDLER_AUTH_TOKEN")

client = fiddler.FiddlerApi(url=FIDDLER_URL, org_id=FIDDLER_ORG_ID, auth_token=FIDDLER_AUTH_TOKEN)


def create_project(project_name):
    existing_projects = client.list_projects()
    if project_name not in existing_projects:
        client.create_project(project_name)


def upload_dataset(dataset_id="wine_quality"):
    dataset = prepare_dataset()
    df_schema = fiddler.DatasetInfo.from_dataframe(dataset["train"], max_inferred_cardinality=1000)
    client.upload_dataset(dataset=dataset, dataset_id=dataset_id, info=df_schema)


def upload_model(project_name, model_id):
    client.upload_model_package(
        artifact_path=ROOT_DIR,
        project_id=project_name,
        model_id=model_id,
        deployment_type="predictor",
    )
