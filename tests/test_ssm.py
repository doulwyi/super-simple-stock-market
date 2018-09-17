# For given stock
# Given any price as input, calculate the dividend yield
# Given any price as input, calculate the P/E Ratio
# Record a trade, with timestamp, quantity of shares, buy or sell indicator and traded price
# Calculate Volume Weighted Stock Price based on trades in past 15 minutes
# Calculate the GBCE All Share Index using the geometric mean of prices for all stocks
import unittest

from sssmarket.sssm import Sssm, gbce_geometric_mean
from tests.data_example import data_example


class TestSsm(unittest.TestCase):

    def test_calculate_dividend_for_common_type(self):
        ssm = Sssm(stock='TEA', stock_type='common', last_dividend=0, fixed_dividend=None, par_value=100)
        price = 10.0
        expected_result = 0
        res = ssm.dividend_yield(price)
        self.assertEqual(expected_result, res)

    def test_calculate_dividend_for_common_type_price_0(self):
        ssm = Sssm(stock='TEA', stock_type='common', last_dividend=0, fixed_dividend=None, par_value=100)
        price = 0
        expected_result = None
        res = ssm.dividend_yield(price)
        self.assertEqual(expected_result, res)

    def test_calculate_dividend_for_common_type_with_dividend_greater_than_0(self):
        ssm = Sssm(stock='POP', stock_type='common', last_dividend=8, fixed_dividend=None, par_value=100)
        price = 10.0
        expected_result = 0.8
        res = ssm.dividend_yield(price)
        self.assertEqual(expected_result, res)

    def test_calculate_dividend_for_preferred_type(self):
        ssm = Sssm(stock='GIN', stock_type='preferred', last_dividend=8, fixed_dividend=2, par_value=100)
        price = 10.0
        expected_result = 0.2
        res = ssm.dividend_yield(price)
        self.assertEqual(expected_result, res)

    def test_calculate_p_e_ratio_with_dividend_greater_than_0(self):
        ssm = Sssm(stock='POP', stock_type='common', last_dividend=8, fixed_dividend=None, par_value=100)
        price = 10.0
        expected_result = 12.5
        res = ssm.calculate_p_e_ratio(price)
        self.assertEqual(expected_result, res)

    def test_calculate_p_e_ratio_with_dividend_less_than_0(self):
        ssm = Sssm(stock='POP', stock_type='common', last_dividend=8, fixed_dividend=None, par_value=100)
        price = 0
        expected_result = None
        res = ssm.calculate_p_e_ratio(price)
        self.assertEqual(expected_result, res)

    def test_record_a_trade(self):
        example_trade = {'shares': 10,
                         'indicator': 'buy',
                         'price': 100}
        ssm = Sssm('TEST').record_a_trade(example_trade)
        self.assertIsInstance(ssm, dict)

    def test_record_a_trade_float_number_shares(self):
        example_trade = {'shares': 10.0,
                         'indicator': 'buy',
                         'price': 100}

        with self.assertRaisesRegex(ValueError, 'Number of shares should be an integer.'):
            Sssm('TEST').record_a_trade(example_trade)

    def test_record_a_trade_str_number_shares(self):
        example_trade = {'shares': '10',
                         'indicator': 'buy',
                         'price': 100}

        with self.assertRaisesRegex(ValueError, 'Number of shares should be an integer.'):
            Sssm('TEST').record_a_trade(example_trade)

    def test_record_a_trade_share_less_than_0(self):
        example_trade = {'shares': -1,
                         'indicator': 'buy',
                         'price': 100}
        with self.assertRaisesRegex(ValueError, 'Shares should be more than 0'):
            Sssm('TEST').record_a_trade(example_trade)

    def test_record_a_trade_with_indicator_different_than_sell_or_buy(self):
        example_trade = {'shares': 10,
                         'indicator': 'foo',
                         'price': 100}
        with self.assertRaisesRegex(ValueError, 'Share indicator should be BUY or SELL'):
            Sssm('TEST').record_a_trade(example_trade)

    def test_record_a_trade_with_price_less_than_0(self):
        example_trade = {'shares': 10,
                         'indicator': 'buy',
                         'price': 0}
        with self.assertRaisesRegex(ValueError, 'Price should be more than 0'):
            Sssm('TEST').record_a_trade(example_trade)

    def test_volume_weighted_stock_price_based_in_past_15_minutes(self):
        ssm = Sssm(data_example[0]['stock_symbol'])
        expected_res = 108.0
        res = ssm.calculate_volume_weighted_stock_price(data_example)
        self.assertEqual(expected_res, res)

    def test_gbce(self):
        expected_res = 109
        res = gbce_geometric_mean(data_example)
        self.assertLess(expected_res, res)


if __name__ == '__main__':
    unittest.main()
