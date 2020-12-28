from typing import Callable

from prometheus_client import Histogram
from prometheus_fastapi_instrumentator import Instrumentator, metrics
from prometheus_fastapi_instrumentator.metrics import Info

instrumentator = Instrumentator(
    should_group_status_codes=True,
    should_ignore_untemplated=True,
    should_respect_env_var=True,
    should_instrument_requests_inprogress=True,
    excluded_handlers=["/metrics"],
    env_var_name="ENABLE_METRICS",
    inprogress_name="inprogress",
    inprogress_labels=True,
)


# ----- custom metrics -----
def regression_model_output() -> Callable[[Info], None]:
    METRIC = Histogram(
        "regression_model_output",
        "Output value of wine quality regression model.",
        buckets=(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, float("inf")),
    )

    def instrumentation(info: Info) -> None:
        if info.modified_handler == "/predict":
            predicted_quality = info.response.headers.get("X-model-score")
            if predicted_quality:
                METRIC.observe(float(predicted_quality))

    return instrumentation


# ----- add metrics -----
instrumentator.add(
    metrics.request_size(
        should_include_handler=True,
        should_include_method=False,
        should_include_status=True,
        metric_namespace="fastapi",
        metric_subsystem="",
    )
)
instrumentator.add(
    metrics.response_size(
        should_include_handler=True,
        should_include_method=False,
        should_include_status=True,
        metric_namespace="fastapi",
        metric_subsystem="",
    )
)
instrumentator.add(
    metrics.latency(
        should_include_handler=True,
        should_include_method=False,
        should_include_status=True,
        metric_namespace="fastapi",
        metric_subsystem="",
    )
)
instrumentator.add(
    metrics.requests(
        should_include_handler=True,
        should_include_method=False,
        should_include_status=True,
        metric_namespace="fastapi",
        metric_subsystem="",
    )
)
instrumentator.add(regression_model_output())
