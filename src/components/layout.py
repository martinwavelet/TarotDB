import pandas as pd
from dash import Dash, html
from src.components.filters import taker_dropdown, season_dropdown, contract_dropdown
from src.components.chart import barchart_taker, table_taker, ranking, table_contract, lines_ranking
from src.components.chart_test import lines_rankinganimated
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
                    dbc.Col(width=12, align="center", lg=1, className="filters-header"),
                    dbc.Col(season_dropdown.render(app, data), width=12, lg=3),
                    dbc.Col(taker_dropdown.render(app, data), width=12, lg=4),
                    dbc.Col(contract_dropdown.render(app, data), width=12, lg=4)
                ], align="center"
            )], className="filters"),
            html.Hr(),

            # RANKING
            ranking.render(app, unpivot_data),
            html.Br(),

            # LINES
            dbc.Tabs([
                dbc.Tab(
                    dbc.Card([
                        html.H4("Evolution du nombre de points par main et par joueur", className="mb-0 text-center"),
                        lines_ranking.render(app, unpivot_data)
                    ], body=True, className="graph-card"), label="Static", tabClassName="ms-auto",
                ),

                dbc.Tab(
                    dbc.Card([
                        html.H4("Evolution du nombre de points par main et par joueur", className="mb-0 text-center"),
                        lines_rankinganimated.render(app, unpivot_data)
                    ], body=True, className="graph-card"), label="Animated"
                )
            ]),
            html.Br(),

            # TAKERS
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        html.H4("Nombre de prises par joueur", className="mb-0 text-center"),
                        html.Br(),
                        table_taker.render(app, data)
                    ], body=True, className="graph-card")
                ], width=12, lg=3),

                dbc.Col([
                    dbc.Card([
                        html.H4("Type de prises par joueur", className="mb-0 text-center"),
                        barchart_taker.render(app, unpivot_data)
                    ], body=True, className="graph-card")
                ], width=12, lg=6),

                dbc.Col([
                    dbc.Card([
                        html.H4("Nombre de contrats réalisés", className="mb-0 text-center"),
                        html.Br(),
                        table_contract.render(app, data)
                    ], body=True, className="graph-card")
                ], width=12, lg=3),
            ]),
            html.Br()
        ],
    fluid=True
    )