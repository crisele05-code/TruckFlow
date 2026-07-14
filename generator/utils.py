"""
Funzioni di utilità per il progetto TruckFlow.
Tutti i generatori utilizzeranno queste funzioni.
"""

from pathlib import Path

import pandas as pd
from faker import Faker

from config import FAKER_LOCALE
import random
from datetime import datetime, timedelta


fake = Faker(FAKER_LOCALE)

BASE_DIR = Path(__file__).resolve().parent.parent
COMUNI_FILE = BASE_DIR / "data" / "anagrafiche" / "comuni_italiani.csv"

OUTPUT_FOLDER = BASE_DIR / "data" / "sorgenti"

COORDINATE_FILE = BASE_DIR / "data" / "anagrafiche" / "gi_comuni.csv"


# =====================================================
# COMUNI
# =====================================================

def load_comuni() -> pd.DataFrame:
    """
    Carica l'anagrafica dei comuni italiani e la integra
    con le coordinate geografiche.

    Restituisce un DataFrame con:

    - codice_istat
    - comune
    - provincia
    - sigla
    - regione
    - lat
    - lon
    """

    # ==========================
    # Dataset ISTAT
    # ==========================

    comuni = pd.read_csv(
        COMUNI_FILE,
        sep=";",
        encoding="cp1252"
    )

    comuni = comuni.rename(
        columns={
            "Codice Comune formato numerico": "codice_istat",
            "Denominazione in italiano": "comune",
            "Denominazione provincia": "provincia",
            "Sigla automobilistica": "sigla",
            "Denominazione regione": "regione"
        }
    )

    comuni = comuni[
        [
            "codice_istat",
            "comune",
            "provincia",
            "sigla",
            "regione"
        ]
    ]

    comuni = comuni.dropna()

    comuni["codice_istat"] = comuni["codice_istat"].astype(int)

    # ==========================
    # Coordinate
    # ==========================

    coordinate = pd.read_csv(
        COORDINATE_FILE,
        sep=";"
    )

    coordinate = coordinate.rename(
        columns={
            "codice_istat": "codice_istat",
            "denominazione_ita": "comune_coordinate"
        }
    )

    coordinate = coordinate[
        [
            "codice_istat",
            "lat",
            "lon"
        ]
    ]

    coordinate["codice_istat"] = (
        coordinate["codice_istat"]
        .astype(int)
    )

    coordinate["lat"] = (
        coordinate["lat"]
        .astype(str)
        .str.replace(",", ".")
        .astype(float)
    )

    coordinate["lon"] = (
        coordinate["lon"]
        .astype(str)
        .str.replace(",", ".")
        .astype(float)
    )

    # ==========================
    # Merge
    # ==========================

    comuni = comuni.merge(
        coordinate,
        on="codice_istat",
        how="left"
    )

    comuni = comuni.dropna(
        subset=[
            "lat",
            "lon"
        ]
    ).reset_index(drop=True)

    return comuni

def generate_id(prefix: str, number: int) -> str:
    """
    Genera un identificativo.

    Esempio:
    C000001
    """
    return f"{prefix}{number:06d}"

def save_csv(df: pd.DataFrame, file_name: str) -> None:
    """
    Salva un DataFrame nella cartella data/sorgenti.
    """

    OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

    file_path = OUTPUT_FOLDER / file_name

    df.to_csv(file_path, index=False)


def generate_partita_iva() -> str:
    """
    Genera una Partita IVA fittizia di 11 cifre.
    """

    prima_cifra = str(random.randint(1, 9))

    altre_cifre = "".join(
        str(random.randint(0, 9))
        for _ in range(10)
    )

    return prima_cifra + altre_cifre

def random_date(start_date: datetime, end_date: datetime) -> datetime:
    """
    Genera una data casuale compresa tra start_date ed end_date.
    """

    delta = end_date - start_date

    giorni = random.randint(0, delta.days)

    return start_date + timedelta(days=giorni)

