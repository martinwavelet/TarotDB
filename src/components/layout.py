import pandas as pd
from dash import Dash, html
from src.components import season_dropdown, barchart_taker, lines_ranking, taker_dropdown, contract_dropdown, ranking
from src.components.navigation import navbar
import dash_bootstrap_components as dbc

def create_layout(app: Dash, data: pd.DataFrame, unpivot_data):
    return dbc.Container([
            navbar.render(),
            html.Br(),
            dbc.Card([dbc.Row([
                dbc.Col(html.H4("FILTRES", className="mb-0"), width=12, align="center", lg=1),
                dbc.Col(season_dropdown.render(app, data), width=12, lg=3),
                dbc.Col(taker_dropdown.render(app, data), width=12, lg=4),
                dbc.Col(contract_dropdown.render(app, data), width=12, lg=4)
                ], align="center"
            )], body=True),
            html.Br(),
            ranking.render(app, unpivot_data),
            lines_ranking.render(app, unpivot_data),
            barchart_taker.render(app, data)
        ],
    fluid=True
    )