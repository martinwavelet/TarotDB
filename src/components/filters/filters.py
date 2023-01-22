import dash_bootstrap_components as dbc
from dash import html

from src.components.filters import season_dropdown, taker_dropdown, contract_dropdown


def render(app, data):
    return html.Div(
        [
            dbc.Col(season_dropdown.render(app, data)),
            dbc.Col(taker_dropdown.render(app, data)),
            dbc.Col(contract_dropdown.render(app, data))
        ],
        className="filters"
    ),
