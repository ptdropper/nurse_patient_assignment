import unittest

from unittest.mock import mock_open, patch
from scheduler.utils import save_schedule

@patch("builtins.open", new_callable=mock_open)
def test_save_schedule(mock_file):
    schedule = [{"nurse": "Nurse A", "patients": [1, 2]}]
    save_schedule(schedule)
    mock_file.assert_called_once_with('data/schedule.json', 'w')


#class MyTestCase(unittest.TestCase):
#    def test_something(self):
#        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()
