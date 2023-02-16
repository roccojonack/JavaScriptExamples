# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
import dash
from dash import dcc
from dash import html
from dash import dash_table
from dash import Input, Output
import plotly.express as px
import pandas as pd
import glob, os
import csv
import plotly.graph_objects as go
from plotly.subplots import make_subplots

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = []
names = []
for f in glob.glob('scenario_1/sum*.csv'):
    df.append(pd.read_csv(f))
    names.append(f)
df1 = pd.read_csv('scenario_1/ncaiu0_axi_nb.read.csv')
df2 = df1['full latency'].value_counts(ascending=True)
counter = 0
sum = df2.values.sum()
running_sum = 0
indexLat = []
valueLat = []
for i in df2:
    running_sum += i
    print("tmp", counter, df2.index[counter], i, sum-running_sum)
    valueLat.append(sum-running_sum)
    indexLat.append(df2.index[counter])
    counter += 1
print( df2.index)
fig = make_subplots(rows=3, cols=2)
list_of_val = range(10)
# fig = go.Figure()
# Create and style traces
for i,data in enumerate(df):
    fig.add_trace(go.Bar(x=df[i]['name'], y=df[i]['bandwidth'], name=names[i]), row=1, col=1)
for i,data in enumerate(df):
    fig.add_trace(go.Bar(x=df[i]['name'], y=df[i]['latencyavg'], name=names[i]), row=1, col=2)
fig.add_trace(go.Histogram(x=df1['Time'], nbinsx=100, y=df1['full latency'], histfunc='avg'), row=3, col=1)
fig.add_trace(go.Scatter(x=indexLat, y=valueLat, name='test'), row=3, col=2)

fig.update_layout(  title='Bandwidth in different scenarios'
                  , height=600
                  , xaxis_title='interface name'
                  , yaxis_title='amount of transfers')
fig.update_layout(barmode='group')

app.layout = html.Div(children=[
    html.H1(children='Dashboard for a Ncore3 scenario'),
    dcc.Graph(
        id='example-graph'
        , figure=fig
    ),
    dcc.RangeSlider(
        min=int(df1['Time'].iloc[0]),
        max=int(df1['Time'].iloc[-1]),
        value=[df1['Time'].iloc[0], df1['Time'].iloc[-1]],
        step=None,
        id='year-slider'
    ),  
    html.Div(id='my-output'),
    dash_table.DataTable(
        id='table',
        sort_action='native',
        filter_action='native',
        columns=[{"name": i, "id": i} for i in df[0].columns],
        data=df[0].to_dict('records'),
    )
])

@app.callback(
    Output(component_id='my-output', component_property='children'),
    Input(component_id='year-slider', component_property='value')
)
def update_output_div(input_value):
    return f'Output: {input_value[0],input_value[-1]}'

if __name__ == '__main__':
    app.run_server(debug=True)
