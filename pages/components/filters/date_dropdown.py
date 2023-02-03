import dash_bootstrap_components as dbc
import pandas as pd
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
from pages.components import ids

def render(data: pd.DataFrame) -> html.Div():
    all_dates = data.date.dt.strftime("%Y-%m-%d").unique().tolist()

    return html.Div(
        children=[
            dbc.Label("Date"),
            html.Div(
                [
                    dcc.Dropdown(
                        id=ids.DATE_DROPDOWN,
                        options=[{"label": date, "value": date} for date in all_dates],
                        value=all_dates)
                ],
                className="filter-input"
            )
        ]
    )
