import unittest
import formatting

class Test_formatting(unittest.TestCase):

    def test_can_format_number_as_string(self):
        single = formatting.format_number(2)
        self.assertEqual("02", single)

if __name__ == '__main__':
    unittest.main()
