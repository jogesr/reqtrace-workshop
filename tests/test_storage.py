import json
import unittest

from reqtrace import storage
from reqtrace.models import ValidationError
from tests.helpers import IsolatedDataTestCase, make_requirement_dict


class StorageTests(IsolatedDataTestCase):
    def test_seed_data_loads(self):
        reqs = storage.load_requirements()
        tcs = storage.load_testcases()
        self.assertEqual(len(reqs), 12)
        self.assertEqual(len(tcs), 10)

    def test_duplicate_ids_are_rejected(self):
        path = self.data_dir / storage.REQUIREMENTS_FILE
        path.write_text(json.dumps([make_requirement_dict(), make_requirement_dict()]), encoding="utf-8")
        with self.assertRaises(ValidationError):
            storage.load_requirements()

    def test_save_and_reload_testcases(self):
        tcs = storage.load_testcases()
        tcs[0].last_result = "failed"
        storage.save_testcases(tcs)
        self.assertEqual(storage.load_testcases()[0].last_result, "failed")


if __name__ == "__main__":
    unittest.main()
