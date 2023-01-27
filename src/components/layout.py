import dash_bootstrap_components as dbc
import pandas as pd
from dash import Dash, html, dcc

from src.components.chart import barchart_taker, table_taker, ranking, table_contract, lines_ranking, sankey_chart, global_cards
from src.components.chart_test import lines_rankinganimated
from src.components.filters import filters
from src.components.navigation import navbar


def create_layout(app: Dash, data: pd.DataFrame, unpivot_data):
    return html.Div([
        navbar.render(),
        dbc.Container(
            dbc.Row([
                dbc.Col([
                    filters.render(app, data),
                    html.Hr(),
                    global_cards.render(app, data),
                    html.Hr(),

                    dbc.Card([
                        dbc.Row([
                            dbc.Col(html.Img(src=f"/assets/img/fft.png", className="img-fluid"), width=3,
                                    lg=3, style={"margin": "auto"}),
                            dbc.Col([
                                dbc.Row(html.H4("Remerciements FFT")),
                                dbc.Row(html.P("Nous remercions chaleuresement la Fédération Française de Tarot, représenté tous les dimanches soirs par Antoine. Ils nous apportent clareté et justice lorsque les plus perfides d'entre nous cherchent l'entourloupe.")),
                                dbc.Row(html.A("N'hésitez pas à consulter les règles officielles.", href="https://fftarot.fr/assets/documents/Reglement%20FFT.pdf"))
                            ], width=12, lg=9)
                        ])
                    ], className="fft-card"),

                html.Br(),
                ], width=12, lg=3),
                dbc.Col(
                    [
                        # RANKING
                        ranking.render(app, unpivot_data),
                        html.Br(),

                        # LINES
                        dbc.Tabs([
                            dbc.Tab(
                                dbc.Card([
                                    html.H4("Evolution du nombre de points par main et par joueur",
                                            className="mb-0 text-center"),
                                    lines_ranking.render(app, unpivot_data, "points")
                                ], body=True, className="graph-card"), label="Points", tabClassName="ms-auto tab-lines",
                            ),

                            dbc.Tab(
                                dbc.Card([
                                    html.H4("Evolution du nombre de points par main et par joueur",
                                            className="mb-0 text-center"),
                                    lines_ranking.render(app, unpivot_data, "classement")
                                ], body=True, className="graph-card"), label="Classement", tabClassName="tab-lines",
                            ),

                            dbc.Tab(
                                dbc.Card([
                                    html.H4("Evolution du nombre de points par main et par joueur",
                                            className="mb-0 text-center"),
                                    lines_rankinganimated.render(app, unpivot_data)
                                ], body=True, className="graph-card"), label="Animated", tabClassName="tab-lines",
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
                                ], body=True, className="graph-card", style={"height": "100%"})
                            ], width=12, lg=3),

                            dbc.Col([
                                dbc.Card([
                                    html.H4("Type de prises par joueur", className="mb-0 text-center"),
                                    barchart_taker.render(app, unpivot_data)
                                ], body=True, className="graph-card", style={"height": "100%"})
                            ], width=12, lg=6),

                            dbc.Col([
                                dbc.Card([
                                    html.H4("Nombre de contrats réalisés", className="mb-0 text-center"),
                                    html.Br(),
                                    table_contract.render(app, data)
                                ], body=True, className="graph-card", style={"height": "100%"})
                            ], width=12, lg=3),
                        ]),
                        html.Br(),

                        dbc.Card([
                            html.H4("Mais avec qui tu joues ?",
                                    className="mb-0 text-center"),
                            dbc.Row([
                                dbc.Col(html.P("Preneur"), width=4, className="text-center mt-2"),
                                dbc.Col(html.P("Coéquipier"), width=4, className="text-center mt-2"),
                                dbc.Col(html.P("Réussite"), width=4, className="text-center mt-2"),
                            ]),
                            sankey_chart.render(app, data)
                        ], body=True, className="graph-card"),
                    html.Br(),
                    ], width=12, lg=9
                )
            ]),
            fluid=True
        ),
    ])
