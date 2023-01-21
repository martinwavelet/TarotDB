import pandas as pd
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
from src.components import ids
import dash_bootstrap_components as dbc


def render(app: Dash, data: pd.DataFrame) -> html.Div():
    all_seasons = data.saison.unique().tolist()

    @app.callback(
        Output(ids.SEASON_DROPDOWN, "value"),
        Input(ids.SELECT_ALL_SEASON_BUTTON, "n_clicks")
    )
    def select_all_seasons(_: int) -> list[str]:
        return all_seasons


    return html.Div(
        children=[
            dbc.Label("Saison"),
            dbc.Row([
                dbc.Col([dcc.Dropdown(
                    id=ids.SEASON_DROPDOWN,
                    multi=True,
                    options=[{"label": season, "value": season} for season in all_seasons],
                    value=all_seasons)], width=9),
                dbc.Col([dbc.Button(
                    id=ids.SELECT_ALL_SEASON_BUTTON,
                    color="dark",
                    outline=True,
                    size="sm",
                    children=["All"])], width=3, style={"display" : "flex", "place-items": "center"})
                    ])

        ]
    )