import pandas as pd
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
from src.components import ids
import dash_bootstrap_components as dbc


def render(app: Dash, data: pd.DataFrame) -> html.Div():
    all_takers = data.preneur.unique().tolist()

    @app.callback(
        Output(ids.TAKER_DROPDOWN, "value"),
        Input(ids.SELECT_ALL_TAKER_BUTTON, "n_clicks")
    )
    def select_all_takers(_: int) -> list[str]:
        return all_takers


    return html.Div(
        children=[
            dbc.Label("Preneur"),
            dbc.Row([
                dbc.Col([
                    dcc.Dropdown(
                        id=ids.TAKER_DROPDOWN,
                        multi=True,
                        options=[{"label": taker, "value": taker} for taker in all_takers],
                        value=all_takers
                    )],
                    width=9,
                    lg=10
                ),
                dbc.Col([
                    dbc.Button(
                        id=ids.SELECT_ALL_TAKER_BUTTON,
                        color="dark",
                        outline=True,
                        size="sm",
                        children=["All"]
                    )],
                    width=3,
                    lg=2,
                    style={"display" : "flex", "place-items": "center"})
                ])

        ]
    )