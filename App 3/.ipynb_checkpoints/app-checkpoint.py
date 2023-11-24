from dash import Dash, html, dash_table, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import numpy as np
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
        ], width=4)
        #dbc.Col([
        #    dcc.Dropdown(['country','continent',None], None, id='dropdown-selection')
        #], width=4)
        
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
            dcc.Graph(id='graph-content-all',  hoverData={'points': [{'customdata': ['Japan']}]})
        ], width=6),

        dbc.Col([
            dbc.Row([
                dcc.Graph(id='graph-content-country')
            ]),
            dbc.Row([
                dcc.Graph(id='graph-hist-selection')
            ]),
        ]),
    ])
    
], fluid=True)



# Histogram based on point selection
def get_figure(df, selectedData, col_chosen_1, col_chosen_2):
    print(selectedData)
    if selectedData is not None and 'points' in selectedData:
        selected_points = selectedData['points']
        selection_bounds = {
            "x0": np.min( [point['x'] for point in selected_points] ),
            "x1": np.max( [point['x'] for point in selected_points] ),
            "y0": np.min( [point['y'] for point in selected_points] ),
            "y1": np.max( [point['y'] for point in selected_points] ),
        }
    else:
        selection_bounds = {
            "x0": np.min(df[col_chosen_1]),
            "x1": np.max(df[col_chosen_1]),
            "y0": np.min(df[col_chosen_2]),
            "y1": np.max(df[col_chosen_2]),
        }
    print(selection_bounds)

    # set which points are selected with the `selectedpoints` property
    # and style those points with the `selected` and `unselected`
    # attribute. see
    # https://medium.com/@plotlygraphs/notes-from-the-latest-plotly-js-release-b035a5b43e21
    # for an explanation
    dff = df.query(f'{col_chosen_1}>{selection_bounds["x0"]} & {col_chosen_1}<{selection_bounds["x1"]}')
    dff = dff.query(f'{col_chosen_2}>{selection_bounds["y0"]} & {col_chosen_2}<{selection_bounds["y1"]}')
    
    fig = px.histogram(dff, x=col_chosen_1, title=f'{col_chosen_1} of selected countries across years')

    return fig



##### Callback of main graph with all countries
@callback(
    Output('graph-content-all', 'figure'),
    ##Input('dropdown-selection', 'value'),
    Input('controls-and-radio-item-1', 'value'),
    Input('controls-and-radio-item-2', 'value'),
    Input('year-slider', 'value')
)
#here, the inputs to update_graph are in the same order as the inputs in the callback and 
#you just need to choose a variable name
def update_graph_1(col_chosen_1, col_chosen_2, year):
    dff = df[df.year==year]
    #return px.line(dff, x='year', y=col_chosen[1], color=value)
    fig =  px.scatter(dff, x=col_chosen_1, y=col_chosen_2, hover_data='country')
    fig.update_layout(transition_duration=500)
    
    fig.update_layout(clickmode='event+select')
    return fig


##### Callback creating subdata from the hovering of the main graph
@callback(
    Output('graph-content-country', 'figure'),
    Input('graph-content-all', 'hoverData'),
    Input('controls-and-radio-item-1', 'value'),
    Input('controls-and-radio-item-2', 'value'),
)
#here, we subset with the country chosen by hovering on the scatter plot
def update_graph_2(hover_all, col_chosen_1, col_chosen_2):
    country=hover_all['points'][0]['customdata'][0]
    print(country)
    dff = df[df.country==country]
    fig =  px.scatter(dff, x=col_chosen_1, y=col_chosen_2, title=f'{country}', hover_data='year')
    fig.update_layout(transition_duration=500)
    return fig

##### Callback creating histogram from data subset
@callback(
    Output('graph-hist-selection', 'figure'),
    Input('graph-content-all', 'selectedData'), #select by shift+click or selection box (chosen from plot menu)
    Input('controls-and-radio-item-1', 'value'),
    Input('controls-and-radio-item-2', 'value'),
    Input('year-slider', 'value') #just using this to redo the same histogram when changing year in the main plot, otherwise gives error!
)
#here, we subset with the country chosen by hovering on the scatter plot
def update_graph_3(selection_all, col_chosen_1, col_chosen_2, year):
    
    print("hello")
    return get_figure(df, selection_all, col_chosen_1, col_chosen_2)

                      
if __name__ == '__main__':
    app.run(debug=True)