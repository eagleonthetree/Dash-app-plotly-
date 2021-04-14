import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import dash.dependencies as dependencies
import os
import json

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
with open('custom.geo.json', 'r',encoding="utf-8") as f:
    data = json.load(f)

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
df = px.data.gapminder()


app.layout = html.Div(children=[
    html.H2(children='Dash app'),
    html.H5(children='created by eaglethetree')
html.Div(
    children=[html.Label('Select Year:'),
dcc.Dropdown(id='select-year',options=[
{'label': '1952', 'value': 1952},
{'label': '1957', 'value': 1957},
{'label': '1962', 'value': 1962},
{'label': '1967', 'value': 1967},
{'label': '1972', 'value': 1972},
{'label': '1977', 'value': 1977},
{'label': '1982', 'value': 1982},
{'label': '1987', 'value': 1987},
{'label': '1992', 'value': 1992},
{'label': '1992', 'value': 1992},
{'label': '2007', 'value': 2007},
],
value=1952 ),

html.Label('Select Chart:'),
dcc.Dropdown(id='select-cat',options=[
{'label': 'Life Expectation', 'value': 'lifeExp'},
{'label': 'GDP Per Capita', 'value': 'gdpPercap'},
{'label': 'Population', 'value': 'pop'}
],
value='lifeExp' ),
], style={'columnCount': 1}),

    dcc.Graph(id='gap-map',figure={}),
    dcc.Graph(id='gap-bar',figure={})

],)

@app.callback(
    dependencies.Output(component_id='gap-map', component_property='figure'),
    dependencies.Input(component_id='select-year', component_property='value'),
    dependencies.Input(component_id='select-cat', component_property='value')
)

def update_fig(year,cat):
    global filtered_df2
    fdf = df[df['year']==year]
    filtered_df2 = fdf[["country", "continent", "year", cat, 'iso_alpha', 'iso_num']]
    fig = px.choropleth_mapbox(filtered_df2,geojson=data, locations="country",
                               featureidkey="properties.sovereignt",
                               color=cat,
                               mapbox_style="carto-positron",
                               zoom=1,
                               opacity=0.7,
                               color_continuous_scale="IceFire",
                               )

    return fig

@app.callback(

    dependencies.Output(component_id='gap-bar', component_property='figure'),
    dependencies.Input('gap-map', 'selectedData'),
    dependencies.Input(component_id='select-year', component_property='value'),
    dependencies.Input(component_id='select-cat', component_property='value'))

def update_bar(selectedData,year,cat):

        dataframe1 = pd.DataFrame(selectedData['points'])
        dataframe1.columns = ['1', '2', '3', 'country', '4']
        y = dataframe1.drop(columns=['1', '2', '3', '4'])
        keys = list(y.columns.values)
        i1 = filtered_df2.set_index(keys).index
        i2 = y.set_index(keys).index
        filtered_df3 = filtered_df2[i1.isin(i2)]
        fig2 = px.bar(filtered_df3, x="country", y=cat,color="country")
        print(selectedData['points'])
        print(filtered_df3)
        return fig2

if __name__ == '__main__':
  app.run_server(debug=True,port=int(os.getenv('PORT', '4544')))


