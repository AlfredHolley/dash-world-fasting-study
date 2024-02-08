from dash import Input, Output, State, callback_context as ctx, ClientsideFunction, Patch
from dash.exceptions import PreventUpdate
import dash
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import dash_echarts
np.random.seed(0)  # no-display
import plotly.io as pio
import time
pio.templates.default = "plotly_white"


df_raw = pd.read_parquet('data/merged_data_wide.parquet')
correlation_matrix = pd.read_excel("data/correlation_matrix.xlsx", index_col=0)
df = df_raw.reset_index(drop = True).set_index("id").copy()
df0 =df.query("timepoint.eq(0)").copy()
df1 =df.query("timepoint.eq(1)").copy()
list_param_correlation = list(correlation_matrix.index)

def update_sex_pie(selected_ids):

    if not selected_ids : 
        n_males = 581
        n_females = 841
    else :                                   # its important to have else here because the dataframe is not in layout.py
        df_filtered = df0.loc[selected_ids]
        n_males = df_filtered[df_filtered.sex == "M"].shape[0]
        n_females = df_filtered[df_filtered.sex == "F"].shape[0]

    option = {
        "title": {
            "text": None,
        },
        "tooltip": {
            "trigger": 'item'
        },
        "series": [
            {
                "labelLine": {"show": False},
                "type": 'pie',
                "selectedMode": 'single',
                "selectedOffset": 6,  #     cette valeur selon vos besoins
                "select": {"itemStyle": {"color": 'red', "opacity": 0.5}},
                "radius": '80%',
                "data": [
                    { "value": n_males, "name": 'M'},
                    { "value": n_females, "name": 'F'},
                ],
                "color": ["#465FFF", "#FFBFF6"],
                "bottom":0,
                "top":0,
                "legend": False,
                "label":{"position":"inner", "formatter": "{b} : {c}", "fontSize": 13, "fontWeight": "bold"},
                "emphasis": {
                    "itemStyle": {
                        "color": 'red',
                        "opacity": 0.5,
                    }
                }
            }
        ],
    }
    
    return option

def update_scatter(parameterY, parameter, selected_id, selectedpoints_local):
    selectedpoint = []
    if selected_id : 
        selectedpoint = [s_id - 1 for s_id in selected_id]
    if parameterY is None:
        y = "weight (kg) change"
        if parameter == 'baseline of the parameter':
            x = y[:-7]
        else : 
            x = parameter
    elif parameterY == 'baseline of the parameter':
        x = parameter
        y = x[:-7]
    else : 
        y = parameterY
        if parameter == 'baseline of the parameter': 
            x = y[:-7]
        else :
            x = parameter

    fig = px.scatter(df0, x=x, y=y, trendline="ols")
    fig.data[0]["name"] = "points"

    fig.update_traces(
        selector=dict(name = "points"),
        selectedpoints=selectedpoint,
        selected={"marker": {"opacity": 0.8,"color" : "red"}},
        unselected={"marker": {"opacity": 0.5, "color" : "blue"}},
    )

    fig.update_layout(
        modebar_activecolor="rgb(0,0,0)" if len(selectedpoint) < 1 else "rgb(255,0,0)",
        margin={"l": 0, "r": 20, "b": 0, "t": 45},
        dragmode="lasso",
        newselection_mode="gradual",
        plot_bgcolor='rgba(245,245,247,1)',
    )
    fig.update_xaxes(fixedrange=True, title= None)
    fig.update_yaxes(fixedrange=True, gridcolor='rgba(0,0,0,0.065)', ticklabelposition="inside top", title=None)

    if selectedpoints_local : #avoid bug to have these double check if conditions (not if _ and _)
        if selectedpoints_local["lassoPoints"]:
            lasso_points = selectedpoints_local["lassoPoints"]
            x_points = lasso_points['x']
            y_points = lasso_points['y']
            lasso_shape = {
                "type": "path",
                "path": 'M' + ' L'.join(f'{x},{y}' for x, y in zip(x_points, y_points)) + ' Z',
                "line": {"width": 2, "dash": "dot", "color": "darkgrey"}
            }
            fig.add_shape(lasso_shape)

    return {"data": fig.data, "layout": fig.layout}


def update_boxplot(selected_y, selected_id, selectedpoints_local, display_selected_box, diff = False):
    selected_id = selected_id if selected_id else []
    selectedpoints = []
    if selected_id: 
        df0["is_selected"] = df0.index.isin(selected_id)
        df["is_selected"] = df.index.isin(selected_id)
        selectedpoints = [id - 1 for id in selected_id]


    if diff == False:
        fig = go.Figure(
                go.Scatter(
                    x=df0["jittered_x"],
                    y=df0[selected_y],
                    showlegend=False,
                    marker=dict(color='blue', size = 5, opacity=0.65),
                    text=df0.index,
                ))

        fig.add_trace(
            go.Scatter(
                showlegend = False,
                x=df1["jittered_x"],
                y=df1[selected_y],
                marker=dict(color='blue',size = 5, opacity=0.65),
                text = df1.index
        ))
        fig.add_trace(
            go.Box(
                x = df["timepoint"],
                y = df[selected_y],
                showlegend = False,
                boxpoints  = False,
                line = dict(color= "rgba(135, 160, 250, 0.9)"),  
                fillcolor = 'rgba(135, 160, 250, 0.3)',  
        ))
        if selected_id and display_selected_box: 
            fig_selected = go.Figure(
                    go.Box(
                        x=df.query("is_selected == False")["timepoint"],
                        y=df.query("is_selected == False")[selected_y],
                        pointpos = 0,
                        boxpoints = "all",
                        marker=dict(color='blue', size = 5, opacity=0.65),
                        showlegend=False,
                    ))
            fig_selected.add_trace(
                go.Box(
                    x=df.query("is_selected")["timepoint"],
                    y=df.query("is_selected")[selected_y],
                    marker=dict(color='red',size = 5, opacity=0.7),
                    marker_color = 'rgba(255, 0, 0, 0.30)',
                    line_color='rgba(255,0,0,0.6)',
                    fillcolor='rgba(255,0,0,0.30)',
                    pointpos = 0,
                    showlegend = False,
                    boxpoints = "all",
                    # name = "selected"
            ))
            fig_selected.update_xaxes(
                tickvals=[0,1],  # List of positions where ticks should be displayed
                ticktext=["pre", "post"]   # List of labels corresponding to each tick position
            )

            fig_selected.update_layout(
                modebar_remove= ["select", "select2d"], 
                xaxis_title='points are not selectable',
                margin = {"l": 10, "r": 10, "b": 0, "t": 25},
                boxmode='group', # group together boxes of the different traces for each value of x
                plot_bgcolor='rgba(245,245,247,1)',

            )
            fig_selected.update_xaxes(fixedrange=True)
            fig_selected.update_yaxes(fixedrange=True, gridcolor='rgba(0,0,0,0.065)')

    else : 
        selected_y = selected_y + " change"
        fig = go.Figure(
                go.Scatter(
                    x=df0["jittered_x"],
                    y=df0[selected_y],
                    showlegend=False,
                    marker=dict(color='blue', size = 5, opacity=0.65),
                    text=df0.index,
                ))
        fig.add_trace(
            go.Box(
                y = df0[selected_y],
                showlegend = False,
                boxpoints  = False,
                line = dict(color= "rgba(135, 160, 250, 0.9)"),  
                fillcolor = 'rgba(135, 160, 250, 0.3)',  
        ))
        if selected_id : 
            fig_selected = go.Figure()
            fig_selected.add_trace(
                go.Box(
                    y=df0[df0['is_selected'] == False][selected_y],
                    name="Not Selected",
                    marker=dict(color='blue', size=5, opacity=0.50),
                    boxpoints="all",  # Display all points
                    pointpos=0,
                    showlegend=False,
                ))
            # Add the box for 'selected'
            fig_selected.add_trace(
                go.Box(
                    y=df0[df0['is_selected'] == True][selected_y],
                    name="Selected",
                    marker=dict(color='red', size=5, opacity=0.50),
                    boxpoints="all",  # Display all points
                    pointpos=0,
                    showlegend=False,
                ))
            fig_selected.update_traces(
                selector=dict(type='scatter'),
                selectedpoints=selectedpoints,
                mode="markers",
            )
            fig_selected.update_layout(
                modebar_remove= ["select", "select2d"], 
                plot_bgcolor='rgba(245,245,247,1)',
                xaxis_title='points are not selectable',
                margin = {"l": 10, "r": 10, "b": 30, "t": 25},
                
            )
            fig_selected.update_xaxes(fixedrange=True)
            fig_selected.update_yaxes(fixedrange=True, gridcolor='rgba(0,0,0,0.065)')
    fig.update_traces(
        selector=dict(type='scatter'),
        selectedpoints=selectedpoints,
        mode="markers",
        selected={"marker": {"opacity": 0.8,"color" : "red"}},
        unselected={"marker": {"opacity": 0.35, "color" : "blue"}},
    )
    fig.update_layout(
        margin={"l": 30, "r": 20, "b": 0, "t": 15},
        dragmode="select",
        modebar_activecolor="rgb(0,0,0)" if len(selected_id) < 1 else "rgb(255,0,0)",
        newselection_mode="gradual",
        xaxis_range = [-0.5, 1.5] if diff == False else [-0.5, 0.5],
        yaxis_range = [min(df[selected_y]) - (max(df[selected_y])/10), max(df[selected_y]) + (max(df[selected_y])/10)],
        plot_bgcolor='rgba(245,245,247,1)',
    )
    fig.update_xaxes(
        fixedrange=True,
        tickvals= [0,1] if diff == False else [0],  # List of positions where ticks should be displayed
        ticktext=["pre", "post"]  if diff == False else ["change"],  # List of labels corresponding to each tick position
    )
    fig.update_yaxes(fixedrange=True, gridcolor='rgba(0,0,0,0.065)')

    if selectedpoints_local : #avoid bug to have these double check if conditions (not if _ and _)
        if selectedpoints_local["range"]:
            ranges = selectedpoints_local["range"]
            selection_bounds = {
                "x0": ranges["x"][0],
                "x1": ranges["x"][1],
                "y0": ranges["y"][0],
                "y1": ranges["y"][1],
            }
            fig.add_shape(
                dict(
                    {"type": "rect", "line": {"width": 2, "dash": "dot", "color": "darkgrey"}},
                    **selection_bounds
                ))
    if display_selected_box == True and selected_id: 
        return {"data": fig_selected.data, "layout": fig_selected.layout}
    else :
        return  {"data": fig.data, "layout": fig.layout}

def register_callbacks(app):
    @app.callback(
        Output('study-characteristics', 'children'),
        Input('store-selected-data', 'data'),
    )
    def update_study_characteristics(selected_data):
        if not selected_data :
            return f"1422 subjects"
        elif len(selected_data) == 0:
            return f"1422 subjects"
        n = len(selected_data)
        return f"{n}/1422 selected"
    
    @app.callback(
        Output(f"graph-1", "figure", allow_duplicate=True),
        Output(f"graph-2", "figure", allow_duplicate=True),
        Output("sex-pie-chart", "option"),
        Output("store-selected-data", "data", allow_duplicate=True),
        Input(f"graph-1", "selectedData"),
        Input(f"graph-2", "selectedData"),
        State(f"parameter-dropdown-1", "value"),
        State(f"switch-selected-1", "checked"),
        State(f"switch-1", "checked"),
        State("dropdown-heatmap-Y", "value"),
        State("dropdown-heatmap-X", "value"),
        State("store-selected-data", "data"),
        prevent_initial_call=True
    )
    def callback_on_selection(select_1, select_2, parameter, switch_box_1, switch_box_2, parameterY, dropdown_scatter, current_data):
        if not current_data :
            current_data = []
        number_id = ctx.triggered_id[-1]

        selected_data  = [select_1, select_2]	
        selection_of_trigger =  selected_data[int(number_id)-1]
        if selection_of_trigger and selection_of_trigger["points"]:
            selected_id = [p["pointIndex"] + 1 for p in selection_of_trigger["points"]]

        else :
            selected_id = [] 
        boxes   = update_boxplot(
                    parameter, selected_id,
                    selected_data[0] if number_id == "1" else None, 
                    switch_box_1, switch_box_2)
        scatter = update_scatter(
                    parameterY, dropdown_scatter, selected_id,
                    selected_data[1] if number_id == "2" else None,
            )
        pie_chart = update_sex_pie(selected_id)
            
        return boxes, scatter, pie_chart, selected_id
    
    @app.callback(
        Output("graph-1", "figure"),
        Input("parameter-dropdown-1", "value"),
        Input(f"switch-selected-1", "checked"),
        Input(f"switch-1", "checked"),
        State("store-selected-data", "data"),
    )
    def callback_parameter_box(parameter, switch_1, switch_2, selected_ids):
        if not selected_ids : 
            selected_ids = []
        return update_boxplot(parameter, selected_ids, None, switch_1, switch_2)

    @app.callback(
        Output("graph-1", "figure", allow_duplicate=True),
        Output("graph-2", "figure", allow_duplicate=True),
        Output('sex-pie-chart', 'option', allow_duplicate=True),
        Output("store-selected-data", "data"),
        Output("slider-age", "value"),
        Output("slider-fast", "value"),
        Output("sex-pie-chart", "reset_id"),
        Input("graph-1", "selectedData"),
        Input("graph-2", "selectedData"),
        Input("slider-age", "value"),
        Input("slider-fast", "value"),
        Input("sex-pie-chart", "selected_data"),
        State("switch-selected-1", "checked"),
        State("switch-1", "checked"),
        State("parameter-dropdown-1", "value"),
        State("sex-pie-chart", "reset_id"),
        prevent_initial_call=True
    )
    def update_age(rect, lasso, age, fast, sex, switch_box_1, switch_box_2, selected_param, reset_id_echarts):
      if "graph" in ctx.triggered_id :
          return dash.no_update, dash.no_update, dash.no_update, dash.no_update, [18,100], [3,23], 1
      
      elif "age" in ctx.triggered_id :
        trigger_var = 0
        selected_id = list(set(df0[df0["age (years)"].between(age[0], age[1])].index))
        reset_id_echarts = 1

      elif "fast" in ctx.triggered_id :
        trigger_var = 1
        selected_id = list(set(df0[df0["fasting duration (days)"].between(fast[0], fast[1])].index))
        reset_id_echarts = 1

      elif "pie" in ctx.triggered_id :
        if len(sex["selected"]) == 0:
            selected_id = []
        else : 
            sex_catched = "M" if sex["selected"][0]["dataIndex"][0] == 0 else "F"
            selected_id = list(set(df0[df0["sex"] == sex_catched].index))
        trigger_var = 2

      selected_id_index = [id - 1 for id in selected_id]

      if len(selected_id) == 1422:
          selected_id = []  
          selected_id_index = []  

      fig_scatter_patched = Patch()
      fig_scatter_patched["data"][0].selectedpoints = selected_id_index      
      fig_scatter_patched.layout.shapes = None


      fig_box_patched = Patch()
      fig_box_patched['data'] = update_boxplot(selected_param, selected_id, None,  switch_box_1, switch_box_2)["data"]
      fig_box_patched.layout.shapes = None
      callback_var = [[dash.no_update,[3,23], 1], [[18,100],dash.no_update, 1], [[18,100],[3,23], 0 if reset_id_echarts != 0 else dash.no_update]]

      return  (fig_box_patched, 
               fig_scatter_patched, 
               update_sex_pie(selected_id) if trigger_var != 2 else update_sex_pie([]),
               selected_id, 
               callback_var[trigger_var][0], 
               callback_var[trigger_var][1], 
               callback_var[trigger_var][2])
      

    @app.callback(
        Output("graph-2", "figure"),
        Input("dropdown-heatmap-Y", "value"),
        Input("dropdown-heatmap-X", "value"),
        State("store-selected-data", "data"),
    )
    def callback_parameter_scatter(parameterY, parameter, selected_ids):
        if not selected_ids : 
            selected_ids = []
        if ctx.triggered_id is None:
            return update_scatter(parameterY, parameter, selected_ids, None)
        else :
            fig_patched = Patch()
            fig_patched["data"] = update_scatter(parameterY, parameter, selected_ids, None)["data"]
            fig_patched.layout.shapes = None

            return fig_patched

    # @app.callback(
    #     Output('sex-pie-chart', 'option'),
    #     Input('store-selected-data', 'data'), 
    #     )
    # def update_sex_option(selected_ids, ts, selected):
    #     if selected : 
    #         print(selected["selected"][0]["dataIndex"][0])

    #     if not selected_ids : 
    #         selected_ids = df0.index

    #     df_filtered = df0.loc[selected_ids]
    #     n_males = df_filtered[df_filtered.sex == "M"].shape[0]
    #     n_females = df_filtered[df_filtered.sex == "F"].shape[0]
    #     option = {
    #         "title": {
    #             "text": None,
    #         },
    #         "tooltip": {
    #             "trigger": 'item'
    #         },
    #         "series": [
    #             {
    #                 "labelLine": {"show": False},
    #                 "type": 'pie',
    #                 "selectedMode": 'single',
    #                 "selectedOffset": 6,  #     cette valeur selon vos besoins
    #                 "select": {"itemStyle": {"color": 'red', "opacity": 0.5}},
    #                 "radius": '80%',
    #                 "data": [
    #                     { "value": n_males, "name": 'M'},
    #                     { "value": n_females, "name": 'F'},
    #                 ],
    #                 "color": ["#465FFF", "#FFBFF6"],
    #                 "bottom":0,
    #                 "top":0,
    #                 "legend": False,
    #                 "label":{"position":"inner", "formatter": "{b} : {c}", "fontSize": 13, "fontWeight": "bold"},
    #                 "emphasis": {
    #                     "itemStyle": {
    #                         "color": 'red',
    #                         "opacity": 0.5,
    #                     }
    #                 }
    #             }
    #         ],
    #     }
        
    #     return option

    @app.callback(
        Output('age-text', 'children'),
        Output('length-fast-text', 'children'),
        Input('store-selected-data', 'data'),
    )
    def update_age(selected_ids):
        if not selected_ids or selected_ids == []: 
            selected_ids = df0.index
            text_age = f"{df0['age (years)'].mean():.1f} years"
            text_length_fast = f"{df0['fasting duration (days)'].mean():.1f} days"	
        else :
            df_filtered = df0.loc[selected_ids]
            text_age = f"{df_filtered['age (years)'].mean():.1f} days"
            text_length_fast = f"{df_filtered['fasting duration (days)'].mean():.1f} days"	
        
        return text_age, text_length_fast


    app.clientside_callback(
        """
        function(param, data) {
            childrens = window.dash_clientside.clientside.div_creator(param, data);
            return childrens;
        }
        """,
        [Output(f'X-menu-div-{i+1}', 'children') for i in range(0, 44)],
        [Output(f'X-menu-div-{i+1}', 'style') for i in range(0, 44)],
        Input('dropdown-heatmap-Y', 'value'),
        State('data-store', 'data'),
    )


    app.clientside_callback(
        """
        function(param, data) {
            childrens = window.dash_clientside.clientside.div_creator(param, data);
            return childrens;
        }
        """,
        [Output(f'Y-menu-div-{i+1}', 'children') for i in range(0, 44)],
        [Output(f'Y-menu-div-{i+1}', 'style') for i in range(0, 44)],
        Input('dropdown-heatmap-X', 'value'),
        State('data-store', 'data'),
    )


    app.clientside_callback(
        """
        function(...timestamps) {
            const dropdown = 'X'
            var content = window.dash_clientside.clientside.update_dropvalue(dropdown, ...timestamps);
            return content;
        }
        """,
        Output('dropdown-heatmap-X', 'value'),
        [Input(f'X-menu-div-{i+1}', 'n_clicks_timestamp') for i in range(0, 44)],
        prevent_initial_call=True
    )

    app.clientside_callback(
        """
        function(...timestamps) {
            const dropdown = 'Y'
            var content = window.dash_clientside.clientside.update_dropvalue(dropdown, ...timestamps);
            return content;
        }
        """,
        Output('dropdown-heatmap-Y', 'value'),
        [Input(f'Y-menu-div-{i+1}', 'n_clicks_timestamp') for i in range(0, 44)],
        prevent_initial_call=True
    )

    app.clientside_callback(
        """
        function() {

            if (dash_clientside.callback_context.triggered[0]) {
                triggered = dash_clientside.callback_context.triggered[0];
                const ctx = triggered.prop_id;

                const output_id = ctx.split('.')[0].slice(-1) + '-heatmap-div';
                var divElement = document.getElementById(output_id);

                if (divElement.style.display === 'block') {
                    divElement.style.display = 'none';
                } else if (divElement.style.display === 'none') {
                    divElement.style.display = 'block';
                } else {
                    divElement.style.display = 'block';
                }
            }
            return {};
        }        
        """,
        Output('X-heatmap-div', 'style'),
        Output('Y-heatmap-div', 'style'),
        Input('updiv-X', 'n_clicks_timestamp'),
        Input('updiv-Y', 'n_clicks_timestamp'),
    )
    app.clientside_callback(
        """
        function() {

            if (dash_clientside.callback_context.triggered[0]) {
                triggered = dash_clientside.callback_context.triggered[0];

                const ctx = triggered.prop_id;
                const output_id = ctx.split('.')[0]
                var divElement = document.getElementById(output_id);
                divElement.style.display = 'none';
            return {};
            }
        }
        """,
        Output('X-heatmap-div', 'style', allow_duplicate=True),
        Output('Y-heatmap-div', 'style', allow_duplicate=True),
        Input('X-heatmap-div', 'n_clicks_timestamp'),
        Input('Y-heatmap-div', 'n_clicks_timestamp'),
        prevent_initial_call=True
    )
