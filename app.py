from dash import Dash
import layout
import callbacks_register

app = Dash(__name__,
        suppress_callback_exceptions=True, 
        meta_tags = [{"name": "viewport", "content": "width=device-width, initial-scale=1.0",}],
        external_scripts=["https://cdn.jsdelivr.net/npm/apexcharts"], 
        external_stylesheets=["https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&display=swap",]
        )
# Import dbc from dash_bootstrap_components
# Wrap the layout in dbc.Container
app.layout = layout.layout

# Register callbacks from callbacks.py
callbacks_register.register_callbacks(app)

app.run(host = "0.0.0.0", debug = False, port = 8051)