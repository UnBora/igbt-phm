"""Create windowed degradation features and remaining-record labels."""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.stats import kurtosis, skew

from src.data_loader import SIGNAL_COLUMNS


FEATURE_COLUMNS = (
    "elapsed_time_hours",
    "supply_voltage",
    "node1_voltage",
    "node2_voltage",
    "collector_emitter_current",
    "package_temperature",
)
TARGET_COLUMN = "remaining_observed_hours"


def extract_time_domain_features(signal_values: np.ndarray) -> dict[str, float | int]:
    """Summarize one complete, finite one-dimensional waveform capture.

    These descriptive statistics are not automatically PHM indicators; interpret
    them only after checking the waveform, measurement conditions, and units.
    """
    values = np.asarray(signal_values, dtype=float).squeeze()
    if values.ndim != 1 or values.size < 4:
        raise ValueError("signal_values must be a one-dimensional array with at least four samples.")
    if not np.isfinite(values).all():
        raise ValueError("signal_values must contain only finite samples.")

    mean = float(np.mean(values))
    standard_deviation = float(np.std(values))
    rms = float(np.sqrt(np.mean(values**2)))
    absolute_peak = float(np.max(np.abs(values)))
    if rms == 0:
        raise ValueError("Crest factor is undefined for a zero-RMS waveform.")
    if standard_deviation <= np.sqrt(np.finfo(float).eps) * max(1.0, abs(mean)):
        shape_skewness = float("nan")
        shape_kurtosis = float("nan")
    else:
        shape_skewness = float(skew(values, bias=False))
        shape_kurtosis = float(kurtosis(values, fisher=True, bias=False))

    return {
        "sample_count": int(values.size),
        "mean": mean,
        "standard_deviation": standard_deviation,
        "rms": rms,
        "minimum": float(np.min(values)),
        "maximum": float(np.max(values)),
        "absolute_peak": absolute_peak,
        "peak_to_peak": float(np.ptp(values)),
        "skewness": shape_skewness,
        "excess_kurtosis": shape_kurtosis,
        "crest_factor": absolute_peak / rms,
    }


def build_rul_features(
    observations: pd.DataFrame, window_seconds: float = 60.0
) -> pd.DataFrame:
    """Aggregate telemetry into windows and label time to each run's last record.

    The target is the remaining *observed test duration*, not time to a verified
    physical failure. See the README before interpreting it as RUL.
    """
    if not np.isfinite(window_seconds) or window_seconds <= 0:
        raise ValueError("window_seconds must be a finite positive number.")
    required_columns = {"device_id", "timestamp_s", *SIGNAL_COLUMNS}
    missing = sorted(required_columns.difference(observations.columns))
    if missing:
        raise ValueError(f"Observations are missing required columns: {', '.join(missing)}")
    if observations.empty:
        raise ValueError("Cannot build features from an empty observations table.")

    device_features = []
    for device_id, device_data in observations.groupby("device_id", sort=True):
        device_data = device_data.sort_values("timestamp_s").copy()
        start_time = float(device_data["timestamp_s"].min())
        end_time = float(device_data["timestamp_s"].max())
        device_data["_window"] = np.floor(
            (device_data["timestamp_s"] - start_time) / window_seconds
        ).astype("int64")

        aggregations = {
            "timestamp_s": "median",
            **{column: "median" for column in SIGNAL_COLUMNS},
        }
        windows = device_data.groupby("_window", sort=True).agg(aggregations).reset_index(drop=True)
        windows["device_id"] = device_id
        windows["elapsed_time_hours"] = (windows["timestamp_s"] - start_time) / 3600.0
        windows[TARGET_COLUMN] = (end_time - windows["timestamp_s"]) / 3600.0
        device_features.append(windows)

    features = pd.concat(device_features, ignore_index=True)
    features = features.replace([np.inf, -np.inf], np.nan)
    features = features.dropna(subset=[*FEATURE_COLUMNS, TARGET_COLUMN])
    if features.empty:
        raise ValueError("No complete feature windows could be created.")
    return features.sort_values(["device_id", "timestamp_s"]).reset_index(drop=True)
