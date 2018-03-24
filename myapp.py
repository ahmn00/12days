#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 23 15:44:58 2018

@author: amir
"""

##TEST STOCK MARKET : 


from bokeh.io import curdoc , show ,output_file

from bokeh.layouts import row, column,widgetbox

from bokeh.models import ColumnDataSource ,Select , HoverTool , PreText ,Button

from bokeh.plotting import figure


import pandas as pd
#############

Mydata=pd.read_csv('wiki_price_data.csv' , index_col='date' , parse_dates=['date'])
Mydata.drop('Unnamed: 0' , axis=1 , inplace=True)
DEFAULT_TICKERS = Mydata['ticker'].unique().tolist()



source=ColumnDataSource(data={
        'days' : Mydata.loc[Mydata['ticker']=='AAPL' , :].index , 
        'close' :Mydata.loc[Mydata['ticker']=='AAPL' ,'close'], 
        'open'  : Mydata.loc[Mydata['ticker']=='AAPL' ,'open'],
        'high' : Mydata.loc[Mydata['ticker']=='AAPL' ,'high']
        
        })


plot=figure(title='Closeing Price-US Stock Market' ,x_axis_label='Days(Feb-Mar,2018)' , 
            y_axis_label='Closing Price', x_axis_type='datetime' , tools='pan,wheel_zoom,reset')

plot.line( x='days',y='close', source=source  )

hover = HoverTool(tooltips=[('Open at','@open'),
                            ('Heighest at','@high') , 
                            ('Close at' , '@close')] , mode='vline')

plot.add_tools(hover)

plot.legend.background_fill_color='grey'


########## N E W : 

stats= PreText(text='' , width=450)


ticker= Select(title='Select ticker: ',width=300,value='AAPL', options=DEFAULT_TICKERS)

######## Interactive : 

def update_plot (attr , old ,new ):
    tk=ticker.value
    new_data= {
         'days' : Mydata.loc[Mydata['ticker']==tk , :].index , 
        'close' : Mydata.loc[Mydata['ticker']==tk ,'close'], 
        'open'  : Mydata.loc[Mydata['ticker']==tk ,'open'],
        'high' : Mydata.loc[Mydata['ticker']==tk ,'high']
        
        
        }
    source.data = new_data    

  
    
def callback():

    select=ticker.value  
    stats.text= str( Mydata.loc[ Mydata['ticker']==select , :].describe())
     
button = Button(label="Display Stats")

button.on_click(callback)     

ticker.on_change('value' , update_plot)  


### LAYOUT : 

## new theme: 
plot.xgrid.band_fill_color = "olive"
plot.xgrid.band_fill_alpha = 0.1



col_1=column(ticker , button , stats)



layout = row (col_1,plot)

curdoc().add_root(layout)

#output_file('bokeh_test.html')



