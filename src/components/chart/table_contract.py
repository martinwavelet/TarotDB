from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
from src.components import ids

def render(app: Dash, data) -> html.Div():
    @app.callback(
        Output(ids.TABLE_CONTRACT, "children"),
        [Input(ids.SEASON_DROPDOWN, "value"), Input(ids.TAKER_DROPDOWN, "value"), Input(ids.CONTRACT_DROPDOWN, "value")]
    )
    def update_barchart(seasons, takers, contracts):
        filtered_data = data.query("saison in @seasons and preneur in @takers and prise in @contracts")
        if filtered_data.shape[0] == 0:
            return html.Div("No data selected")

        table_contract = filtered_data.groupby(["prise"]).sum().reset_index()[["prise","contrat_rempli","count"]].sort_values(by="count", ascending=False)
        table_contract.columns = ["Contrat", "contrat_rempli", "Prises"]
        table_contract["Réussies"] = round(table_contract.contrat_rempli/table_contract.Prises*100,0).astype(int).astype(str) + "%"
        table_contract = table_contract.drop(["contrat_rempli"], axis=1)

        table = dbc.Table.from_dataframe(table_contract, striped=True, bordered=False, hover=True, responsive=True)

        return html.Div(table, id=ids.TABLE_CONTRACT, className="chart-table")

    return html.Div(id=ids.TABLE_CONTRACT)