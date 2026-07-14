"""
build_fact.py

Costruisce la FACT_SPEDIZIONI a partire
dalle tabelle di staging.

Autore: Crisele Ariola
Project Work PW21
"""

import pandas as pd

from database import create_connection


# =====================================================
# LETTURA TABELLE
# =====================================================

def read_table(
        conn,
        table_name: str
) -> pd.DataFrame:
    """
    Legge una tabella SQLite.
    """

    return pd.read_sql_query(
        f"SELECT * FROM {table_name}",
        conn
    )


# =====================================================
# LOOKUP DIMENSIONI
# =====================================================

def lookup_dimension(
        fact: pd.DataFrame,
        dimensione: pd.DataFrame,
        left_on: str,
        right_on: str,
        surrogate_key: str
) -> pd.DataFrame:
    """
    Aggiunge alla FACT la surrogate key
    di una dimensione.
    """

    fact = fact.merge(

        dimensione[
            [
                surrogate_key,
                right_on
            ]
        ],

        left_on=left_on,
        right_on=right_on,
        how="left"

    )



    return fact


def lookup_tempo(
        fact: pd.DataFrame,
        dim_tempo: pd.DataFrame,
        colonna_data: str,
        nome_chiave: str
) -> pd.DataFrame:
    """
    Esegue il lookup della DIM_TEMPO.
    """

    fact = fact.merge(

        dim_tempo[
            [
                "tempo_key",
                "data"
            ]
        ],

        left_on=colonna_data,

        right_on="data",

        how="left"

    )

    fact = fact.rename(
        columns={
            "tempo_key": nome_chiave
        }
    )

    fact = fact.drop(
        columns=["data"],
        errors="ignore"
    )

    return fact

# =====================================================
# CLEANUP FACT
# =====================================================

def cleanup_fact(fact: pd.DataFrame) -> pd.DataFrame:
    """
    Mantiene solamente le colonne
    della FACT_SPEDIZIONI.
    """

    colonne_fact = [

        "id_richiesta",
        "id_offerta",

        "cliente_key",
        "trasportatore_key",

        "origine_key",
        "destinazione_key",

        "tempo_richiesta_key",
        "tempo_offerta_key",
        "tempo_consegna_key",

        "veicolo_key",
        "merce_key",

        "peso_kg",

        "distanza_km",
        "costo_km",

        "importo_offerto",
        "commissione"

    ]

    return fact[colonne_fact].copy()

# =====================================================
# BUILD FACT
# =====================================================

def build_fact():

    conn = create_connection()

    # ==========================
    # STAGING
    # ==========================

    app = read_table(
        conn,
        "STG_APP_CLIENTI"
    )

    marketplace = read_table(
        conn,
        "STG_MARKETPLACE"
    )

    # ==========================
    # DIMENSIONI
    # ==========================

    dim_cliente = read_table(
        conn,
        "DIM_CLIENTE"
    )

    dim_trasportatore = read_table(
        conn,
        "DIM_TRASPORTATORE"
    )

    dim_veicolo = read_table(
        conn,
        "DIM_VEICOLO"
    )

    dim_merce = read_table(
        conn,
        "DIM_MERCE"
    )

    dim_localita = read_table(
        conn,
        "DIM_LOCALITA"
    )

    dim_tempo = read_table(
        conn,
        "DIM_TEMPO"
    )

    conn.close()


    # ==========================
    # Merge richieste + offerte
    # ==========================

    fact = app.merge(

        marketplace,

        on="id_richiesta",

        how="inner"

    )

    # ==========================
    # Cliente
    # ==========================

    fact = lookup_dimension(

        fact,
        dim_cliente,

        left_on="id_cliente",
        right_on="id_cliente",

        surrogate_key="cliente_key"

    )

    # ==========================
    # Trasportatore
    # ==========================

    fact = lookup_dimension(

        fact,
        dim_trasportatore,

        left_on="id_trasportatore",
        right_on="id_trasportatore",

        surrogate_key="trasportatore_key"

    )

    # ==========================
    # Veicolo
    # ==========================

    fact = lookup_dimension(

        fact,
        dim_veicolo,

        left_on="tipo_veicolo",
        right_on="tipo_veicolo",

        surrogate_key="veicolo_key"

    )

    # ==========================
    # Merce
    # ==========================

    fact = lookup_dimension(

        fact,
        dim_merce,

        left_on="categoria_merce",
        right_on="categoria_merce",

        surrogate_key="merce_key"

    )

    # ==========================
    # Origine
    # ==========================

    fact = lookup_dimension(

        fact,
        dim_localita,

        left_on="comune_origine",
        right_on="comune",

        surrogate_key="localita_key"

    )

    fact = fact.rename(
        columns={
            "localita_key": "origine_key"
        }
    )

    # ==========================
    # Destinazione
    # ==========================

    fact = lookup_dimension(

        fact,
        dim_localita,

        left_on="comune_destinazione",
        right_on="comune",

        surrogate_key="localita_key"

    )

    fact = fact.rename(
        columns={
            "localita_key": "destinazione_key"
        }
    )

    # ==========================
    # Tempo richiesta
    # ==========================

    fact = lookup_tempo(

        fact,

        dim_tempo,

        colonna_data="data_richiesta",

        nome_chiave="tempo_richiesta_key"

    )

    # ==========================
    # Tempo offerta
    # ==========================

    fact = lookup_tempo(

        fact,

        dim_tempo,

        colonna_data="data_offerta",

        nome_chiave="tempo_offerta_key"

    )

    # ==========================
    # Tempo consegna
    # ==========================

    fact = lookup_tempo(

        fact,

        dim_tempo,

        colonna_data="data_consegna_prevista",

        nome_chiave="tempo_consegna_key"

    )

    fact = cleanup_fact(fact)

    return fact



# =====================================================
# MAIN
# =====================================================

def main():

    fact = build_fact()

    print(f"\nRecord FACT: {len(fact)}\n")

    print(fact.columns)

    print()

    print(fact.head())


if __name__ == "__main__":
    main()