import random

import pandas as pd

from config import NUM_TRASPORTATORI, RANDOM_SEED
from generator.utils import (
    generate_id,
    load_comuni,
    save_csv
)

random.seed(RANDOM_SEED)

# ============================
# Costanti
# ============================

from config import (
    COMPANY_PREFIX,
    COMPANY_SUFFIX
)

SUFFIX = [
    "S.r.l.",
    "S.p.A."
]


# ============================
# Funzioni
# ============================

def generate_company_name(comune: str) -> str:

    prefix = random.choice(COMPANY_PREFIX)
    suffix = random.choice(COMPANY_SUFFIX)

    return f"{prefix} {comune} {suffix}"


def generate_partita_iva() -> str:
    """
    Genera una partita IVA fittizia di 11 cifre.
    """
    prima_cifra = str(random.randint(1, 9))

    altre_cifre = "".join(
        str(random.randint(0, 9))
        for _ in range(10)
    )

    return prima_cifra + altre_cifre


def generate_partner(partner_number: int, comuni: pd.DataFrame) -> dict:
    """
    Genera un trasportatore.
    """

    localita = comuni.sample(1).iloc[0]

    return {
        "id_trasportatore": generate_id("T", partner_number),
        "ragione_sociale": generate_company_name(localita["comune"]),
        "partita_iva": generate_partita_iva(),
        "comune": localita["comune"],
        "provincia": localita["provincia"],
        "sigla": localita["sigla"],
        "regione": localita["regione"]
    }


def generate():
    """
    Genera il dataset dei trasportatori.
    """

    comuni = load_comuni()

    partners = []

    nomi_utilizzati = set()
    partite_iva_utilizzate = set()

    for i in range(1, NUM_TRASPORTATORI + 1):

        while True:

            partner = generate_partner(i, comuni)

            if (
                partner["ragione_sociale"] not in nomi_utilizzati
                and partner["partita_iva"] not in partite_iva_utilizzate
            ):
                nomi_utilizzati.add(partner["ragione_sociale"])
                partite_iva_utilizzate.add(partner["partita_iva"])
                partners.append(partner)
                break

    df = pd.DataFrame(partners)

    df = df[
        [
            "id_trasportatore",
            "ragione_sociale",
            "partita_iva",
            "comune",
            "provincia",
            "sigla",
            "regione"
        ]
    ]

    save_csv(df, "archivio_partner.csv")

    return df


def main():

    df = generate()

    print(df.head())

    print()
    print(f"Trasportatori generati: {len(df)}")

    print(df.columns)


if __name__ == "__main__":
    main()