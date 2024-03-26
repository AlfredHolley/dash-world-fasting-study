window.dash_clientside = Object.assign({}, window.dash_clientside, {

    clientside : {

            update_dropdown_value: function(...timestamps) {
                var clicked_id = dash_clientside.callback_context.triggered[0].prop_id.split(".")[0]
                if (clicked_id) {
                    var dropdown_trigger = clicked_id[0]
                    var clickedContent = document.getElementById(clicked_id);
                    if (clickedContent) {
                        var trimmedText = clickedContent.textContent.trim();
                        var contentWithoutSuffix = trimmedText.replace(/:.*/, '').trim();

                        var outputX = [contentWithoutSuffix, window.dash_clientside.no_update]
                        var outputY = [window.dash_clientside.no_update, contentWithoutSuffix]
                        if (dropdown_trigger === "X"){
                            return outputX
                        }
                        return outputY
                    }
                }
                return window.dash_clientside.no_update;
            },

            div_creator: function(paramX, paramY, data) {
                function getBackgroundColor(value) {
                    var intensity = Math.floor(255 * Math.abs(value));
                    return 'rgba(0, 0, 255, ' + intensity / 400 + ')';
                }
                function create_divs(X_or_Y, param, data){
                    var filteredDataDict = {};
                    for (var key in data[0][param]) {
                        var value = parseFloat(data[0][param][key]).toFixed(2);
                        if (!isNaN(value) && value !== null && value !== "None") {
                            filteredDataDict[key] = value;
                        }
                    }
                    var sortedDataDict = Object.fromEntries(
                        Object.entries(filteredDataDict).sort((a, b) => Math.abs(b[1]) - Math.abs(a[1]))
                        );
                    for (var i = 0; i < 44; i++) {
                        if (i < Object.keys(sortedDataDict).length) {
                            var content = Object.entries(sortedDataDict)[i];      
                            id_div = i+1              
                            div_id = X_or_Y + "-menu-div-"+ id_div.toString()
                            div =document.getElementById(div_id)
                            // Now we can edit the div whith new style & content
                            div.style.backgroundColor = getBackgroundColor(content[1])
                            div.innerText = content[0] + ' : ' + content[1]
                        ;} 
                    }
                }

                var ctx = dash_clientside.callback_context.triggered[0]
                if (ctx) {
                    ctx_trigger = ctx.prop_id.split(".")[0].slice(-1)
                    var dropdown_to_update = ctx_trigger === "X"? "Y":"X";
                    var param = ctx_trigger === "X" ? paramX : paramY;
                    create_divs(dropdown_to_update, param, data)
                } else {
                    create_divs("X", "weight (kg) change", data)
                    create_divs("Y", "baseline of the parameter", data)
                }

                return window.dash_clientside.no_update;
            },



            resetSelectedData: function(n_clicks) {

                if (n_clicks > 0) {

                    return [null, null, 1];
                }
                return [window.dash_clientside.no_update, window.dash_clientside.no_update]
            },
            add_icon:function(){
                var icon1 = {
                    'width': 512,
                    'height': 512,
                    'path': 'M20.5 224H40c-13.3 0-24-10.7-24-24V72c0-9.7 5.8-18.5 14.8-22.2s19.3-1.7 26.2 5.2L98.6 96.6c87.6-86.5 228.7-86.2 315.8 1c87.5 87.5 87.5 229.3 0 316.8s-229.3 87.5-316.8 0c-12.5-12.5-12.5-32.8 0-45.3s32.8-12.5 45.3 0c62.5 62.5 163.8 62.5 226.3 0s62.5-163.8 0-226.3c-62.2-62.2-162.7-62.5-225.3-1L185 183c6.9 6.9 8.9 17.2 5.2 26.2s-12.5 14.8-22.2 14.8H48.5z',
                    }
                var config_box = {
                    displayModeBar: true,
                    displaylogo: false,
                    modeBarButtonsToAdd: [
                        {
                            name: 'Reset Selection',
                            icon: icon1,
                            click: function(gd) {
                                document.getElementById('button-reset').click();
                            },
                        }
                    ],
                    modeBarButtonsToRemove: [
                        "toImage","zoom2d", "pan2d","lasso2d", "zoomIn2d", "zoomOut2d", "autoScale2d", "resetScale2d",
                        "hoverClosestCartesian", "hoverCompareCartesian", "toggleSpikelines"
                    ] 
                }
                var config_scatter = {
                    displayModeBar: true,
                    displaylogo: false,
                    modeBarButtonsToAdd: [
                        {
                            name: 'Reset Selection',
                            icon: icon1,
                            click: function(gd) {
                                document.getElementById('button-reset').click();
                            },
                        }
                    ],
                    modeBarButtonsToRemove: [
                        "toImage","zoom2d", "pan2d","select2d", "zoomIn2d", "zoomOut2d", "autoScale2d", "resetScale2d",
                        "hoverClosestCartesian", "hoverCompareCartesian", "toggleSpikelines"
                    ]
                }
                return [config_box, config_scatter];
                },

                update_selection: function(fig, selected_ids) {
                    let selectedpoints = [];
                    if (selected_ids.length > 0) {
                        selectedpoints = selected_ids.map(id => id - 1);
                    }
                    let new_fig = fig
                    new_fig.data.forEach(trace => {
                        trace.selectedpoints = selectedpoints;
                    });
                    return new_fig;
                },
                callback_on_selection: function(selectedpoints_g1,selectedpoints_g2, fig_box,fig_scatter, data) {
                    let ctx = dash_clientside.callback_context;
                    let number_id = ctx.triggered.map(t => t.prop_id.split('.')[0])[0].slice(-1);
                    number_id = number_id[number_id.length - 1]; 
                    
                    let selection = [selectedpoints_g1, selectedpoints_g2];
                    let selection_triggered = selection[parseInt(number_id) - 1];
                    let selected_ids = [];
                    
                    if (selection_triggered && selection_triggered.points) {
                        selected_ids = selection_triggered.points.map(p => p.pointIndex + 1);
                    }
                    
                    let updated_box = this.update_selection(fig_box, selected_ids);
                    let data_box = updated_box.data
                    let layout_box = updated_box.layout

                    let updated_scatter = this.update_selection(fig_scatter, selected_ids);
                    let data_scatter = updated_scatter.data
                    let layout_scatter = updated_scatter.layout

                    return [{data:data_box, layout:layout_box},
                            {data:data_scatter, layout:layout_scatter},
                            selected_ids];
                },
        
                update_sex_pie: function(data_stored, selectedIds) {
                    var records = data_stored.filter(item => item.timepoint === 0)
                    if (selectedIds && selectedIds.length > 0) {
                        var records = records.filter(item => selectedIds.includes(item.id));
                    } 
                    const sexCount = records.reduce((acc, record) => {
                        acc[record.sex] = (acc[record.sex] || 0) + 1;
                        return acc;
                      }, {});
                      
                      // Prepare data for the Sunburst chart
                      const data = [{
                        labels: Object.keys(sexCount),
                        parents: [], // No parents since we're not showing hierarchy
                        values: Object.values(sexCount),
                        type: 'sunburst',
                        sort: false, // This ensures our segments stay in the order we specified
                        branchvalues: 'total', // This is usually used for hierarchical data but necessary for the structure
                      }];
                      
                      // Layout configuration
                      const layout = {
                        margin: {l: 0, r: 0, b: 0, t: 0},
                        sunburstcolorway:["#636efa","#ef553b","#00cc96"],
                      };
                      
                    return {data:data, layout:layout};
                },
                orchestre_callbacks:function(data, rect, lasso, age, fast, test3, param_box, switch_1, switch_2, paramY, paramX){
                    var triggered_id = dash_clientside.callback_context.triggered[0].prop_id.split('.')[0]
                    df0 = data.filter(row => row["timepoint"] === 0);
                    if (triggered_id.includes("graph")) {
                        return [window.dash_clientside.no_update, window.dash_clientside.no_update, window.dash_clientside.no_update, [18, 100], [3, 23]];
                    } else if (triggered_id.includes("age")) {
                        var trigger_var = 0;
                        var indices = new Set();
        
                        df0.forEach((item, idx) => {
                            if (item["age (years)"] >= age[0] && item["age (years)"] <= age[1]) {
                                indices.add(idx);
                            }
                        });
                        var selected_ids = Array.from(indices);
                    } else if (triggered_id.includes("fast")) {
                        var trigger_var = 1;
                        var indices = new Set();
        
                        df0.forEach((item, idx) => {
                            if (item["fasting duration (days)"] >= fast[0] && item["fasting duration (days)"] <= fast[1]) {
                                indices.add(idx);
                            }
                        });
                        var selected_ids = Array.from(indices);
                    }else  {
                        var trigger_var = 2;
                        if (test3 === "none") {
                            var selected_ids = [];
                        } else {
                            var sex_catched = document.getElementById("test-3").innerHTML;
                            var indices = new Set();
                            df0.forEach((item, idx) => {
                                if (item["sex"] === sex_catched) {
                                    indices.add(idx);
                                }
                            });
                            var selected_ids = Array.from(indices);
                        }
                    }
                    var selected_ids_index = selected_ids.map(id => id + 1);
                    if (selected_ids.length === 1422) {
                        selected_ids = [];
                        selected_ids_index = [];
                    }
                    let fig_box_obj = this.update_boxplot(data, param_box, selected_ids_index, switch_1, switch_2);
                    let fig_box_dict = {data : fig_box_obj.data, layout : fig_box_obj.layout}
                    
                    var paramY =document.getElementById("dropdown-heatmap-Y").innerText
                    let fig_scatter_obj = this.update_scatter(data, paramY,paramX, selected_ids_index);
                    let fig_scatter_dict = {data : fig_scatter_obj.data, layout : fig_scatter_obj.layout}

                    var callback_var = [
                        [window.dash_clientside.no_update, [3,23]], // we call age slider, we reset age
                        [[18,100], window.dash_clientside.no_update], // we call fast, we reset fast
                        [[18,100], [3,23]] // we call the sex, we reset both slider to default
                    ];
                    var response = [
                        fig_box_dict,
                        fig_scatter_dict, 
                        selected_ids_index, 
                        callback_var[trigger_var][0], 
                        callback_var[trigger_var][1], 
                    ];
        
                    return response;
                },
        
                update_graph3: function(data_stored, selected_ids) {

                    let records = data_stored.filter(item => item.timepoint === 0);

                    if (selected_ids && selected_ids.length > 0) {
                        records = records.filter(item => selected_ids.includes(item.id));
                    }
                
                    const sexCount = records.reduce((acc, record) => {
                        acc[record.sex] = (acc[record.sex] || 0) + 1;
                        return acc;
                    }, {});
                
                    var n_males = sexCount['M'] || 0;
                    var n_females = sexCount['F'] || 0;

                    document.getElementById("graph-3").innerHTML=""
                    var baseColors = ["#465FFF", "#FFBFF6"];
                    var options = {
                            series: [n_males, n_females],
                            chart: {
                                type: 'pie',
                                height: '180px',
                                toolbar: {
                                    show: false,
                                },
                                events: {
                                    dataPointSelection: function(event, chartContext, config) {
                                        // Determine the index of the selected slice
                                        var selectedSliceIndex = config.dataPointIndex;
                                        colors_stored_div = document.getElementById("test-3")

                                        if( selectedSliceIndex === 0){
                                            if (document.getElementById("test-3").innerHTML ===  "none"){
                                                colors_stored_div.innerHTML="M"
                                                colors_stored_div.click()
                                                var newColors = ["#FF6D6D","#FFBFF6"]
                                            }else{
                                                colors_stored_div.innerHTML="none"
                                                colors_stored_div.click()
                                                var newColors = ["#465FFF","#FFBFF6"]

                                            }
                                        }else{
                                            if (document.getElementById("test-3").innerHTML ===  "none"){
                                                colors_stored_div.innerHTML="F"
                                                // launch the callback
                                                colors_stored_div.click()
                                                var newColors = ["#465FFF","#FF6D6D"]
                                            }else{
                                                colors_stored_div.innerHTML="none"
                                                // launch the callback
                                                colors_stored_div.click()
                                                var newColors = ["#465FFF","#FFBFF6"]

                                            }
                                        }
                                            chartContext.updateOptions({
                                            colors: newColors,
                                        });

                                    }
                                },
                                animations: {
                                    enabled: true,
                                    easing: 'easeinout',
                                    speed: 500,
                                },
                            },
                            states: {
                                hover: {
                                    filter: {
                                        type: 'lighten',
                                    },
                                },
                                active: {
                                    filter: {
                                        type: 'none',
                                    }
                                }
                            },
                        
                            labels: ['M', 'F'],
                            colors: baseColors,
                            legend: {
                                show: false,
                            },
                            dataLabels: {
                                enabled: true,
                                formatter: function (val, opts) {
                                    return  opts.w.config.labels[opts.seriesIndex] + " : " + opts.w.config.series[opts.seriesIndex];
                                },
                                textAnchor: 'end',
                                distributed: false,
                                style: {
                                    fontSize: '13px',
                                    fontWeight: 'bold',
                                    colors: ['transparent'],
                                },
                                background: {
                                    enabled: true,
                                    foreColor: '#000',
                                    padding:0,
                                    margin:20,
                                    borderWidth: 0,
                                },
                                dropShadow: {
                                    enabled: false
                                }
                            },
                            plotOptions: {
                                pie: {

                                    donut: {
                                        labels: {
                                            show: false,
                                            textAnchor:"start"
                                        }
                                },
                                expandOnClick: false,
                                }
                            },
                            tooltip: {
                                enabled: false,
                            },
                      };
                      if (window.graph3) {
                        window.graph3.updateOptions(options);
                    } else {
                        window.graph3 = new ApexCharts(document.getElementById("graph-3"), options);
                        window.graph3.render();
                    }
                return window.dash_clientside.no_update;
                },


                update_boxplot: function(df, selectedY, selectedIds, display_selected, diff) {
                    selectedIds = selectedIds || [];
                    let df0 = df.filter(record => record.timepoint === 0);
                    let df1 = df.filter(record => record.timepoint === 1);
                    // preparation of variable
                    let selectedPoints = [];
                    selectedPoints = selectedIds.map(id => id - 1);

                    df0.forEach(item => {
                        item.is_selected = selectedIds.includes(item.id); // Supposant que 'id' est la propriété à vérifier
                    });
                    df.forEach(item => {
                        item.is_selected = selectedIds.includes(item.id); // De même pour 'df'
                    });
                            
                    if (diff === false) {
                        if (!display_selected){
                            let traces = [];

                            traces.push({
                                x: df0.map(item => item.jittered_x),
                                y: df0.map(item => item[selectedY]),
                                type: 'scatter',
                                mode: 'markers',
                                showlegend: false,
                                marker: {
                                    color: 'blue',
                                    size: 5,
                                    opacity: 0.85
                                },
                                selector: {type:'scatter'},
                                selectedpoints: selectedPoints,
                                selected: {marker: {color: 'red', size: 5}},
                                unselected: {marker: {opacity: 0.7}},
                            });
                            traces.push({
                                x: df1.map(item => item.jittered_x),
                                y: df1.map(item => item[selectedY]),
                                type: 'scatter',
                                mode: 'markers',
                                showlegend: false,
                                marker: {
                                    color: 'blue',
                                    size: 5,
                                    opacity: 0.85
                                },
                                selector: {type:'scatter'},
                                selectedpoints: selectedPoints,
                                selected: {marker: {color: 'red', size: 5}},
                                unselected: {marker: {opacity: 0.7}},

                            });
                            traces.push({
                                x: df.map(item => item.timepoint),
                                y: df.map(item => item[selectedY]),
                                type: 'box',
                                boxpoints: false,
                                line: {color: "rgba(100, 100, 250, 1)"},
                                fillcolor: 'rgba(135, 160, 250, 0.5)',
                                showlegend: false,
                            });
                            let layout = {
                                newselection:{mode:"gradual"},
                                hovermode: false,
                                xaxis: {
                                    tickvals: [0, 1],
                                    ticktext: ['Baseline', 'Fasting'],
                                    zeroline: false,
                                    fixedrange: true,
                                },
                                yaxis: {
                                    zeroline: false,
                                    showline: false, 
                                    fixedrange: true,
                                    ticklabelposition: "inside top"
                                },                                
                                dragmode: false,
                                plot_bgcolor:'rgba(245,245,247,1)', 
                                margin : {"l": 16, "r": 16, "b": 30, "t": 25}
                            };
                            
                            return {data: traces, layout: layout};

                        } else if (display_selected) {
                            let traces_selected = [];
                            traces_selected.push({
                                x: df.filter(item => !item.is_selected).map(item => item.timepoint),
                                y: df.filter(item => !item.is_selected).map(item => item[selectedY]),
                                type: 'box',
                                name: 'Not Selected',
                                line: {color: "rgba(100, 100, 250, 1)"},
                                fillcolor: 'rgba(135, 160, 250, 0.5)',
                                showlegend: false,
                                boxpoints: 'all',
                                pointpos:0,
                                selector: {type:'scatter'},
                                marker: {color: 'blue', size: 5, opacity: 0.7},
                            });
                            traces_selected.push({
                                x: df.filter(item => item.is_selected).map(item => item.timepoint),
                                y: df.filter(item => item.is_selected).map(item => item[selectedY]),
                                type: 'box',
                                name: 'selected',
                                boxpoints: 'all',
                                pointpos:0,
                                marker: {color: 'red', size: 5, opacity: 0.7},

                                line: {color: 'rgba(255,0,0,0.6)'},
                                fillcolor: 'rgba(255,0,0,0.3)',
                            });
                            let layout_selected = {
                                showlegend: false, 
                                boxmode: 'group',
                                legend: false, 
                                modebar: {remove: ["select2d", "Reset Selection"]},
                                hovermode: false,
                                dragmode: false,
                                plot_bgcolor:'rgba(245,245,247,1)',
                                xaxis: {
                                    tickvals: [0, 1],
                                    ticktext: ['Baseline', 'Fasting'],
                                    // title: 'Points are not selectable', 
                                    zeroline: false,
                                    fixedrange: true,
                                },
                                yaxis: {
                                    zeroline: false,
                                    showline: false, 
                                    fixedrange: true,
                                    ticklabelposition: "inside top"
                                },
                                margin : {"l": 16, "r": 16, "b": 30, "t": 25}

                            };
                            return {data: traces_selected, layout: layout_selected };
                        }

                    } else {
                        let selected_y_change = selectedY ? selectedY + ' change' : 'weight (kg) change';

                        if (!display_selected){
                            let traces = [];
                            traces.push({
                                x: df0.map(item => item.jittered_x),
                                y: df0.map(item => item[selected_y_change]),
                                type: 'scatter',
                                mode: 'markers',
                                showlegend: false,
                                marker: {
                                    color: 'blue',
                                    size: 5,
                                    opacity: 0.85
                                },
                                selectedpoints: selectedPoints,
                                selected: {marker: {color: 'red', size: 5}},
                                unselected: {marker: {opacity: 0.7}},
                            });
                            traces.push({
                                y:df0.map(item => item[selected_y_change]), 
                                type: 'box',
                                showlegend: false,
                                boxpoints: false,
                                line: {color: "rgba(100, 100, 250, 1)"},
                                fillcolor: 'rgba(135, 160, 250, 0.5)',
                            });
                            let layout = {
                                hovermode: false,
                                dragmode: false,
                                showline: false, 
                                yaxis: {
                                    zeroline: false,
                                    showline: false, 
                                    fixedrange: true,
                                    ticklabelposition: "inside top"
                                },          

                                xaxis: {
                                    tickvals: [0],
                                    ticktext: ['Changes'],
                                    zeroline: false,
                                    showline: false, 
                                    fixedrange: true,
                                },
                                newselection:{mode:"gradual"},
                                plot_bgcolor:'rgba(245,245,247,1)', 
                                margin : {"l": 16, "r": 16, "b": 30, "t": 25}
                            };
                            return {data: traces, layout: layout};

                        } else {
                        let traces_selected = [];
    
                        traces_selected.push({
                            y: df0.filter(item => !item.is_selected).map(item => item[selected_y_change]),
                            type: 'box',
                            name: 'Not Selected',
                            showlegend: false,
                            boxpoints: 'all',
                            pointpos:0,
                            line: {color: "rgba(100, 100, 250, 1)"},
                            fillcolor: 'rgba(135, 160, 250, 0.5)',
                            marker: {color: 'blue', size: 5, opacity: 0.7},
                        });
                        traces_selected.push({
                            y: df0.filter(item => item.is_selected).map(item => item[selected_y_change]),
                            type: 'box',
                            name: 'Selected',
                            boxpoints: 'all',
                            pointpos:0,
                            marker: {color: 'red', size: 5, opacity: 0.7},
                            line: {color: 'rgba(255,0,0,0.6)'},
                            fillcolor: 'rgba(255,0,0,0.2)',
                            selected: {color: 'red', size: 5, opacity: 0.7},
                            unselected : {color: 'red', size: 5, opacity: 0.7},

                        });
                        let layout_selected = {
                            showlegend: false, 
                            hovermode: false,
                            modebar: {remove: ["select2d", "Reset Selection"],},
                            dragmode: false,
                            plot_bgcolor:'rgba(245,245,247,1)',
                            yaxis: {
                                zeroline: false,
                                showline: false, 
                                fixedrange: true,
                                ticklabelposition: "inside top"
                            },

                            xaxis: {
                                tickvals: selectedIds.length > 0 ? [0.5] : [0],
                                ticktext: ['Changes'],
                                // title: 'Points are not selectable',
                                zeroline: false,
                                showline: false, 
                                fixedrange: true,

                            },
                            margin : {"l": 16, "r": 16, "b": 30, "t": 25}

                        };

                        return {data: traces_selected, layout: layout_selected};
                        // {data: traces_selected, layout: layout_selected};
                    }
                }
            },

            update_scatter: function(data_stored, parameterY, parameterX, selectedIds) {
                let selectedpoint = selectedIds ? selectedIds.map(s_id => s_id - 1) : [];
                let x, y;
            
                if (!parameterY) {
                    y = "weight (kg) change";
                    x = 'weight (kg)' ;
                } else {
                    y = parameterY === 'baseline of the parameter' ? parameterX.slice(0, -7) : parameterY;
                    x = parameterX === 'baseline of the parameter' ? y.slice(0, -7) : parameterX;
                }
                let dataFiltered = data_stored.filter(item => item.timepoint === 0);

                let trace = {
                    x: dataFiltered.map(record => record[x]), // Assurez-vous que 'x' correspond à la clé correcte dans vos objets
                    y: dataFiltered.map(record => record[y]), // Idem pour 'y'
                    mode: 'markers',
                    type: 'scatter',
                    name: 'points',
                    marker: { color: 'blue', opacity: 0.7 },
                    unselected: {marker: {opacity: 0.7, color: "blue"}}, 
                    selected: {marker: {opacity: 1, color: "red"}},
                };
                
                
                let layout = {
                    hovermode: false,
                    margin: {l: 0, r: 20, b: 21, t: 45},
                    dragmode: false,
                    newselection:{mode:"gradual"},
                    plot_bgcolor: 'rgba(245,245,247,1)',
                    xaxis: {fixedrange: true, zeroline: false},
                    yaxis: {fixedrange: true, gridcolor: 'rgba(0,0,0,0.065)', 
                            ticklabelposition: "inside top", title: null,zeroline: false}
                };

                trace.selectedpoints = selectedpoint;
                let data = [trace];

                return {data: data, layout: layout};
            }, 

            update_age: function(selected_ids, data_store) {
                let text_age, text_length_fast;

                let filteredTimepoint = data_store.filter(record => record.timepoint === 0);
                if (selected_ids && selected_ids.length > 0) {
                    filteredData = filteredTimepoint.filter(record => selected_ids.includes(record.id));
                }
                else {
                    filteredData = filteredTimepoint;
                }

                const sum_age = filteredData.reduce((acc, curr) => acc + curr['age (years)'], 0);
                const sum_fast = filteredData.reduce((acc, curr) => acc + curr['fasting duration (days)'], 0);
                const avg_age = sum_age / filteredData.length;
                const avg_fast = sum_fast / filteredData.length;

                text_age = `${avg_age.toFixed(1)} years`;
                text_length_fast = `${avg_fast.toFixed(1)} days`;

                return [text_age, text_length_fast];
            },

    
    }
});

