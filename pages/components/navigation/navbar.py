from dash import html
import dash_bootstrap_components as dbc

def render():
    LOGO = "https://play-lh.googleusercontent.com/IVU_FKFhyYp_jYkTS-brlgAsxdIrcELBetfa3QsuRjtsAd-h_YJXskvpkJ41hZ6Q24c"

    navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Home", href="/")),
            dbc.NavItem(dbc.NavLink("Data", href="datatable")),
        ],
        brand="Tarot Dashboard",
        brand_href="#",
        className="top-navbar",
    )

    return navbar