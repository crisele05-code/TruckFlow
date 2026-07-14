"""
transform.py

Esegue le trasformazioni dei dati necessarie
per il caricamento delle dimensioni del
Data Warehouse TruckFlow.

Autore: Crisele Ariola
Project Work PW21
"""

from extract import (
    extract_clienti,
    extract_partner,
    extract_app_clienti,
    extract_marketplace
)

from generator.utils import load_comuni
import pandas as pd

from datetime import timedelta

MESI = {
    1: "Gennaio",
    2: "Febbraio",
    3: "Marzo",
    4: "Aprile",
    5: "Maggio",
    6: "Giugno",
    7: "Luglio",
    8: "Agosto",
    9: "Settembre",
    10: "Ottobre",
    11: "Novembre",
    12: "Dicembre"
}

GIORNI = {
    1: "Lunedì",
    2: "Martedì",
    3: "Mercoledì",
    4: "Giovedì",
    5: "Venerdì",
    6: "Sabato",
    7: "Domenica"
}

# =====================================================
# DIM_CLIENTE
# =====================================================

def transform_dim_cliente():
    """
    Trasforma l'anagrafica clienti.
    """

    clienti = extract_clienti()

    clienti = clienti.drop(
        columns=["profilo"],
        errors="ignore"
    )

    clienti = clienti.drop_duplicates(
        subset=["id_cliente"]
    )

    return clienti


# =====================================================
# DIM_TRASPORTATORE
# =====================================================

def transform_dim_trasportatore():
    """
    Trasforma l'anagrafica trasportatori.
    """

    trasportatori = extract_partner()

    trasportatori = trasportatori.drop_duplicates(
        subset=["id_trasportatore"]
    )

    return trasportatori


# =====================================================
# DIM_VEICOLO
# =====================================================

def transform_dim_veicolo():
    """
    Estrae i tipi di veicolo.
    """

    richieste = extract_app_clienti()

    veicoli = (
        richieste[["tipo_veicolo"]]
        .drop_duplicates()
        .sort_values("tipo_veicolo")
        .reset_index(drop=True)
    )

    return veicoli


# =====================================================
# DIM_MERCE
# =====================================================

def transform_dim_merce():
    """
    Estrae le categorie merce.
    """

    richieste = extract_app_clienti()

    merci = (
        richieste[["categoria_merce"]]
        .drop_duplicates()
        .sort_values("categoria_merce")
        .reset_index(drop=True)
    )

    return merci




# =====================================================
# DIM_LOCALITA
# =====================================================

def transform_dim_localita():
    """
    Costruisce la dimensione delle località.
    """

    comuni = load_comuni()

    comuni = comuni.drop_duplicates(
        subset=["codice_istat"]
    )

    comuni = comuni.sort_values(
        by="codice_istat"
    )

    comuni = comuni.reset_index(
        drop=True
    )

    return comuni

# =====================================================
# DIM_TEMPO
# =====================================================

def transform_dim_tempo():
    """
    Costruisce la dimensione temporale.
    """

    app = extract_app_clienti()
    marketplace = extract_marketplace()

    date = pd.concat([
        app["data_richiesta"],
        app["data_consegna_prevista"],
        marketplace["data_offerta"]
    ])

    date = pd.to_datetime(date)

    data_min = date.min()
    data_max = date.max()

    calendario = pd.date_range(
        start=data_min,
        end=data_max,
        freq="D"
    )

    dim_tempo = pd.DataFrame({
        "data": calendario
    })

    dim_tempo["giorno"] = dim_tempo["data"].dt.day

    dim_tempo["mese"] = dim_tempo["data"].dt.month
    dim_tempo["nome_mese"] = dim_tempo["mese"].map(MESI)

    dim_tempo["trimestre"] = dim_tempo["data"].dt.quarter

    dim_tempo["anno"] = dim_tempo["data"].dt.year

    dim_tempo["giorno_settimana"] = dim_tempo["data"].dt.weekday + 1
    dim_tempo["nome_giorno"] = dim_tempo["giorno_settimana"].map(GIORNI)

    dim_tempo["weekend"] = (
        dim_tempo["giorno_settimana"]
        .isin([6, 7])
        .astype(int)
    )

    dim_tempo["data"] = dim_tempo["data"].dt.strftime("%Y-%m-%d")

    return dim_tempo