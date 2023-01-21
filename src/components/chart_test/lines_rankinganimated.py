from dash import Dash, dcc, html, Input, Output
import plotly.express as px
from src.components import ids
import plotly.graph_objects as go

def render(app: Dash, data) -> html.Div():
    @app.callback(
        Output(ids.LINES_RANKING_ANIMATED, "children"),
        [Input(ids.SEASON_DROPDOWN, "value"), Input(ids.TAKER_DROPDOWN, "value"), Input(ids.CONTRACT_DROPDOWN, "value")]
    )
    def update_barchart(seasons, takers, contracts):
        filtered_data = data.query("saison in @seasons and preneur in @takers and prise in @contracts")
        filtered_data["points_cumules"] = filtered_data.groupby(["joueur"])["points"].cumsum()

        if filtered_data.shape[0] == 0:
            return html.Div("No data selected")

        antoine = go.Scatter(x=filtered_data[filtered_data.joueur == "Antoine"]['main'][:2],
                            y=filtered_data[filtered_data.joueur == "Antoine"]['points_cumules'][:2],
                            mode='lines',
                            line=dict(width=1.5))
        martin = go.Scatter(x=filtered_data[filtered_data.joueur == "Martin"]['main'][:2],
                            y=filtered_data[filtered_data.joueur == "Martin"]['points_cumules'][:2],
                            mode='lines',
                            line=dict(width=1.5))
        lulu = go.Scatter(x=filtered_data[filtered_data.joueur == "Lulu"]['main'][:2],
                            y=filtered_data[filtered_data.joueur == "Lulu"]['points_cumules'][:2],
                            mode='lines',
                            line=dict(width=1.5))
        seb = go.Scatter(x=filtered_data[filtered_data.joueur == "Seb"]['main'][:2],
                            y=filtered_data[filtered_data.joueur == "Seb"]['points_cumules'][:2],
                            mode='lines',
                            line=dict(width=1.5))
        simon = go.Scatter(x=filtered_data[filtered_data.joueur == "Simon"]['main'][:2],
                            y=filtered_data[filtered_data.joueur == "Simon"]['points_cumules'][:2],
                            mode='lines',
                            line=dict(width=1.5))

        frames = [dict(data=[dict(type='scatter',
                                  x=filtered_data[filtered_data.joueur == "Antoine"]['main'][:k + 1],
                                  y=filtered_data[filtered_data.joueur == "Antoine"]['points_cumules'][:k + 1]),
                             dict(type='scatter',
                                  x=filtered_data[filtered_data.joueur == "Martin"]['main'][:k + 1],
                                  y=filtered_data[filtered_data.joueur == "Martin"]['points_cumules'][:k + 1]),
                             dict(type='scatter',
                                  x=filtered_data[filtered_data.joueur == "Lulu"]['main'][:k + 1],
                                  y=filtered_data[filtered_data.joueur == "Lulu"]['points_cumules'][:k + 1]),
                             dict(type='scatter',
                                  x=filtered_data[filtered_data.joueur == "Seb"]['main'][:k + 1],
                                  y=filtered_data[filtered_data.joueur == "Seb"]['points_cumules'][:k + 1]),
                             dict(type='scatter',
                                  x=filtered_data[filtered_data.joueur == "Simon"]['main'][:k + 1],
                                  y=filtered_data[filtered_data.joueur == "Simon"]['points_cumules'][:k + 1]),
                             ],
                       traces=[0, 1, 2, 3, 4],
                       ) for k in range(1, len(filtered_data[filtered_data.joueur == "Antoine"]) - 1)]

        layout = go.Layout(
                           showlegend=True,
                           hovermode='x unified',
                           updatemenus=[
                               dict(
                                   type='buttons', showactive=False,
                                   y=1.05,
                                   x=1.15,
                                   xanchor='right',
                                   yanchor='middle',
                                   pad=dict(t=0, r=10),
                                   buttons=[dict(label='Play',
                                                 method='animate',
                                                 args=[None,
                                                       dict(frame=dict(duration=5,
                                                                       redraw=False),
                                                            transition=dict(duration=0),
                                                            fromcurrent=True,
                                                            mode='immediate')]
                                                 )]
                               ),
                           ]
                           )

        layout.update(xaxis=dict(range=[filtered_data.main.min(), filtered_data.main.max()], autorange=False),
                      yaxis=dict(range=[filtered_data.points_cumules.min(), filtered_data.points_cumules.max()], autorange=False))

        fig = go.Figure(data=[antoine, martin, seb, lulu, simon], frames=frames, layout=layout)
        fig.update_layout(xaxis_title="Main", yaxis_title="Points")

        return html.Div(dcc.Graph(figure=fig), id=ids.LINES_RANKING_ANIMATED)

    return html.Div(id=ids.LINES_RANKING_ANIMATED)