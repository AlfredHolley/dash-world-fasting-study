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



    # @app.callback(
    #     Output(f"graph-1", "figure", allow_duplicate=True),
    #     Output(f"graph-2", "figure", allow_duplicate=True),
    #     Output("sex-pie-chart", "option"),
    #     Output("store-selected-data", "data", allow_duplicate=True),
    #     Input(f"graph-1", "selectedData"),
    #     Input(f"graph-2", "selectedData"),
    #     State(f"parameter-dropdown-1", "value"),
    #     State(f"switch-selected-1", "checked"),
    #     State(f"switch-1", "checked"),
    #     State("dropdown-heatmap-Y", "value"),
    #     State("dropdown-heatmap-X", "value"),
    #     prevent_initial_call=True
    # )
    # def callback_on_selection(select_1, select_2, parameter, switch_box_1, switch_box_2, parameterY, dropdown_scatter):
    #     number_id = ctx.triggered_id[-1]

    #     selected_data  = [select_1, select_2]	
    #     selection_of_trigger =  selected_data[int(number_id)-1]
    #     if selection_of_trigger and selection_of_trigger["points"]:
    #         selected_id = [p["pointIndex"] + 1 for p in selection_of_trigger["points"]]

    #     else :
    #         selected_id = [] 
    #     boxes   = update_boxplot(
    #                 parameter, selected_id,
    #                 selected_data[0] if number_id == "1" else None, 
    #                 switch_box_1, switch_box_2)
    #     scatter = update_scatter(
    #                 parameterY, dropdown_scatter, selected_id,
    #                 selected_data[1] if number_id == "2" else None,
    #         )
    #     pie_chart = update_sex_pie(selected_id)
    #     return boxes, scatter, pie_chart, selected_id
    
    # @app.callback(
    #     Output("graph-1", "figure"),
    #     Input("parameter-dropdown-1", "value"),
    #     Input(f"switch-selected-1", "checked"),
    #     Input(f"switch-1", "checked"),
    #     State("store-selected-data", "data"),
    # )
    # def callback_parameter_box(parameter, switch_1, switch_2, selected_ids):
    #     if not selected_ids : 
    #         selected_ids = []
    #     return update_boxplot(parameter, selected_ids, None, switch_1, switch_2)



    # app.clientside_callback(
    #     """
    #     function(data, rect, lasso, age, fast, sex, switch_box_1, switch_box_2, selected_param,scatterY, scatterX,  reset_id_echarts) {
    #         var triggered_id = dash_clientside.callback_context.triggered[0].prop_id.split('.')[0]
    #         console.log(triggered_id)
    #         df0 = data.filter(row => row["timepoint"] === 0);
    #         if (triggered_id.includes("graph")) {
    #             return [window.dash_clientside.no_update, window.dash_clientside.no_update, window.dash_clientside.no_update, window.dash_clientside.no_update, [18, 100], [3, 23], 1];
    #         } else if (triggered_id.includes("age")) {
    #             var trigger_var = 0;
    #             var indices = new Set();

    #             df0.forEach((item, idx) => {
    #                 if (item["age (years)"] >= age[0] && item["age (years)"] <= age[1]) {
    #                     indices.add(idx);
    #                 }
    #             });
    #             var selected_id = Array.from(indices);
    #             var reset_id_echarts = 1;
    #         } else if (triggered_id.includes("fast")) {
    #             var trigger_var = 1;
    #             var indices = new Set();

    #             df0.forEach((item, idx) => {
    #                 if (item["fasting duration (days)"] >= fast[0] && item["fasting duration (days)"] <= fast[1]) {
    #                     indices.add(idx);
    #                 }
    #             });
    #             var selected_id = Array.from(indices);
    #             var reset_id_echarts = 1;
    #         } else if (triggered_id.includes("pie")) {
                
    #             if (sex.selected.length === 0) {
    #                 var selected_id = [];
    #             } else {
    #                 var sex_catched = sex.selected[0].dataIndex[0] === 0 ? "M" : "F";
    #                 var indices = new Set();
    #                 df0.forEach((item, idx) => {
    #                     if (item["sex"] === sex_catched) {
    #                         indices.add(idx);
    #                     }
    #                 });
    #                 var selected_id = Array.from(indices);
                
    #             }
    #             var trigger_var = 2;
    #         }
    #         var selected_id_index = selected_id.map(id => id - 1);
    #         if (selected_id.length === 1422) {
    #             selected_id = [];
    #             selected_id_index = [];
    #         }
    #         var fig_box = window.dash_clientside.clientside.update_boxplot(data, selected_param, selected_id, switch_box_1, switch_box_2);
    #         var fig_scatter = window.dash_clientside.clientside.update_scatter(data, scatterY, scatterX, selected_id);

    #         var callback_var = [
    #             [window.dash_clientside.no_update, [3,23], 1], 
    #             [[18,100], window.dash_clientside.no_update, 1], 
    #             [[18,100], [3,23], reset_id_echarts !== 0 ? 0 : window.dash_clientside.no_update]
    #         ];
    #         var fig_pie = window.dash_clientside.clientside.update_sex_pie(data, trigger_var !== 2 ? selected_id : []);
    #         var response = [
    #             fig_box, 
    #             fig_scatter, 
    #             fig_pie, 
    #             selected_id, 
    #             callback_var[trigger_var][0], 
    #             callback_var[trigger_var][1], 
    #             callback_var[trigger_var][2]
    #         ];

    #         return response;
    #     }
    #     """,
    #     Output("graph-1", "figure", allow_duplicate=True),
    #     Output("graph-2", "figure", allow_duplicate=True),
    #     Output('sex-pie-chart', 'option', allow_duplicate=True),
    #     Output("store-selected-data", "data"),
    #     Output("slider-age", "value"),
    #     Output("slider-fast", "value"),
    #     Output("sex-pie-chart", "reset_id"),
    #     Input("main-store", "data"),
    #     Input("graph-1", "selectedData"),
    #     Input("graph-2", "selectedData"),
    #     Input("slider-age", "value"),
    #     Input("slider-fast", "value"),
    #     Input("sex-pie-chart", "selected_data"),
    #     State("switch-selected-1", "checked"),
    #     State("switch-1", "checked"),
    #     State("parameter-dropdown-1", "value"),
    #     State("dropdown-heatmap-Y", "value"),
    #     State("dropdown-heatmap-X", "value"),

    #     State("sex-pie-chart", "reset_id"),
    #     prevent_initial_call=True
    # )


    # @app.callback(
    #     Output("graph-1", "figure", allow_duplicate=True),
    #     Output("graph-2", "figure", allow_duplicate=True),
    #     Output('sex-pie-chart', 'option', allow_duplicate=True),
    #     Output("store-selected-data", "data"),
    #     Output("slider-age", "value"),
    #     Output("slider-fast", "value"),
    #     Output("sex-pie-chart", "reset_id"),
    #     Input("graph-1", "selectedData"),
    #     Input("graph-2", "selectedData"),
    #     Input("slider-age", "value"),
    #     Input("slider-fast", "value"),
    #     Input("sex-pie-chart", "selected_data"),
    #     State("switch-selected-1", "checked"),
    #     State("switch-1", "checked"),
    #     State("parameter-dropdown-1", "value"),
    #     State("sex-pie-chart", "reset_id"),
    #     prevent_initial_call=True
    # )
    # def update_age(rect, lasso, age, fast, sex, switch_box_1, switch_box_2, selected_param, reset_id_echarts):
    #   if "graph" in ctx.triggered_id :
    #       return dash.no_update, dash.no_update, dash.no_update, dash.no_update, [18,100], [3,23], 1
      
    #   elif "age" in ctx.triggered_id :
    #     trigger_var = 0
    #     selected_id = list(set(df0[df0["age (years)"].between(age[0], age[1])].index))
    #     reset_id_echarts = 1

    #   elif "fast" in ctx.triggered_id :
    #     trigger_var = 1
    #     selected_id = list(set(df0[df0["fasting duration (days)"].between(fast[0], fast[1])].index))
    #     reset_id_echarts = 1

    #   elif "pie" in ctx.triggered_id :
    #     if len(sex["selected"]) == 0:
    #         selected_id = []
    #     else : 
    #         sex_catched = "M" if sex["selected"][0]["dataIndex"][0] == 0 else "F"
    #         selected_id = list(set(df0[df0["sex"] == sex_catched].index))
    #     trigger_var = 2

    #   selected_id_index = [id - 1 for id in selected_id]

    #   if len(selected_id) == 1422:
    #       selected_id = []  
    #       selected_id_index = []  

    #   fig_scatter_patched = Patch()
    #   fig_scatter_patched["data"][0].selectedpoints = selected_id_index      
    #   fig_scatter_patched["data"].remove("trendline_selected")


    #   fig_box_patched = Patch()
    #   fig_box_patched['data'] = update_boxplot(selected_param, selected_id, None,  switch_box_1, switch_box_2)["data"]
    #   fig_box_patched.layout.shapes = None
    #   callback_var = [[dash.no_update,[3,23], 1], [[18,100],dash.no_update, 1], [[18,100],[3,23], 0 if reset_id_echarts != 0 else dash.no_update]]

    #   return  (fig_box_patched, 
    #            fig_scatter_patched, 
    #            update_sex_pie(selected_id) if trigger_var != 2 else update_sex_pie([]),
    #            selected_id, 
    #            callback_var[trigger_var][0], 
    #            callback_var[trigger_var][1], 
    #            callback_var[trigger_var][2])
      





    # @app.callback(
    #     Output("graph-2", "figure"),
    #     Input("dropdown-heatmap-Y", "value"),
    #     Input("dropdown-heatmap-X", "value"),
    #     State("store-selected-data", "data"),
    # )
    # def callback_parameter_scatter(parameterY, parameter, selected_ids):
    #     if not selected_ids : 
    #         selected_ids = []
    #     if ctx.triggered_id is None:
    #         return update_scatter(parameterY, parameter, selected_ids, None)
    #     else :
    #         fig_patched = Patch()
    #         fig_patched["data"] = update_scatter(parameterY, parameter, selected_ids, None)["data"]
    #         fig_patched.layout.shapes = None

    #         return fig_patched
#
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
    Input('graph-1','id')
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
