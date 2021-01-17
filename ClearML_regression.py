#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 15 19:39:37 2021

@author: Wasilios Goutas
"""
import argparse
import yfinance as yf
import pandas as pd
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

    process(param=parameters, df=tickerDf, symbol=args[0].symbol, attrib='Close', plot=True)
    return

def plot_(df, show=False):
    import plotly.express as px
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
    from sklearn.metrics import mean_squared_error
    model = None
    df_valid      = df[-30:]
    df_process    = df[:-30]
    df_lag1d = df_process - df_process.shift(shift)
    df_change = df_lag1d / df_process * 100
    df_change.columns += '_pcent'
    df_change = df_change[1:]       # remove first row containing NaN
    df_process = df_process[1:]

    y = df_change[attrib+'_pcent']
    X = df_change.drop(y.name, axis=1)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
    assert (0 == X_train.isna().sum().sum())
    assert (0 == y.isna().sum())

    df_plot = pd.concat([df_process[attrib], df_change[attrib+'_pcent']], axis=1)
    df_plot.index = df_plot.index.astype(str)
    assert (0 == df_plot.isna().sum().sum())
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
            model.fit(X_train, y_train)

            y_test.index = y_test.index.astype(str)
            y_pred = pd.DataFrame(model.predict(X_test), index=y_test.index, columns=[y.name + '_predicted'])
            res_test = pd.concat([y_test, y_pred], axis=1)

            assert (0 == res_test.isna().sum().sum())
            setattr(res_test, 'ticker', symbol)
            fig = plot_(res_test, show=True)
            task.get_logger().report_plotly(title='finance', series='reality vs prediction', iteration=0, figure=fig)
            mse = mean_squared_error(y_test, y_pred)
            print(f'{p} mean squared error: {round(mse, 3)} ')

    return


#%%
if __name__ == '__main__':
    main()
    print('done')

#%%
