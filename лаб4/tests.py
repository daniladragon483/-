import unittest
import os
from model import MeasurementModel

class TestLab4(unittest.TestCase):
    def setUp(self):
        self.model = MeasurementModel()

    def test_remove_condition(self):
        self.model.execute_command('ADD 2026.01.01 Moscow 15.0 red')
        self.model.execute_command('ADD 2026.01.02 Tomsk 5.0 blue')
        self.model.execute_command('REM value < 10.0')
        self.assertEqual(len(self.model.items), 1)
        self.assertEqual(self.model.items[0].location, 'Moscow')

    def test_command_direct(self):
        self.model.execute_command('ADD 2026.05.05;Omsk;25.0;red')
        self.model.execute_command('PRINT')
        self.model.execute_command('SAVE output_test.txt')
        
        self.assertEqual(len(self.model.items), 1)
        self.assertTrue(os.path.exists('output_test.txt'))
        
        if os.path.exists('output_test.txt'):
            os.remove('output_test.txt')

if __name__ == '__main__':
    unittest.main()