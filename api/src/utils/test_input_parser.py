import unittest

from input_parser import tidy_input, parse_input


class TestTidyInput(unittest.TestCase):
    """Test the function tidy_input()"""

    def test_tidy_input(self):
        self.assertEqual(tidy_input('2 d20  kh -4'), '2d20kh-4')
        self.assertEqual(tidy_input('1d4 + 3'), '1d4+3')
        self.assertEqual(tidy_input('1D2KH+0'), '1d2kh+0')


class TestParseInput(unittest.TestCase):
    """Test the function parse_input()"""

    def test_parse_input(self):

        self.assertDictEqual(parse_input('10d6'),
            {
                'input': '10d6',
                'input_no_const': '10d6',
                'num': 10,
                'sides': 6,
                'kh_mod': None,
                'r_mod': None,
                'r_val': 0,
                'const_sign': None,
                'const': 0
            })

        self.assertDictEqual(parse_input('2d20dl-3'),
            {
                'input': '2d20dl-3',
                'input_no_const': '2d20dl',
                'num': 2,
                'sides': 20,
                'kh_mod': 'dl',
                'r_mod': None,
                'r_val': 0,
                'const_sign': '-',
                'const': -3
            })

        self.assertDictEqual(parse_input('4d12r<2+10'),
            {
                'input': '4d12r<2+10',
                'input_no_const': '4d12r<2',
                'num': 4,
                'sides': 12,
                'kh_mod': None,
                'r_mod': 'r<',
                'r_val': 2,
                'const_sign': '+',
                'const': 10
            })


if __name__ == '__main__':
    unittest.main()
