from dash import html, Input, Output
import dash_bootstrap_components as dbc
from src.components import ids
import random

def render(app, data):
    @app.callback(
        Output(ids.RANKING_CARDS, "children"),
        [Input(ids.SEASON_DROPDOWN, "value"), Input(ids.TAKER_DROPDOWN, "value"), Input(ids.CONTRACT_DROPDOWN, "value")]
    )
    def render_cards(seasons, takers, contracts):
        filtered_data = data.query("saison in @seasons and preneur in @takers and prise in @contracts")
        if filtered_data.shape[0] == 0:
            return html.Div("No data selected")

        def render_card(filtered_data, rank):
            ranks = filtered_data.groupby("joueur")["points"].sum().reset_index().sort_values(by="points", ascending=False)
            player_name = ranks.iloc[rank-1,0]
            player_points = ranks.iloc[rank-1,1]
            player_take_rate = round(filtered_data[filtered_data.preneur == player_name].main.nunique()/filtered_data.main.nunique()*100,1)
            player_take_success_rate = round(filtered_data[(filtered_data.preneur == player_name) & (filtered_data.contrat_rempli == 1)].main.nunique()/filtered_data[filtered_data.preneur == player_name].main.nunique()*100,1)
            player_citation = {
                "Martin" : ["Le roi déchu", "Tu connais RocketLeague ?", "Mauvais perdant"],
                "Seb" : ["Le portugais volant", "Jamais sans son thé", "SIUUUUUUUUUUUUUU", "Le roi caché"],
                "Simon" : ["On attend encore qu'il joue ...", "Bob le bricoleur", "Le leader d'Hugo"],
                "Lulu" : ["Gare au courroux du dragon", "La cisaille", "Plus personne a d'atout ?", "Pose clope"],
                "Antoine" : ["J'ai toujours rêvé de faire ça !", "N'appelle pas carreau", "Meilleur sur sorare qu'ici"]
            }
            rank_color = {
                1 : "#ffd700",
                2 : "#868992",
                3 : "#d17a52",
                4 : "#b3382f",
                5 : "#d10000"
            }

            card = dbc.Card(
                [
                    # dbc.Row(
                    #     [
                            dbc.Col(
                                dbc.CardImg(
                                    src=f"/assets/img/{player_name}.png",
                                    # src="https://picsum.photos/1000/700",
                                    className="img-fluid",
                                    style={'height': '100%', 'object-fit': 'cover'}
                                ),
                                className="col-md-4",
                                style={'height': '100%'}
                            ),
                            dbc.Col(
                                dbc.CardBody(
                                    [
                                        html.H4(f"#{rank} {player_name}", style={'color': rank_color[rank]}, className="card-title"),
                                        html.P([
                                            f"{player_points} pts", html.Br(),
                                            f"{player_take_rate}% de prises ", html.Br(),
                                            f"{player_take_success_rate}% de prises réussies"],
                                            className="card-text",
                                        ),
                                        html.Small(
                                            f"{random.choice(player_citation[player_name])}",
                                            className="card-text text-muted",
                                        ),
                                    ]
                                ),
                                className="col-md-8",
                        #     ),
                        # ],
                        # className="g-0 d-flex align-items-center",
                    )
                ],
                className="d-flex",
                style={"flex-direction": "row"}
            )
            return card

        cards = dbc.CardGroup([render_card(filtered_data, n) for n in range(1,6)], id=ids.RANKING_CARDS)

        return cards
    return dbc.Row(dbc.Col(html.Div(id=ids.RANKING_CARDS)))