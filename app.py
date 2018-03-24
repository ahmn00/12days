#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 23 16:30:30 2018

@author: amir
"""

### SAMPLE _BOKEH: 
### thing to do : 


# 1 add hover :
# add opening 


from bokeh.io import curdoc , show  , output_file 
from bokeh.layouts import row, column
from bokeh.models import ColumnDataSource ,Select ,HoverTool
from bokeh.plotting import figure 
import pandas as pd
import numpy as np 



#### data: 


Mydata=pd.read_csv('wiki_price_data.csv' , index_col='date' , parse_dates=['date'])
Mydata.drop('Unnamed: 0' , axis=1 , inplace=True)
DEFAULT_TICKERS = Mydata.index.unique().tolist()



new_data=Mydata.loc[Mydata['ticker']=='AAPL' , :]

source=ColumnDataSource(data={
        'days' : Mydata.loc[Mydata['ticker']=='AAPL' , :].index , 
        'close' :Mydata.loc[Mydata['ticker']=='AAPL' ,'close'],
        'open'  : Mydata.loc[Mydata['ticker']=='AAPL' ,'open'],
        'high' : Mydata.loc[Mydata['ticker']=='AAPL' ,'high']
        
        })


    
    
plot=figure(tools='box_select',title='yechizii' ,x_axis_label='time' , 
            y_axis_label='tokhoob', x_axis_type='datetime')

plot.line( x='days',y='close', source=source , alpha=0.8 ,legend='AAPL')

hover = HoverTool(tooltips=[('Open at','@open'),('Heighest at','@close')] , mode='vline')

plot.add_tools(hover)

plot.legend.background_fill_color='grey'


plot.xgrid.band_fill_color = "olive"
plot.xgrid.band_fill_alpha = 0.1


output_file('test.html')

show(plot)