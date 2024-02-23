import dash
import dash_core_components as dcc
import dash_html_components as html
from plotly.subplots import make_subplots
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go

app = dash.Dash(__name__)

data = pd.read_csv("./data/programming-languages-pupularity.csv")
data["Date"] = pd.to_datetime(data["Date"])
languages = sorted(data.columns[3:], key=lambda x: data[x].mean(), reverse=True)

@app.callback(
    Output("graph", "figure"),
    Input("top-n", "value"),
)
def build_graph(n=10):
    n = int(n)

    fig = make_subplots(shared_yaxes=True, shared_xaxes=True)
    for lang in languages[:n]:
        fig.add_trace(go.Scatter(x=data["Date"], y=data[lang], mode='lines', name=lang))

    fig.update_layout(title=f'Top {n} Programming Languages popularity change',
                      xaxis_title='Year',
                      yaxis_title='Ratings(%)')
    
    return fig 


app.layout = html.Div(children=[
   html.H1(children='Popularity of Programming Languages'),

   html.Div(children='The line graph presents the dynamics of the programming languages popularity from 2004 to 2023'),

   dcc.Graph(
       id='graph'
   ),

   dcc.Slider(
       id="top-n",
       min=1,
       max=len(languages),
       marks={i: 'Top{}'.format(i) for i in range(1, len(languages))},
       value=10,
   )
])

if __name__ == '__main__':
   app.run_server(debug=True)