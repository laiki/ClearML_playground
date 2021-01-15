#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 15 19:39:37 2021

@author: Wasilios Goutas
"""
import argparse
import yfinance as yf
from clearml import Task

#task = Task.init(project_name='Regression test with configurable arguments', task_name='finance')

parser = argparse.ArgumentParser()
parser.add_argument('--symbol', help='symbol used for regression', default='AAPL')
args = parser.parse_args()

tickerData = yf.Ticker(args.symbol)
tickerDf = tickerData.history(period='max')
type(tickerDf)
