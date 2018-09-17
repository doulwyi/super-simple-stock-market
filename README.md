# super-simple-stock-market


## How to clone this project
`git clone https://github.com/doulwyi/super-simple-stock-market.git`

`cd super-simple-stock-market/`

## Creating a virtual environment

- Python 3.6, 3.7 (Preferred)

`python -m venv venv` *Creates a virtual environment*

`/venv/Scripts/Activate.bat` *On CMD*

`/venv/Scripts/Activate.ps1` *On PowerShell*

`/venv/Scripts/Activate` *On Unix*

## Installing the python package
`pip install .`

## Usage

```
>>> from sssmarket import sssm
>>> s = sssm.Sssm(stock='POP')

>>> s.stock_type = 'common'
>>> s.last_dividend = 8
>>> s.par_value = 100

>>> s.dividend_yield(10)
0.8

>>> s.calculate_p_e_ratio(10)
12.5

>>> s.record_a_trade({'shares': 10, 'indicator': 'buy', 'price':100})
{'timestamp': '2018-09-16T22:08:15.208716', 'stock_symbol': 'POP', 'shares': 10, 'indicator': 'buy', 'price': 100}
```

### Unit tests
`python -m unittest -v tests/test_ssm.py`

