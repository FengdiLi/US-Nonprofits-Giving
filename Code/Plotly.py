# -*- coding: utf-8 -*-
"""
Created on Sun Nov 25 20:50:59 2018

@author: lifen
"""
import plotly.graph_objs as go
from plotly.offline import plot
import pandas as pd
import numpy as np
#from plotly import tools
#%%
df = pd.read_csv('STATE_stats.csv')
df['ASSET_AVG'] = df['ASSET_AVG']/(10**6)
df['REVENUE_AVG'] = df['REVENUE_AVG']/(10**6)
df['INCOME_AVG'] = df['INCOME_AVG']/(10**6)
df['Count'] = df['Count']/(10**3)
df = df.round(1)
df['REGION_cat'] = df['REGION'].astype('category').cat.codes
df['TEXT1'] = 'State: '+df['STATE']+', Average Asset: '+df['ASSET_AVG'].astype(str)+', Org Count: '+df['Count'].astype(str)
df['TEXT2'] = 'State: '+df['STATE']+', Average Revenue: '+df['REVENUE_AVG'].astype(str)+', Org Count: '+df['Count'].astype(str)
df['TEXT3'] = 'State: '+df['STATE']+', Average Income: '+df['INCOME_AVG'].astype(str)+', Org Count: '+df['Count'].astype(str)
trace1 = go.Scatter(
                x=df['ASSET_AVG'][df['REGION_cat'] == 0],
                y=df['Count'][df['REGION_cat'] == 0],
                text = df['TEXT1'][df['REGION_cat'] == 0],
                mode='markers',
                marker={'size': 20,
                        'color': 'orange',
                        'opacity': 0.6
                       },
                hoverinfo = 'text',
                name = 'Coast')
x = np.array(df['ASSET_AVG'][df['REGION_cat'] == 0])
y = np.array(df['Count'][df['REGION_cat'] == 0])
z = np.polyfit(x, y, 1)
f = np.poly1d(z)
x_new = np.linspace(min(x), max(x), 50)
y_new = f(x_new)
trace11 = go.Scatter(
                  x=x_new,
                  y=y_new,
                  mode='lines',
                  marker={'color': 'orange',                          
                          'opacity': 0.8},
                  name='Coast Fit'
                  )
trace2 = go.Scatter(
                x=df['ASSET_AVG'][df['REGION_cat'] == 1],
                y=df['Count'][df['REGION_cat'] == 1],
                text = df['TEXT1'][df['REGION_cat'] == 1],
                mode='markers',
                marker={'size': 20,
                        'color': 'DodgerBlue',
                        'opacity': 0.6
                       },
                hoverinfo = 'text',
                name = 'Mid')
x = np.array(df['ASSET_AVG'][df['REGION_cat'] == 1])
y = np.array(df['Count'][df['REGION_cat'] == 1])
z = np.polyfit(x, y, 1)
f = np.poly1d(z)
x_new = np.linspace(min(x), max(x), 50)
y_new = f(x_new)
trace21 = go.Scatter(
                  x=x_new,
                  y=y_new,
                  mode='lines',
                  marker={'color': 'DodgerBlue',                          
                          'opacity': 0.8},
                  name='Mid Fit'
                  )
trace3 = go.Scatter(
                x=df['ASSET_AVG'][df['REGION_cat'] == 2],
                y=df['Count'][df['REGION_cat'] == 2],
                text = df['TEXT1'][df['REGION_cat'] == 2],
                mode='markers',
                marker={'size': 20,
                        'color': 'limegreen',
                        'opacity': 0.6
                       },
                hoverinfo = 'text',
                name = 'Northeast')
x = np.array(df['ASSET_AVG'][df['REGION_cat'] == 2])
y = np.array(df['Count'][df['REGION_cat'] == 2])
z = np.polyfit(x, y, 1)
f = np.poly1d(z)
x_new = np.linspace(min(x), max(x), 50)
y_new = f(x_new)
trace31 = go.Scatter(
                  x=x_new,
                  y=y_new,
                  mode='lines',
                  marker={'color': 'limegreen',                          
                          'opacity': 0.8},
                  name='Northeast Fit'
                  )
trace4 = go.Scatter(
                x=df['REVENUE_AVG'][df['REGION_cat'] == 0],
                y=df['Count'][df['REGION_cat'] == 0],
                text = df['TEXT2'][df['REGION_cat'] == 0],
                mode='markers',
                marker={'size': 20,
                        'color': 'orange',
                        'opacity': 0.6
                       },
                hoverinfo = 'text',
                name = 'Coast')
x = np.array(df['REVENUE_AVG'][df['REGION_cat'] == 0])
y = np.array(df['Count'][df['REGION_cat'] == 0])
z = np.polyfit(x, y, 1)
f = np.poly1d(z)
x_new = np.linspace(min(x), max(x), 50)
y_new = f(x_new)
trace41 = go.Scatter(
                  x=x_new,
                  y=y_new,
                  mode='lines',
                  marker={'color': 'orange',                          
                          'opacity': 0.8},
                  name='Coast Fit'
                  )
trace5 = go.Scatter(
                x=df['REVENUE_AVG'][df['REGION_cat'] == 1],
                y=df['Count'][df['REGION_cat'] == 1],
                text = df['TEXT2'][df['REGION_cat'] == 1],
                mode='markers',
                marker={'size': 20,
                        'color': 'DodgerBlue',
                        'opacity': 0.6
                       },
                hoverinfo = 'text',
                name = 'Mid')
x = np.array(df['REVENUE_AVG'][df['REGION_cat'] == 1])
y = np.array(df['Count'][df['REGION_cat'] == 1])
z = np.polyfit(x, y, 1)
f = np.poly1d(z)
x_new = np.linspace(min(x), max(x), 50)
y_new = f(x_new)
trace51 = go.Scatter(
                  x=x_new,
                  y=y_new,
                  mode='lines',
                  marker={'color': 'DodgerBlue',                          
                          'opacity': 0.8},
                  name='Mid Fit'
                  )
trace6 = go.Scatter(
                x=df['REVENUE_AVG'][df['REGION_cat'] == 2],
                y=df['Count'][df['REGION_cat'] == 2],
                text = df['TEXT2'][df['REGION_cat'] == 2],
                mode='markers',
                marker={'size': 20,
                        'color': 'limegreen',
                        'opacity': 0.6
                       },
                hoverinfo = 'text',
                name = 'Northeast')
x = np.array(df['REVENUE_AVG'][df['REGION_cat'] == 2])
y = np.array(df['Count'][df['REGION_cat'] == 2])
z = np.polyfit(x, y, 1)
f = np.poly1d(z)
x_new = np.linspace(min(x), max(x), 50)
y_new = f(x_new)
trace61 = go.Scatter(
                  x=x_new,
                  y=y_new,
                  mode='lines',
                  marker={'color': 'limegreen',                          
                          'opacity': 0.8},
                  name='Northeast Fit'
                  )
trace7 = go.Scatter(
                x=df['INCOME_AVG'][df['REGION_cat'] == 0],
                y=df['Count'][df['REGION_cat'] == 0],
                text = df['TEXT3'][df['REGION_cat'] == 0],
                mode='markers',
                marker={'size': 20,
                        'color': 'orange',
                        'opacity': 0.6
                       },
                hoverinfo = 'text',
                name = 'Coast')
x = np.array(df['INCOME_AVG'][df['REGION_cat'] == 0])
y = np.array(df['Count'][df['REGION_cat'] == 0])
z = np.polyfit(x, y, 1)
f = np.poly1d(z)
x_new = np.linspace(min(x), max(x), 50)
y_new = f(x_new)
trace71 = go.Scatter(
                  x=x_new,
                  y=y_new,
                  mode='lines',
                  marker={'color': 'orange',                          
                          'opacity': 0.8},
                  name='Coast Fit'
                  )
trace8 = go.Scatter(
                x=df['INCOME_AVG'][df['REGION_cat'] == 1],
                y=df['Count'][df['REGION_cat'] == 1],
                text = df['TEXT3'][df['REGION_cat'] == 1],
                mode='markers',
                marker={'size': 20,
                        'color': 'DodgerBlue',
                        'opacity': 0.6
                       },
                hoverinfo = 'text',
                name = 'Mid')
x = np.array(df['INCOME_AVG'][df['REGION_cat'] == 1])
y = np.array(df['Count'][df['REGION_cat'] == 1])
z = np.polyfit(x, y, 1)
f = np.poly1d(z)
x_new = np.linspace(min(x), max(x), 50)
y_new = f(x_new)
trace81 = go.Scatter(
                  x=x_new,
                  y=y_new,
                  mode='lines',
                  marker={'color': 'DodgerBlue',                          
                          'opacity': 0.8},
                  name='Mid Fit'
                  )
trace9 = go.Scatter(
                x=df['INCOME_AVG'][df['REGION_cat'] == 2],
                y=df['Count'][df['REGION_cat'] == 2],
                text = df['TEXT3'][df['REGION_cat'] == 2],
                mode='markers',
                marker={'size': 20,
                        'color': 'limegreen',
                        'opacity': 0.6
                       },
                hoverinfo = 'text',
                name = 'Northeast')
x = np.array(df['INCOME_AVG'][df['REGION_cat'] == 2])
y = np.array(df['Count'][df['REGION_cat'] == 2])
z = np.polyfit(x, y, 1)
f = np.poly1d(z)
x_new = np.linspace(min(x), max(x), 50)
y_new = f(x_new)
trace91 = go.Scatter(
                  x=x_new,
                  y=y_new,
                  mode='lines',
                  marker={'color': 'limegreen',                          
                          'opacity': 0.8},
                  name='Northeast Fit'
                  )
#%%
layout1 = dict(title = 'Relationship between Average Asset (*M USD) & Org Count (*K)',
               xaxis=dict(
                       title='Average Asset in Million USD'),
               yaxis=dict(
                       title='Number of Organizations in Thousands'),
               autosize=False,
               width = 600,
               height = 600,
               legend=dict(
                       x = 0.3,
                       y = 0.95,
                       orientation="h")
             )
layout2 = dict(title = 'Relationship between Average Revenue (*M USD) & Org Count (*K)',
               xaxis=dict(
                       title='Average Revenue in Million USD'),
               yaxis=dict(
                       title='Number of Organizations in Thousands'),
               autosize=False,
               width = 600,
               height = 600,
               legend=dict(
                       x = 0.3,
                       y = 0.95,
                       orientation="h")
             )
layout3 = dict(title = 'Relationship between Average Income (*M USD) & Org Count (*K)',
               xaxis=dict(
                       title='Average in Million USD'),
               yaxis=dict(
                       title='Number of Organizations in Thousands'),
               autosize=False,
               width = 600,
               height = 600,
               legend=dict(
                       x = 0.3,
                       y = 0.95,
                       orientation="h")
             )
#%%
## small subplots cannot present the graph well, use seperate graphs instead
fig = dict(data=[trace1, trace2, trace3, trace11, trace21, trace31], layout = layout1)
plot(fig, filename='scatter1.html')
fig = dict(data=[trace4, trace5, trace6, trace41, trace51, trace61], layout = layout2)
plot(fig, filename='scatter2.html')
fig = dict(data=[trace7, trace8, trace9, trace71, trace81, trace91], layout = layout3)
plot(fig, filename='scatter3.html')
#fig = tools.make_subplots(rows=1, cols=3, subplot_titles=('Asset & Revenue', 'Revenue & Income', 'Income & Asset'))
#fig.append_trace(trace1, 1, 1)
#fig.append_trace(trace2, 1, 2)
#fig.append_trace(trace3, 1, 3)
#fig['layout'].update(title = 'Relationship between Income, Revenue, Asset(Billions) and Count(Thousands)',
#              autosize=False,
#              width = 1800,
#              height = 800)
#py.iplot(fig, filename='scatter')

