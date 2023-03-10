import dash_bootstrap_components as dbc
import pandas as pd
from dash import Dash, html, dcc
from dash.dependencies import Input, Output

from src.components import ids


def render(app: Dash, data: pd.DataFrame) -> html.Div():
    all_contracts = data.prise.unique().tolist()

    @app.callback(
        Output(ids.CONTRACT_DROPDOWN, "value"),
        Input(ids.SELECT_ALL_CONTRACT_BUTTON, "n_clicks")
    )
    def select_all_contracts(_: int) -> list[str]:
        return all_contracts

    return html.Div(
        children=[
            dbc.Label("Contrat"),
            html.Div(
                [
                    dcc.Dropdown(
                        id=ids.CONTRACT_DROPDOWN,
                        multi=True,
                        options=[{"label": contract, "value": contract} for contract in all_contracts],
                        value=all_contracts),
                    dbc.Button(
                        id=ids.SELECT_ALL_CONTRACT_BUTTON,
                        color="dark",
                        outline=True,
                        size="sm",
                        children=["All"])
                ],
                className="filter-input"
            )
        ]
    )
