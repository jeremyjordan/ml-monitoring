import os
from pathlib import Path

import fiddler as fdl

from ..train import prepare_dataset
from ..app.schemas import feature_names

ROOT_DIR = Path(__file__).parent

FIDDLER_URL = os.environ.get("FIDDLER_URL")
FIDDLER_ORG_ID = os.environ.get("FIDDLER_ORG_ID")
FIDDLER_AUTH_TOKEN = os.environ.get("FIDDLER_AUTH_TOKEN")

client = fdl.FiddlerApi(url=FIDDLER_URL, org_id=FIDDLER_ORG_ID, auth_token=FIDDLER_AUTH_TOKEN)


def create_project(project_id="jj_wine_quality"):
    existing_projects = client.list_projects()
    if project_id not in existing_projects:
        client.create_project(project_id)


def upload_dataset(project_id="jj_wine_quality", dataset_id="wine_quality"):
    dataset = prepare_dataset()
    df_schema = fdl.DatasetInfo.from_dataframe(dataset["train"], max_inferred_cardinality=1000)
    client.upload_dataset(
        project_id=project_id, dataset=dataset, dataset_id=dataset_id, info=df_schema
    )


def upload_model(
    project_id="jj_wine_quality",
    dataset_id="wine_quality",
    model_id="sklearn_model",
    target="quality",
    metadata_cols=[],
    decision_cols=[],
    outputs=["predicted_quality"],
):
    dataset_info = client.get_dataset_info(project_id, dataset_id)
    model_info = fdl.ModelInfo.from_dataset_info(
        dataset_info=dataset_info,
        target=target,
        features=feature_names,
        metadata_cols=metadata_cols,
        decision_cols=decision_cols,
        outputs=outputs,
        input_type=fdl.ModelInputType.TABULAR,
        model_task=fdl.ModelTask.REGRESSION,
        display_name="Wine quality prediction model",
        description="",
    )
    client.register_model(project_id, model_id, dataset_id, model_info)
    client.update_model(project_id, model_id, ROOT_DIR)
