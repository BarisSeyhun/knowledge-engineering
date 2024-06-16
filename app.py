from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
from dash import Dash, dcc, html
import json
from PIL import Image

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

df = pd.read_csv('sustainable_energy_nl.csv')
df['BevolkingAanHetEindeVanDePeriode_15'] = df['BevolkingAanHetEindeVanDePeriode_15'].str.replace(',', '.')
df['BevolkingAanHetEindeVanDePeriode_15'] = pd.to_numeric(df['BevolkingAanHetEindeVanDePeriode_15'], errors='coerce')
df.fillna(0, inplace=True)
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


def create_figure(filtered_df, topic, fraction_filter):
    fig = go.Figure()

    # Adding background image (map)
    fig.add_layout_image(
        dict(
            source=map,
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

    # Determine the marker information based on the selected topic
    if topic == 'Population':
        selected_topic = filtered_df['BevolkingAanHetEindeVanDePeriode_15']
        size = selected_topic.clip(lower=1)
        hovertemplate = "<b>%{text}</b><br>Population: %{customdata[1]}<extra></extra>"
        customdata = filtered_df[['ID_x', 'BevolkingAanHetBeginVanDePeriode_1']]
        color = 'cornflowerblue'
        sizeref = selected_topic.max()
    elif topic == 'Solar Energy':
        selected_topic = filtered_df['norm_prod_solar_allpower']
        size = selected_topic.clip(lower=1)
        hovertemplate = "<b>%{text}</b><br>Solar Energy: %{customdata[1]}<extra></extra>"
        customdata = filtered_df[['ID_x', 'norm_prod_solar_allpower']]
        color = '#ffea2d'
        sizeref = selected_topic.max()
    elif topic == 'Wind Energy':
        selected_topic = filtered_df['norm_prod_wind']
        size = selected_topic.clip(lower=1)
        hovertemplate = "<b>%{text}</b><br>Wind Energy: %{customdata[1]}<extra></extra>"
        customdata = filtered_df[['ID_x', 'norm_prod_wind']]
        color = '#008080'
        sizeref = selected_topic.max()
    elif topic == 'Fraction (Solar)':
        selected_topic = filtered_df['FractionSolar']
        if fraction_filter:
            filtered_df = filtered_df[selected_topic > 1]
        size = selected_topic.clip(lower=0)
        hovertemplate = "<b>%{text}</b><br>Fraction (Solar): %{customdata[1]}<extra></extra>"
        customdata = filtered_df[['ID_x', 'FractionSolar']]
        color = 'coral'
        sizeref = selected_topic.max()
    elif topic == 'Fraction (Wind)':
        selected_topic = filtered_df['FractionWind']
        if fraction_filter:
            filtered_df = filtered_df[selected_topic > 1]
        size = selected_topic.clip(lower=0)
        hovertemplate = "<b>%{text}</b><br>Fraction (Wind): %{customdata[1]}<extra></extra>"
        customdata = filtered_df[['ID_x', 'FractionWind']]
        color = 'midnightblue'
        sizeref = selected_topic.max()
    elif topic == 'Fraction (Total)':
        selected_topic = filtered_df['FractionTotal']
        if fraction_filter:
            filtered_df = filtered_df[selected_topic > 1]
        size = selected_topic.clip(lower=0)
        hovertemplate = "<b>%{text}</b><br>Fraction (Total): %{customdata[1]}<extra></extra>"
        customdata = filtered_df[['ID_x', 'FractionTotal']]
        color = 'purple'
        sizeref = selected_topic.max()

    fig.add_trace(go.Scatter(
        x=filtered_df['x'],
        y=filtered_df['y'],
        mode='markers+text',
        text=filtered_df['RegioS'],
        textposition="top center",
        customdata=customdata,
        marker=dict(
            color=color,
            size=size,  # Adjust the size scaling factor as needed
            sizemode='area',
            sizeref=sizeref / 30 ** 2,  # Adjust marker size
        ),
        hovertemplate=hovertemplate
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
                        value='2018JJ00'
                    ),
                ]),
                html.Div([
                    dcc.Dropdown(
                        id='topic-selection',
                        options=[
                            {'label': 'Population', 'value': 'Population'},
                            {'label': 'Solar Energy', 'value': 'Solar Energy'},
                            {'label': 'Wind Energy', 'value': 'Wind Energy'},
                            {'label': 'Fraction (Solar)', 'value': 'Fraction (Solar)'},
                            {'label': 'Fraction (Wind)', 'value': 'Fraction (Wind)'},
                            {'label': 'Fraction (Total)', 'value': 'Fraction (Total)'}
                        ],
                        placeholder="Select a topic",
                        value='Population'  # Default value
                    ),
                ]),

                html.Div([
                    dcc.Checklist(
                        id='fraction-filter',
                        options=[{'label': 'Self-sufficient sub-regions', 'value': 'filter'}],
                        value=[]
                    )
                ])
            ]
        )
    ]
)


# Define interactions
@app.callback(
    Output('basic-interactions', 'figure'),
    [Input('year-filter', 'value'), Input('topic-selection', 'value'), Input('fraction-filter', 'value')]
)
def update_figure(selected_year, selected_topic, fraction_filter):
    filtered_df = df[df['Perioden'] == selected_year]
    fraction_filter = 'filter' in fraction_filter
    return create_figure(filtered_df, selected_topic, fraction_filter)


if __name__ == '__main__':
    app.run_server(debug=False)
