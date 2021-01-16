#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 15 19:39:37 2021

@author: Wasilios Goutas
"""
import argparse
import yfinance as yf
import pandas as pd
import plotly.express as px
from clearml import Task

task = Task.init(project_name='first ClearML steps', task_name='finance')

#%%
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--symbol', help='symbol used for regression', default='AAPL')
    args = parser.parse_args()

    tickerData      = yf.Ticker(args.symbol)
    tickerDf        = tickerData.history(period='max', interval='1d')[['Open', 'High', 'Low', 'Close', 'Volume']]
    tickerDf_lag1d  = tickerDf - tickerDf.shift(1)
    tickerDf_Change = tickerDf_lag1d / tickerDf * 100
    tickerDf_Change.columns += '_pcent'
    
    df = pd.concat([tickerDf.Close, tickerDf_Change.Close_pcent], axis=1)
    setattr(df, 'ticker', args.symbol)
    fig = plot_(df, show=True)
    task.get_logger().report_plotly(title='finance', series=args.symbol, iteration=0, figure=fig)

    return


def plot_(df, show=False):
    import plotly.io as pio
    pio.renderers.default='browser'
    #pio.renderers.default='svg'
    fig = px.line(df, title=getattr(df, 'ticker'))
    if show: fig.show()

    return fig

#%%
if __name__ == '__main__':
    main()
    print('done')

#%%
