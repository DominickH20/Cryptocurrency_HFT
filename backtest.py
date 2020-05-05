from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime
import os.path
import sys
import backtrader as bt
import backtrader.analyzers as btanalyzers
import backtrader.feeds as btfeed
import backtrader.strategies as btstrats

class customCSV(btfeed.GenericCSVData):
    params = (
        ('dtformat', '%Y-%m-%d'),
        ('tmformat', '%H:%M:%S.%f'),
        ('datetime', 0),
        ('time', 1),
        ('open', 2),
        ('high', 2),
        ('low', 2),
        ('close', 2),
        ('volume', 6),
        ('openinterest', -1),
    )

class TestStrategy(bt.Strategy):
    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None
        self.buyprice = None
        self.buycomm = None

        #self.sma = bt.indicators.SimpleMovingAverage(self.datas[0], period=20)
        #self.rsi = bt.indicators.RelativeStrengthIndex()
        #self.bb = bt.indicators.BollingerBands()
        self.direction = self.datas[0].volume

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Write down: no pending order
        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def next(self):
        #self.log('Close, %.2f' % self.dataclose[0])
        #print('rsi:', self.rsi[0])
        if self.order:
            return

        if not self.position:
            #if (self.rsi[0] < 30):
            if (self.direction[0] ==2): #buy signal
                self.log('BUY CREATE, %.2f' % self.dataclose[0])
                self.order = self.buy()

        else:
            #if (self.rsi[0] > 70):
            if (self.direction[0]==0): #sell signal
                self.log('SELL CREATE, %.2f' % self.dataclose[0])
                self.order = self.sell()


if __name__ == '__main__':
    cerebro = bt.Cerebro(stdstats=False)
    cerebro.addobserver(bt.observers.Value)
    cerebro.addobserver(bt.observers.Trades)
    #cerebro.addobserver(bt.observers.BuySell) a bit too messy I feel, plots the buy sell arrows

    cerebro.addstrategy(TestStrategy)
    #cerebro.addanalyzer(btanalyzers.SharpeRatio, _name='mysharpe',timeframe=bt.TimeFrame.Ticks) bug in his library
    #cerebro.broker.setcommission(commission=0.005) Coinbase fee is 0.5%. Other exchanges have lower fees especially if using limit orders and higher volume that could make the strategy most viable

    datapath = 'test_predictions.csv'

    # Create a Data Feed
    data = customCSV(dataname='test_predictions.csv', timeframe = bt.TimeFrame.Ticks)

    cerebro.adddata(data)
    cerebro.broker.setcash(100000.0)
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    thestrats = cerebro.run()
    thestrat = thestrats[0]
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.plot()
