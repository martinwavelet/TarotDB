from dash import Dash, dcc, html, Input, Output
import plotly.express as px
from src.components import ids

def render(app: Dash, unpivot_data) -> html.Div():
    @app.callback(
        Output(ids.BARCHART_TAKER, "children"),
        [Input(ids.SEASON_DROPDOWN, "value"), Input(ids.TAKER_DROPDOWN, "value"), Input(ids.CONTRACT_DROPDOWN, "value")]
    )
    def update_barchart(seasons, takers, contracts):
        filtered_data = unpivot_data.query("saison in @seasons and preneur in @takers and prise in @contracts")
        if filtered_data.shape[0] == 0:
            return html.Div("No data selected")

        contracts_by_player = filtered_data.groupby(["preneur", "prise"]).main.nunique().reset_index()
        contracts_by_player["Percentage"] = filtered_data.groupby(["preneur", "prise"]).main.nunique().groupby(level=0).apply(lambda x:100 * x/float(x.sum())).values
        contracts_by_player["Percentage"] = round(contracts_by_player['Percentage'], 1)
        contracts_by_player.columns = ["preneur", "prise", "n", "%"]

        color_map={
            "Petite": "#D4EFDF",
            "Garde": "#7DCEA0",
            "Garde sans": "#229954",
            "Garde contre": "#145A32"
        }
        fig = px.bar(contracts_by_player, x="preneur", y="%", color="prise", barmode="stack", color_discrete_map=color_map,
                     text="%", category_orders={"prise":["Petite", "Garde", "Garde sans", "Garde contre"]})
        fig.update_layout(legend_orientation="h", legend_title ="Contrats", legend_tracegroupgap=20, xaxis_title=None)
        fig.update_traces(texttemplate='%{text}%')
        fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')

        return html.Div(dcc.Graph(figure=fig), id=ids.BARCHART_TAKER)

    return html.Div(id=ids.BARCHART_TAKER)