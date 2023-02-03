from dash import Dash, page_container, html
from dash_bootstrap_components.themes import LUX
from dash_bootstrap_templates import load_figure_template
from pages.components.navigation import navbar

load_figure_template(LUX)

app = Dash(__name__, external_stylesheets=[LUX], use_pages=True)
server = app.server
app.title = "Tarot Du Dimanche"
app.layout = html.Div([
    navbar.render(),
    page_container
])


if __name__ == "__main__":
    app.run_server(debug=False)
