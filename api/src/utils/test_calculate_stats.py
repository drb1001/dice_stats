import unittest
from decimal import Decimal

from calculate_stats import calc_stats


class TestCalcStats(unittest.TestCase):
    """Test the function calc_stats()"""

    def test_calc_stats_1(self):

        input1 = [
            {'pip_total': 13, 'probability': Decimal('0.15')},
            {'pip_total': 14, 'probability': Decimal('0.35')},
            {'pip_total': 15, 'probability': Decimal('0.45')},
            {'pip_total': 16, 'probability': Decimal('0.05')}
        ]

        output1 = {
            'name': 'Test 1',
            'avg': 14.4,
            'min': 13,
            'max': 16,
            'mode': '15',
            'perc_10': 13,
            'perc_90': 15,
            'pct80_range': '13 to 15',
            'max_range': '13 to 16'
        }

        self.assertDictEqual(calc_stats(roll_name='Test 1', rolls=input1), output1)


    def test_calc_stats_2(self):

        input1 = [
            {'pip_total': 3, 'probability': Decimal('0.1')},
            {'pip_total': 4, 'probability': Decimal('0.4')},
            {'pip_total': 5, 'probability': Decimal('0.4')},
            {'pip_total': 6, 'probability': Decimal('0.1')}
        ]

        output1 = {
            'name': 'Test 2',
            'avg': 4.5,
            'min': 3,
            'max': 6,
            'mode': '4 & 5',
            'perc_10': 4,
            'perc_90': 5,
            'pct80_range': '4 to 5',
            'max_range': '3 to 6'
        }

        self.assertDictEqual(calc_stats(roll_name='Test 2', rolls=input1), output1)



if __name__ == '__main__':
    unittest.main()
