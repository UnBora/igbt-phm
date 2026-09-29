import unittest

import pandas as pd

from src.data_loader import SIGNAL_COLUMNS
from src.evaluation import evaluate_leave_one_device_out
from src.features import FEATURE_COLUMNS, TARGET_COLUMN, build_rul_features


def make_observations() -> pd.DataFrame:
    rows = []
    for device_number, duration in enumerate((240, 300, 360), start=2):
        for timestamp in range(0, duration + 1, 30):
            rows.append(
                {
                    "device_id": f"device_{device_number}",
                    "timestamp_s": 1_000_000 + device_number * 10_000 + timestamp,
                    "supply_voltage": 5.0 + device_number / 10,
                    "node1_voltage": 4.0 + timestamp / 1000,
                    "node2_voltage": 3.0 + timestamp / 1000,
                    "collector_emitter_current": 0.1 + device_number / 100,
                    "package_temperature": 25.0 + timestamp / 100,
                    "source_file": f"Device{device_number}.mat",
                }
            )
    return pd.DataFrame(rows, columns=["device_id", "timestamp_s", *SIGNAL_COLUMNS, "source_file"])


class RulWorkflowTests(unittest.TestCase):
    def test_features_are_windowed_and_label_run_end(self):
        features = build_rul_features(make_observations(), window_seconds=60)

        self.assertEqual(set(features["device_id"]), {"device_2", "device_3", "device_4"})
        self.assertEqual(
            features.groupby("device_id").size().to_dict(),
            {"device_2": 5, "device_3": 6, "device_4": 7},
        )
        self.assertTrue((features[TARGET_COLUMN] >= 0).all())
        self.assertTrue(
            features.groupby("device_id")[TARGET_COLUMN].min().eq(0).all()
        )
        self.assertTrue(set(FEATURE_COLUMNS).issubset(features.columns))

    def test_grouped_evaluation_predicts_each_device_once(self):
        features = build_rul_features(make_observations(), window_seconds=60)

        metrics, predictions = evaluate_leave_one_device_out(features)

        self.assertEqual(len(predictions), len(features))
        self.assertFalse(predictions.duplicated(["device_id", "timestamp_s"]).any())
        self.assertEqual(
            set(metrics.loc[metrics["held_out_device"] != "ALL_HELD_OUT", "held_out_device"]),
            set(features["device_id"]),
        )
        self.assertEqual(
            set(metrics.loc[metrics["held_out_device"] == "ALL_HELD_OUT", "model"]),
            {"training_median", "random_forest"},
        )

    def test_invalid_window_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "finite positive"):
            build_rul_features(make_observations(), window_seconds=0)


if __name__ == "__main__":
    unittest.main()
