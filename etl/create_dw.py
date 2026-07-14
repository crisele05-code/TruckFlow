"""
create_dw.py

Crea il database SQLite TruckFlow.db e definisce
la struttura del Data Warehouse:

- Tabelle di Staging
- Tabelle Dimensionali
- Fact Table

Autore: Crisele Ariola
Project Work PW21
"""


import sqlite3
from paths import DATABASE_DIR

DATABASE_FILE = DATABASE_DIR / "TruckFlow.db"

def create_connection():

    DATABASE_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    return sqlite3.connect(DATABASE_FILE)



def create_stg_app_clienti(cursor):

    cursor.execute("""

        CREATE TABLE IF NOT EXISTS STG_APP_CLIENTI (

            id_richiesta TEXT,

            id_cliente TEXT,

            data_richiesta DATE,

            data_consegna_prevista DATE,

            comune_origine TEXT,

            provincia_origine TEXT,

            regione_origine TEXT,

            comune_destinazione TEXT,

            provincia_destinazione TEXT,

            regione_destinazione TEXT,

            categoria_merce TEXT,

            tipo_veicolo TEXT,

            peso_kg REAL,

            stato_richiesta TEXT

        )

    """)

def create_stg_partner(cursor):

    cursor.execute("""

        CREATE TABLE IF NOT EXISTS STG_PARTNER (

            id_trasportatore TEXT,

            ragione_sociale TEXT,

            partita_iva TEXT,

            comune TEXT,

            provincia TEXT,

            sigla TEXT,

            regione TEXT

        )

    """)

def create_stg_marketplace(cursor):

    cursor.execute("""

        CREATE TABLE IF NOT EXISTS STG_MARKETPLACE (

            id_offerta TEXT,

            id_richiesta TEXT,

            id_trasportatore TEXT,

            data_offerta DATE,

            distanza_km REAL,

            costo_km REAL,

            importo_offerto REAL,

            commissione REAL,

            stato_offerta TEXT

        )

    """)



def create_dim_cliente(cursor):

    cursor.execute("""

        CREATE TABLE IF NOT EXISTS DIM_CLIENTE (

            cliente_key INTEGER PRIMARY KEY AUTOINCREMENT,

            id_cliente TEXT NOT NULL UNIQUE,

            ragione_sociale TEXT NOT NULL,

            partita_iva TEXT NOT NULL,

            categoria_prevalente TEXT,

            comune TEXT,

            provincia TEXT,

            sigla TEXT,

            regione TEXT

        )

    """)


def create_dim_trasportatore(cursor):

    cursor.execute("""

        CREATE TABLE IF NOT EXISTS DIM_TRASPORTATORE (

            trasportatore_key INTEGER PRIMARY KEY AUTOINCREMENT,

            id_trasportatore TEXT NOT NULL UNIQUE,

            ragione_sociale TEXT NOT NULL,

            partita_iva TEXT NOT NULL,

            comune TEXT,

            provincia TEXT,

            sigla TEXT,

            regione TEXT

        )

    """)


def create_dim_localita(cursor):

    cursor.execute("""

        CREATE TABLE IF NOT EXISTS DIM_LOCALITA (

            localita_key INTEGER PRIMARY KEY AUTOINCREMENT,

            codice_istat INTEGER NOT NULL UNIQUE,

            comune TEXT NOT NULL,

            provincia TEXT,

            sigla TEXT,

            regione TEXT,

            lat REAL,

            lon REAL

        )

    """)


def create_dim_tempo(cursor):

    cursor.execute("""

        CREATE TABLE IF NOT EXISTS DIM_TEMPO (

            tempo_key INTEGER PRIMARY KEY AUTOINCREMENT,

            data DATE NOT NULL UNIQUE,

            giorno INTEGER,

            mese INTEGER,

            nome_mese TEXT,

            trimestre INTEGER,

            anno INTEGER,

            giorno_settimana INTEGER,

            nome_giorno TEXT,

            weekend INTEGER

        )

    """)

def create_dim_veicolo(cursor):

    cursor.execute("""

        CREATE TABLE IF NOT EXISTS DIM_VEICOLO (

            veicolo_key INTEGER PRIMARY KEY AUTOINCREMENT,

            tipo_veicolo TEXT NOT NULL UNIQUE

        )

    """)

def create_dim_merce(cursor):

    cursor.execute("""

        CREATE TABLE IF NOT EXISTS DIM_MERCE (

            merce_key INTEGER PRIMARY KEY AUTOINCREMENT,

            categoria_merce TEXT NOT NULL UNIQUE

        )

    """)

def create_fact_spedizioni(cursor):

    cursor.execute("""

        CREATE TABLE IF NOT EXISTS FACT_SPEDIZIONI (

            spedizione_key INTEGER PRIMARY KEY AUTOINCREMENT,

            id_richiesta TEXT NOT NULL,

            id_offerta TEXT NOT NULL,

            cliente_key INTEGER NOT NULL,

            trasportatore_key INTEGER NOT NULL,

            origine_key INTEGER NOT NULL,

            destinazione_key INTEGER NOT NULL,

            tempo_richiesta_key INTEGER NOT NULL,

            tempo_offerta_key INTEGER NOT NULL,
            
            tempo_consegna_key INTEGER NOT NULL,

            veicolo_key INTEGER NOT NULL,

            merce_key INTEGER NOT NULL,

            peso_kg REAL,

            distanza_km REAL,

            costo_km REAL,

            importo_offerto REAL,

            commissione REAL

        )

    """)

def drop_tables(cursor):
    """
    Elimina tutte le tabelle del Data Warehouse.
    Utile durante lo sviluppo per ricreare il database da zero.
    """

    tables = [

        # FACT
        "FACT_SPEDIZIONI",

        # DIM
        "DIM_MERCE",
        "DIM_VEICOLO",
        "DIM_TEMPO",
        "DIM_LOCALITA",
        "DIM_TRASPORTATORE",
        "DIM_CLIENTE",

        # STAGING
        "STG_MARKETPLACE",
        "STG_PARTNER",
        "STG_APP_CLIENTI"

    ]

    for table in tables:
        cursor.execute(
            f"DROP TABLE IF EXISTS {table}"
        )

def show_tables(cursor):
    """
    Visualizza tutte le tabelle presenti nel database.
    """

    cursor.execute("""

        SELECT name
        FROM sqlite_master
        WHERE type='table'
        ORDER BY name

    """)

    print("\nTabelle create:\n")

    for table in cursor.fetchall():
        print(f"- {table[0]}")


def main():

    conn = create_connection()
    cursor = conn.cursor()

    # Elimina tutte le tabelle
    drop_tables(cursor)

    # STAGING
    create_stg_app_clienti(cursor)
    create_stg_partner(cursor)
    create_stg_marketplace(cursor)

    # DIMENSIONI
    create_dim_cliente(cursor)
    create_dim_trasportatore(cursor)
    create_dim_localita(cursor)
    create_dim_tempo(cursor)
    create_dim_veicolo(cursor)
    create_dim_merce(cursor)

    # FACT
    create_fact_spedizioni(cursor)

    show_tables(cursor)

    conn.commit()
    conn.close()

    print("TruckFlow.db creato correttamente.")


if __name__ == "__main__":
    main()