import dash_bootstrap_components as dbc
import pandas as pd
from dash import Dash, html, dcc, callback
from dash.dependencies import Input, Output

from pages.components import ids


def render(data: pd.DataFrame) -> html.Div():
    all_seasons = data.saison.unique().tolist()

    @callback(
        Output(ids.SEASON_DROPDOWN, "value"),
        Input(ids.SELECT_ALL_SEASON_BUTTON, "n_clicks")
    )
    def select_all_seasons(_: int) -> list[str]:
        return all_seasons

    return html.Div(
        children=[
            dbc.Label("Saison"),
            html.Div(
                [
                    dcc.Dropdown(
                        id=ids.SEASON_DROPDOWN,
                        multi=True,
                        options=[{"label": season, "value": season} for season in all_seasons],
                        value=all_seasons),
                    dbc.Button(
                        id=ids.SELECT_ALL_SEASON_BUTTON,
                        color="dark",
                        outline=True,
                        size="sm",
                        children=["All"])
                ],
                className="filter-input"
            )
        ]
    )
