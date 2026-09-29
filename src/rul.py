"""Run an educational, device-held-out RUL baseline on the NASA IGBT data."""

from __future__ import annotations

import argparse
from pathlib import Path

import joblib
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from src.data_loader import load_aging_observations
from src.evaluation import evaluate_leave_one_device_out, make_regressor
from src.features import FEATURE_COLUMNS, TARGET_COLUMN, build_rul_features


def run_workflow(
    data_root: Path,
    project_root: Path,
    window_seconds: float = 60.0,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Load data, build labels, evaluate, and save workflow outputs."""
    observations = load_aging_observations(data_root)
    features = build_rul_features(observations, window_seconds=window_seconds)
    metrics, predictions = evaluate_leave_one_device_out(features)

    feature_path = project_root / "data" / "features" / "rul_features.csv"
    metric_path = project_root / "results" / "metrics" / "rul_lodo_metrics.csv"
    prediction_path = project_root / "results" / "metrics" / "rul_lodo_predictions.csv"
    figure_path = project_root / "results" / "figures" / "rul_lodo_predictions.png"
    model_path = project_root / "models" / "rul_random_forest.joblib"
    for path in (feature_path, metric_path, prediction_path, figure_path, model_path):
        path.parent.mkdir(parents=True, exist_ok=True)

    features.to_csv(feature_path, index=False)
    metrics.to_csv(metric_path, index=False)
    predictions.to_csv(prediction_path, index=False)
    _save_prediction_figure(predictions, figure_path)

    final_model = make_regressor()
    final_model.fit(features[list(FEATURE_COLUMNS)], features[TARGET_COLUMN])
    joblib.dump(
        {
            "model": final_model,
            "feature_columns": list(FEATURE_COLUMNS),
            "target_column": TARGET_COLUMN,
            "target_definition": "hours remaining until the last recorded observation",
            "window_seconds": window_seconds,
        },
        model_path,
    )
    return features, metrics, predictions


def _save_prediction_figure(predictions: pd.DataFrame, path: Path) -> None:
    actual = predictions[TARGET_COLUMN]
    maximum = max(float(actual.max()), 1e-9)
    fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharex=True, sharey=True)
    for ax, model_name, title in (
        (axes[0], "training_median", "Training-median baseline"),
        (axes[1], "random_forest", "Random forest"),
    ):
        predicted = predictions[f"{model_name}_prediction_hours"]
        for device_id, indices in predictions.groupby("device_id").groups.items():
            ax.scatter(
                actual.loc[indices],
                predicted.loc[indices],
                s=18,
                alpha=0.7,
                label=device_id,
            )
        ax.plot([0, maximum], [0, maximum], "k--", linewidth=1, label="ideal")
        ax.set(title=title, xlabel="Observed remaining time (hours)")
        ax.grid(alpha=0.25)
    axes[0].set_ylabel("Predicted remaining time (hours)")
    axes[1].legend(title="Held-out device", fontsize="small")
    fig.suptitle("Leave-one-device-out predictions (observation-horizon proxy)")
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--data-root",
        type=Path,
        default=project_root / "data" / "raw" / "IGBTAgingData_04022009",
        help="Dataset extraction directory (or the Aging Data directory itself).",
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        default=project_root,
        help="Project directory where features, metrics, figure, and model are saved.",
    )
    parser.add_argument(
        "--window-seconds",
        type=float,
        default=60.0,
        help="Window size used to aggregate steady-state records.",
    )
    args = parser.parse_args()

    features, metrics, _ = run_workflow(
        args.data_root,
        args.project_root,
        window_seconds=args.window_seconds,
    )
    print(f"Created {len(features)} feature windows across {features['device_id'].nunique()} devices.")
    print(metrics.loc[metrics["held_out_device"] == "ALL_HELD_OUT"].to_string(index=False))
    print("Interpret the target as time to the end of the recorded run, not verified physical RUL.")


if __name__ == "__main__":
    main()