from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
from pages.components import ids
import datetime as dt

def render(data) -> html.Div():
    @callback(
        Output(ids.TABLE_TAKER, "children"),
        [Input(ids.SEASON_DROPDOWN, "value"), Input(ids.TAKER_DROPDOWN, "value"), Input(ids.CONTRACT_DROPDOWN, "value"), Input(ids.DATE_DROPDOWN, "value")]
    )
    def update_barchart(seasons, takers, contracts, dates):
        filtered_data = data.query("saison in @seasons and preneur in @takers and prise in @contracts and date in @dates")
        if filtered_data.shape[0] == 0:
            return html.Div("No data selected")

        table_taker = filtered_data.groupby(["preneur"]).sum().reset_index()[["preneur","contrat_rempli","count"]].sort_values(by="count", ascending=False)
        table_taker.columns = ["Joueur", "contrat_rempli", "Prises"]
        table_taker["Réussies"] = round(table_taker.contrat_rempli/table_taker.Prises*100,0).astype(int).astype(str) + "%"
        table_taker = table_taker.drop(["contrat_rempli"], axis=1)


        table = dbc.Table.from_dataframe(table_taker, striped=True, bordered=False, hover=True, responsive=True)

        return html.Div(table, id=ids.TABLE_TAKER, className="chart-table")

    return html.Div(id=ids.TABLE_TAKER)