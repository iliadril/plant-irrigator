import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots

CSV_PATH = './data/data.csv'


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
    assigned_humidity_in_percent = []
    csv_content = pd.read_csv(path, names=['data', 'humidity', 'assigned_humidity', 'water_level'])
    assigned_humidity = csv_content['assigned_humidity'].tolist()[1:]
    for i in assigned_humidity:
        assigned_humidity_in_percent.append(round(int(i) / 7.5, 2))
    return assigned_humidity_in_percent


def get_acutal_given_humidity(path):
    csv_content = pd.read_csv(path, names=['data', 'humidity', 'assigned_humidity', 'water_level'])
    assigned_humidity = csv_content['assigned_humidity'].tolist()[1:]
    return round(int(assigned_humidity[-1]) / 7.5, 0) if len(assigned_humidity) > 1 else 50


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server


def make_plot():
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Scatter(x=get_data(CSV_PATH), y=get_humidity(CSV_PATH), name="Wilgotność", line=dict(color='blue')))

    fig.add_trace(
        go.Scatter(x=get_data(CSV_PATH), y=get_water(CSV_PATH), name="Poziom Wody", line=dict(color='red'), yaxis="y2"))

    fig.add_trace(
        go.Scatter(x=get_data(CSV_PATH), y=get_assigned(CSV_PATH), name="Zadana Wilgotność", line=dict(color='green'),
                   yaxis="y3"))

    fig.update_layout(
        xaxis=dict(
            domain=[0.1, 1]),
        yaxis=dict(
            autotypenumbers='convert types',
            range=[0, 105],
            title="Wilgotność",
            titlefont=dict(
                color='blue'
            ),
            tickfont=dict(
                color='blue'
            )
        ),
        yaxis2=dict(
            autotypenumbers='convert types',
            range=[0, 4.2],
            title="Poziom Wody",
            titlefont=dict(
                color='red'
            ),
            tickfont=dict(
                color='red'
            ),
            anchor="free",
            overlaying="y",
            side="left",
            position=0.05
        ),
        yaxis3=dict(
            range=[0, 105],
            autotypenumbers='convert types',
            title="Zadana Wilgotność",
            titlefont=dict(
                color='green'
            ),
            tickfont=dict(
                color='green'
            ),
            anchor="free",
            overlaying="y",
            side="left",
            position=0
        )
    )

    fig.update_layout(
        title_text="Wykres symulujący działanie robota nawadniającego"
    )

    # Set x-axis title
    fig.update_xaxes(title_text="Czas")
    return fig


def serve_layout():
    return dbc.Container([
        dbc.Row(
            dbc.Col(
                dcc.Graph(
                    figure=make_plot(),
                    id='graph',
                ),
            )
        ),
        dbc.Row(
            dbc.Col(
                html.H6("nastawa pożądanej wilgotności"),
            ),
        ),
        dbc.Row(
            dbc.Col(
                dcc.Slider(
                    0, 100,
                    value=get_acutal_given_humidity(CSV_PATH),
                    id='target-humidity-slider',
                    tooltip={'placement': 'bottom'}
                ),
                width=6,
            )
        ),
        dcc.Interval(
            id='interval-component-graph',
            interval=1 * 1000 * 60,  # in milliseconds
            n_intervals=0,
        ),

    ])


app.layout = serve_layout


@app.callback(
    Output('target-humidity-slider', 'value'),
    Input('target-humidity-slider', 'value'),
)
def update_output(slider_value):
    # rabbit.send_message('config', f'{int(slider_value * 7.5)}')
    return slider_value


@app.callback(
    Output('graph', 'figure'),
    Input('interval-component-graph', 'n_intervals')
)
def update_graph(n):
    fig = make_plot()
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
