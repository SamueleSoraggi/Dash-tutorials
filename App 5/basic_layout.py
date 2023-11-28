from dash import Dash, html, dash_table, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc
import json

# Dash app initialization
app = Dash(__name__)

# App layout
app.layout = html.Div([
    html.H1("Dash App with Tabs"),

    dcc.Tabs(id='tabs', value='tab1', children=[
        dcc.Tab(label='Tab 1', value='tab1'),
        dcc.Tab(label='Tab 2', value='tab2'),
    ]),

    html.Div(id='tabs-content')
])

# Callback to update the content of the tabs
@app.callback(
    Output('tabs-content', 'children'),
    [Input('tabs', 'value')]
)
def update_tab_content(selected_tab):
    if selected_tab == 'tab1':
        return html.Div([
            html.H3('Content of Tab 1'),
            dcc.Graph(
                id='graph1',
                figure={'data': [{'y': [3, 1, 2]}], 'layout': {'title': 'Graph in Tab 1'}}
            ),
        ])
    elif selected_tab == 'tab2':
        return html.Div([
            html.H3('Content of Tab 2'),
            dcc.Graph(
                id='graph2',
                figure={'data': [{'y': [1, 3, 2]}], 'layout': {'title': 'Graph in Tab 2'}}
            ),
        ])
    else:
        return html.Div([])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
