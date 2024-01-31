from dash import Input, Output, State, callback_context as ctx
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
        margin={"l": 30, "r": 20, "b": 15, "t": 45},
        dragmode="lasso",
        newselection_mode="gradual",
    )
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
                xaxis_title='points are not selectable',
                margin = {"l": 10, "r": 10, "b": 0, "t": 25},
                boxmode='group' # group together boxes of the different traces for each value of x
            )

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
                plot_bgcolor="white",
                xaxis_title='points are not selectable',
                margin = {"l": 10, "r": 10, "b": 30, "t": 25},
            )

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
        newselection_mode="gradual",
        xaxis_range = [-0.5, 1.5] if diff == False else [-0.5, 0.5],
        yaxis_range = [min(df[selected_y]) - (max(df[selected_y])/10), max(df[selected_y]) + (max(df[selected_y])/10)],
        font=dict(size=15.2)

    )
    fig.update_xaxes(
        tickvals= [0,1] if diff == False else [0],  # List of positions where ticks should be displayed
        ticktext=["pre", "post"]  if diff == False else ["change"],  # List of labels corresponding to each tick position
    )

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
            return f"1422 subjects."
        elif len(selected_data) == 0:
            return f"1422 subjects."
        n = len(selected_data)
        return f"{n}/1422 selected"
    
    @app.callback(
        Output(f"graph-1", "figure", allow_duplicate=True),
        Output(f"graph-2", "figure", allow_duplicate=True),
        Output("store-selected-data", "data",allow_duplicate=True),
        Input(f"graph-1", "selectedData"),
        Input(f"graph-2", "selectedData"),
        State(f"parameter-dropdown-1", "value"),
        State(f"switch-1", "value"),
        State(f"switch-selected-1", "value"),
        State("heatmap-graph", "clickData"),
        State("dropdown-heatmap", "value"),
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
        Input(f"switch-selected-1", "value"),
        Input(f"switch-1", "value"),
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
        Output("heatmap-graph", "figure"),
        Input("dropdown-heatmap", "value"),
    )
    def update_heatmap(param):
        filtered_matrix = correlation_matrix.loc[:,param].reset_index().set_index("index").dropna()
        filtered_matrix.sort_values(by = param,inplace=True)
        filtered_matrix = filtered_matrix[filtered_matrix.index != param]
        fig = go.Figure(
            data=go.Heatmap(
                x=filtered_matrix.columns,
                y=filtered_matrix.index,    
                z=filtered_matrix.values,
                colorscale='RdBu',
                colorbar=dict(title='Correlation', orientation="v", thickness=15, tickfont=dict(size=9)),
                hoverongaps = False, 
                hoverinfo='none',  # Disable hovering
                text=[[name] for name in list(filtered_matrix.index)],
                texttemplate="%{text}",
                textfont={"size":10}
                )
            )
        fig.update_layout(
                margin=dict(l=30, r=20, t=50, b=0),
                yaxis = dict(title = "",showticklabels=False ),
                xaxis = dict(title = "",showticklabels=False ),
            )
        fig.update_xaxes(title=f"Correlation with: {param}")
        return fig

    @app.callback(
        Output("graph-2", "figure"),
        Input("heatmap-graph", "clickData"),
        Input("dropdown-heatmap", "value"),
        State("store-selected-data", "data"),
    )
    def callback_parameter_scatter(clickData, parameter, selected_ids):
        if not selected_ids : 
            selected_ids = []
        return update_scatter(clickData, parameter, selected_ids, None)

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
