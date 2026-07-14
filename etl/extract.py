import pandas as pd


from paths import SOURCE_DIR


def extract_app_clienti():

    return pd.read_csv(
        SOURCE_DIR / "app_clienti.csv"
    )


def extract_partner():

    return pd.read_csv(
        SOURCE_DIR / "archivio_partner.csv"
    )


def extract_marketplace():

    return pd.read_csv(
        SOURCE_DIR / "marketplace.csv"
    )


def extract_clienti():

    return pd.read_csv(
        SOURCE_DIR / "clienti.csv"
    )


def extract_all():

    return {

        "app_clienti": extract_app_clienti(),

        "partner": extract_partner(),

        "marketplace": extract_marketplace(),

        "clienti": extract_clienti()

    }

def main():

    data = extract_all()

    print()

    for nome, df in data.items():

        print(f"{nome}: {len(df)} record")

    print()