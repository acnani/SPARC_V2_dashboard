import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
from aggregateHelper import app
import aggregateHelper as af
from dash.dependencies import Input, Output
import base64
from apps import RFlogger#, NoteDash, PsychoPhysics
import os

app.layout = html.Div(
    [
        html.Div(
            [
                html.Span(u'SPARC-V\u00b2 Dashboard', className='app-title'),
                html.Div(
                    # html.Img(
                        # src='data:image/png;base64,{}'.format(base64.b64encode(open("R:\users\\amn69\Projects\mdf\SPARC_hackathon\Images\RNEL_logo.png",'rb').read())),height="100%")
                    # ,style={"float": "right", "height": "70%",}
                )
            ],
            className="row header"
        ),

        # tabs
        html.Div([
            dcc.Tabs(
                id="tabs",
                parent_className='custom_tabs',
                className='custom-tabs-container',
                style={"height":"20","verticalAlign":"middle",'alignItems':'center',},
                children=[
                        dcc.Tab(label='Model-Graph Viewer', value='graphView_tab',className='custom-tab',selected_className='custom-tab--selected'),
                        dcc.Tab(label='Metadata browser', value='noteApp_tab',className='custom-tab',selected_className='custom-tab--selected'),
                ],
                value='graphView_tab'
            ),
        ],
        className="row tabs_div"
        ),

        # hidden table. this is temporary till the datatable is becomes a core component
        html.Div(dt.DataTable(rows=[{}]), style={'display': 'none'}),
        # divs that save dataframe for each tab
        # html.Div(
        #     sf_manager.get_opportunities().to_json(orient="split"),  # opportunities df
        #     id="RFlogger_df",
        #     style={"display": "none"},
        # ),
        # html.Div(sf_manager.get_leads().to_json(orient="split"), id="pSpace_df", style={"display": "none"}),  # leads df
        # html.Div(sf_manager.get_cases().to_json(orient="split"), id="trialCount_df", style={"display": "none"}),  # cases df



        # Tab content
        html.Div(id="tab_content", className="row", style={"margin": "2% 3%"},),
        html.Link(href="https://use.fontawesome.com/releases/v5.2.0/css/all.css", rel="stylesheet"),
        html.Link(href="https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css",rel="stylesheet"),
        html.Link(href="https://fonts.googleapis.com/css?family=Dosis", rel="stylesheet"),
        html.Link(href="https://fonts.googleapis.com/css?family=Open+Sans", rel="stylesheet"),
        html.Link(href="https://fonts.googleapis.com/css?family=Ubuntu", rel="stylesheet"),
        html.Link(href="https://cdn.rawgit.com/amadoukane96/8a8cfdac5d2cecad866952c52a70a50e/raw/cd5a9bf0b30856f4fc7e3812162c74bfc0ebe011/dash_crm.css",rel="stylesheet")

    ],
)

@app.callback(Output("tab_content", "children"), [Input("tabs", "value")])
def render_content(tab):
    if tab == "RFlogger_tab":
        return RFlogger.layout
    # elif tab == "noteApp_tab":
    #     return NoteDash.layout
    # elif tab == "psycho_tab":
    #     return PsychoPhysics.layout
    else:
        return RFlogger.layout



if __name__ == '__main__':
    # app.run_server(debug=False, port=8050,host='0.0.0.0')
    app.run_server(debug=True)