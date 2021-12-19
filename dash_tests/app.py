# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
import dash
from dash import dcc
from dash import html
from dash import dash_table
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
fig = make_subplots(rows=3, cols=2)

# fig = go.Figure()
# Create and style traces
for i,data in enumerate(df):
    fig.add_trace(go.Bar(x=df[i]['name'], y=df[i]['bandwidth'], name=names[i]), row=1, col=1)
for i,data in enumerate(df):
    fig.add_trace(go.Bar(x=df[i]['name'], y=df[i]['latencyavg'], name=names[i]), row=1, col=2)
fig.add_trace(go.Histogram(x=df1['Time'], nbinsx=100, y=df1['full latency'], histfunc='avg'), row=3, col=1)

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
    dash_table.DataTable(
        id='table',
        sort_action='native',
        filter_action='native',
        columns=[{"name": i, "id": i} for i in df[0].columns],
        data=df[0].to_dict('records'),
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
