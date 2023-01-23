from dash import Dash, dcc, html, Input, Output
import plotly.express as px
from src.components import ids

def render(app: Dash, data, mode) -> html.Div():
    id = ids.LINES_RANKING_POINTS if mode == "points" else ids.LINES_RANKING_RANK

    color_map = {
        "Seb": "#80ffa8",
        "Martin": "#80bfff",
        "Antoine": "#ffb380",
        "Lulu": "#e2b3ff",
        "Simon": "#ff8080"
    }

    @app.callback(
        Output(id, "children"),
        [Input(ids.SEASON_DROPDOWN, "value"), Input(ids.TAKER_DROPDOWN, "value"), Input(ids.CONTRACT_DROPDOWN, "value")]
    )
    def update_linechart(seasons, takers, contracts):
        filtered_data = data.query("saison in @seasons and preneur in @takers and prise in @contracts")
        filtered_data["points_cumules"] = filtered_data.groupby(["joueur"])["points"].cumsum()
        filtered_data["Classement"] = filtered_data.groupby(["main"])["points_cumules"].rank("dense")

        if filtered_data.shape[0] == 0:
            return html.Div("No data selected")

        fig = px.line(filtered_data, x="main", y="points_cumules" if mode == "points" else "Classement", color="joueur", color_discrete_map=color_map)
        fig.update_layout(hovermode='x unified')
        fig.update_layout(legend_title="Joueurs")

        return html.Div(dcc.Graph(figure=fig), id=id)

    return html.Div(id=id)