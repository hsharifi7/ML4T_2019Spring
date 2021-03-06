import pandas as pd
import datetime as dt
import numpy as np
import math

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from util import get_data


def get_price(symbols, dates):
    # get prices of stocks indicated by the symbols, NOTE: get the adjusted closing price.

    # always get the price data with SPY to make sure there is no missing dates
    prices_all = get_data(symbols, dates, addSPY=True, colname='Adj Close')

    prices = prices_all[symbols]  # only portfolio symbols
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later

    # dealing with missing values in the data file.
    prices.fillna(method='ffill', inplace=True)
    prices.fillna(method='bfill', inplace=True)

    return prices, prices_SPY


def get_SMA(prices, lookback):
    # calculate simple moving average from prices
    SMA = prices.rolling(window=lookback,center=False).mean()
    # calculate the price to SMA ratio (PSR)
    PSR = prices / SMA - 1

    return SMA, PSR


def get_BB(prices, lookback):
    # calculate Bollinger Bands from price

    SMA, _ = get_SMA(prices, lookback)
    rolling_std = prices.rolling(window=lookback,center=False).std()
    upper_bb = SMA + (2 * rolling_std)
    lower_bb = SMA - (2 * rolling_std)
    bb_indicator = (prices - SMA) / (2 * rolling_std)
    return upper_bb, lower_bb, bb_indicator


def get_volatility(prices):
    daily_returns = (prices / prices.shift(1)) - 1
    daily_returns = daily_returns[1:]

    VOL = daily_returns.std()

    return VOL


def get_momentum(prices, lookback):

    momentum = prices / prices.shift(lookback) - 1
    return momentum

def plot_indicators():
    # This function WILL NOT be called by the auto grader
    # Do not assume that any variables defined here are available to your function/code
    # It is only here to help you set up and test your code
    #
    # Define input parameters
    # Note that ALL of these values will be set to different values by
    # the autograder!

    start_date = dt.datetime(2008, 1, 1)
    end_date = dt.datetime(2009, 12, 31)
    dates = pd.date_range(start_date, end_date)
    lookback = 14
    symbols = ['JPM']

    # Assess the portfolio
    prices, prices_SPY = get_price(symbols, dates)
    # normed_prices = prices / prices.iloc[0,:]
    # normed_prices_SPY = prices_SPY / prices_SPY.iloc[0]

    SMA, PSR = get_SMA(prices, lookback)

    upper_bb, lower_bb, bb_indicator = get_BB(prices, lookback) # 14 day

    momentum = get_momentum(prices, lookback)

    # figure 1.
    fig = plt.figure(figsize=(12,6.5))
    top = plt.subplot2grid((5,1), (0,0), rowspan=3, colspan=1)
    bottom = plt.subplot2grid((5,1), (3,0), rowspan=2, colspan=1, sharex=top)
    top.xaxis_date()
    top.grid(True)
    top.plot(prices, lw=2, color='blue', label='Price')

    top.plot(SMA, label='SMA - {}-day lookback'.format(lookback), lw=1,color='red')

    top.set_title('Simple Moving Average - JPM')
    top.set_ylabel('Stock Price $ (Adjused Closing)')

    bottom.plot(PSR, color='olive', lw=1)
    bottom.set_title('Price over SMA ratio')

    bottom.axhline(y = -0.2,  color = 'grey', linestyle='--', alpha = 0.5)
    bottom.axhline(y = 0,   color = 'grey', linestyle='--', alpha = 0.5)
    bottom.axhline(y = .2,   color = 'grey', linestyle='--', alpha = 0.5)
    bottom.set_ylim(-0.5, .5)

    top.legend()
    top.axes.get_xaxis().set_visible(False)
    plt.xlim(start_date,end_date)

    filename = '01_Price_over_SMA_ratio.png'

    plt.savefig(filename)

    # figure 2.
    fig = plt.figure(figsize=(12,6.5))
    top = plt.subplot2grid((5,1), (0,0), rowspan=4, colspan=1)
    bottom = plt.subplot2grid((5,1), (4,0), rowspan=1, colspan=1, sharex=top)
    top.xaxis_date()
    top.grid(True)
    top.plot(prices, lw=2, color='blue', label='Price')

    top.plot(SMA, label='SMA - 14-day lookback', lw=1,color='red')
    top.plot(upper_bb, label='Upper band', lw=1,color='limegreen')
    top.plot(lower_bb, label='Lower band', lw=1,color='olive')

    top.set_title('Bollinger Bands - JPM')
    top.set_ylabel('Stock Price $ (Adjused Closing)')
    bottom.plot(bb_indicator, color='olive', lw=1)
    bottom.set_title('Bollinger Bands Indicator')

    bottom.axhline(y = -1,  color = 'grey', linestyle='--', alpha = 0.5)
    bottom.axhline(y = 0,   color = 'grey', linestyle='--', alpha = 0.5)
    bottom.axhline(y = 1,   color = 'grey', linestyle='--', alpha = 0.5)

    top.legend()
    top.axes.get_xaxis().set_visible(False)
    plt.xlim(start_date,end_date)

    filename = '02_bb_indicator.png'

    plt.savefig(filename)


    # figure 3.
    fig = plt.figure(figsize=(12,6.5))
    top = plt.subplot2grid((5,1), (0,0), rowspan=3, colspan=1)
    bottom = plt.subplot2grid((5,1), (3,0), rowspan=2, colspan=1, sharex=top)
    top.xaxis_date()
    top.grid(True)
    top.plot(prices, lw=2, color='blue', label='Price')


    top.set_title('Price - JPM')
    top.set_ylabel('Stock Price $ (Adjused Closing)')
    bottom.plot(momentum, color='olive', lw=1)
    bottom.set_title('Momentum')

    bottom.axhline(y = -0.2,  color = 'grey', linestyle='--', alpha = 0.5)
    bottom.axhline(y = 0,   color = 'grey', linestyle='--', alpha = 0.5)
    bottom.axhline(y = 0.2,   color = 'grey', linestyle='--', alpha = 0.5)

    top.legend()
    top.axes.get_xaxis().set_visible(False)
    plt.xlim(start_date,end_date)

    filename = '03_momentum.png'

    plt.savefig(filename)




if __name__ == "__main__":
    # This code WILL NOT be called by the auto grader
    # Do not assume that it will be called
    plot_indicators()
