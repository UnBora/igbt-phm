"""Device-held-out evaluation for remaining-observation-time models."""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from src.features import FEATURE_COLUMNS, TARGET_COLUMN


def make_regressor() -> RandomForestRegressor:
    """Return the baseline nonlinear regressor used in the workflow."""
    return RandomForestRegressor(
        n_estimators=200,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1,
    )


def _regression_metrics(actual: np.ndarray, predicted: np.ndarray) -> dict[str, float]:
    return {
        "mae_hours": float(mean_absolute_error(actual, predicted)),
        "rmse_hours": float(np.sqrt(mean_squared_error(actual, predicted))),
        "r2": float(r2_score(actual, predicted)) if len(actual) > 1 else float("nan"),
    }


def evaluate_leave_one_device_out(
    features: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Evaluate with each complete device held out once to prevent device leakage."""
    required = {"device_id", "timestamp_s", *FEATURE_COLUMNS, TARGET_COLUMN}
    missing = sorted(required.difference(features.columns))
    if missing:
        raise ValueError(f"Feature table is missing required columns: {', '.join(missing)}")

    device_ids = sorted(features["device_id"].dropna().unique())
    if len(device_ids) < 2:
        raise ValueError("Leave-one-device-out evaluation requires at least two devices.")

    metric_rows: list[dict[str, str | int | float]] = []
    prediction_rows: list[pd.DataFrame] = []
    for held_out_device in device_ids:
        test = features.loc[features["device_id"] == held_out_device]
        train = features.loc[features["device_id"] != held_out_device]
        if train.empty or test.empty:
            raise ValueError(f"Cannot evaluate held-out device {held_out_device!r}.")

        actual = test[TARGET_COLUMN].to_numpy(dtype=float)
        models = {
            "training_median": DummyRegressor(strategy="median"),
            "random_forest": make_regressor(),
        }
        fold_predictions = test[["device_id", "timestamp_s", TARGET_COLUMN]].copy()
        for model_name, model in models.items():
            model.fit(train[list(FEATURE_COLUMNS)], train[TARGET_COLUMN])
            predicted = model.predict(test[list(FEATURE_COLUMNS)])
            metric_rows.append(
                {
                    "held_out_device": held_out_device,
                    "model": model_name,
                    "n_windows": len(test),
                    **_regression_metrics(actual, predicted),
                }
            )
            fold_predictions[f"{model_name}_prediction_hours"] = predicted
        prediction_rows.append(fold_predictions)

    predictions = pd.concat(prediction_rows, ignore_index=True)
    for model_name in ("training_median", "random_forest"):
        prediction_column = f"{model_name}_prediction_hours"
        metric_rows.append(
            {
                "held_out_device": "ALL_HELD_OUT",
                "model": model_name,
                "n_windows": len(predictions),
                **_regression_metrics(
                    predictions[TARGET_COLUMN].to_numpy(dtype=float),
                    predictions[prediction_column].to_numpy(dtype=float),
                ),
            }
        )
    return pd.DataFrame(metric_rows), predictions