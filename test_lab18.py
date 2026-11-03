import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / ".agents" / "skills" / "buffett-investor" / "scripts"))
from sec_buffett import validate_memo


class MemoValidatorTests(unittest.TestCase):
    def setUp(self):
        self.analysis = {"rows": [{"ROE": {"percent": 18.2}, "Revenue": {"millions": 100.0}, "Net income": {"millions": 10.0},
                                    "Operating cash flow": {"millions": 20.0}, "Capital spending": {"millions": 5.0},
                                    "Equity": {"millions": 50.0}, "Owner earnings": {"millions": 15.0}}]}

    def test_unsupported_percentage_is_flagged_without_year_false_positive(self):
        issues = validate_memo("FY2026 had ROE of 40.0%. COST had $10.0 million in net income.", self.analysis)
        self.assertIn("Unsupported percentage: 40.0%", issues)
        self.assertFalse(any("2026" in issue for issue in issues))

    def test_supported_numbers_pass_validator(self):
        self.assertEqual(validate_memo("FY2026 ROE was 18.2%; net income was $10.0 million.", self.analysis), [])
