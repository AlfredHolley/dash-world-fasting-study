import dash
from dash import dcc, html, clientside_callback, Input, Output, State
import pandas as pd
correlation_matrix = pd.read_excel("data/correlation_matrix.xlsx", index_col=0)
json_matrix = [correlation_matrix.to_dict()]

app = dash.Dash(__name__)

# Styles CSS similaires au code HTML précédent
app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

app.layout = html.Div(
    children=[
        dcc.Store(id='data-store', data={'matrix': json_matrix}),
        html.Div(
            className='dropdown', 
            children=[
                html.P('Produits', id='dropdown-link'),
                html.Div(
                    id ="output-div",
                    className='dropdown-content',
                    children=[
                        html.Div(id=f"div-{i}") for i in range(1, 42)
                    ])
            ]
        ),
    html.Button('Afficher la première ligne', id='show-button'),

    html.Div(id='content', style={'margin-top': '20px', 'padding': '10px', 'background-color': '#eee'}),
    html.Div(id='content-2', style={'margin-top': '20px', 'padding': '10px', 'background-color': '#eee'}),

])

app.clientside_callback(
    """
    function(contentId, ...timestamps) {

        timestamps = timestamps.map(timestamp => timestamp || 0);
        var highestTimestamp = Math.max(...timestamps);
        var clicked_id = null;

        for (var i = 1; i <= timestamps.length; i++) {
            if (timestamps[i - 1] === highestTimestamp) {
                clicked_id = 'div-' + i;
                break;
            }
        }
        console.log('Clicked ID:', clicked_id);

        if (clicked_id) {
            var contentElement = document.getElementById(contentId);
            var clickedContent = document.getElementById(clicked_id);
            if (contentElement && clickedContent) {
                contentElement.innerHTML = 'Contenu récupéré : ' + clickedContent.textContent.trim();
            }
        }
    }
    """,
    Output('dropdown-heatmap-X', 'value'),
    Input('dropdown-heatmap-X', 'id'),
    [Input(f'menu-div-{i}', 'n_clicks_timestamp') for i in range(1, 42)],
)
@app.callback(
    Output('output-div', 'children'),
    [State('data-store', 'data')]
)
def update_output_div(data):
    def get_background_color(value):
        # Map the absolute value to a color intensity between 0 (white) and 255 (red)
        intensity = int(255 * abs(value))
        return f'rgba(0, 0,255, {intensity/400})'

    data = data['matrix']
    filtered_data_dict = {key: round(float(value),2) for key, value in data[0].get("baseline of the parameter").items() if not str(value) =="None"}
    sorted_data_dict = dict(sorted(filtered_data_dict.items(), key=lambda item: abs(item[1]), reverse=True))

    children = [
        html.Div(
            html.P(f'{content[0]} : {content[1]}'),
            id=f'div-{i+1}',
            className='div-menu',
            style={'background-color': get_background_color(content[1])}
        )
        for i, content in enumerate(sorted_data_dict.items())
    ]
    return children

@app.callback(
    Output('dropdown-heatmap-X', 'value'),
    State('data-store', 'data')
)
def update_output_div(data):

if __name__ == '__main__':
    app.run_server(debug=True)
