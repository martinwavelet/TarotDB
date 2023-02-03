import dash_bootstrap_components as dbc
from dash import html, dcc

from pages.components.filters import season_dropdown, taker_dropdown, contract_dropdown, date_dropdown


def render(data):
    return html.Div([
        dcc.Input(
            # type='checkbox',
            id="filters-toggle-checkbox",
            name="filters-toggle-checkbox"
        ),
        html.Label(htmlFor="filters-toggle-checkbox", id="filters-toggle"),
        html.Div(
            [
                dbc.Col(season_dropdown.render(data)),
                dbc.Col(taker_dropdown.render(data)),
                dbc.Col(contract_dropdown.render(data)),
                dbc.Col(date_dropdown.render(data))
            ],
            className="filters"
        ),
    ])
