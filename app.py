from dash import Dash
import layout
import callbacks_register

app = Dash(__name__)

# Import layout from layout.py
app.layout = layout.layout

# Register callbacks from callbacks.py
callbacks_register.register_callbacks(app)

app.run()