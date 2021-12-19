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

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 10],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")
df = pd.read_csv('scenario_1/sum.csv')

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
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
    )
])

if __name__ == '__main__':
    data = {}
    key = {}
    os.chdir("./")
    for file in glob.glob("*.csv"):
        if file=="sum.csv":
            data[file] = {}
            key[file]  = []
            with open(file, newline='') as csvfile:
                myreader = csv.reader(csvfile, delimiter=',', quotechar='|')
                for index, lines in enumerate(myreader):
                    for itIndex,item in enumerate(lines):
                        if index==0:
                            print ("dbg:",file,key[file],index,itIndex)
                            data[file][item] = []
                            key[file].append(item)
                        else:
                            print ("dbg:",file,key[file],index,itIndex)
                            data[file][key[file][itIndex]].append(item)
    app.run_server(debug=True)

    
