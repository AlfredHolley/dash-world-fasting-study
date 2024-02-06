from dash import Input, Output, State, callback_context as ctx, ClientsideFunction, html
from dash.exceptions import PreventUpdate
import dash
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

np.random.seed(0)  # no-display
import plotly.io as pio
pio.templates.default = "plotly_white"


df_raw = pd.read_parquet('data/merged_data_wide.parquet')
correlation_matrix = pd.read_excel("data/correlation_matrix.xlsx", index_col=0)
df = df_raw.reset_index(drop = True).set_index("id").copy()
df0 =df.query("timepoint.eq(0)").copy()
df1 =df.query("timepoint.eq(1)").copy()
list_param_correlation = list(correlation_matrix.index)

def update_scatter(clickData, parameter, selected_id, selectedpoints_local):
    selectedpoint = []
    if selected_id : 
        selectedpoint = [s_id - 1 for s_id in selected_id]
    if clickData is None:
        y = "weight (kg) change"
        if parameter == 'baseline of the parameter':
            x = y[:-7]
        else : 
            x = parameter
    elif clickData.get('points')[0].get('y') == 'baseline of the parameter':
        x = parameter
        y = x[:-7]
    else : 
        y = clickData.get('points')[0].get('y')
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

    if selectedpoints_local and selectedpoints_local["lassoPoints"]:
            lasso_points = selectedpoints_local["lassoPoints"]
            x_points = lasso_points['x']
            y_points = lasso_points['y']
            lasso_shape = {
                "type": "path",
                "path": 'M' + ' L'.join(f'{x},{y}' for x, y in zip(x_points, y_points)) + ' Z',
                "line": {"width": 2, "dash": "dot", "color": "darkgrey"}
            }
            fig.add_shape(lasso_shape)

    return fig


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

    if selectedpoints_local and selectedpoints_local["range"]:
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
        return fig_selected
    else :
        return fig

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
        Output("store-selected-data", "data",allow_duplicate=True),
        Input(f"graph-1", "selectedData"),
        Input(f"graph-2", "selectedData"),
        State(f"parameter-dropdown-1", "value"),
        State(f"switch-selected-1", "checked"),
        State(f"switch-1", "checked"),
        State("heatmap-graph-X", "clickData"),
        State("dropdown-heatmap-X", "value"),
        State("store-selected-data", "data"),
        prevent_initial_call=True
    )
    def callback_on_selection(select_1, select_2, parameter, switch_box_1, switch_box_2, click_heatmap, dropdown_scatter, current_data):
        if not current_data :
            current_data = []
        number_id = ctx.triggered_id[-1]

        selected_data  = [select_1, select_2]	
        selection_of_trigger =  selected_data[int(number_id)-1]
        if selection_of_trigger and selection_of_trigger["points"]:
            selected_id = [p["pointIndex"] + 1 for p in selection_of_trigger["points"]]
        else :
            selected_id = [] 

        boxes = [
            update_boxplot(
                parameter, selected_id,
                selected_data[0] if number_id == "1" else None, 
                switch_box_1, switch_box_2)]
        scatter = [
            update_scatter(
                click_heatmap, dropdown_scatter, selected_id,
                selected_data[1] if number_id == "2" else None,
            )]
            
        return boxes + scatter + [selected_id]

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
        Output('sex-pie-chart', 'figure'),
        Input('store-selected-data', 'data'),
        )
    def update_sex(selected_ids):
        if not selected_ids : 
            selected_ids = df0.index

        df_filtered = df0.loc[selected_ids]
        counts_sex = df_filtered.sex.value_counts().sort_index(ascending=False)
        fig = px.pie(values=counts_sex.values, names=counts_sex.index)
        fig.update_traces(
            textposition='inside', textfont_size=15, textinfo='percent+label',sort=False,
            showlegend=False, textfont_color="white", texttemplate="%{label}<br>%{percent:.0%}"
            )
        fig.update_layout(
            margin={"l": 0, "r": 0, "b": 0, "t": 15}
            )
        return fig 

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
            text_age = f"{df_filtered['age (years)'].mean():.1f}"
            text_length_fast = f"{df_filtered['fasting duration (days)'].mean():.1f} days"	
        
        return text_age, text_length_fast


    @app.callback(
        Output("data-store", "data"),
        Input("dropdown-heatmap-X", "value"),
        Input("dropdown-heatmap-Y", "value"),
        State("data-store", "data"),
    )
    def update_heatmap_data( param_x, param_y, data):
        matrix = data["matrix"]
        if ctx.triggered_id == "dropdown-heatmap-X":
            dataY = {key: round(float(value),2) for key, value in matrix[0].get(f"{param_x}").items() if not str(value) =="None"}
            dataY_sorted = dict(sorted(dataY.items(), key=lambda item: abs(item[1]), reverse=True))
            data["Y"] = dataY_sorted
            return data
        elif ctx.triggered_id == "dropdown-heatmap-Y":
            dataX = {key: round(float(value),2) for key, value in matrix[0].get(f"{param_y}").items() if not str(value) =="None"}
            dataX_sorted = dict(sorted(dataX.items(), key=lambda item: abs(item[1]), reverse=True))
            data["X"] = dataX_sorted
            return data
        else : 
            dataY = {key: round(float(value),2) for key, value in matrix[0].get(f"{param_x}").items() if not str(value) =="None"}
            dataY_sorted = dict(sorted(dataY.items(), key=lambda item: abs(item[1]), reverse=True))
            data["Y"] = dataY_sorted
            dataX = {key: round(float(value),2) for key, value in matrix[0].get(f"{param_y}").items() if not str(value) =="None"}
            dataX_sorted = dict(sorted(dataX.items(), key=lambda item: abs(item[1]), reverse=True))
            data["X"] = dataX_sorted

            return data
    @app.callback(
            Output('dropdown-heatmap-X', 'value'),
            [Input(f'X-menu-div-{i}', 'n_clicks_timestamp') for i in range(1, 42)],
            State("data-store", "data"),
    )
    def update_Xvalue(*args):
        data = args[-1]
        if not ctx.triggered_id :
            raise PreventUpdate
        id_menu = ctx.triggered_id[-2:]
        try: 
            id_menu = abs(int(id_menu))
        except:
            id_menu = int(id_menu[1])
        new_param = list(data["X"].keys())[id_menu-1]
        return new_param
    
    @app.callback(
        Output('heatmap-graph-X', 'children'),
        Input('dropdown-heatmap-Y', 'value'),        
        Input('data-store', 'data'),
    )
    def update_output_div(param, data):
        def get_background_color(value):
            # Map the absolute value to a color intensity between 0 (white) and 255 (red)
            intensity = int(255 * abs(value))
            return f'rgba(0, 0,255, {intensity/400})'
        print(data["matrix"][0].get(f"{param}"))
        filtered_data_dict = {key: round(float(value),2) for key, value in data["matrix"][0].get(f"{param}").items() if not str(value) =="None"}
        sorted_data_dict = dict(sorted(filtered_data_dict.items(), key=lambda item: abs(item[1]), reverse=True))

        children = [
            html.Div(
                html.P(f'{content[0]} : {content[1]}'),
                id=f'X-menu-div-{i+1}',
                className='div-menu',
                style={'background-color': get_background_color(content[1])}
            )
            for i, content in enumerate(sorted_data_dict.items())
        ]
        return children

    @app.callback(
        Output('heatmap-graph-Y', 'children'),
        Input('dropdown-heatmap-X', 'value'),        
        Input('data-store', 'data'),
    )
    def update_output_div(param, data):
        def get_background_color(value):
            # Map the absolute value to a color intensity between 0 (white) and 255 (red)
            intensity = int(255 * abs(value))
            return f'rgba(0, 0,255, {intensity/400})'
        print(data["matrix"][0].get(f"{param}"))
        filtered_data_dict = {key: round(float(value),2) for key, value in data["matrix"][0].get(f"{param}").items() if not str(value) =="None"}
        sorted_data_dict = dict(sorted(filtered_data_dict.items(), key=lambda item: abs(item[1]), reverse=True))

        children = [
            html.Div(
                html.P(f'{content[0]} : {content[1]}'),
                id=f'Y-menu-div-{i+1}',
                className='div-menu',
                style={'background-color': get_background_color(content[1])}
            )
            for i, content in enumerate(sorted_data_dict.items())
        ]
        return children

    app.clientside_callback(
        """
        function(n_clicks_1) {
            updateDivDisplay(n_clicks_1);
            return {};
        }
        """,
        Output('X-heatmap-div', 'style', allow_duplicate=True),
        Input('dropX-div', 'n_clicks'),
        prevent_initial_call=True   
    )
    app.clientside_callback(
        """
        function(n_clicks_2) {
            updateDivDisplay_2(n_clicks_2);
            return {};
        }
        """,
        Output('X-heatmap-div', 'style'),
        Input('X-heatmap-div', 'n_clicks_timestamp'),
    )

    # app.clientside_callback(
    #     """
    #     function(contentId,...timestamps, heatmapDivDisplay) {
    #         timestamps = timestamps.map(timestamp => timestamp || 0);
    #         var highestTimestamp = Math.max(...timestamps);
    #         var clicked_id = null;

    #         for (var i = 1; i <= timestamps.length; i++) {
    #             if (timestamps[i - 1] === highestTimestamp) {
    #                 clicked_id = 'div-' + i;
    #                 break;
    #             }
    #         }
    #         console.log('Clicked ID:', clicked_id);

    #         if (clicked_id) {
    #             var contentElement = document.getElementById(contentId);
    #             var clickedContent = document.getElementById(clicked_id);
    #             var heatmapDiv = document.getElementById('heatmap-div');

    #             if (heatmapDiv && window.getComputedStyle(heatmapDiv).display === 'none') {
    #                 return 'weight (kg) change';
    #             }

    #             if (contentElement && clickedContent) {
    #                 return clickedContent.textContent.trim();
    #             }
    #         }
    #         return null;
    #     }
    #     """,
    #     Output('dropdown-heatmap-X', 'value'),
    #     Input('dropdown-heatmap-X', 'id'),
    #     [Input(f'menu-div-{i}', 'n_clicks_timestamp') for i in range(1, 42)],
    #     State('heatmap-div', 'style'),

    # )

    @app.callback(
        Output("graph-2", "figure"),
        Input("heatmap-graph-X", "clickData"),
        Input("dropdown-heatmap-X", "value"),
        State("store-selected-data", "data"),
    )
    def callback_parameter_scatter(clickData, parameter, selected_ids):
        if not selected_ids : 
            selected_ids = []
        return update_scatter(clickData, parameter, selected_ids, None)

    # @app.callback(
    #     Output("visualMap-id", "option"),
    #     Input("dropdown-heatmap-X", "value"),
    # )
    # def load_visualMap(param):
    #     return {
    #         'visualMap': {
    #             'min': -1.0,
    #             'max': 1.0,
    #             "top":0,
    #             "right":0,
    #             'left': 0,
    #             "borderColor" : "#fff111",
    #             'itemWidth':90,
    #             'itemHeight':30, 

    #             'bottom': 0,
    #             'calculable': True,
    #             'orient': 'horizontal',
    #             }
    #         }
    # @app.callback(
    #     Output("store-selected-data", "data"),
    #     Input("slider-age", "value"),
    #     Input("slider-age", "marks"),
    #     State("store-selected-data", "data"),
    # )
    # def callback_update_store(age_slider, length_fasting_slider, current_data):        

# if not ctx.triggered_id :
#     boxes  = [update_boxplot(parameter, None, None, False, False)]
#     scatter = [update_scatter(None, None,  None, None)]
#     return boxes + scatter + [[]]
