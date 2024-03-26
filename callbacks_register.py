from dash import Input, Output, State, callback_context as ctx, ClientsideFunction
import dash
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
np.random.seed(0)  # no-display
import plotly.io as pio
pio.templates.default = "plotly_white"

def register_callbacks(app):

## 1. the interaction between the graph and the dropdown/ button/ store of selected points.

    app.clientside_callback(
        """
        function(data, parameter, switch_1, switch_2, selected_ids) {
            if (!selected_ids) {
                selected_ids = [];
            }
            return window.dash_clientside.clientside.update_boxplot(data,parameter, selected_ids,switch_1, switch_2);
        }
        """,
        Output("graph-1", "figure"),
        Input("main-store", "data"),
        Input("parameter-dropdown-1", "value"),
        Input(f"switch-selected-1", "checked"),
        Input(f"switch-1", "checked"),
        State("store-selected-data", "data"),
    )

## 2. interaction of selection function 
    app.clientside_callback(
        ClientsideFunction(
            namespace='clientside',
            function_name='callback_on_selection'
        ),
        Output("graph-1", "figure", allow_duplicate=True),
        Output(f"graph-2", "figure", allow_duplicate=True),
        Output("store-selected-data", "data", allow_duplicate=True),
        Input("graph-1", "selectedData"),
        Input(f"graph-2", "selectedData"),
        State('graph-1', 'figure'),
        State('graph-2', 'figure'),
        State('main-store', 'data'),
        # State("parameter-dropdown-1", "value"),
        # State(f"switch-selected-1", "checked"),
        # State(f"switch-1", "checked"),

        prevent_initial_call=True
    )
#3 update data on change of age, etc.

    app.clientside_callback(
        """
        function(selected_id){
            if (!selected_id || selected_id.length === 0){
                return "1422 subjects"
            } else {
                return selected_id.length.toString() + "/ 1422"
            }
        }
        """,
        Output('study-characteristics', 'children'),
        Input('store-selected-data', 'data'),
    )


    app.clientside_callback(
        ClientsideFunction(
            namespace='clientside',
            function_name='orchestre_callbacks'
        ),
        Output("graph-1", "figure", allow_duplicate=True),
        Output("graph-2", "figure", allow_duplicate=True),
        Output("store-selected-data", "data"),
        Output("slider-age", "value"),
        Output("slider-fast", "value"),
        Input("main-store", "data"),
        Input("graph-1", "selectedData"),
        Input("graph-2", "selectedData"),
        Input("slider-age", "value"),
        Input("slider-fast", "value"),
        Input("test-3", "n_clicks"),
        State("parameter-dropdown-1", "value"),
        State(f"switch-selected-1", "checked"),
        State(f"switch-1", "checked"),
        State("dropdown-heatmap-Y", "value"),
        State("dropdown-heatmap-X", "value"),

        prevent_initial_call=True
    )
# update text info : age, length of fasting...
    app.clientside_callback(
        ClientsideFunction(
            namespace='clientside',
            function_name='update_age'
        ),
        Output('age-text', 'children'), 
        Output('length-fast-text', 'children'),
        Input('store-selected-data', 'data'), 
        Input('main-store', 'data')
)
# Our sex proportion set up
    app.clientside_callback(
        """
        function(data, selected_ids){
            return window.dash_clientside.clientside.update_graph3(data,selected_ids)
        }
        """,
        Output("graph-3", "children"), 
        Input("main-store", "data"),
        Input('store-selected-data', 'data'), 
    )

    app.clientside_callback(
        ClientsideFunction(
            namespace='clientside',
            function_name='update_scatter'
        ),
        Output("graph-2", "figure"),
        Input("main-store", "data"),
        Input("dropdown-heatmap-Y", "value"),
        Input("dropdown-heatmap-X", "value"),
        State("store-selected-data", "data"),
    )


    app.clientside_callback(
        ClientsideFunction(
            namespace='clientside',
            function_name='add_icon'
        ),
    Output('graph-1','config'),
    Output('graph-2','config'),
    Input('graph-1','config'),
    Input('graph-2','id'),
    )

    app.clientside_callback(
        ClientsideFunction(
            namespace='clientside',
            function_name='resetSelectedData'
        ),
        # Output('store-selected-data', 'data', allow_duplicate=True),
        Output('graph-1', 'selectedData', allow_duplicate=True),
        Output('graph-2', 'selectedData', allow_duplicate=True),
        Input('button-reset', 'n_clicks'),
        prevent_initial_call=True
    )

    app.clientside_callback(
        ClientsideFunction(
            namespace='clientside',
            function_name='div_creator'
        ),
        Output('info-div', 'children'),
        Input('dropdown-heatmap-X', 'value'),
        Input('dropdown-heatmap-Y', 'value'),
        Input('data-store', 'data'),
    )
    
    app.clientside_callback(
        ClientsideFunction(
            namespace= "clientside",
            function_name = "update_dropdown_value"
        ),
        Output('dropdown-heatmap-X', 'value'),
        Output('dropdown-heatmap-Y', 'value'),
        [Input(f'X-menu-div-{i+1}', 'n_clicks_timestamp') for i in range(0, 44)],
        [Input(f'Y-menu-div-{i+1}', 'n_clicks_timestamp') for i in range(0, 44)],
        prevent_initial_call = True
    )
##  Copy the  style of a dropdown with arrows
    app.clientside_callback(
        """
        function() {

            if (dash_clientside.callback_context.triggered[0]) {
                triggered = dash_clientside.callback_context.triggered[0];
                const ctx = triggered.prop_id;
                const output_id = ctx.split('.')[0].slice(-1) ;
                var divElement = document.getElementById(output_id  + '-heatmap-div');
                var spanElement = document.getElementById('my-span' + output_id);
                if (output_id === 'X') {
                    var rotate_off = 'rotate(0deg)';
                    var rotate_on = 'rotate(180deg)';
                } else {
                    var rotate_off = 'rotate(-90deg)';
                	var rotate_on = 'rotate(90deg)';
                }
                if (divElement.style.display === 'block') {
                    divElement.style.display = 'none';
                    spanElement.style.transform = rotate_off;
                } else if (divElement.style.display === 'none') {
                    divElement.style.display = 'block';
                    spanElement.style.transform = rotate_on
                } else {
                    divElement.style.display = 'block';
                    spanElement.style.transform = rotate_on
                }
            }
            return window.dash_clientside.no_update;
        }        
        """,
        Output('info-div', 'children', allow_duplicate = True),
        Input('updiv-X', 'n_clicks'),
        Input('updiv-Y', 'n_clicks'),
        prevent_initial_call = True
    )

    ## The Select menu outer personnalized
    app.clientside_callback(
        """
        function() {

            if (dash_clientside.callback_context.triggered[0]) {
                triggered = dash_clientside.callback_context.triggered[0];

                const ctx = triggered.prop_id;
                const output_id = ctx.split('.')[0]
                var divElement = document.getElementById(output_id);
                divElement.style.display = 'none';
            return window.dash_clientside.no_update;
            }
        }
        """,
        Output('info-div', 'children', allow_duplicate = True),
        Input('X-heatmap-div', 'n_clicks_timestamp'),
        Input('Y-heatmap-div', 'n_clicks_timestamp'),
        prevent_initial_call=True
    )
