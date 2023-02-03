from dash import Dash, dcc, html, Input, Output, callback
from pages.components import ids
import dash_bootstrap_components as dbc
from datetime import datetime

def render(data) -> html.Div():

    @callback(
        Output(ids.GLOBAL_CARDS, "children"),
        [Input(ids.SEASON_DROPDOWN, "value"), Input(ids.TAKER_DROPDOWN, "value"), Input(ids.CONTRACT_DROPDOWN, "value"), Input(ids.DATE_DROPDOWN, "value")]
    )
    def update_barchart(seasons, takers, contracts, dates):
        filtered_data = data.query("saison in @seasons and preneur in @takers and prise in @contracts and date in @dates")
        if filtered_data.shape[0] == 0:
            return html.Div("No data selected")

        filtered_data["max_points"] = filtered_data[["Antoine", "Simon", "Seb", "Lulu", "Martin"]].values.max(1)
        filtered_data["min_points"] = filtered_data[["Antoine", "Simon", "Seb", "Lulu", "Martin"]].values.min(1)

        sessions_number = filtered_data.date.nunique()
        hands_number = len(filtered_data)
        points_total = filtered_data.max_points.sum()
        largest_win = filtered_data.max_points.max()
        largest_win_player = filtered_data[largest_win == filtered_data.max_points].preneur.values[0]
        largest_win_date = filtered_data[largest_win == filtered_data.max_points].date.values[0].astype(str)[:10]
        largest_loose = filtered_data.min_points.min()
        largest_loose_player = filtered_data[largest_loose == filtered_data.min_points].preneur.values[0]
        largest_loose_date = filtered_data[largest_loose == filtered_data.min_points].date.values[0].astype(str)[:10]

        cards = [
            dbc.Card([
                dbc.Row([
                    dbc.Col(html.Img(src=f"/assets/img/global-cards/calendar.png", className="img-fluid"),  width=3, lg=3),
                    dbc.Col([
                        dbc.Row(html.H4(f"{sessions_number}")),
                        dbc.Row(html.P("Dimanche soirs"))
                    ], width=12, lg=9)
                ])
            ], className="global-card"),

            html.Br(),

            dbc.Card([
                dbc.Row([
                    dbc.Col(html.Img(src=f"/assets/img/global-cards/tarot_cards.png", className="img-fluid"), width=3, lg=3),
                    dbc.Col([
                        dbc.Row(html.H4(f"{hands_number}")),
                        dbc.Row(html.P("Main joués"))
                    ], width=12, lg=9)
                ])
            ], className="global-card"),

            html.Br(),

            dbc.Card([
                dbc.Row([
                    dbc.Col(html.Img(src=f"/assets/img/global-cards/sum.png", className="img-fluid"), width=3, lg=3),
                    dbc.Col([
                        dbc.Row(html.H4(f"{'{:,}'.format(points_total).replace(',', ' ')}")),
                        dbc.Row(html.P("Points gagnés"))
                    ], width=12, lg=9)
                ])
            ], className="global-card"),

            html.Br(),

            dbc.Card([
                dbc.Row([
                    dbc.Col(html.Img(src=f"/assets/img/global-cards/worldcup.gif", className="img-fluid"), width=3, lg=3),
                    dbc.Col([
                        dbc.Row(html.H4(f"+ {'{:,}'.format(largest_win).replace(',', ' ')}")),
                        dbc.Row(html.P(f"Par {largest_win_player} le {largest_win_date}"))
                    ], width=12, lg=9)
                ])
            ], className="global-card"),

            html.Br(),

            dbc.Card([
                dbc.Row([
                    dbc.Col(html.Img(src=f"/assets/img/global-cards/test.gif", className="img-fluid"), width=3, lg=3),
                    dbc.Col([
                        dbc.Row(html.H4(f"{'{:,}'.format(largest_loose).replace(',', ' ')}")),
                        dbc.Row(html.P(f"Par {largest_loose_player} le {largest_loose_date}"))
                    ], width=12, lg=9)
                ])
            ], className="global-card"),

        ]

        return html.Div(cards, id=ids.GLOBAL_CARDS)

    return html.Div(id=ids.GLOBAL_CARDS)