import pandas as pd
from dash import Dash, html
from src.components import season_dropdown, barchart_taker, lines_ranking, taker_dropdown, table_taker, table_contract, contract_dropdown, ranking
from src.components.navigation import navbar
import dash_bootstrap_components as dbc

def create_layout(app: Dash, data: pd.DataFrame, unpivot_data):
    return dbc.Container([
            # NAVBAR
            navbar.render(),
            html.Br(),

            # FILTRES
            dbc.Card([
                dbc.Row([
                    dbc.Col(html.H4("FILTRES", className="mb-0"), width=12, align="center", lg=1),
                    dbc.Col(season_dropdown.render(app, data), width=12, lg=3),
                    dbc.Col(taker_dropdown.render(app, data), width=12, lg=4),
                    dbc.Col(contract_dropdown.render(app, data), width=12, lg=4)
                ], align="center"
            )], body=True),
            html.Br(),

            # RANKING
            ranking.render(app, unpivot_data),
            html.Br(),

            # LINES
            dbc.Card([
                html.H4("Evolution du nombre de points par main et par joueur", className="mb-0 text-center"),
                lines_ranking.render(app, unpivot_data)
            ], body=True),
            html.Br(),

            # TAKERS
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        html.H4("Nombre de prises par joueur", className="mb-0 text-center"),
                        html.Br(),
                        table_taker.render(app, data)
                    ], body=True)
                ], width=12, lg=3),

                dbc.Col([
                    dbc.Card([
                        html.H4("Type de prises par joueur", className="mb-0 text-center"),
                        barchart_taker.render(app, unpivot_data)
                    ], body=True)
                ], width=12, lg=6),

                dbc.Col([
                    dbc.Card([
                        html.H4("Nombre de contrats réalisés", className="mb-0 text-center"),
                        html.Br(),
                        table_contract.render(app, data)
                    ], body=True)
                ], width=12, lg=3),
            ]),
            html.Br()
        ],
    fluid=True
    )