from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
from src.components import ids

def render(app: Dash, data) -> html.Div():
    @app.callback(
        Output(ids.TABLE_TAKER, "children"),
        [Input(ids.SEASON_DROPDOWN, "value"), Input(ids.TAKER_DROPDOWN, "value"), Input(ids.CONTRACT_DROPDOWN, "value")]
    )
    def update_barchart(seasons, takers, contracts):
        filtered_data = data.query("saison in @seasons and preneur in @takers and prise in @contracts")
        if filtered_data.shape[0] == 0:
            return html.Div("No data selected")

        table_taker = filtered_data.preneur.value_counts().reset_index()
        table_taker.columns = ['Joueur', 'Prises']
        table_taker["%"] = round(filtered_data.preneur.value_counts().reset_index().preneur/sum(filtered_data.preneur.value_counts().reset_index().preneur)*100,1)

        table = dbc.Table.from_dataframe(table_taker, striped=True, bordered=False, hover=True, responsive=True)

        return html.Div(table, id=ids.TABLE_TAKER)

    return html.Div(id=ids.TABLE_TAKER)