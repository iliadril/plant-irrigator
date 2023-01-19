from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go
import plotly.graph_objects as no
from plotly.subplots import make_subplots
import numpy as np
CSV_PATH = 'data\\test.csv'


def get_data(path):
    readable_data = []
    csv_content = pd.read_csv(path, names=['data', 'humidity', 'assigned_humidity', 'water_level'])
    data = csv_content['data'].tolist()
    for i in data[1:]:
        readable_data.append(pd.to_datetime(i, unit='s'))
    return readable_data

def get_humidity(path):
    humidity_percentage = []
    csv_content = pd.read_csv(path, names=['data', 'humidity', 'assigned_humidity', 'water_level'])
    humidity = csv_content['humidity'].tolist()
    for i in humidity[1:]:
        humidity_percentage.append(round(int(i) / 750 * 100, 2))
    return humidity_percentage

def get_water(path):
    csv_content = pd.read_csv(path, names=['data', 'humidity', 'assigned_humidity', 'water_level'])
    water_level = csv_content['water_level'].tolist()[1:]
    return water_level

def get_assigned(path):
    csv_content = pd.read_csv(path, names=['data', 'humidity', 'assigned_humidity', 'water_level'])
    assigned_humidity = csv_content['assigned_humidity'].tolist()[1:]
    return assigned_humidity

# print(readable_data)           #data Timestamp
# print(humidity_percentage)     # %wilgotnosci
# print(water_level)             #poziom wody w zbiorniku
# print(assigned_humidity)       #zadana wilgotnosc

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)

def make_plot():
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Scatter(x=get_data(CSV_PATH), y=get_humidity(CSV_PATH), name="Wilgotność"))

    fig.add_trace(
        go.Scatter(x=get_data(CSV_PATH), y=get_water(CSV_PATH), name="Poziom Wody", yaxis="y2"))

    fig.add_trace(
        go.Scatter(x=get_data(CSV_PATH), y=get_assigned(CSV_PATH), name="Zadana Wilgotność", yaxis="y3"))


    fig.update_layout(
        xaxis=dict(
            domain=[0.1, 1]),
        yaxis=dict(
            range=[0,105],
            title="Wilgotność",
            titlefont=dict(
                color="#1f77b4"
            ),
            tickfont=dict(
                color="#1f77b4"
            )
        ),
        yaxis2=dict(
            range=[0, 4.2],
            title="Poziom Wody",
            titlefont=dict(
                color="#ff7f0e"
            ),
            tickfont=dict(
                color="#ff7f0e"
            ),
            anchor="free",
            overlaying="y",
            side="left",
            position = 0.05
        ),
        yaxis3=dict(
            range=[0, 105],
            title="Zadana Wilgotność",
            titlefont=dict(
                color="#d62728"
            ),
            tickfont=dict(
                color="#d62728"
            ),
            anchor="free",
            overlaying="y",
            side="left",
            position = 0
        )
    )

    fig.update_layout(
        title_text="C", width = 1800, height = 760
    )

    # Set x-axis title
    fig.update_xaxes(title_text="Czas")
    return fig



app.layout = html.Div([
    html.H1(children='Wykres symulujący działanie robota nawadniającego'),
    dcc.Graph(
        figure=make_plot(),
        id='graph',
        ),
    dcc.Slider(
        0, 100,
        value=50,
        marks=None,
        id='my-slider'
        ),
    dcc.Interval(
            id='interval-component-graph',
            interval=1*8000, # in milliseconds
            n_intervals=0
        ),
    dcc.Interval(
            id='interval-component-slider',
            interval=1*1000, # in milliseconds
            n_intervals=0
        ),
    html.Div(id='slider-output-container'),
])

steps=[]      # steps of slider

@app.callback(
    Output('slider-output-container', 'children'),
    Input('my-slider', 'value'),
    Input('interval-component-slider', 'n_intervals'))
def update_output(value, n):
    #TODO zapis do pliku
    steps.append(format(value))
    return


@app.callback(
    Output('graph', 'figure'),
    Input('interval-component-graph', 'n_intervals')
)
def update_graph(n):
    fig = make_plot()
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
