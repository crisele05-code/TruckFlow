import random
from datetime import timedelta
import pandas as pd
from generator.distance import haversine_distance
from config import (
    RANDOM_SEED,
    COMMISSIONE,
    COSTO_KM_MIN,
    COSTO_KM_MAX
)

from generator.utils import (
    generate_id,
    save_csv,
    load_comuni
)

random.seed(RANDOM_SEED)

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_FOLDER = BASE_DIR / "data" / "sorgenti"


def load_data():

    richieste = pd.read_csv(
        DATA_FOLDER / "app_clienti.csv"
    )

    trasportatori = pd.read_csv(
        DATA_FOLDER / "archivio_partner.csv"
    )

    comuni = load_comuni()


    return richieste, trasportatori, comuni

def find_comune(
        comuni: pd.DataFrame,
        nome_comune: str
):
    return comuni[
        comuni["comune"] == nome_comune
        ].iloc[0]

def calculate_km(
        richiesta,
        comuni
):

    origine = find_comune(
        comuni,
        richiesta["comune_origine"]
    )

    destinazione = find_comune(
        comuni,
        richiesta["comune_destinazione"]
    )

    return haversine_distance(

        origine["lat"],
        origine["lon"],

        destinazione["lat"],
        destinazione["lon"]

    )

# Per le tratte inferiori a 100 km viene applicata
# una tariffa minima indipendente dal costo al km.
def calculate_price(distanza_km: float):

    costo_km = round(
        random.uniform(
            COSTO_KM_MIN,
            COSTO_KM_MAX
        ),
        2
    )

    if distanza_km < 100:

        importo = round(
            random.uniform(150, 200),
            2
        )

    else:

        importo = round(
            distanza_km * costo_km,
            2
        )

    commissione = round(
        importo * COMMISSIONE,
        2
    )

    return (
        costo_km,
        importo,
        commissione
    )




def generate_offer(
        offer_number: int,
        richiesta: pd.Series,
        trasportatori: pd.DataFrame,
        comuni: pd.DataFrame
) -> dict:
    """
    Genera un'offerta accettata del marketplace.
    """

    trasportatore = choose_transporter(
        trasportatori
    )

    distanza_km = calculate_km(
        richiesta,
        comuni
    )

    costo_km, importo, commissione = calculate_price(
        distanza_km
    )

    data_richiesta = pd.to_datetime(
        richiesta["data_richiesta"]
    )

    data_offerta = (
        data_richiesta +
        timedelta(
            days=random.randint(0, 2)
        )
    )

    return {

        "id_offerta":
            generate_id(
                "O",
                offer_number
            ),

        "id_richiesta":
            richiesta["id_richiesta"],

        "id_trasportatore":
            trasportatore["id_trasportatore"],

        "data_offerta":
            data_offerta.strftime("%Y-%m-%d"),

        "distanza_km":
            distanza_km,

        "costo_km":
            costo_km,

        "importo_offerto":
            importo,

        "commissione":
            commissione,

        "stato_offerta":
            "Accettata"

    }

def choose_transporter(
        trasportatori: pd.DataFrame
):
    """
    Seleziona casualmente un trasportatore.
    """

    return trasportatori.sample(
        1
    ).iloc[0]


def generate():

    richieste, trasportatori, comuni = load_data()

    offerte = []

    offer_number = 1

    for _, richiesta in richieste.iterrows():

        # Le richieste annullate non arrivano al marketplace
        if richiesta["stato_richiesta"] == "ANNULLATA":
            continue

        offerta = generate_offer(
            offer_number=offer_number,
            richiesta=richiesta,
            trasportatori=trasportatori,
            comuni=comuni
        )

        offerte.append(offerta)

        offer_number += 1

    df = pd.DataFrame(offerte)

    save_csv(
        df,
        "marketplace.csv"
    )

    return df


def main():

    df = generate()

    print("\nPrime 10 offerte:\n")

    print(df.head(10))

    print()

    print(
        f"Offerte generate: {len(df)}"
    )


if __name__ == "__main__":
    main()