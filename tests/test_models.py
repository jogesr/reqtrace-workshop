import unittest

from reqtrace.models import Requirement, TestCaseSpec, ValidationError
from tests.helpers import make_requirement_dict, make_testcase_dict


class RequirementTests(unittest.TestCase):
    def test_valid_requirement_is_parsed(self):
        req = Requirement.from_dict(make_requirement_dict())
        self.assertEqual(req.id, "REQ-100")
        self.assertEqual(req.priority, "mittel")

    def test_unknown_priority_is_rejected(self):
        with self.assertRaises(ValidationError):
            Requirement.from_dict(make_requirement_dict(priority="dringend"))

    def test_missing_title_is_rejected(self):
        with self.assertRaises(ValidationError):
            Requirement.from_dict(make_requirement_dict(title="  "))

    def test_roundtrip_to_dict(self):
        data = make_requirement_dict()
        self.assertEqual(Requirement.from_dict(data).to_dict(), data)

    # Übung 4: Weitere Tests zu APP-02 (ID-Format) aus REQUIREMENTS.md ableiten.


class TestCaseSpecTests(unittest.TestCase):
    def test_valid_testcase_defaults_to_not_run(self):
        tc = TestCaseSpec.from_dict(make_testcase_dict())
        self.assertEqual(tc.last_result, "not_run")
        self.assertEqual(tc.requirement_ids, ["REQ-100"])

    def test_invalid_requirement_reference_is_rejected(self):
        with self.assertRaises(ValidationError):
            TestCaseSpec.from_dict(make_testcase_dict(requirement_ids=["REQ-1"]))


if __name__ == "__main__":
    unittest.main()
