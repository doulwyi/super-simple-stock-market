import datetime
import operator
from functools import reduce
from operator import itemgetter


class Sssm:

    def __init__(self, stock: str, stock_type: str = None, last_dividend: int = None, fixed_dividend: int = None,
                 par_value: int = None):

        self.stock = stock
        self.stock_type = stock_type
        self.last_dividend = last_dividend
        self.fixed_dividend = fixed_dividend
        self.par_value = par_value

    def dividend_yield(self, price):
        """
        Given any price as input, calculate the dividend yield
        :param price: Price as float.
        :type price: float
        :returns: Returns None if price is 0.
                  Returns Last dividend divide by price if stock type is common.
                  Returns 'preferred' formula if stock type is preferred.
        """
        if price == 0:
            return None
        if self.stock_type == 'common':
            return self.last_dividend / price
        return (float(self.fixed_dividend / 100) * self.par_value) / price

    def calculate_p_e_ratio(self, price):
        """
        Given any price as input, calculate the P/E Ratio
        :param price: Price as float.
        :type price: float
        :returns: Returns None if price 0.
                  Returns p/e ratio formula.
        """
        div_value = self.dividend_yield(price)
        if div_value == 0 or div_value is None:
            return None
        return price / div_value

    def record_a_trade(self, trade: dict):
        """
        Record a trade, with timestamp, quantity of shares, buy or sell indicator and traded price.
        :param trade: Dictionary with quantity of shares, buy or sell indicator and traded price
        :type trade: dict
        :return: Returns a dictionary with all information to be recorded.
        :rtype: dict
        """
        # Some test to validate the data from dictionary.
        if not isinstance(trade['shares'], int):
            raise ValueError('Number of shares should be an integer.')
        if trade['shares'] < 1:
            raise ValueError('Shares should be more than 0')
        if not trade['indicator'] in ['buy', 'sell']:
            raise ValueError('Share indicator should be BUY or SELL')
        if trade['price'] <= 0:
            raise ValueError('Price should be more than 0')

        # This generate a dictionary that can be saved to a JSON or database
        res = {'timestamp': datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f'),
               'stock_symbol': self.stock,
               'shares': trade['shares'],
               'indicator': trade['indicator'],
               'price': trade['price']}
        return res

    def calculate_volume_weighted_stock_price(self, trades: list, time: int = 15):
        """
        Calculate Volume Weighted Stock Price based on trades in past 15 minutes
        :param trades: List of dictionaries with all trades performed.
        :type trades: list
        :param time: Time to calculate vwsp. Default is 15 minutes.
        :type time: int
        :return: Volume weighted.
        """
        # Assuming the data is on JSON format (or CSV or a SQL query converted to dictionary), this function will read
        # the timestamp generated when it records a trade, sorted it for the latest trade.
        sorted_trades = sorted(trades, key=itemgetter('timestamp'), reverse=True)
        nt = datetime.datetime.strptime(sorted_trades[0]['timestamp'], '%Y-%m-%dT%H:%M:%S.%f')
        # It will find the time delta between the latest timestamp to time requested (default is 15 minutes)
        latest_trade = datetime.datetime(nt.year, nt.month, nt.day, nt.hour, nt.minute, nt.second,
                                         nt.microsecond) - datetime.timedelta(minutes=time)
        sum_prices = 0
        quantity = 0
        for trade in sorted_trades:
            if trade['stock_symbol'] == self.stock:
                trade_timestamp = datetime.datetime.strptime(trade['timestamp'], '%Y-%m-%dT%H:%M:%S.%f')
                if trade_timestamp >= latest_trade:
                    sum_prices += trade['price'] * trade['shares']
                    quantity += trade['shares']
        res = sum_prices / quantity
        return res


def gbce_geometric_mean(stocks: list):
    """
    Calculate the GBCE All Share Index using the geometric mean of prices for all stocks
    :param stocks:
    :return:
    """
    # Assuming all trades have been saved in a database or JSON file, this function expected a list of dictionaries
    # with all information needed to calculate the geometric mean of prices.
    price_list = list()
    for stock in stocks:
        price_list.append(stock['price'])
    res = reduce(operator.mul, price_list) ** (1 / len(price_list))
    return res
