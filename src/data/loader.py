import pandas as pd

def load_tarot_data(path):
    data = pd.read_csv(
        path,
        parse_dates=["date"],
        infer_datetime_format=True)
    data["count"] = 1

    return data

def unpivot_tarot_data(data):
    unpivot_data = pd.melt(
        data,
        id_vars=["main", "date", "saison", "prise", "preneur", "contrat_rempli"],
        value_vars=["Antoine","Simon","Lulu","Seb","Martin"],
        var_name="joueur",
        value_name="points"
    )

    return unpivot_data