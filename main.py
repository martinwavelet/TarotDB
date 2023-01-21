from dash import Dash, html
from dash_bootstrap_components.themes import LUX
from src.components.layout import create_layout
from src.data.loader import load_tarot_data, unpivot_tarot_data
from dash_bootstrap_templates import load_figure_template

DATA_PATH = "./data/tarot_dataset.csv"
load_figure_template(LUX)


def main() -> None:
    data = load_tarot_data(DATA_PATH)
    unpivot_data = unpivot_tarot_data(data)
    app = Dash(__name__, external_stylesheets=[LUX])
    app.title = "Tarot dashboard"
    app.layout = create_layout(app, data, unpivot_data)
    app.run()


if __name__ == "__main__":
    main()
