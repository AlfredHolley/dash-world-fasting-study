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

def categorize_length_of_fast(value):
    if value < 3:
        return None  
    elif value < 8:
        return '3-7'
    elif value < 13:
        return '8-12'
    elif value < 18:
        return '13-17'
    else:
        return '18+'

df = pd.read_parquet('data/merged_data_wide.parquet')
correlation_matrix = pd.read_excel("data/correlation_matrix.xlsx", index_col=0)
df = df.reset_index(drop = True).set_index("id")
df0 =df.query("timepoint.eq(0)").copy()
df1 =df.query("timepoint.eq(1)").copy()

def update_scatter(clickData, selected_id, selectedpoints_local):
    selectedpoint = []
    if selected_id : 
        selectedpoint = [s_id - 1 for s_id in selected_id]
    if clickData is None:
        x = 'weight (kg) change'
        y = 'baseline'
    else : 
        x = clickData.get('points')[0].get('x')
        y = clickData.get('points')[0].get('y')

    if y == 'baseline':
        ytitle = 'Baseline of ' + x.replace(' change','')
        xtitle = x
        title = f"{y.title()} of {x.replace(' change','')}"
        y = x[:-7] # remove ' change'

    else:
        ytitle = y
        xtitle = x
        title = f"{y} vs {x}"

    fig = px.scatter(df0, x=y, y=x, trendline="ols")
    fig.data[0]["name"] = "points"

    fig.update_traces(
        selector=dict(name = "points"),
        selectedpoints=selectedpoint,
        selected={"marker": {"opacity": 0.8,"color" : "red"}},
        unselected={"marker": {"opacity": 0.5, "color" : "blue"}},
    )

    fig.update_layout(
        title=f'{title}',
        xaxis_title=ytitle,
        yaxis_title=xtitle,
        xaxis_range = [min(df0[y]) - (max(df0[y])/10), max(df0[y]) + (max(df0[y])/10)],
        yaxis_range = [min(df0[x]) - (max(df0[x])/6), max(df0[x]) + (max(df0[x])/6)],
        height=600, width=800,
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
            

def box_plot(selected_y, selected_id, selectedpoints_local, display_selected_box, diff = False):
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
                margin = {"l": 10, "r": 10, "b": 30, "t": 25},
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
        margin={"l": 30, "r": 20, "b": 15, "t": 15},
        dragmode="select",
        newselection_mode="gradual",
        width=400,
        xaxis_range = [-0.5, 1.5] if diff == False else [-0.5, 0.5],
        yaxis_range = [min(df[selected_y]) - (max(df[selected_y])/10), max(df[selected_y]) + (max(df[selected_y])/10)],

    )
    fig.update_xaxes(
        tickvals= [0,1] if diff == False else [0],  # List of positions where ticks should be displayed
        ticktext=["pre", "post"]  if diff == False else ["change"] # List of labels corresponding to each tick position
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
            return f"Characteristics of the study population : 1422 subjects."
        elif len(selected_data) == 0:
            return f"Characteristics of the study population : 1422 subjects."
        n = len(selected_data)
        return f"Characteristics of the study population : {n} selected amount 1422 subjects."
    
    @app.callback(
        [Output(f"graph-{i}", "figure") for i in range(1, 6)],
        Output("store-selected-data", "data"),
        [Input(f"parameter-dropdown-{i}", "value") for i in range(1, 5)],
        [Input(f"graph-{i}", "selectedData") for i in range(1, 6)],
        [Input(f"switch-{i}", "value") for i in range(1, 5)],
        [Input(f"switch-selected-{i}", "value") for i in range(1, 5)],
        Input("heatmap-graph", "clickData"),
        State("store-selected-data", "data"),
    )
    def callback(*args):
        parameters = args[:4]
        selected_data = args[4:9]
        switch_show_changes = args[9:13]
        switch_show_comparaison = args[13:17]
        click_heatmap = args[-2]
        if args[-1] :
            current_data = args[-1]
        else : current_data = []

        if not ctx.triggered_id :
            boxes  = [box_plot(parameters[i-1], None, None, False, False) for i in range(1,5)]
            scatter = [update_scatter(None, None, None)]
            return boxes + scatter + [[]]
        trigger_id, number_id = ctx.triggered_id, ctx.triggered_id[-1]

        if ("heatmap" in trigger_id) & (not current_data): 
            boxes =  [dash.no_update for i in range(1,5)]
            scatter = [update_scatter(click_heatmap, [], None)]
            current_data =  [dash.no_update]
            return boxes + scatter + current_data

        if current_data:
            scatter = [update_scatter(click_heatmap, current_data, None)]
            if "heatmap" in trigger_id :
                boxes =  [dash.no_update for i in range(1,5)]
                current_data = [dash.no_update]
                return boxes + scatter + current_data

            elif "dropdown" in trigger_id :
                boxes = [box_plot(parameters[i-1], current_data, None, switch_show_comparaison[i-1], switch_show_changes[i-1] ) 
                          if number_id == f"{i}" else dash.no_update 
                    for i in range(1,5)]
                scatter = [dash.no_update]
                data_store = [current_data]
                return boxes + scatter + data_store

        selection_of_trigger =  selected_data[int(number_id)-1]
        if selection_of_trigger and selection_of_trigger["points"]:
            selected_id = [p["pointIndex"] + 1 for p in selection_of_trigger["points"]]
        else :
            selected_id = [] 

        if  "switch" in trigger_id:
            boxes = [box_plot(parameters[i-1],
                            current_data,
                            selected_data[i-1] if number_id == f"{i}" else None, 
                            switch_show_comparaison[i-1], 
                            switch_show_changes[i-1])
                          if number_id == f"{i}" else dash.no_update 
                    for i in range(1,5)]
            return boxes + [dash.no_update] + [current_data]

        boxes = [box_plot(parameters[i-1],
                          selected_id,
                          selected_data[i-1] if number_id == f"{i}" else None, 
                          switch_show_comparaison[i-1], 
                          switch_show_changes[i-1])
                # if number_id == f"{i}" else dash.no_update 
                for i in range(1,5)]
        scatter = [update_scatter(click_heatmap, 
                                  selected_id,
                                  selected_data[4] if number_id == "5" else None,
                                  )]
        data_store = [selected_id]
        return boxes + scatter + data_store
    
    # @app.callback(
    #     Output('sex-pie-chart', 'figure'),
    #     Input('store-selected-data', 'data'),
    #     )
    
    # def update_sex(selected_ids):
    #     if not selected_ids : 
    #         selected_ids = df0.index

    #     df_filtered = df0.loc[selected_ids]
    #     counts_sex = df_filtered.sex.value_counts().sort_index(ascending=False)
    #     fig = px.pie(values=counts_sex.values, names=counts_sex.index, 
    #                 title='Gender proportion', height=350,
    #                 )
    #     fig.update_layout(margin={"l": 40, "r": 30, "b": 60, "t": 50},)
    #     return fig 

    # @app.callback(
    #     Output('age-histogram', 'figure'),
    #     Input('store-selected-data', 'data'),
    #     prevent_initial_call=True
    # )
    # def update_age(selected_ids):
    #     if not selected_ids : 
    #         selected_ids = df0.index

    #     df_filtered = df0.loc[selected_ids]
    #     counts_age = df_filtered["age"].value_counts().sort_index()
    #     fig = go.Figure(
    #             go.Bar(x=counts_age.index, y=counts_age.values)
    #         )
    #     mean_age = df_filtered["age"].mean()
    #     fig.update_layout(title=f'Age distribution (mean = {mean_age:.1f} years)',
    #                       xaxis=dict(title='Age (years)'),
    #                       yaxis=dict(title='Count'), 
    #                       bargap=0.2, height=350,
    #                       margin={"l": 30, "r": 20, "b": 15, "t": 50},
    #                       )    
    #     return fig
    
    # @app.callback(
    #     Output('length-fast-histogram', 'figure'),
    #     Input('store-selected-data', 'data'),
    #     prevent_initial_call=True
    # )
    # def update_fast(selected_ids):
    #     if not selected_ids : 
    #         selected_ids = df0.index

    #     df_filtered = df0.loc[selected_ids]
    #     df_filtered['length_of_fast_group'] = df_filtered['length_of_fast'].apply(categorize_length_of_fast)
    #     counts_length_fast = df_filtered.length_of_fast_group.value_counts().sort_index()

    #     fig = px.bar(counts_length_fast, x=counts_length_fast.index, y=counts_length_fast.values)
    #     mean = df_filtered["length_of_fast"].mean()

    #     fig.update_layout(
    #         title=f'Length of the fast distribution (mean = {mean:.1f} days)',
    #         xaxis=dict(title='length of the fast (days)', tickfont=dict(size=10)),  
    #         yaxis=dict(title='Count', tickfont=dict(size=10)),
    #         bargap=0.1,
    #         height=350,
    #         margin={"l": 30, "r": 20, "b": 15, "t": 50},
    #         )    
    #     return fig

    # Define the callback function to update the graph based on the selected group
    @app.callback(
        Output("heatmap-graph", "figure"),
        Input("slider-heatmap", "value"),
    )
    def update_heatmap(threshold):
        filtered_matrix = correlation_matrix[abs(correlation_matrix) >= threshold]
        fig = go.Figure(data=go.Heatmap(
                    z=filtered_matrix.values,
                    x=filtered_matrix.columns,
                    y=filtered_matrix.index,
                    colorscale='Portland',  # Change the colorscale to 'viridis'
                    colorbar=dict(title='Correlation', orientation="h", thickness=15),
                    hoverongaps = False, 
                ))
        fig.update_layout(title=f'Correlation Matrix Heatmap filtered > {threshold}',
                xaxis=dict(title=''), # , tickfont=dict(size=12)),
                yaxis=dict(title=''),# tickfont=dict(size=12)),
                height=700, width=800,
                xaxis_nticks=correlation_matrix.shape[0],
                yaxis_nticks=correlation_matrix.shape[1]
            ).update_xaxes(
                automargin=True,
            ).update_yaxes(
                automargin=True
            )

        return fig


