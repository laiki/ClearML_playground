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
    args = parser.parse_known_args()

    parameters = {
        'LinearRegression': True,
        'Ridge': False,
        'SVR': False,
    }
    parameters = task.connect_configuration(configuration=parameters, name='regressor selection',
                                            description='set which regressor to run')
    tickerData      = yf.Ticker(args[0].symbol)
    tickerDf        = tickerData.history(period='max', interval='1d')[['Open', 'High', 'Low', 'Close', 'Volume']]
    setattr(tickerDf, 'ticker', args[0].symbol)
    process(param=parameters, df=tickerDf, symbol=args[0].symbol, attrib='Close', plot=True)
    return

def plot_(df, show=False):
    import plotly.io as pio
    pio.renderers.default='browser'
    #pio.renderers.default='svg'
    fig = px.line(df, title=getattr(df, 'ticker'))
    if show: fig.show()

    return fig

def process(param, df, symbol, attrib='Close', shift=1, plot=False):
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LinearRegression, Ridge
    from sklearn.svm import SVR
    model = None
    df_valid      = df[-30:]
    df_process    = df[:-30]
    df_lag1d = df_process - df_process.shift(shift)
    df_change = df_lag1d / df_process * 100
    df_change.columns += '_pcent'
    y = df_change[1:][attrib+'_pcent']
    X = df_change[1:].drop(y.name, axis=1)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
    symbol = getattr(df, 'ticker')
    df_plot = pd.concat([df_process[attrib], df_change[attrib+'_pcent']], axis=1)
    setattr(df_plot, 'ticker', symbol)
    fig = plot_(df_plot, show=plot)
    task.get_logger().report_plotly(title='finance', series=symbol, iteration=0, figure=fig)

    for p in param:
        if True == param[p]:
            if 'LinearRegression' == p:
                model = LinearRegression(fit_intercept=False, normalize=False)
            elif 'Ridge' == p:
                model = Ridge()
            elif 'SVR' == p:
                model = SVR()
            else:
                continue
    return


#%%
if __name__ == '__main__':
    main()
    print('done')

#%%
