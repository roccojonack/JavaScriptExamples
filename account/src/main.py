from dash import Dash, dash_table, html, dcc
import pandas as pd
import plotly.express as px

df = pd.read_csv('targo_biz.txt')
df1 = df['amount']
s = df1.cumsum()
df['sum'] = s
print(s)
app = Dash(__name__)

fig = px.line(df, x='date', y="sum")
# fig. = px.line(s, x='date', y="amount")

app.layout = html.Div([
    dcc.Graph(
        id='example-graph'
        , figure=fig
    ),
    dash_table.DataTable(df.to_dict('records'), 
        [{"name": i, "id": i} for i in df.columns]
    ),
])

if __name__ == '__main__':
    app.run_server(debug=True)
    