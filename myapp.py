#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 23 15:44:58 2018

@author: amir
"""

##TEST STOCK MARKET : 


from bokeh.io import curdoc

from bokeh.layouts import row, column,widgetbox

from bokeh.models import ColumnDataSource ,Select , HoverTool , PreText ,Button

from bokeh.plotting import figure

from bokeh.models.widgets import Panel ,Tabs, Div ,Paragraph




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


plot=figure(title='Closing Price-US Stock Market' ,x_axis_label='Days(Feb-Mar,2018)' , 
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
     
button = Button(label="Display Stats" , button_type="success")

button.on_click(callback)     

ticker.on_change('value' , update_plot)  


### LAYOUT : 

## new theme: 
plot.xgrid.band_fill_color = "olive"
plot.xgrid.band_fill_alpha = 0.1
####################3

#### ABOUT ME : 

about_me_1= Paragraph(text="""My name is Amir Mousavi. I am a Ph.D. candidate and Data Scientist at the George Washington University. As a data scientist, I have worked on several different projects, such
as: Credit Risk; Portfolio Analysis; and Data visualization for Bike Sharing for the Washington DC area. I also further developed my knowledge about natural language processes and deep learning by attending online courses.
""")

about_me_2= Paragraph(text=""" The most recent project that I worked on was Uber Demand Modeling that I submitted for
the “Data Incubator Fellowship Program.” My success on this project led me to be accepted
into the fellowship. For this project, I built an interactive dashboard using R-shiny and built
time series models to forecast Uber demand in New York City. (Link to the dashboard:
https://amousavi.shinyapps.io/UBER/)
  """ )

linkdin=Div(text= """My:<a href="https://www.linkedin.com/in/mousavi-amir/">Linkedin</a>""")  
github= Div(text= """Project:<a href="https://github.com/ahmn00/12days.git">github</a>""")   
tdi=Div(text= """More about The Data Incubator <a href="https://www.thedataincubator.com/">TDI</a>""")  
#################### TABS : 

col_1=column(ticker , button , stats)
layout_1 = row (col_1,plot)

layout_2=row( column(about_me_1 , about_me_2)  , column( widgetbox( linkdin )  , widgetbox(github) , tdi))



tab1=Panel(child=layout_1, title='12 days project')

tab2=Panel(child=layout_2, title='About me')





layout=Tabs(tabs=[tab1,tab2])


curdoc().add_root(layout)




