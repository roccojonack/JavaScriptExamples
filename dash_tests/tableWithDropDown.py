from dash import Dash, dash_table, html, dcc
import pandas as pd
from collections import OrderedDict


app = Dash(__name__)

df = pd.DataFrame(OrderedDict([
    ('climate', ['Sunny', 'Snowy', 'Sunny', 'Rainy']),
    ('temperature', [13, 43, 50, 30]),
    ('city', ['NYC', 'Montreal', 'Miami', 'NYC'])
]))


app.layout = html.Div([
    dash_table.DataTable(
        id='table-dropdown',
        data=df.to_dict('records'),
        columns=[
            {'id': 'climate', 'name': 'climate', 'presentation': 'dropdown'},
            {'id': 'temperature', 'name': 'temperature'},
            {'id': 'city', 'name': 'city', 'presentation': 'dropdown'},
        ],

        editable=True,
        dropdown={
            'climate': {
                'options': [
                    {'label': i, 'value': i}
                    for i in df['climate'].unique()
                ]
            },
            'city': {
                 'options': [
                    {'label': i, 'value': i}
                    for i in df['city'].unique()
                ]
            }
        }
    ),
    html.Div(id='table-dropdown-container'),
    html.Div(
        dcc.Dropdown(df['climate'], "test", id='first')
        ,style={'width': '49%', 'display': 'inline-block'}
        ),
    html.Div(
        dcc.Dropdown(df['city'], "test", id='second')
        ,style={'width': '49%', 'display': 'inline-block'}
    )
])


if __name__ == '__main__':
    app.run_server(debug=True)