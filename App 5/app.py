from dash import Dash, html, dash_table, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc
import json
#import scanpy as sc

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')
df_car = pd.read_csv('../Cars.csv')[ ['Make', 'Modle', 'Year_from', 'Year_to', 'Series', 'Trim', 'battery_capacity_KW_per_h',
       'electric_range_km', 'charging_time_h', 'country_of_origin', 'acceleration_0_100_km/h_s',
       'max_speed_km_per_h', 'city_fuel_per_100km_l', 'CO2_emissions_g/km', 'turning_circle_m', 'full_weight_kg'] ]
df_car.head()
# Initialize the app - incorporate a Dash Bootstrap theme
external_stylesheets = [dbc.themes.CERULEAN]
app = Dash(__name__, external_stylesheets=external_stylesheets,
           suppress_callback_exceptions=True)



# App layout
app.layout = dbc.Container([
    dbc.Row(
        html.H1("Multitab dashboard") 
        ),

    dcc.Tabs(id='tabs', value='tab1', children=[
        dcc.Tab(label='Cars data', value='tab1'),
        dcc.Tab(label='Population data', value='tab2'),
    ]),

    dbc.Row(
        html.Div(id='tabs-content')
    )
], fluid=True)


@app.callback(
    Output('tabs-content', 'children'),
    [Input('tabs', 'value')]
)
def update_tab_content(selected_tab):
    if selected_tab == 'tab1':
        return html.Div([ dbc.Row([
            dbc.Col([
                dcc.Dropdown(['battery_capacity_KW_per_h', 'electric_range_km', 
                              'charging_time_h', 'country_of_origin', 
                              'acceleration_0_100_km/h_s', 'max_speed_km_per_h', 
                              'city_fuel_per_100km_l', 'CO2_emissions_g/km', 
                              'turning_circle_m', 'full_weight_kg'], 'CO2_emissions_g/km', id='dropdown-x'),
                dcc.Dropdown(['battery_capacity_KW_per_h', 'electric_range_km', 
                              'charging_time_h', 'country_of_origin', 
                              'acceleration_0_100_km/h_s', 'max_speed_km_per_h', 
                              'city_fuel_per_100km_l', 'CO2_emissions_g/km', 
                              'turning_circle_m', 'full_weight_kg'], 'full_weight_kg', id='dropdown-y')
            ], width=4),
            dbc.Col([
                dbc.RadioItems(options=[{"label": x, "value": x} for x in ['pop', 'lifeExp', 'gdpPercap']],
                       value='pop',
                       inline=True,
                       id='controls-and-radio-item-2')
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
            dbc.Col(          
                dcc.Graph(id='graph-content-all', hoverData={'points': [{'customdata': ['Japan']}]}),     
            style={'height': '800px'}),
    
            dbc.Col([
                dbc.Row(
                    dcc.Graph(id='graph-content-country')
                , align='center'),
                dbc.Row(
                    dcc.Graph(id='graph-hist-selection')
                , align='center'),
            ],style={'height': '800px'}),
        ]),
 
        dbc.Row([
            dcc.Dropdown(['country','continent'], 'country', id='dropdown'),
            dcc.Graph(id='graph-mean-histogram'),
            # dcc.Store stores the intermediate value
            dcc.Store(id='intermediate-value')
        ])
    ])
    elif selected_tab == 'tab2':
        return html.Div([
            html.H3('Content of Tab 2'),
            dcc.Graph(
                id='graph2',
                figure={'data': [{'y': [1, 3, 2]}], 
                    'layout': {'title': 'Graph in Tab 2'}}
            ),
        ])
    else:
        return html.Div([])  




# Histogram based on point selection
def get_figure(df, selectedData, col_chosen_1, col_chosen_2):
    #print(selectedData)
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
    #print(selection_bounds)

    # set which points are selected with the `selectedpoints` property
    # and style those points with the `selected` and `unselected`
    # attribute. see
    # https://medium.com/@plotlygraphs/notes-from-the-latest-plotly-js-release-b035a5b43e21
    # for an explanation
    dff = df.query(f'{col_chosen_1}>{selection_bounds["x0"]} & {col_chosen_1}<{selection_bounds["x1"]}')
    dff = dff.query(f'{col_chosen_2}>{selection_bounds["y0"]} & {col_chosen_2}<{selection_bounds["y1"]}')
    
    fig = px.histogram(dff, x=col_chosen_1, title=f'{col_chosen_1} of selected countries across years', height=400)

    return fig

# Plot of selected countries with averages across years
# using saved data on dcc.Store

#### Save elaborated data - This is calculated only once and passed into 
# a json object.
@callback(Output('intermediate-value', 'data'), Input('dropdown', 'value'))
def clean_data(value):
    # cleaned_df = slow_processing_step(value)

    # a few filter steps that compute the data
    # as it's needed in the future callbacks

    df_1 = df[ ['continent', 'lifeExp'] ]
    df_1 = df_1.groupby('continent').mean()

    df_2 = df[ ['country', 'lifeExp'] ]
    df_2 = df_2.groupby('country').mean()
     

    datasets = {
        'continent': df_1.to_json(orient='split', date_format='iso'),
        'country': df_2.to_json(orient='split', date_format='iso'),
    }

    print(datasets['continent'])
    print(datasets['country'])

    return json.dumps(datasets)


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
    fig =  px.scatter(dff, x=col_chosen_1, y=col_chosen_2, 
                      hover_data='country', height=800,
                      title=f'{col_chosen_1} vs {col_chosen_2} across countries')
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
    dff = df[df.country==country]
    fig =  px.scatter(dff, x=col_chosen_1, y=col_chosen_2, title=f'{country}', hover_data='year', height=400)
    fig.update_layout(transition_duration=500)
    return fig


# printing a graph from json'ed data
@callback(
    Output('graph-mean-histogram', 'figure'),
    Input('intermediate-value', 'data'),
    Input('dropdown', 'value'),
    )
def update_graph_4(jsonified_cleaned_data, value):
    datasets = json.loads(jsonified_cleaned_data)
    dff = pd.read_json(datasets[value], orient='split')
    figure = px.histogram(dff, x='lifeExp', title=f'Average {value} life expectancy')
    return figure


##### Callback creating histogram from data subset
@callback(
    Output('graph-hist-selection', 'figure'),
    Input('graph-content-all', 'selectedData'), #select by shift+click or selection box (chosen from plot menu)
    Input('controls-and-radio-item-1', 'value'),
    Input('controls-and-radio-item-2', 'value'),
    Input('year-slider', 'value') #just using this to redo the same histogram when changing year in the main plot, otherwise gives error!
)
#here, we subset with the country chosen by selection on the scatter plot
def update_graph_3(selection_all, col_chosen_1, col_chosen_2, year):
    
    print("hello")
    return get_figure(df, selection_all, col_chosen_1, col_chosen_2)

                      
if __name__ == '__main__':
    app.run(debug=True)