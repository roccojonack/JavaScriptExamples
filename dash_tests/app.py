# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import plotly.express as px
import pandas as pd
import glob, os
import csv
import plotly.graph_objects as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

df = []
names = []
for f in glob.glob('scenario_1/sum*.csv'):
    df.append(pd.read_csv(f))
    names.append(f)
print(df)
# df = pd.read_csv('scenario_1/sum.csv')
# fig = px.line(df, x="name", y="bandwidth")
fig = go.Figure()
# Create and style traces
for i,data in enumerate(df):
    fig.add_trace(go.Bar(x=df[i]['name'], y=df[i]['bandwidth'], name=names[i]))

fig.update_layout(title='Bandwidth in different scenarios',
                   xaxis_title='interface name',
                   yaxis_title='amount of transfers')
fig.update_layout(barmode='group')

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
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
    app.run_server(host='192.168.178.30',debug=True)

    
