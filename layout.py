import dash_daq as daq 
from dash import html, dcc
import dash_bootstrap_components as dbc


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
        'glucose (mmol/l)', 'puls (beats/min)', 'waist (cm)',
        'weight (kg)']
    text_header = """ 
    It was conducted at Buchinger Wilhelmi, a well-established fasting clinic, by a team led by Dr. Françoise Wilhelmi de Toledo and with the support of many of our guests and patients.
    The study collected and evaluated data from 1,422 who completed the Buchinger Wilhelmi fasting programme over a period of 5, 10, 15 or 20 days in 2016. \n

    The results of the study were published online on January 2, 2019 in the peer-reviewed journal PLOS ONE under the title “Safety, health improvement and well-being during a 4 to 21-day fasting period in an observational study including 1422 subjects

    We present an interactive dashboard that leverages the data gathered in this study, offering a dynamic and user-friendly interface for comprehending the outcomes of long-term fasting.
    """
    section_text_1 = """
    Physicians gathered clinical data, and trained nurses recorded participants' body weight each morning, following a standardized protocol. Blood pressure and pulse were measured in a seated position on the non-dominant arm. Abdominal circumference was determined using a measuring tape placed midway between the lowest rib and the iliac crest.    """

    section_text_2 = """
    In order to assess well-being, participants under the supervision of nurses provided daily self-reports of their physical well-being and emotional well-being using numeric rating scales ranging from 0 (very bad) to 10 (excellent). The objective was to record the tolerance levels of the fasting program.
    """
    section_text_3 = """
    The participants independently measured the levels of ketone bodies in their first-morning urine by employing Ketostix. Ketone bodies serve as indicators of fat burning, reflecting a shift in energy metabolism from utilizing dietary energy sources to the process of burning stored fats for energy.
    """
    section_text_4 = """
    Blood analysis was conducted following international protocols to understand what are the effects of long-term fasting on lipid profiles, glycemic markers, and blood count metrics to coagulation factors, liver function indicators, inflammatory biomarkers, renal function measures, and electrolyte levels.
    """

    clinical_param = ['weight (kg)','BMI (kg/m²)','waist (cm)','SBP (mmHg)','DBP (mmHg)','puls (beats/min)']
    well_being = ['PWB (0-10)','EWB (0-10)']
    ketones = ['Acetoacetic acid (mg/dL)']
    blood_analysis = list(set(all_param) - set(clinical_param) - set(well_being) - set(ketones))
    parameters = [clinical_param, well_being, ketones, blood_analysis]
    def add_switch(id_graph):
        return html.Div(
            [
                daq.ToggleSwitch(
                    id = f"switch-{id_graph}",
                    label='show changes',
                    labelPosition='right',
                    value = False
                ),
                daq.ToggleSwitch(
                    id = f"switch-selected-{id_graph}",
                    label='show comparaison with selected data',
                    labelPosition='right', 
                    value = False
                )
            ], style = {"display": "flex"})
        
    def add_box_div(id_graph, section_title, section_text, even = True): 
        graph_div = html.Div(
                        children = [
                            html.H5(section_title), 
                            dcc.Dropdown(
                                id=f'parameter-dropdown-{id_graph}',
                                options=[
                                    {'label': param, 'value': param} for param in parameters[int(id_graph)-1]
                                    ]
                                ,
                                value=parameters[int(id_graph)-1][0]
                            ),
                            add_switch(id_graph),
                            dcc.Graph(id=f'graph-{id_graph}',config={"displayModeBar": False}),
                        ]
                    )
        text_div = html.Div(html.P(section_text))
        div_even = html.Div([graph_div, text_div], className="row")
        div_odd = html.Div([text_div, graph_div], className="row")
        if even:
            return div_even
        return div_odd


    return html.Div([
            dcc.Store(id='store-selected-data'),
                html.Img(src="assets/BW_logo.svg", alt="BW_logo", width="200px", id = "logo"),
            html.Div([
                html.H3("World largest Study on the fasting", id="header-title"),
                html.H6(f"{text_header}"),
                html.H6(id='study-characteristics'),
            ], className="header-container"),

            html.Div([
                add_box_div("1", "Clinical measurements", section_text_1), 
                add_box_div("2", "Well-being", section_text_2, even = False), 
                add_box_div("3", "Urine analysis", section_text_3), 
                add_box_div("4", "Blood analysis", section_text_4, even = False), 

            ], className="graph-container-1"),

            html.Div([
            dcc.Slider(0, 1, 0.01, value=0.20, marks=None,
                       id = "slider-heatmap",
                tooltip={"placement": "bottom", "always_visible": True})

            ]),
            html.Div([
                html.Div(dcc.Graph(id = 'heatmap-graph'), id = "heatmap"),
                html.Div(dcc.Graph(id = 'graph-5')),
            ], className="div-heatmap", 
            style={'width': '100%', 
                   'height':'1000',
                   'padding': '10'}),
        ])
