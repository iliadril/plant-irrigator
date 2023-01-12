import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

csv_content = pd.read_csv('data.csv', names = ['data','humidity','water_level'])
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


# Create figure with secondary y-axis
fig = make_subplots(specs=[[{"secondary_y": True}]])

# Add traces
fig.add_trace(
    go.Scatter(x=readable_data, y=humidity_percentage, name="Wilgotność"))

fig.add_trace(
    go.Scatter(x=readable_data, y=water_level, name="Poziom Wody", yaxis="y2"))

scroll_bar =[]          # TODO shit do wyjebania
for i in range(0,10):
    scroll_bar.append(i*(-1))

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

#kurwa TODO
for step in np.arange(0, 100, 5):
    fig.add_trace(
        go.Scatter(
            visible=False,
            line=dict(color="#00CED1", width=3),
            x=readable_data,
            y=np.sin(step * np.arange(0, 100, 5))))


steps = []
for i in range(20):
    step = dict(
        method="update",
        args=[{"visible": [False] * len(fig.data)}],
    )
    step["args"][0]["visible"][i] = True
    steps.append(step)

sliders = [dict(
    active=10,
    pad={"t": 50},
    steps=steps
)]
fig.update_layout(
    sliders=sliders
)

#TODO KURWA

# Add figure title
fig.update_layout(
    title_text="C", width = 1600
)

# Set x-axis title
fig.update_xaxes(title_text="Czas")
fig.show()
