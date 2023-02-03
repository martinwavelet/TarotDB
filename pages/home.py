import dash_bootstrap_components as dbc
import pandas as pd
from dash import Dash, html, dcc, register_page

from pages.data.loader import load_tarot_data, unpivot_tarot_data
from pages.components.chart import barchart_taker, table_taker, ranking, table_contract, lines_ranking, sankey_chart, global_cards,duo_perf
from pages.components.chart_test import lines_rankinganimated
from pages.components.filters import filters


DATA_PATH = "./data/tarot_dataset.csv"

data = load_tarot_data(DATA_PATH)
unpivot_data = unpivot_tarot_data(data)

register_page(__name__, path ="/")

layout = html.Div([
        dbc.Container(
            dbc.Row([
                dbc.Col([
                    filters.render(data),
                    html.Hr(),
                    global_cards.render(data),
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
                        ranking.render(unpivot_data),
                        html.Br(),

                        # LINES
                        dbc.Tabs([
                            dbc.Tab(
                                dbc.Card([
                                    html.H4("Evolution du nombre de points par main et par joueur",
                                            className="mb-0 text-center"),
                                    lines_ranking.render(unpivot_data, "points")
                                ], body=True, className="graph-card"), label="Points", tabClassName="ms-auto tab-lines",
                            ),

                            dbc.Tab(
                                dbc.Card([
                                    html.H4("Evolution du nombre de points par main et par joueur",
                                            className="mb-0 text-center"),
                                    lines_ranking.render(unpivot_data, "classement")
                                ], body=True, className="graph-card"), label="Classement", tabClassName="tab-lines",
                            ),

                            dbc.Tab(
                                dbc.Card([
                                    html.H4("Evolution du nombre de points par main et par joueur",
                                            className="mb-0 text-center"),
                                    lines_rankinganimated.render(unpivot_data)
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
                                    table_taker.render(data)
                                ], body=True, className="graph-card", style={"height": "100%"})
                            ], width=12, lg=3),

                            dbc.Col([
                                dbc.Card([
                                    html.H4("Type de prises par joueur", className="mb-0 text-center"),
                                    barchart_taker.render(unpivot_data)
                                ], body=True, className="graph-card", style={"height": "100%"})
                            ], width=12, lg=6),

                            dbc.Col([
                                dbc.Card([
                                    html.H4("Nombre de contrats réalisés", className="mb-0 text-center"),
                                    html.Br(),
                                    table_contract.render(data)
                                ], body=True, className="graph-card", style={"height": "100%"})
                            ], width=12, lg=3),
                        ]),
                        html.Br(),

                        dbc.Card([
                            html.H4("Mais avec qui tu joues ?",
                                    className="mb-0 text-center"),
                            html.Br(),
                            dbc.Row([
                                dbc.Col(html.H4(""), width=4, className="text-center mt-2"),
                                dbc.Col(html.P("Preneur"), width=2, className="text-center mt-2"),
                                dbc.Col(html.P("Coéquipier"), width=4, className="text-center mt-2"),
                                dbc.Col(html.P("Réussite"), width=2, className="text-center mt-2"),
                            ]),
                            dbc.Row([
                                dbc.Col(duo_perf.render(data), width=12, lg=4),
                                dbc.Col(sankey_chart.render(data), width=12, lg=8)
                            ])
                        ], body=True, className="graph-card"),
                    html.Br(),
                    ], width=12, lg=9
                )
            ]),
            fluid=True
        ),
    ])
