from dash import Dash, dcc, html, Input, Output
from pages.components import ids
from raceplotly.plots import barplot

def render(app: Dash, data) -> html.Div():
    @app.callback(
        Output(ids.LINES_RANKING, "children"),
        Input(ids.SEASON_DROPDOWN, "value")
    )
    def update_barchart(seasons):
        filtered_data = data.query("saison in @seasons")
        filtered_data["points_cumules"] = filtered_data.groupby(["joueur"])["points"].cumsum()
        filtered_data["points_cumules"] = filtered_data["points_cumules"] + 6000

        if filtered_data.shape[0] == 0:
            return html.Div("No data selected")

        raceplot = barplot(filtered_data,
                              item_column='joueur',
                              value_column='points_cumules',
                              time_column='main')

        fig = raceplot.plot(title = 'Top 10 Crops from 1961 to 2018',
                 item_label = 'Top 10 crops',
                 value_label = 'Production quantity (tonnes)',
                 frame_duration = 100,)

        return html.Div(dcc.Graph(figure=fig), id=ids.LINES_RANKING)

    return html.Div(id=ids.LINES_RANKING)