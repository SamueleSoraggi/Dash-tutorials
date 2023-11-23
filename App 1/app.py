from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
#import scanpy as sc

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

app = Dash(__name__)


#Simpe layout using HTML and some dash components (2 radio buttons + 1 dropdown menu)                                         
app.layout = html.Div([
    html.H1(children='Title of Dash App', style={'textAlign':'center'}),
    dcc.RadioItems(options=['pop', 'lifeExp', 'gdpPercap'], value='lifeExp', id='controls-and-radio-item-1'),
    dcc.RadioItems(options=['pop', 'lifeExp', 'gdpPercap'], value='lifeExp', id='controls-and-radio-item-2'),
    #dcc.Dropdown(df.country.unique(), 'Canada', id='dropdown-selection'),
    dcc.Dropdown(['country','continent',None], None, id='dropdown-selection'),
    dcc.Graph(figure={}, id='graph-content')
])

@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value'),
    Input('controls-and-radio-item-1', 'value'),
    Input('controls-and-radio-item-2', 'value')
)

#here, the inputs to update_graph are in the same order as the inputs in the callback and 
#you just need to choose a variable name
def update_graph(value, col_chosen_1, col_chosen_2):
    #dff = df[df.country==value]
    #return px.line(dff, x='year', y=col_chosen[1], color=value)
    return px.scatter(df, x=col_chosen_1, y=col_chosen_2, color=value)

if __name__ == '__main__':
    app.run(debug=True)