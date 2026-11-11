import unittest
import json
from scheduler.utils import save_schedule


def test_save_schedule_writes_json_to_requested_path(tmp_path):
    schedule = [{"nurse": "Nurse A", "patients": [1, 2]}]
    output_file = tmp_path / "schedule.json"

    save_schedule(schedule, filename=output_file)

    assert json.loads(output_file.read_text(encoding="utf-8")) == schedule

#class MyTestCase(unittest.TestCase):
#    def test_something(self):
#        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()
