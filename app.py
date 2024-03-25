from dash import Dash
import layout
import callbacks_register

app = Dash(__name__,
        suppress_callback_exceptions=True, 
        meta_tags = [{"name": "viewport", "content": "width=device-width, initial-scale=1.0",}],
        external_scripts=["https://cdn.jsdelivr.net/npm/apexcharts"])

# Import dbc from dash_bootstrap_components
# Wrap the layout in dbc.Container
app.layout = layout.layout

# Register callbacks from callbacks.py
callbacks_register.register_callbacks(app)

app.run(host = "0.0.0.0", debug = True, port = 8051)