from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import pandas as pd
import dash_echarts
from callbacks_register import update_sex_pie
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
        'EWB (0-10) change', 'PWB (0-10) change','AP (µkat/l) change','GOT (µkat/l) change', 'GPT (µkat/l) change', 'GGT (µkat/l) change',
        'Na (mmol/l) change', 'Ca (mmol/l) change',  'K (mmol/l) change','Mg (mmol/l) change','PTT (sec) change', 'Erythrocytes (106/µl) change',
        'Creatinine (µmol/l) change', 'Urea (mmol/l) change', 'Quick (%) change',
        'Thrombocytes (103/µl) change', 'ESR 1h change', 
        'CRP (mg/l) change', 'ESR 2h change', 'Leucocytes (103/µl) change', 'MCH (pg) change','MCV (fl) change', 'MCHC (g/dl) change',
        'Haematocrit (%) change',  'Haemoglobin (mmol/l) change','INR change']
    text_header = """ 
    The largest scientific study on the effects of therapeutic fasting was conducted at the Buchinger Wilhelmi Clinic in Überlingen, Germany. 
    The scientific team looked at data from 1,422 people who completed a fasting program lasting between 4 to 21 days. 
    The results of the study were published in the scientific journal PLOS ONE on January 2, 2019. This interactive dashboard uses the data from this study to help people understand the effects of long-term fasting.
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
    text_corr = """The chart above shows how different factors are connected in our study. The colours in the horizontal menu indicate how strongly each factor is linked (correlated) to the one chosen on the vertical axis."""
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
                dcc.Store(id='data-store', data= json_matrix),
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
                            dbc.CardBody(html.Div(dash_echarts.DashECharts(id = "sex-pie-chart", option = update_sex_pie([])), id = "sex-div"))
                ]
                ),
                dbc.Card([
                            dbc.CardHeader("Age (mean)"),
                            dbc.CardBody([html.Div(html.H4(id='age-text'), className="card_info")]),
                            dbc.CardFooter(
                                dcc.RangeSlider(
                                    18, 100, value=[18,100], allowCross=False, marks  = None, 
                                    id = "slider-age",
                                    step=1,  # Ajoutez cette propriété pour définir le saut à 1
                                    tooltip={"placement": "bottom", "always_visible": True}
                                    )
                            )
                        ],
                ), 
                dbc.Card(
                        [
                        dbc.CardHeader("Fasting duration (mean)"),
                        dbc.CardBody(
                            [html.Div(html.H4(id='length-fast-text'), className="card_info")]
                            ),
                        dbc.CardFooter(
                            dcc.RangeSlider(
                                3, 23, value=[3,23], allowCross=False, marks  = None, 
                                id = "slider-fast",
                                tooltip={"placement": "bottom", "always_visible": True}
                                )
                        )
                        ],
                    )
                ], className="card-container",
            ),
            html.Div([
                html.Div(id = "updiv-Y"), 
                html.Div(
                    dcc.Dropdown(
                        id=f'dropdown-heatmap-Y',
                        options=[{"label": str(param), "value": param } for param in correlation_params],
                        value="weight (kg) change",
                        clearable=False,
                        searchable=False,
                    ), id = "dropY-div"
                ),
                html.Div(
                    children=[
                            html.Div(
                                id ="heatmap-graph-Y",
                                className='dropdown-content',
                                children=[
                                    html.Div(id=f"Y-menu-div-{i}", className = "div-menu") for i in range(1, 45)
                                ]
                                )
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
                    html.Div([
                        html.Div(
                            id=f'updiv-X',
                            style={"width": "48vw","font-size": "13px", "z-index": 1000},
                        ), 
                        dcc.Dropdown(
                            id = "dropdown-heatmap-X", 
                            options=[{"label": param, "value":param } for param in correlation_params],
                            value='baseline of the parameter',
                            clearable=False,
                            searchable=False,
                            style={"width": "48vw","font-size": "13px"},
                        )
                    ], id = "dropX-div"
                    ),
                    html.Div(
                        children=[
                            html.Div(
                                id ="heatmap-graph-X",
                                className='dropdown-content',
                                children=[
                                    html.Div(id=f"X-menu-div-{i}", className = "div-menu") for i in range(1, 45)
                                ])
                            ], id = "X-heatmap-div"
                    ),
                ])
            ], id = "div-graph-2"),
            html.Div(html.P(f"{text_corr}"), className="header-container"), 
            html.Div(style = {"height": "100px"}), 
            html.Footer(id = "footer", 
                        children = [
                            html.Div(style = {"height": "40px"}),
                            html.H5("Contact"),
                            dcc.Markdown("Wilhelm-Beck-Str. 27 &nbsp | &nbsp 88662 Überlingen &nbsp | &nbsp Germany", id = "markdown-footer-1"),
                            dcc.Markdown("Tel: +49 7551 807-0  &nbsp | &nbsp Fax: +49 7551 807-100", id = "markdown-footer-2"),
                            html.A("https://www.buchinger-wilhelmi.com/", href="https://www.buchinger-wilhelmi.com/", target="_blank"),
                            html.Div(style = {"height": "64px"})
                                    ] 
            )

    ])
