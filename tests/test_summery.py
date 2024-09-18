import unittest

from histral_core.summery import extractive_summary


class TestSummary(unittest.TestCase):
    """
    Unit tests for `histral_core.summery` module
    """

    def test_extractive_summary_success(self):
        # Large text to ensure summarization
        text = "This is a test document. " * 50

        summary = extractive_summary(text)

        self.assertLess(len(summary), len(text))

    def test_extractive_summary_percentage(self):
        text = "This is a test document. " * 50
        percentage = 0.1  # 10% of the original length
        expected_len = min(len(text) * percentage, 1200)

        summary = extractive_summary(text, percentage)

        self.assertLessEqual(len(summary), expected_len)

    def test_extractive_summary_empty_text(self):
        text = ""

        summary = extractive_summary(text)

        # An empty input should return an empty summary
        self.assertEqual(summary, "")

    def test_extractive_summary_single_sentence(self):
        text = "Single sentence"

        summary = extractive_summary(text)

        # A single sentence should return itself
        self.assertEqual(summary, text)


if __name__ == "__main__":
    unittest.main()
