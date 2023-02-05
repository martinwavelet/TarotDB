from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
from src.components import ids
import datetime as dt

def render(app: Dash, data) -> html.Div():
    @app.callback(
        Output(ids.DUO_PERF, "children"),
        [Input(ids.SEASON_DROPDOWN, "value"), Input(ids.TAKER_DROPDOWN, "value"), Input(ids.CONTRACT_DROPDOWN, "value"), Input(ids.DATE_DROPDOWN, "value")]
    )
    def update_barchart(seasons, takers, contracts, dates):
        filtered_data = data.query("saison in @seasons and preneur in @takers and prise in @contracts and date in @dates")
        if filtered_data.shape[0] == 0:
            return html.Div("No data selected")

        filtered_data = filtered_data[filtered_data.teammate != "zSeul"]
        processed_data = filtered_data.groupby(["preneur", "teammate"])["count", "contrat_rempli"].sum().reset_index()
        equipe=[]
        p1=[]
        p2=[]
        for _, row in processed_data.iterrows():
            preneur = row.preneur
            teammate = row.teammate
            team = sorted([row.preneur, row.teammate])
            print(team)
            equipe.append(team)
            p1.append(team[0])
            p2.append(team[1])

        processed_data["equipe"] = equipe
        processed_data["p1"] = p1
        processed_data["p2"] = p2

        final_data = processed_data.groupby(["p1", "p2"])["count", "contrat_rempli"].sum().reset_index()
        final_data["taux_victoire"] = final_data["contrat_rempli"] / final_data["count"]
        total_hand = final_data["count"].sum()
        final_data["taux_occurence"] = final_data["count"] / total_hand
        final_data = final_data.sort_values("taux_victoire", ascending=False)


        return html.Div([
            dbc.Col([
                # Winner stats
                html.H4("Les boss", className="text-center mt-2"),
                html.Br(),
                dbc.Row([
                    dbc.Col([
                        html.Img(src=f"/assets/img/round_cards/{final_data.iloc[0, 0].lower()}.png",
                                 className="duo-img-boss"),
                        html.Img(src=f"/assets/img/round_cards/{final_data.iloc[0, 1].lower()}.png",
                                 className="duo-img-boss-2"),
                        html.P(f"{round(final_data.iloc[0, 4] * 100, 1)}% de réussite", className="duo-text")
                    ], width=12, lg=6),

                    dbc.Col([
                        html.Img(src=f"/assets/img/round_cards/{final_data.iloc[1, 0].lower()}.png",
                                 className="duo-img-boss"),
                        html.Img(src=f"/assets/img/round_cards/{final_data.iloc[1, 1].lower()}.png",
                                 className="duo-img-boss-2"),
                        html.P(f"{round(final_data.iloc[1, 4] * 100, 1)}% de réussite", className="duo-text")
                    ], width=12, lg=6)
                ]),

                html.Br(),

                # Looser stats
                html.H4("Les flops", className="text-center mt-2"),
                html.Br(),
                dbc.Row([
                    dbc.Col([
                        html.Img(src=f"/assets/img/round_cards/{final_data.iloc[-1, 0].lower()}.png",
                                 className="duo-img-flop"),
                        html.Img(src=f"/assets/img/round_cards/{final_data.iloc[-1, 1].lower()}.png",
                                 className="duo-img-flop-2"),
                        html.P(f"{round(final_data.iloc[-1, 4] * 100, 1)}% de réussite", className="duo-text")
                    ], width=12, lg=6),

                    dbc.Col([
                        html.Img(src=f"/assets/img/round_cards/{final_data.iloc[-2, 0].lower()}.png",
                                 className="duo-img-flop"),
                        html.Img(src=f"/assets/img/round_cards/{final_data.iloc[-2, 1].lower()}.png",
                                 className="duo-img-flop-2"),
                        html.P(f"{round(final_data.iloc[-2, 4] * 100, 1)}% de réussite", className="duo-text")
                    ], width=12, lg=6)
                ]),
            ])


        ], id=ids.DUO_PERF)

    return html.Div(id=ids.DUO_PERF)