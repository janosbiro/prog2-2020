#dash
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
#open
players_all = pd.read_csv('data_final_5000.csv')
players_all['len_name'] = players_all['name'].str.len()
players_all = players_all.drop_duplicates(subset='playerId')
#app
#general attributes to the dash
external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
players_all = players_all.loc[players_all['BMI'] > 0]
players_all = players_all.loc[players_all['BMI'] < 50]
colors = {
    'background': "#D9EBC6"}

#Scatter
#personal_attributes = ["height","weight","BMI","age","len_name"]

personal_attributes = [{"label":'Height', "value":'height'}, {"label":"Weight", "value":"weight"}, 
                       {"label":"Age", "value":"age"}, {"label":"BMI - body mass index", "value": "BMI"},
          {"label":"Length of his name", "value":"len_name"
         }]

performance_variables = players_all.columns.tolist()[6:-2]
extra_filters = ['goals','field','yellow_card','red_card',"goal_keeper"]
figure1 = px.scatter(players_all, x="BMI", y="ratings", 
                     marginal_y="rug", marginal_x="histogram",
                     color_continuous_scale=px.colors.sequential.Viridis)

#Correlogram
corr = players_all.corr()
variables = [name for name in players_all.columns.to_list()[2:]]
heat = go.Heatmap(z=corr,
                  x=variables,
                  y=variables,
                  xgap=1, ygap=1,
                  colorbar_thickness=20,
                  colorbar_ticklen=3,
                  colorscale="Viridis",

                   )
layout = go.Layout( height = 1000,
                   xaxis_showgrid=False,
                   yaxis_showgrid=False,
                   yaxis_autorange='reversed')
variables_list = ["BMI","age"] 
##APP
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(style={'backgroundColor': colors['background']}, children = [
    html.H1('Spurious correlations in Football', style={'color': 'white','backgroundColor':'#3C706A'}),
   
    ##első ábrához a dropdownok                                   
    html.Div(children = [
        html.Div(children = [
            html.H3('Choose a random personal attribute'),
            dcc.Dropdown(
                            id="variables_1",
                            options=personal_attributes,
                value=[]
                        )
        ], className="six columns"),
        html.Div(children = [
            html.H3('Choose a random performance attribute'),
            dcc.Dropdown(
                            id="variables_2",
                            options=[{'label' : i, 'value' : i} for i in performance_variables],
                        )
        ], className="six columns"),
    ], className="row")
, html.H3(''),
    #első ábra
    html.Div(children=[
        html.Div(style={'color': 'white','backgroundColor':'#163B70'}, children = [
            dcc.Graph(
                            id="stat-graph",
                            figure= figure1
                        )
        ], className="ten columns"),
        html.Div(children = [
            html.H3('Extra layers'),
            dcc.Dropdown(
                            id="variables_3",
                            options=[{'label' : i, 'value' : i} for i in extra_filters],
                        )
        ], className="two columns"),
    ], className="row"),
   #második ábra és a checklistje
    html.Div(children = [
        html.Div(children = [
            html.H3('Choose variables'),
            dcc.Checklist(id='select-all',
                  options=[{'label' : i, 'value' : i} for i in players_all.columns.tolist()[2:]])
        ], className="two columns"),
        
        html.Div(children = [
            html.H3('Correlation matrix'),
             dcc.Graph(id='matrix', figure = go.Figure(data=[heat], layout = layout))
        ], className="ten columns"),
    ], className="row"),
     html.H5('source: https://www.whoscored.com/')
])
    


@app.callback(
    dash.dependencies.Output("stat-graph", "figure"),
    [dash.dependencies.Input("variables_1", "value"),dash.dependencies.Input("variables_2", "value"),
    dash.dependencies.Input("variables_3", "value")
    ],
)
def update_output(value1,value2, value3):
    figure1 = px.scatter(players_all, x=value1, y=value2, color=value3, 
                         marginal_y="rug", marginal_x="histogram", 
                         color_continuous_scale=px.colors.sequential.Viridis)
    return figure1


@app.callback(
    dash.dependencies.Output("matrix", "figure"),
    [dash.dependencies.Input("select-all", "value")],
)
def update_output2(variables_update):
    variables_list = variables_update
    corr_update = corr.loc[ variables_list, variables_list ]
    heat = go.Heatmap(z=corr_update,
                      x=variables_list,
                      y=variables_list,
                      xgap=1, ygap=1,
                      colorscale="Viridis",
                      colorbar_thickness=20,
                      colorbar_ticklen=3)
   
    return go.Figure(data=[heat], layout = layout)


if __name__=="__main__":

    app.run_server(debug = False, port=5001)
