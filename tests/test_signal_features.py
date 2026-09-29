import unittest

import numpy as np

from src.features import extract_time_domain_features


class TimeDomainFeatureTests(unittest.TestCase):
    def test_extracts_descriptive_statistics(self):
        values = np.array([-2.0, -1.0, 1.0, 2.0])

        features = extract_time_domain_features(values)

        self.assertEqual(features["sample_count"], 4)
        self.assertEqual(features["mean"], 0.0)
        self.assertAlmostEqual(features["rms"], np.sqrt(2.5))
        self.assertEqual(features["minimum"], -2.0)
        self.assertEqual(features["maximum"], 2.0)
        self.assertEqual(features["absolute_peak"], 2.0)
        self.assertEqual(features["peak_to_peak"], 4.0)
        self.assertAlmostEqual(features["crest_factor"], 2 / np.sqrt(2.5))
        self.assertAlmostEqual(features["skewness"], 0.0, places=12)

    def test_rejects_non_finite_values(self):
        with self.assertRaisesRegex(ValueError, "finite"):
            extract_time_domain_features(np.array([0.0, 1.0, np.nan, 2.0]))

    def test_rejects_too_few_samples(self):
        with self.assertRaisesRegex(ValueError, "at least four"):
            extract_time_domain_features(np.array([1.0, 2.0, 3.0]))

    def test_rejects_zero_rms_waveform(self):
        with self.assertRaisesRegex(ValueError, "zero-RMS"):
            extract_time_domain_features(np.zeros(4))


if __name__ == "__main__":
    unittest.main()
