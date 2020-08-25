import backtrader as bt
from datetime import datetime
import argparse
 
def parse_args():
    parser = argparse.ArgumentParser(description='Argparse Example program\
                        for backtesting')

    parser.add_argument('instrument',
                        help='The yahoo ticker of the instrument being tested')

    parser.add_argument('start_year', type=int,
                        help='Starting date in YYYY')
    parser.add_argument('start_month', type=int,
                    help='Starting date in MM format')
    parser.add_argument('start_day', type=int,
                        help='Starting date in DD format')
    parser.add_argument('end_year', type=int,
                        help='Ending date in YYYY format')
    parser.add_argument('end_month', type=int,
                        help='Ending date in MM format')
    parser.add_argument('end_day', type=int,
                        help='Ending date in DD format')

    parser.add_argument('-p', '--period',
                        default=21,
                        type=int,
                        help='Select the RSI lookback period')

    parser.add_argument('-r', '--rsi',
                        choices=['SMA', 'EMA'],
                        help='Select wether a simple moving average or exponential\
                         moving average is used in the RSI calcuation')

    return parser.parse_args()
  
class firstStrategy(bt.Strategy):
    params = (
        ('rsi', 'SMA'),
        ('period', 21),
        )

    def __init__(self):
        if self.p.rsi == 'EMA':
            self.rsi = bt.indicators.RSI_EMA(self.data.close, period=self.p.period)
        else:
            self.rsi = bt.indicators.RSI_SMA(self.data.close, period=self.p.period)

    def next(self):
        if not self.position:
            if self.rsi < 30:
                self.buy(size=100)
        else:
            if self.rsi > 70:
                self.sell(size=100)
    pass
#Get Args
args = parse_args()
print(args.instrument)
 
#Convert date args to datetime objects
fd = datetime(args.start_year, args.start_month, args.start_day)
td = datetime(args.end_year, args.end_month, args.end_day)
 
#Variable for our starting cash
startcash = 10000
 
#Create an instance of cerebro
cerebro = bt.Cerebro()
 
#Add our strategy
cerebro.addstrategy(firstStrategy, rsi=args.rsi, period=args.period)
 
#Get Apple data from Yahoo Finance.
data = bt.feeds.Quandl(
    dataname=args.instrument,
    fromdate = fd,
    todate = td,
    buffered= True
    )

#Add the data to Cerebro
cerebro.adddata(data)
 
# Set our desired cash start
cerebro.broker.setcash(startcash)
 
# Run over everything
cerebro.run()
 
#Get final portfolio Value
portvalue = cerebro.broker.getvalue()
pnl = portvalue - startcash
 
#Print out the final result
print('Final Portfolio Value: ${}'.format(portvalue))
print('P/L: ${}'.format(pnl))
 
#Finally plot the end results
#cerebro.plot(style='candlestick')