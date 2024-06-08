from jbi100_app.main import app
from jbi100_app.views.menu import make_menu_layout
from jbi100_app.views.scatterplot import Scatterplot

from dash.dependencies import Input, Output

import plotly.express as px
from dash import Dash, dcc, html, Input, Output, callback
import plotly.graph_objs as go
import pandas as pd
import json
from PIL import Image

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

df = pd.read_csv("sustainable_energy_nl.csv") 

df['BevolkingAanHetEindeVanDePeriode_15'] = pd.to_numeric(df['BevolkingAanHetEindeVanDePeriode_15'], errors='coerce')
df['BevolkingAanHetEindeVanDePeriode_15'] = df['BevolkingAanHetEindeVanDePeriode_15'].fillna(0)

coordinates = {
    'ET3002': (560, 48),
    'ET3001': (600, 68),
    'ET3003': (570, 98),
    'ET2901': (600, 200),
    'ET2601': (500, 250),
    'ET2701': (500, 340),
    'ET2501': (405, 300),
    'ET2801': (300, 300),
    'ET2401': (125, 275),
    'ET1901': (200, 365),
    'ET2001': (265, 380),
    'ET1801': (320, 390),
    'ET1701': (355, 420),
    'ET2301': (240, 440),
    'ET2201': (325, 450),
    'ET1101': (450, 405),
    'ET1401': (400, 465),
    'ET0902': (513, 458),
    'ET0801': (580, 420),
    'ET0701': (700, 450),
    'ET1201': (610, 525),
    'ET0901': (540, 490),
    'ET1001': (530, 550),
    'ET1301': (470, 510),
    'ET1604': (420, 540),
    'ET1601': (360, 590),
    'ET1606': (355, 560),
    'ET1605': (325, 570),
    'ET2101': (300, 515),
    'ET1602': (300, 600),
    'ET1603': (370, 630),
    'ET0601': (490, 600),
    'ET0501': (670, 650),
    'ET0401': (760, 575),
    'ET1503': (400, 705),
    'ET1502': (330, 675),
    'ET1501': (360, 750),
    'ET0301': (740, 770),
    'ET0201': (575, 840),
    'ET0101': (760, 910),
}

df['x'] = df['RegioS'].map(lambda regio: coordinates[regio][0])
df['y'] = df['RegioS'].map(lambda regio: coordinates[regio][1])

map = Image.open('map.png')

app = Dash(__name__, external_stylesheets=external_stylesheets)

def create_figure(filtered_df):
    fig = go.Figure()

    # Adding background image (map)
    fig.add_layout_image(
        dict(
            source= map,
            xref="x",
            yref="y",
            x=0,
            y=1032,
            sizex=898,
            sizey=1032,
            sizing="stretch",
            opacity=1,
            layer="below"
        )
    )

    # Adding scatter plot with RegioS regions and population data
    fig.add_trace(go.Scatter(
        x=filtered_df['x'],
        y=filtered_df['y'],
        mode='markers+text',
        text=filtered_df['RegioS'],
        textposition="top center",
        customdata=filtered_df[['ID_x', 'BevolkingAanHetBeginVanDePeriode_1']],
        marker=dict(
            size=(filtered_df['BevolkingAanHetEindeVanDePeriode_15'] / 1).clip(lower=10),  # Adjust the size scaling factor as needed
            sizemode='area',
            sizeref=2. * max(filtered_df['BevolkingAanHetEindeVanDePeriode_15']) / (40. ** 2),  # Adjust marker size
        ),
        hovertemplate="<b>%{text}</b><br>Population: %{customdata[1]}<extra></extra>"
    ))

    fig.update_layout(
        xaxis=dict(
            visible=False,
            range=[0, 898]
        ),
        yaxis=dict(
            visible=False,
            range=[0, 1032],
            scaleanchor="x",
            scaleratio=1
        ),
        width=898,
        height=1032,
        margin=dict(l=0, r=0, t=0, b=0),
        clickmode='event+select'
    )

    return fig

# App layout
app.layout = html.Div(
    id="app-container",
    style={'display': 'flex', 'height': '100vh'},
    children=[
        html.Div(
            id="left-column",
            style={'flex': '2', 'max-width': '70%', 'height': '100%'},
            children=[
                dcc.Graph(
                    id='basic-interactions',
                    style={'width': '100%', 'height': '100%'}
                )
            ]
        ),
        html.Div(
            id="right-column",
            style={'flex': '1', 'padding-left': '20px', 'overflow-y': 'scroll'},
            children=[
                html.Div([
                    dcc.Dropdown(
                        id='year-filter',
                        options=[{'label': period, 'value': period} for period in df['Perioden'].unique()],
                        placeholder="Select a year"
                    ),
                ]),
                html.Div([
                    dcc.Markdown("""
                        **Hover Data**

                        Mouse over values in the graph.
                    """),
                    html.Pre(id='hover-data', style={'border': 'thin lightgrey solid', 'overflowX': 'scroll'})
                ], className='six columns'),

                html.Div([
                    dcc.Markdown("""
                        **Click Data**

                        Click on points in the graph.
                    """),
                    html.Pre(id='click-data', style={'border': 'thin lightgrey solid', 'overflowX': 'scroll'}),
                ], className='six columns'),

                html.Div([
                    dcc.Markdown("""
                        **Selection Data**

                        Choose the lasso or rectangle tool in the graph's menu
                        bar and then select points in the graph.
                    """),
                    html.Pre(id='selected-data', style={'border': 'thin lightgrey solid', 'overflowX': 'scroll'}),
                ], className='six columns'),

                html.Div([
                    dcc.Markdown("""
                        **Zoom and Relayout Data**

                        Click and drag on the graph to zoom or click on the zoom
                        buttons in the graph's menu bar.
                    """),
                    html.Pre(id='relayout-data', style={'border': 'thin lightgrey solid', 'overflowX': 'scroll'}),
                ], className='six columns')
            ]
        )
    ]
)
    # Define interactions
@app.callback(
    Output('basic-interactions', 'figure'),
    Input('year-filter', 'value'))
def update_figure(selected_year):
    if selected_year:
        filtered_df = df[df['Perioden'] == selected_year]
    else:
        filtered_df = df
    return create_figure(filtered_df)

@app.callback(
    Output('hover-data', 'children'),
    Input('basic-interactions', 'hoverData'))
def display_hover_data(hoverData):
    return json.dumps(hoverData, indent=2)

@app.callback(
    Output('click-data', 'children'),
    Input('basic-interactions', 'clickData'))
def display_click_data(clickData):
    return json.dumps(clickData, indent=2)

@app.callback(
    Output('selected-data', 'children'),
    Input('basic-interactions', 'selectedData'))
def display_selected_data(selectedData):
    return json.dumps(selectedData, indent=2)

@app.callback(
    Output('relayout-data', 'children'),
    Input('basic-interactions', 'relayoutData'))
def display_relayout_data(relayoutData):
    return json.dumps(relayoutData, indent=2)

if __name__ == '__main__':
    app.run_server(debug=False)