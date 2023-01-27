from dash import Dash, dcc, html, Input, Output
import plotly.express as px
from src.components import ids
import datetime as dt
import plotly.graph_objects as go

def render(app: Dash, data) -> html.Div():
    player_color = {
        "Seb": "rgba(128, 255, 168, 0.5)",
        "Martin": "rgba(128, 191, 255, 0.5)",
        "Antoine": "rgba(255, 179, 128, 0.5)",
        "Lulu": "rgba(226, 179, 255, 0.5)",
        "Simon": "rgba(255, 128, 128, 0.5)"
    }

    @app.callback(
        Output(ids.SANKEY_CHART, "children"),
        [Input(ids.SEASON_DROPDOWN, "value"), Input(ids.TAKER_DROPDOWN, "value"), Input(ids.CONTRACT_DROPDOWN, "value"), Input(ids.DATE_DROPDOWN, "value")]
    )
    def update_barchart(seasons, takers, contracts, dates):
        filtered_data = data.query("saison in @seasons and preneur in @takers and prise in @contracts and date in @dates")
        if filtered_data.shape[0] == 0:
            return html.Div("No data selected")

        # data
        label = ["Antoine", "Lulu", "Martin", "Seb", "Simon", "Antoine", "Lulu", "Martin", "Seb", "Simon", "Seul", "Perdu", "Réussi"]
        source = [0, 0, 0, 0, 0,
                  1, 1, 1, 1, 1,
                  2, 2, 2, 2, 2,
                  3, 3, 3, 3, 3,
                  4, 4, 4, 4, 4,
                  5, 5,
                  6, 6,
                  7, 7,
                  8, 8,
                  9, 9,
                  10, 10]
        target = [6, 7, 8, 9, 10,
                  5, 7, 8, 9, 10,
                  5, 6, 8, 9, 10,
                  5, 6, 7, 9, 10,
                  5, 6, 7, 8, 10,
                  11, 12,
                  11, 12,
                  11, 12,
                  11, 12,
                  11, 12,
                  11, 12]

        value_teammate = filtered_data.groupby(["preneur"]).teammate.value_counts().reset_index(name="teamcount").sort_values(["preneur","teammate"]).teamcount.to_list()
        value_reussite = filtered_data.groupby(["teammate"]).contrat_rempli.value_counts().reset_index(name="teamcount").sort_values(["teammate", "contrat_rempli"]).teamcount.to_list()
        value = value_teammate + value_reussite

        color_link = [
            player_color["Antoine"], player_color["Antoine"], player_color["Antoine"], player_color["Antoine"], player_color["Antoine"],
            player_color["Lulu"], player_color["Lulu"], player_color["Lulu"], player_color["Lulu"], player_color["Lulu"],
            player_color["Martin"], player_color["Martin"], player_color["Martin"], player_color["Martin"], player_color["Martin"],
            player_color["Seb"], player_color["Seb"], player_color["Seb"], player_color["Seb"], player_color["Seb"],
            player_color["Simon"], player_color["Simon"], player_color["Simon"], player_color["Simon"], player_color["Simon"],
            player_color["Antoine"], player_color["Antoine"],
            player_color["Lulu"], player_color["Lulu"],
            player_color["Martin"], player_color["Martin"],
            player_color["Seb"], player_color["Seb"],
            player_color["Simon"], player_color["Simon"],
            "rgba(154, 154, 154, 0.59)", "rgba(154, 154, 154, 0.59)"
        ]

        color_node= [
            player_color["Antoine"],
            player_color["Lulu"],
            player_color["Martin"],
            player_color["Seb"],
            player_color["Simon"],
            player_color["Antoine"],
            player_color["Lulu"],
            player_color["Martin"],
            player_color["Seb"],
            player_color["Simon"],
            "rgba(154, 154, 154, 0.83)",
            "red",
            "green"
        ]

        # data to dict, dict to sankey
        link = dict(source=source, target=target, value=value, color=color_link,)
        node = dict(label=label, pad=20, thickness=20, color=color_node)
        sankey = go.Sankey(link=link, node=node)

        fig = go.Figure(sankey)

        return html.Div(dcc.Graph(figure=fig), id=ids.SANKEY_CHART)

    return html.Div(id=ids.SANKEY_CHART)