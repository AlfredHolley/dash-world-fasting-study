import dash_daq as daq 
from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import dash_echarts
import pandas as pd
# correlation_matrix = pd.read_excel("data/correlation_matrix.xlsx", index_col=0)
# json_matrix = correlation_matrix.to_dict(orient="records")
correlation_matrix = pd.read_excel("data/correlation_matrix.xlsx", index_col=0)
json_matrix = [correlation_matrix.to_dict()]

def layout():
    all_param = ['AP (µkat/l)', 'Acetoacetic acid (mg/dL)', 'BMI (kg/m²)',
        'CRP (mg/l)', 'Ca (mmol/l)', 'Creatinine (µmol/l)', 'DBP (mmHg)',
        'ESR 1h', 'ESR 2h', 'EWB (0-10)', 'Erythrocytes (106/µl)',
        'GGT (µkat/l)', 'GOT (µkat/l)', 'GPT (µkat/l)', 'HDL-C (mmol/l)',
        'Haematocrit (%)', 'Haemoglobin (mmol/l)', 'HbA1c (mmol/mol)',
        'INR', 'K (mmol/l)', 'LDL-C (mmol/l)', 'LDL/HDL ratio',
        'Leucocytes (103/µl)', 'MCH (pg)', 'MCHC (g/dl)', 'MCV (fl)',
        'Mg (mmol/l)', 'Na (mmol/l)', 'PTT (sec)', 'PWB (0-10)',
        'Quick (%)', 'SBP (mmHg)', 'TC (mmol/l)', 'TG (mmol/l)',
        'Thrombocytes (103/µl)', 'Urea (mmol/l)', 'Uric acid (µmol/l)',
        'glucose (mmol/l)', 'puls (beats/min)', 'waist (cm)','weight (kg)']

    correlation_params = ['baseline of the parameter', 'fasting duration (days)','age (years)',
        'weight (kg) change','BMI (kg/m²) change','waist (cm) change', 'SBP (mmHg) change','DBP (mmHg) change',
        'puls (beats/min) change','LDL-C (mmol/l) change','HDL-C (mmol/l) change','LDL/HDL ratio change',
        'TG (mmol/l) change', 'glucose (mmol/l) change','HbA1c (mmol/mol) change','TC (mmol/l) change',
        'Acetoacetic acid (mg/dL) change', 'Uric acid (µmol/l) change',
        'EWB (0-10) change', 'PWB (0-10) change','GOT (µkat/l) change', 'GPT (µkat/l) change', 'GGT (µkat/l) change',
        'Na (mmol/l) change', 'Ca (mmol/l) change',  'K (mmol/l) change','Mg (mmol/l) change','PTT (sec) change', 'Erythrocytes (106/µl) change',
        'Creatinine (µmol/l) change', 'Urea (mmol/l) change', 'Quick (%) change',
        'Thrombocytes (103/µl) change', 'ESR 1h change', 
        'CRP (mg/l) change', 'ESR 2h change', 'Leucocytes (103/µl) change', 'MCH (pg) change','MCV (fl) change', 'MCHC (g/dl) change',
        'Haematocrit (%) change',  'Haemoglobin (mmol/l) change','INR change']
    text_header = """ 
    It was conducted at Buchinger Wilhelmi, a well-established fasting clinic, by a team led by Dr. Françoise Wilhelmi de Toledo and with the support of many of our guests and patients.
    The study collected and evaluated data from 1,422 who completed the Buchinger Wilhelmi fasting programme over a period of 5, 10, 15 or 20 days in 2016. \n
    The results of the study were published online on January 2, 2019 in the peer-reviewed journal PLOS ONE under the title “Safety, health improvement and well-being during a 4 to 21-day fasting period in an observational study including 1422 subjects.
    We present an interactive dashboard that leverages the data gathered in this study, offering a dynamic and user-friendly interface for comprehending the outcomes of long-term fasting.
    """
    section_text_1 = """
    Physicians gathered clinical data, and trained nurses recorded participants' body weight each morning, following a standardized protocol. Blood pressure and pulse were measured in a seated position on the non-dominant arm. Abdominal circumference was determined using a measuring tape placed midway between the lowest rib and the iliac crest. 
       
    """
    section_text_2 = """
    In order to assess well-being, participants under the supervision of nurses provided daily self-reports of their physical well-being and emotional well-being using numeric rating scales ranging from 0 (very bad) to 10 (excellent). The objective was to record the tolerance levels of the fasting program.
    
    """
    section_text_3 = """
    The participants independently measured the levels of ketone bodies in their first-morning urine by employing Ketostix. Ketone bodies serve as indicators of fat burning, reflecting a shift in energy metabolism from utilizing dietary energy sources to the process of burning stored fats for energy.
    
    """
    section_text_4 = """
    Blood analysis was conducted following international protocols to understand what are the effects of long-term fasting on lipid profiles, glycemic markers, and blood count metrics to coagulation factors, liver function indicators, inflammatory biomarkers, renal function measures, and electrolyte levels.
    """
    all_text = section_text_1 + "\n" + section_text_2 + "\n" + section_text_3 + "\n" + section_text_4
    clinical_param = ['weight (kg)','BMI (kg/m²)','waist (cm)','SBP (mmHg)','DBP (mmHg)','puls (beats/min)']
    well_being = ['PWB (0-10)','EWB (0-10)']
    ketones = ['Acetoacetic acid (mg/dL)']
    blood_analysis = list(set(all_param) - set(clinical_param) - set(well_being) - set(ketones))
    parameters = [clinical_param, well_being, ketones, blood_analysis]
    all_parameters = clinical_param + well_being + ketones + blood_analysis

    def add_switch(id_graph):
        return html.Div(
            [
                dcc.Store(id='data-store', data={'matrix': json_matrix, 'current_data':None}),
                dcc.Store(id="store-selected-data"),

                dmc.Switch(
                    size="xs",
                    label="changes",
                    checked=False,
                    id =  f"switch-{id_graph}"
                    ), 
                dmc.Switch(
                    size="xs",
                    id = f"switch-selected-{id_graph}",
                    label='selected data ',
                    checked = False
                )
            ], id = "toggles-div" )
        
    return html.Div([
                html.Img(src="assets/BW_logo.svg", alt="BW_logo", width="200px", id = "logo"),
            html.Div([
                html.H4("World largest Study on the fasting", id="header-title"),
                html.P(f"{text_header}"),
            ], className="header-container"),

            html.Div([
                html.Div(
                        children = [
                            html.H5("Measurements"), 
                            dcc.Dropdown(
                                id=f'parameter-dropdown-1',
                                options=[param for param in all_parameters],
                                value=all_parameters[0],
                                clearable=False, 
                                searchable=False

                            ),
                            dcc.Graph(id=f'graph-1',
                            config={
                                "displayModeBar": True,
                                'displaylogo': False,
                                "modeBarButtonsToRemove" :["toImage","zoom2d", "pan2d","lasso2d", "zoomIn2d", "zoomOut2d", "autoScale2d", "resetScale2d",
                                                    "hoverClosestCartesian", "hoverCompareCartesian", "toggleSpikelines", "resetViews",],
                                }),
                            add_switch(1),
                        ], id = "div-1"
                    ) 

            ], className="graph-container-1"),

            html.Div(html.H4(id='study-characteristics'), className="card_info", style = {"text-align": "center"}), 
            html.Div([
                dbc.Card([
                            dbc.CardHeader("Sex proportion"),
                            dbc.CardBody(
                                    dcc.Graph(id='sex-pie-chart',config={"displayModeBar": False})
                                )
                    ]
                ),
                dbc.Card([
                            dbc.CardHeader("Age (mean)"),
                            dbc.CardBody([html.Div(html.H4(id='age-text'), className="card_info")]),
                            dbc.CardFooter(
                                dcc.RangeSlider(
                                    18, 100, value=[18,100], allowCross=False, marks  = None, 
                                    id = "slider-age",
                                    tooltip={"placement": "bottom", "always_visible": True}
                                    )
                            )
                        ],
                ), 
                dbc.Card(
                        [
                            dbc.CardHeader("Fasting duration (mean)"),
                            dbc.CardBody(
                                [
                                    html.Div(html.H4(id='length-fast-text'), className="card_info"),
                                ]
                            ),
                        ],
                    )
                ], className="card-container",
            ),
            html.Div([
                html.Div(
                    dcc.Dropdown(
                        id=f'dropdown-heatmap-Y',
                        options=[{"label": str(param), "value": param } for param in correlation_params],
                        value="weight (kg) change",
                        clearable=False,
                        searchable=False,
                    )
                    ,id = "dropY-div"
                ),
                html.Div(
                    children=[
                            html.Div(
                                id ="heatmap-graph-Y",
                                className='dropdown-content',
                                children=[
                                    html.Div(id=f"Y-menu-div-{i}") for i in range(1, 42)
                                ])
                            ], id = "Y-heatmap-div"
                        
                    ),
                html.Div(id= "blank-div"),	
                dcc.Graph(
                    id = 'graph-2',
                    config={
                    "displayModeBar": True,
                    'displaylogo': False,
                    "modeBarButtonsToRemove" :["toImage","zoom2d", "pan2d","select2d",
                                    "zoomIn2d", "zoomOut2d", "autoScale2d", "resetScale2d",
                                    "hoverClosestCartesian", "hoverCompareCartesian", 
                                    "toggleSpikelines", "resetViews"],

                }),
                html.Div([
                    html.Div(
                        dcc.Dropdown(
                            id=f'dropdown-heatmap-X',
                            options=[{"label": param, "value":param } for param in correlation_params],
                            value='baseline of the parameter',
                            clearable=False,
                            searchable=False,
                            style={"width": "48vw","font-size": "13px"},
                        )
                    , id = "dropX-div"),
                    html.Div(
                        children=[
                            html.Div(
                                id ="heatmap-graph-X",
                                className='dropdown-content',
                                children=[
                                    html.Div(id=f"X-menu-div-{i}") for i in range(1, 42)
                                ])
                            ], id = "X-heatmap-div"
                    ),
                # html.Div(dcc.Graph(id = 'heatmap-graph', config={"displayModeBar": False} ), id = "heatmap-div"),
                ])
            ], id = "div-graph-2"),

            html.Div([
                # dash_echarts.DashECharts(
                #     id = "visualMap-id", 
                # ),  

                # html.Div([
                    # html.Img(src="data:image/svg+xml;charset=utf-8,<svg xmlns='http://www.w3.org/2000/svg' width='25' height='25' viewBox='0 0 24 24'><path fill='none' stroke='black' stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M12 5v14m6-6l-6 6m-6-6l6 6'/></svg>"),
                    # html.P("Correlation with the parameter selected : click on a parameter the Y-axis of the graph."),
                    # html.Img(src="data:image/svg+xml;charset=utf-8,<svg xmlns='http://www.w3.org/2000/svg' width='25' height='25' viewBox='0 0 24 24'><path fill='none' stroke='black' stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M12 5v14m6-6l-6 6m-6-6l6 6'/></svg>"),
                # ], style = {"text-align": "center", "font-size": "12px", "display":"flex", "justify-content":"center"}),
                # html.Div(dcc.Graph(id = 'heatmap-graph', config={"displayModeBar": False} ), id = "heatmap-div"),
            ], className="div-heatmap",    
            ),

    ])
