from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

csv_content = pd.read_csv('data\\test.csv', names = ['data','humidity','water_level'])
data = csv_content['data'].tolist()
humidity = csv_content['humidity'].tolist()
water_level = csv_content['water_level'].tolist()[1:]

readable_data = []
humidity_percentage = []

for i in humidity[1:]:
    humidity_percentage.append(round(int(i)/750 * 100,2))

for i in data[1:]:
    readable_data.append(pd.to_datetime(i,unit='s'))

#print(readable_data)           #data Timestamp
#print(humidity_percentage)     # %wilgotnosci
#print(water_level)             #poziom wody w zbiorniku

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)
fig = make_subplots(specs=[[{"secondary_y": True}]])

# Add traces
fig.add_trace(
    go.Scatter(x=readable_data, y=humidity_percentage, name="Wilgotność"))

fig.add_trace(
    go.Scatter(x=readable_data, y=water_level, name="Poziom Wody", yaxis="y2"))

p=[]
scroll_bar = []
scroll_bar.append(50)
def kamil_gej(value):
    p.append(value)
    for i in range(len(p)):
        scroll_bar.append(p[i])
    fig.add_trace(
        go.Scatter(x=readable_data, y=scroll_bar, name="Zadana Wilgotność", yaxis="y3"))

fig.update_layout(
    xaxis=dict(
        domain=[0.1, 1]),
    yaxis=dict(
        title="Wilgotność",
        titlefont=dict(
            color="#1f77b4"
        ),
        tickfont=dict(
            color="#1f77b4"
        )
    ),
    yaxis2=dict(
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


app.layout = html.Div([
    html.H1(children='Wykres symulujący działanie robota nawadniającego'),
    dcc.Graph(figure=fig,
              id='graph',
              ),
    dcc.Slider(0, 100,
               value=50,
               marks=None,
               id='my-slider'
    ),

    html.Div(id='slider-output-container')
])

#app.layout = html.Div([])
tab = []

@app.callback(
    Output('slider-output-container', 'children'),
    Input('my-slider', 'value'))

def update_output(value):
    tab.append(format(value))
    kamil_gej(value)
    return tab

if __name__ == '__main__':
    app.run_server(debug=True)
