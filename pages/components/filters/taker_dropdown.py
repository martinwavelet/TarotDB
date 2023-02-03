import dash_bootstrap_components as dbc
import pandas as pd
from dash import Dash, html, dcc, callback
from dash.dependencies import Input, Output

from pages.components import ids


def render(data: pd.DataFrame) -> html.Div():
    all_takers = data.preneur.unique().tolist()

    @callback(
        Output(ids.TAKER_DROPDOWN, "value"),
        Input(ids.SELECT_ALL_TAKER_BUTTON, "n_clicks")
    )
    def select_all_takers(_: int) -> list[str]:
        return all_takers

    return html.Div(
        children=[
            dbc.Label("Preneur"),
            html.Div(
                [
                    dcc.Dropdown(
                        id=ids.TAKER_DROPDOWN,
                        multi=True,
                        options=[{"label": taker, "value": taker} for taker in all_takers],
                        value=all_takers
                    ),
                    dbc.Button(
                        id=ids.SELECT_ALL_TAKER_BUTTON,
                        color="dark",
                        outline=True,
                        size="sm",
                        children=["All"]
                    )
                ],
                className="filter-input"
            )
        ]
    )
