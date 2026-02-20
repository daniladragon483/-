import unittest
from model import MeasurementModel

class TestTemperatureModel(unittest.TestCase):
    def setUp(self):
        self.model = MeasurementModel()

    def test_add_correct_line(self):
        line = 'Entry 2026.02.16 "Moscow" 12.5 "красный"'
        result = self.model.add_from_line(line)
        self.assertTrue(result)
        self.assertEqual(len(self.model.items), 1)

    def test_add_incorrect_date(self):
        line = 'Entry 2026.99.99 "London" 10.0 "белый"'
        result = self.model.add_from_line(line)
        self.assertFalse(result)
        self.assertEqual(len(self.model.items), 0)

if __name__ == '__main__':
    unittest.main()