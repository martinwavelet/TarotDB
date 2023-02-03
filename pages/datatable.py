import dash_bootstrap_components as dbc
import pandas as pd
from dash import Dash, html, dcc, register_page, dash_table
from pages.data.loader import load_tarot_data, unpivot_tarot_data


DATA_PATH = "./data/tarot_dataset.csv"

data = load_tarot_data(DATA_PATH)
unpivot_data = unpivot_tarot_data(data)

register_page(__name__)



layout = html.Div([
    dbc.Card([
        html.H4("TEST PAGE"),
        dash_table.DataTable(data.to_dict('records'), [{"name": i, "id": i} for i in data.columns])
    ], className="graph-card")
])
