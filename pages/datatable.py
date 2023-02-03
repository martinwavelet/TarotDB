import dash_bootstrap_components as dbc
import pandas as pd
from dash import html, dcc, register_page, dash_table, callback, Output, Input, ctx
from pages.data.loader import load_tarot_data, unpivot_tarot_data
from datetime import date

DATA_PATH = "./data/tarot_dataset.csv"

data = load_tarot_data(DATA_PATH)
unpivot_data = unpivot_tarot_data(data)

register_page(__name__)
data["Datestr"] = data["date"].dt.strftime('%Y-%m-%d')
df = data[["saison", "Datestr", "main", "preneur", "prise", "contrat_rempli", "Antoine", "Simon", "Lulu", "Seb", "Martin"]]
df.columns = ["Saison", "Date", "Main", "Preneur", "Prise", "Contrat rempli", "Antoine", "Simon", "Lulu", "Seb", "Martin"]
df = df.sort_values(by="Main", ascending=False)

total_points = 91
points_needed_bouts = {
    "0": 56,
    "1": 51,
    "2": 41,
    "3": 36
}
contract_multiplier = {
    "Petite": 1,
    "Garde": 2,
    "Garde sans": 4,
    "Garde contre": 6,
}
success_contract_points = 25

layout = html.Div([
    dbc.Container([
        dbc.Card([
            html.H4("Jeu de données", className="mb-0 text-center"),

            html.Br(),

            dbc.Row([
                dbc.Col([
                    dbc.Label("Preneur"),
                    dcc.Dropdown(
                        id="taker-selection",
                        multi=False,
                        options=[{"label": taker, "value": taker} for taker in df.Preneur.unique().tolist()])
                ], width=2),

                dbc.Col([
                    dbc.Label("Coéquipier"),
                    dcc.Dropdown(
                        id="teammate-selection",
                        multi=False,
                        options=[{"label": taker, "value": taker} for taker in df.Preneur.unique().tolist()+['0']])
                ], width=2),

                dbc.Col([
                    dbc.Label("Contrat"),
                    dcc.Dropdown(
                        id="contract-selection",
                        multi=False,
                        options=[{"label": prise, "value": prise} for prise in df.Prise.unique().tolist()]),
                ], width=2),

                dbc.Col([
                    dbc.Label("Nombre de bouts"),
                    dcc.Dropdown(
                        id="bout-selection",
                        multi=False,
                        options=[{"label": bout, "value": bout} for bout in ["0", "1", "2", "3"]]),
                ], width=2),

                dbc.Col([
                    dbc.Label("Points marqués"),
                    dcc.Input(
                        id="points-input",
                        type="number")
                ], width=2),


                dbc.Col([
                    dbc.Button("+", n_clicks=0, id="add-btn"),
                ], width=1),

                dbc.Col([
                    dbc.Button("Save data", n_clicks=0, id="save-btn"),
                ], width=1)
            ]),

            html.Hr(),

            dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns], id="table-score", row_deletable=True, editable=True)

        ], body=True, className="graph-card")

    ], fluid=True)

])

@callback(
    Output("table-score", "data"),
    Input("add-btn", "n_clicks"),
    Input("table-score", "data"),
    Input("taker-selection", "value"),
    Input("teammate-selection", "value"),
    Input("contract-selection", "value"),
    Input("bout-selection", "value"),
    Input("points-input", "value"),
    prevent_initial_call=True
)
def add_row(n_clicks, rows, taker, teammate, contract, bout, points):

    df_order = pd.DataFrame(rows)
    if ctx.triggered_id == "add-btn":
        earned_points = points - points_needed_bouts[bout]
        if earned_points >= 0:
            contract_point = (success_contract_points + earned_points) * contract_multiplier[contract]
        else:
            contract_point = -(success_contract_points - earned_points) * contract_multiplier[contract]

        if teammate != "0":
            not_player = ["Antoine", "Lulu", "Seb", "Martin", "Simon"]
            not_player.remove(taker)
            not_player.remove(teammate)
            dict_points = dict((player, -contract_point) for player in not_player)
            dict_points[taker] = 2 * contract_point
            dict_points[teammate] = contract_point
        else:
            not_player = ["Antoine", "Lulu", "Seb", "Martin", "Simon"]
            not_player.remove(taker)
            dict_points = dict((player, -contract_point) for player in not_player)
            dict_points[taker] = 4 * contract_point

        new_line = {
            "Saison": "Saison 3",
            "Date": date.today().strftime("%Y-%m-%d"),
            "Main": df_order.Main.max()+1,
            "Preneur": taker,
            "Prise": contract,
            "Contrat rempli": 0 if contract_point < 0 else 1,
            "Antoine": dict_points["Antoine"],
            "Simon": dict_points["Simon"],
            "Lulu": dict_points["Lulu"],
            "Seb": dict_points["Seb"],
            "Martin": dict_points["Martin"]
        }

        df_new_order_line = pd.DataFrame(new_line, index=[0])

        # df_order = df_order.append(df_new_order_line, ignore_index=True)
        df_order = pd.concat([df_new_order_line, df_order])

    return df_order.to_dict("records")