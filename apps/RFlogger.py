import dash_core_components as dcc
import dash_html_components as html
from aggregateHelper import app
import aggregateHelper as af
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
import json
import urllib2
import igraph as ig

data = []
req = urllib2.Request("https://raw.githubusercontent.com/plotly/datasets/master/miserables.json")
opener = urllib2.build_opener()
f = opener.open(req)
data = json.loads(f.read())

af.getDataset('SPARC December 2018')
datasetList= af.getDatasets()
# data = af.getObjectNeighbours('R:Grant:24b3b2af-2461-b746-d462-4b78715b9e95')
N=len(data['nodes'])
L=len(data['links'])
Edges=[(data['links'][k]['source'], data['links'][k]['target']) for k in range(L)]

G=ig.Graph(Edges, directed=False)
labels=[]
group=[]
for node in data['nodes']:
    labels.append(node['name'])
    group.append(node['group'])

layt=G.layout('kk', dim=3)
Xn=[layt[k][0] for k in range(N)]# x-coordinates of nodes
Yn=[layt[k][1] for k in range(N)]# y-coordinates
Zn=[layt[k][2] for k in range(N)]# z-coordinates
Xe=[]
Ye=[]
Ze=[]
for e in Edges:
    Xe+=[layt[e[0]][0],layt[e[1]][0], None]# x-coordinates of edge ends
    Ye+=[layt[e[0]][1],layt[e[1]][1], None]
    Ze+=[layt[e[0]][2],layt[e[1]][2], None]

import plotly.plotly as py
import plotly.graph_objs as go

trace1=go.Scatter3d(x=Xe,
               y=Ye,
               z=Ze,
               mode='lines',
               line=dict(color='rgb(125,125,125)', width=1),
               hoverinfo='none'
               )

trace2=go.Scatter3d(x=Xn,
               y=Yn,
               z=Zn,
               mode='markers',
               name='actors',
               marker=dict(symbol='circle',
                             size=7,
                             color=group,
                             colorscale='Jet',
                             line=dict(color='rgb(50,50,50)', width=0.5)
                             ),
               text=labels,
               hoverinfo='text'
               )

axis=dict(
    #showbackground=False,
    showline=False,
    zeroline=False,
    showgrid=False,
    showticklabels=False,
    title='' )


layoutQWE = go.Layout(
    title="Blackfynn Model",
    xaxis=axis,
    yaxis= axis,
    showlegend = False,
    margin={'t':0,'b': 0, 'l':0, 'r':0},
    hovermode='closest',
)

data=[trace1, trace2]
fig=go.Figure(data=data, layout=layoutQWE)

# datasetList = []
# for iKey in bfDatasetDict.keys():
#     datasetList.append({"label":iKey, 'value':bfDatasetDict[iKey]})

layout = [
    # top controls
    html.Div(
        [

            html.Div(
                dcc.Dropdown(
                    id="sortDropdown1",
                    placeholder = 'Select dataset',
                    options=datasetList,
                    value=datasetList[-1]['value'],
                    clearable=False,
                ),
                className="four columns",
            ),
            html.Div(
                dcc.Dropdown(
                    id="sortDropdown2",
                    options=[],
                    value='',
                    clearable=False,
                    # multi=True,
                    # disabled=True,
                    placeholder = 'Select record types'
                ),
                className="four columns",
            ),

            html.Div(
                html.P('# records'),className="one columns",),

            html.Div(
                dcc.Slider(
                    id='slider-updatemode',
                    marks={i-2: '{}'.format(10 ** i) for i in range(2,6)},
                    max=3,
                    value=2,
                    step=0.01,
                    updatemode='drag',
                ),
                className="three columns",
                style={"marginLeft": "10"},

            ),


        ],
        className="row",
        style={"marginBottom": "10"},
    ),

    # indicators row div
    html.Div(
        [
            af.indicator(
                "#00cc96", "Unique records", "left_leads_indicator", '12768'
            ),
            af.indicator(
                "#119DFF", "Clustering coefficient", "middle_leads_indicator", '63.45%'
            ),
            af.indicator("#EF553B","Orphan objects", "right_leads_indicator",  4
            ),
        ],
        className="row",
    ),

    # charts row div
    html.Div(
        [
            html.Div(
                [
                    html.P("Blackfynn Model/Dataset"),
                    dcc.Graph(
                        id="map",
                        style={"height": "90%", "width": "98%"},
                        config=dict(displayModeBar=False),
                        figure = fig
                    ),
                ],
                className="eight columns chart_div",style=dict(height='65vh')
            ),

            html.Div(
                dcc.Textarea(
                    id='surfaceResponse',
                    style={'width': '100%', 'height': '100%'},
                    value='n/a',
                    # maxLength=50,
                    readOnly=False,
                    title='Responses entered on Surface',
                    draggable=False
                ),
                className="four columns chart_div",style=dict(height='65vh')
            ),

        ],
        className="row",
        style={"marginTop": "5"},
    ),

    # RF images
    # html.Div(
    #     [
    #         af.getRFtemplate(0,'RF'),
    #         af.getRFtemplate(1,'RF'),
    #         af.getRFtemplate(2,'RF'),
    #         af.getRFtemplate(3,'RF'),
    #         af.getRFtemplate(4,'RF'),
    #         af.getRFtemplate(5,'RF')
    #     ],
    # className = "row",
    # style={"marginTop": "10"},
    # ),
]



# @app.callback (Output("reportButton", "children"),
#                [Input('reportButton', 'n_clicks')],
#               [State('reportButton', 'value')])
# def generateReport(n,a):
#     if n != 0:
#         return "Coming soon"
#     else:
#         return 'Download report'
#
# updates left indicator based on df updates
# @app.callback (Output("left_leads_indicator", "children"),
#               [Input('refreshButton', 'n_clicks'),
#                Input('sortDropdown1', 'value'),
#                Input('sortDropdown2', 'value')])
# def update_left_leads_indicator(n, v1, v2):
#     return af.getNumChans(v1,v2)
#
# @app.callback (Output("middle_leads_indicator", "children"),
#                [Input('refreshButton', 'n_clicks'),
#                 Input('sortDropdown1', 'value'),
#                 Input('sortDropdown2', 'value')])
# def update_middle_leads_indicator(n, v1, v2):
#     return af.getNumSensations(v1,v2)
#
# @app.callback (Output("right_leads_indicator", "children"),
#                [Input('refreshButton', 'n_clicks'),
#                 Input('sortDropdown1', 'value'),
#                 Input('sortDropdown2', 'value')])
# def update_right_leads_indicator(n, v1, v2):
#     return af.getNumTrials(v1,v2)
#
#
# @app.callback(
#     Output("modalityBar", "figure"),
#     [Input('refreshButton', 'n_clicks'),
#      Input('sortDropdown1', 'value'),
#      Input('sortDropdown2', 'value')],)
# def modalityBar_callback(n, v1, v2):
#
#     trace = go.Bar(
#         x=af.perceptDescriptors,
#         y=af.getPerceptModality(v1,v2)
#     )
#
#     layout = dict(margin=dict(l=40, r=10, t=0, b=70), legend=dict(orientation="h"),xaxis=dict(tickangle=-45, fixedrange=True), yaxis=dict(fixedrange=True))
#
#     return dict(data=[trace], layout=layout)
#
#
# @app.callback(
#     Output("locationPie", "figure"),
#     [Input('refreshButton', 'n_clicks'),
#      Input('sortDropdown1', 'value'),
#      Input('sortDropdown2', 'value')],)
# def locationPie_callback(n, v1, v2):
#
#     RFcounts = af.getPerceptLocation(v1,v2)
#     numPercepts = 0
#     for i in RFcounts:
#         numPercepts += i
#
#     if  numPercepts != 0:
#         pieLabel = af.imgName
#         pieVals = [x/float(numPercepts) for x in RFcounts]
#         trace = go.Pie(
#             labels=pieLabel,
#             values=pieVals
#         )
#
#         layout = dict(margin=dict(l=15, r=10, t=20, b=65), legend=dict(orientation="v"))
#
#         return dict(data=[trace], layout=layout)
#
#     else:
#         return []
#
#
# @app.callback(
#     Output('Blegs_RF', 'figure'),
#     [Input('refreshButton', 'n_clicks'),
#      Input('sortDropdown1', 'value'),
#      Input('sortDropdown2', 'value')],
#      [State('Blegs_RF', 'figure')])
# def drawBlegs(n,v1,v2, fig):
#     getCoords = af.getPixelCoords(v1,v2, 'Blegs')
#     fig['data'] = []
#     if getCoords:
#         # fig['data'] = [go.Heatmap(z= getCoords['Blegs'],showscale=False,colorscale=[[0,'white'], [1,'red']])]
#         op = 1/float(len(getCoords['Blegs']))
#         if op < 0.005:
#             op = 0.005
#         for iLine in getCoords['Blegs']:
#             fig['data'].append({'x': iLine[::2], 'y': iLine[1::2], 'mode': 'lines', 'opacity': op,'fill':'toself','fillcolor' :af.colorOrder[0],'line':dict(color=af.colorOrder[0]),'hoverinfo': 'none'})
#     return fig
#
#
# @app.callback(
#     Output('Flegs_RF', 'figure'),
#     [Input('refreshButton', 'n_clicks'),
#      Input('sortDropdown1', 'value'),
#      Input('sortDropdown2', 'value')],
#      [State('Flegs_RF', 'figure')])
# def drawFlegs(n,v1,v2, fig):
#     getCoords = af.getPixelCoords(v1,v2, 'Flegs')
#     fig['data'] = []
#     if getCoords:
#         # fig['data'] = [go.Heatmap(z= getCoords['Flegs'],showscale=False,colorscale=[[0,0,0],'B','R'])]
#         op = 1/float(len(getCoords['Flegs']))
#         if op < 0.005:
#             op = 0.005
#         for iLine in getCoords['Flegs']:
#             fig['data'].append({'x': iLine[::2], 'y': iLine[1::2], 'mode': 'lines', 'opacity': op,'fill':'toself','fillcolor' :af.colorOrder[1],'line':dict(color=af.colorOrder[1]),'hoverinfo': 'none'})
#     return fig
#
#
# @app.callback(
#     Output('Ldors_RF', 'figure'),
#     [Input('refreshButton', 'n_clicks'),
#      Input('sortDropdown1', 'value'),
#      Input('sortDropdown2', 'value')],
#      [State('Ldors_RF', 'figure')])
# def drawLdors(n,v1,v2, fig):
#     getCoords = af.getPixelCoords(v1,v2, 'Ldors')
#     fig['data'] = []
#     if getCoords:
#         # fig['data'] = [go.Heatmap(z= getCoords['Ldors'],showscale=False,zmin = 1)]
#         op = 1/float(len(getCoords['Ldors']))
#         if op < 0.005:
#             op = 0.005
#         for iLine in getCoords['Ldors']:
#             fig['data'].append({'x': iLine[::2], 'y': iLine[1::2], 'mode': 'lines', 'opacity': op,'fill':'toself','fillcolor' :af.colorOrder[2],'line':dict(color=af.colorOrder[2]),'hoverinfo': 'none'})
#     return fig
#
#
# @app.callback(
#     Output('Rdors_RF', 'figure'),
#     [Input('refreshButton', 'n_clicks'),
#      Input('sortDropdown1', 'value'),
#      Input('sortDropdown2', 'value')],
#      [State('Rdors_RF', 'figure')])
# def drawRdors(n,v1,v2, fig):
#     getCoords = af.getPixelCoords(v1,v2, 'Rdors')
#     fig['data'] = []
#     if getCoords:
#         # fig['data'] = [go.Heatmap(z= getCoords['Rdors'],showscale=False,zmin = 1)]
#         op = 1/float(len(getCoords['Rdors']))
#         if op < 0.005:
#             op = 0.005
#         for iLine in getCoords['Rdors']:
#             fig['data'].append({'x': iLine[::2], 'y': iLine[1::2], 'mode': 'lines', 'opacity': op,'fill':'toself','fillcolor' :af.colorOrder[3],'line':dict(color=af.colorOrder[3]),'hoverinfo': 'none'})
#     return fig
#
#
# @app.callback(
#     Output('Lsole_RF', 'figure'),
#     [Input('refreshButton', 'n_clicks'),
#      Input('sortDropdown1', 'value'),
#      Input('sortDropdown2', 'value')],
#      [State('Lsole_RF', 'figure')])
# def drawLsole(n,v1,v2, fig):
#     getCoords = af.getPixelCoords(v1,v2, 'Lsole')
#     fig['data'] = []
#     if getCoords:
#         # fig['data'] = [go.Heatmap(z= getCoords['Lsole'],showscale=False,zmin = 1)]
#         op = 1/float(len(getCoords['Lsole']))
#         if op < 0.005:
#             op = 0.005
#         for iLine in getCoords['Lsole']:
#             fig['data'].append({'x': iLine[::2], 'y': iLine[1::2], 'mode': 'lines', 'opacity': op,'fill':'toself','fillcolor' :af.colorOrder[4],'line':dict(color=af.colorOrder[4]),'hoverinfo': 'none'})
#     return fig
#
#
# @app.callback(
#     Output('Rsole_RF', 'figure'),
#     [Input('refreshButton', 'n_clicks'),
#      Input('sortDropdown1', 'value'),
#      Input('sortDropdown2', 'value')],
#      [State('Rsole_RF', 'figure')])
# def drawRsole(n,v1,v2, fig):
#     getCoords = af.getPixelCoords(v1,v2, 'Rsole')
#     fig['data'] = []
#     if getCoords:
#         # fig['data'] = [go.Heatmap(z= getCoords['Rsole'],showscale=False,zmin = 1)]
#         op = 1/float(len(getCoords['Rsole']))
#         if op < 0.005:
#             op = 0.005
#         for iLine in getCoords['Rsole']:
#             fig['data'].append({'x': iLine[::2], 'y': iLine[1::2], 'mode': 'lines', 'opacity': op,'fill':'toself','fillcolor' :af.colorOrder[5],'line':dict(color=af.colorOrder[5]),'hoverinfo': 'none'})
#     return fig
#
#
#
@app.callback(
    Output('sortDropdown2', 'options'),
    [Input('sortDropdown1', 'value')])
def dropdown1_callback(value):
    modelNames = []
    if value:
        af.getDataset(value)
        modelNames = af.getModelsNames()

        return modelNames

@app.callback(
    Output('sortDropdown2', 'value'),
    [Input('sortDropdown1', 'value')])
def dropdown1_callback(value):
    modelNames = []
    if value:
        af.getDataset(value)
        modelNames = af.getModelsNames()
    return modelNames[0]['value']

# @app.callback(
#     Output('sortDropdown3', 'options'),
#     [Input('sortDropdown1', 'value'), Input('sortDropdown2', 'value')])
# def dropdown1_callback(dataset, model):
#     modelNames = []
#     if model:
#         tmp = af.getModelsInfo()
#
#         return tmp
#
# @app.callback(
#     Output('sortDropdown3', 'value'),
#     [Input('sortDropdown1', 'value'), Input('sortDropdown2', 'value')])
# def dropdown1_callback(dataset, model):
#     if model:
#         tmp = af.getModelsInfo()
#         return tmp