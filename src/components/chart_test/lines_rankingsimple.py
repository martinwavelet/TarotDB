from dash import Dash, dcc, html, Input, Output
import plotly.express as px
from src.components import ids

def render(app: Dash, data) -> html.Div():
    @app.callback(
        Output(ids.LINES_RANKING, "children"),
        [Input(ids.SEASON_DROPDOWN, "value"), Input(ids.TAKER_DROPDOWN, "value"), Input(ids.CONTRACT_DROPDOWN, "value")]
    )
    def update_linechart(seasons, takers, contracts):
        filtered_data = data.query("saison in @seasons and preneur in @takers and prise in @contracts")
        filtered_data["points_cumules"] = filtered_data.groupby(["joueur"])["points"].cumsum()

        if filtered_data.shape[0] == 0:
            return html.Div("No data selected")

        fig = px.line(filtered_data, x="main", y="points_cumules", color="joueur")
        fig.update_layout(
            hovermode='x unified'
        )
        return html.Div(dcc.Graph(figure=fig), id=ids.LINES_RANKING)

    return html.Div(id=ids.LINES_RANKING)