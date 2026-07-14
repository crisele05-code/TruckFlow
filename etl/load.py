"""
load.py

Carica le dimensioni del Data Warehouse TruckFlow.

Autore: Crisele Ariola
Project Work PW21
"""

from database import (
    create_connection,
    clear_table,
    load_dataframe
)

from transform import (
    transform_dim_cliente,
    transform_dim_trasportatore,
    transform_dim_veicolo,
    transform_dim_merce,
    transform_dim_tempo
)


from transform import (
    transform_dim_localita
)
from build_fact import build_fact

# =====================================================
# DIM_CLIENTE
# =====================================================

def load_dim_cliente(conn):
    """
    Carica DIM_CLIENTE.
    """

    clienti = transform_dim_cliente()

    clear_table(
        conn,
        "DIM_CLIENTE"
    )

    load_dataframe(
        conn,
        clienti,
        "DIM_CLIENTE"
    )

    print(f"✓ DIM_CLIENTE: {len(clienti)} record")


# =====================================================
# DIM_TRASPORTATORE
# =====================================================

def load_dim_trasportatore(conn):
    """
    Carica DIM_TRASPORTATORE.
    """

    trasportatori = transform_dim_trasportatore()

    clear_table(
        conn,
        "DIM_TRASPORTATORE"
    )

    load_dataframe(
        conn,
        trasportatori,
        "DIM_TRASPORTATORE"
    )

    print(f"✓ DIM_TRASPORTATORE: {len(trasportatori)} record")


# =====================================================
# DIM_VEICOLO
# =====================================================

def load_dim_veicolo(conn):
    """
    Carica DIM_VEICOLO.
    """

    veicoli = transform_dim_veicolo()

    clear_table(
        conn,
        "DIM_VEICOLO"
    )

    load_dataframe(
        conn,
        veicoli,
        "DIM_VEICOLO"
    )

    print(f"✓ DIM_VEICOLO: {len(veicoli)} record")


# =====================================================
# DIM_MERCE
# =====================================================

def load_dim_merce(conn):
    """
    Carica DIM_MERCE.
    """

    merci = transform_dim_merce()

    clear_table(
        conn,
        "DIM_MERCE"
    )

    load_dataframe(
        conn,
        merci,
        "DIM_MERCE"
    )

    print(f"✓ DIM_MERCE: {len(merci)} record")

# =====================================================
# DIM_LOCALITA
# =====================================================

def load_dim_localita(conn):
    """
    Carica DIM_LOCALITA.
    """

    localita = transform_dim_localita()

    clear_table(
        conn,
        "DIM_LOCALITA"
    )

    load_dataframe(
        conn,
        localita,
        "DIM_LOCALITA"
    )

    print(
        f"✓ DIM_LOCALITA: {len(localita)} record"
    )


def load_dim_tempo(conn):

    tempo = transform_dim_tempo()

    clear_table(
        conn,
        "DIM_TEMPO"
    )

    load_dataframe(
        conn,
        tempo,
        "DIM_TEMPO"
    )

    print(f"✓ DIM_TEMPO: {len(tempo)} record")


# =====================================================
# FACT_SPEDIZIONI
# =====================================================

def load_fact(conn):
    """
    Carica la FACT_SPEDIZIONI.
    """

    fact = build_fact()

    clear_table(
        conn,
        "FACT_SPEDIZIONI"
    )

    load_dataframe(
        conn,
        fact,
        "FACT_SPEDIZIONI"
    )

    print(
        f"✓ FACT_SPEDIZIONI: {len(fact)} record"
    )

# =====================================================
# MAIN
# =====================================================

def main():

    conn = create_connection()

    print("\nCaricamento dimensioni...\n")

    load_dim_cliente(conn)

    load_dim_trasportatore(conn)

    load_dim_veicolo(conn)

    load_dim_merce(conn)

    load_dim_localita(conn)

    load_dim_tempo(conn)
    load_fact(conn)

    conn.commit()

    conn.close()

    print("\nCaricamento completato.\n")


if __name__ == "__main__":
    main()