from dash import Dash, dcc, html, Input, Output
import plotly.express as px
from pages.components import ids

def render(app: Dash, data) -> html.Div():
    @app.callback(
        Output(ids.BARCHART_TAKER, "children"),
        [Input(ids.SEASON_DROPDOWN, "value"), Input(ids.TAKER_DROPDOWN, "value"), Input(ids.CONTRACT_DROPDOWN, "value")]
    )
    def update_barchart(seasons, takers, contracts):
        filtered_data = data.query("saison in @seasons and preneur in @takers and prise in @contracts")
        if filtered_data.shape[0] == 0:
            return html.Div("No data selected")
        fig = px.histogram(filtered_data, x="preneur", y="count", color="prise")
        return html.Div(dcc.Graph(figure=fig), id=ids.BARCHART_TAKER)

    return html.Div(id=ids.BARCHART_TAKER)