from dash import Dash, html, dash_table, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
#import scanpy as sc

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

# Initialize the app - incorporate a Dash Bootstrap theme
external_stylesheets = [dbc.themes.CERULEAN]
app = Dash(__name__, external_stylesheets=external_stylesheets)



# App layout
app.layout = dbc.Container([
    dbc.Row([
        html.Div('App to explore some simple dataset', className="text-primary text-center fs-3")
    ]),

    dbc.Row([
        dbc.Col([
            dbc.RadioItems(options=[{"label": x, "value": x} for x in ['pop', 'lifeExp', 'gdpPercap']],
                       value='lifeExp',
                       inline=True,
                       id='controls-and-radio-item-1')
        ], width=4),
        dbc.Col([
            dbc.RadioItems(options=[{"label": x, "value": x} for x in ['pop', 'lifeExp', 'gdpPercap']],
                       value='lifeExp',
                       inline=True,
                       id='controls-and-radio-item-2')
        ], width=4),
        dbc.Col([
            dcc.Dropdown(['country','continent',None], None, id='dropdown-selection')
        ], width=4)
        
    ]),
    
    dbc.Row([
        dcc.Slider(
            df['year'].min(),
            df['year'].max(),
            step=None,
            value=df['year'].min(),
            marks={str(year): str(year) for year in df['year'].unique()},
            id='year-slider'
        )
    ]),
    
    dbc.Row([
        dbc.Col([
            dash_table.DataTable(data=df.to_dict('records'), page_size=12, style_table={'overflowX': 'auto'})
        ], width=6),

        dbc.Col([
            dcc.Graph(figure={}, id='graph-content')
        ], width=6),
    ]),

], fluid=True)

@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value'),
    Input('controls-and-radio-item-1', 'value'),
    Input('controls-and-radio-item-2', 'value'),
    Input('year-slider', 'value')
)

#here, the inputs to update_graph are in the same order as the inputs in the callback and 
#you just need to choose a variable name
def update_graph(value, col_chosen_1, col_chosen_2, year):
    dff = df[df.year==year]
    #return px.line(dff, x='year', y=col_chosen[1], color=value)
    fig =  px.scatter(dff, x=col_chosen_1, y=col_chosen_2, color=value)
    fig.update_layout(transition_duration=500)
    return fig

if __name__ == '__main__':
    app.run(debug=True)