"""Tests for eval aggregation and the run order."""

from __future__ import annotations

import unittest

from stats import decide, interleave, summarize


class StatsTests(unittest.TestCase):
    def test_median_ratio_and_interval_are_stable(self):
        summary = summarize(
            {"orders": ([10, 80, 12, 11, 13], [20, 21, 19, 22, 20])},
            lower_is_better=True,
            seed=2,
            draws=200,
        )
        self.assertAlmostEqual(summary["ratio"], 12 / 20)
        self.assertEqual(summary["better_on"], "1 / 1")
        self.assertFalse(summary["crosses_one"])
        self.assertEqual(summary["tasks"][0]["experiment_range"], (10, 80))

    def test_zero_control_is_undefined(self):
        summary = summarize({"empty": ([1, 1, 1], [0, 0, 0])}, seed=1, draws=50)
        self.assertIsNone(summary["ratio"])
        self.assertEqual(summary["undefined"], ["empty"])
        self.assertTrue(summary["crosses_one"])

    def test_noise_hides_a_gap_inside_the_spread(self):
        summary = summarize({"noisy": ([10, 30], [12, 28])}, seed=1, draws=40)
        self.assertFalse(summary["tasks"][0]["measurable"])

    def test_quality_drop_is_not_a_win(self):
        quality = summarize({"q": ([0.4, 0.4, 0.4], [0.9, 0.9, 0.9])}, lower_is_better=False, seed=1, draws=40)
        hard = summarize({"h": ([5, 5, 5], [20, 20, 20])}, lower_is_better=True, seed=1, draws=40)
        flags = dict(limiter_named=True, settings_match=True, errors_checked=True, work_confirmed=True)
        self.assertEqual(decide(quality=quality, hard=hard, **flags), "regressed")

    def test_missing_proof_is_inconclusive(self):
        quality = summarize({"q": ([1, 1], [1, 1])}, lower_is_better=False, seed=1, draws=20)
        hard = summarize({"h": ([5, 5], [10, 10])}, seed=1, draws=20)
        verdict = decide(
            quality=quality,
            hard=hard,
            limiter_named=True,
            settings_match=False,
            errors_checked=True,
            work_confirmed=True,
        )
        self.assertEqual(verdict, "inconclusive")

    def test_interleave_alternates_arms(self):
        order = interleave(["new", "previous", "none"], ["bug-1"], 2)
        self.assertEqual([item["arm"] for item in order], ["new", "previous", "none", "new", "previous", "none"])
        self.assertEqual(len(order), 6)


if __name__ == "__main__":
    unittest.main()
