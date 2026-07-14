"""
repository.py

Funzioni di accesso ai dati del
Data Warehouse TruckFlow.

Autore: Crisele Ariola
Project Work PW21
"""

import sqlite3
import pandas as pd

from paths import DATABASE_DIR


DATABASE_FILE = DATABASE_DIR / "TruckFlow.db"


# =====================================================
# CONNESSIONE
# =====================================================

def create_connection():
    """
    Crea una connessione al database.
    """

    return sqlite3.connect(
        DATABASE_FILE
    )

# =====================================================
# COSTANTI
# =====================================================

MESI = {

    1: "Gen",
    2: "Feb",
    3: "Mar",
    4: "Apr",
    5: "Mag",
    6: "Giu",
    7: "Lug",
    8: "Ago",
    9: "Set",
    10: "Ott",
    11: "Nov",
    12: "Dic"

}

# =====================================================
# QUERY GENERICA
# =====================================================

def execute_query(
        query: str
) -> pd.DataFrame:
    """
    Esegue una query SQL
    e restituisce un DataFrame.
    """

    conn = create_connection()

    df = pd.read_sql_query(
        query,
        conn
    )

    conn.close()

    return df


# =====================================================
# KPI
# =====================================================

# =====================================================
# KPI
# =====================================================

def get_kpi() -> pd.DataFrame:
    """
    Restituisce i KPI principali
    del marketplace.
    """

    query = """

        SELECT

            (
                SELECT COUNT(*)
                FROM STG_APP_CLIENTI
            ) AS richieste,

            COUNT(*) AS spedizioni,

            ROUND(
                COUNT(*) * 100.0 /
                (
                    SELECT COUNT(*)
                    FROM STG_APP_CLIENTI
                ),
                1
            ) AS conversione,

            ROUND(
                SUM(importo_offerto),
                2
            ) AS valore_spedizioni,

            ROUND(
                SUM(commissione),
                2
            ) AS commissioni,

            ROUND(
                AVG(distanza_km),
                2
            ) AS distanza_media,

            ROUND(
                AVG(peso_kg),
                2
            ) AS peso_medio,

            ROUND(
                AVG(
                    julianday(t_offerta.data) -
                    julianday(t_richiesta.data)
                ),
                2
            ) AS tempo_medio

        FROM FACT_SPEDIZIONI f

        JOIN DIM_TEMPO t_richiesta

            ON f.tempo_richiesta_key = t_richiesta.tempo_key

        JOIN DIM_TEMPO t_offerta

            ON f.tempo_offerta_key = t_offerta.tempo_key

    """

    return execute_query(query)


# =====================================================
# SPEDIZIONI MENSILI
# =====================================================

def get_spedizioni_mensili() -> pd.DataFrame:
    """
    Restituisce il numero di spedizioni
    per mese.
    """

    query = """

        SELECT

            t.anno,

            t.mese,

            COUNT(*) AS spedizioni

        FROM FACT_SPEDIZIONI f

        JOIN DIM_TEMPO t

            ON f.tempo_richiesta_key = t.tempo_key

        GROUP BY

            t.anno,

            t.mese

        ORDER BY

            t.anno,

            t.mese

    """

    return execute_query(
        query
    )

# =====================================================
# SPEDIZIONI MENSILI
# =====================================================

def get_spedizioni_mensili() -> pd.DataFrame:
    """
    Restituisce il numero di spedizioni
    per mese.
    """

    query = """

        SELECT

            t.anno,

            t.mese,

            COUNT(*) AS spedizioni

        FROM FACT_SPEDIZIONI f

        JOIN DIM_TEMPO t

            ON f.tempo_richiesta_key = t.tempo_key

        GROUP BY

            t.anno,
            t.mese

        ORDER BY

            t.anno,
            t.mese

    """

    return execute_query(query)

# =====================================================
# RICHIESTE MENSILI
# =====================================================

def get_richieste_mensili() -> pd.DataFrame:
    """
    Restituisce il numero di richieste
    ricevute per mese.
    """

    query = """

        SELECT

            t.anno,

            t.mese,

            COUNT(*) AS richieste

        FROM STG_APP_CLIENTI a

        JOIN DIM_TEMPO t

            ON a.data_richiesta = t.data

        GROUP BY

            t.anno,
            t.mese

        ORDER BY

            t.anno,
            t.mese

    """

    df = execute_query(query)

    df["mese_nome"] = df["mese"].map(MESI)

    return df


# =====================================================
# COMMISSIONI MENSILI
# =====================================================

def get_commissioni_mensili() -> pd.DataFrame:
    """
    Restituisce le commissioni
    per mese.
    """

    query = """

        SELECT

            t.anno,

            t.mese,

            ROUND(
                SUM(f.commissione),
                2
            ) AS commissioni

        FROM FACT_SPEDIZIONI f

        JOIN DIM_TEMPO t

            ON f.tempo_richiesta_key = t.tempo_key

        GROUP BY

            t.anno,
            t.mese

        ORDER BY

            t.anno,
            t.mese

    """

    df = execute_query(query)

    df["mese_nome"] = df["mese"].map(MESI)

    return df





# =====================================================
# VALORE SPEDIZIONI MENSILE
# =====================================================

def get_valore_spedizioni_mensile() -> pd.DataFrame:
    """
    Restituisce il valore economico
    delle spedizioni per mese.
    """

    query = """

        SELECT

            t.anno,

            t.mese,

            ROUND(
                SUM(f.importo_offerto),
                2
            ) AS valore_spedizioni

        FROM FACT_SPEDIZIONI f

        JOIN DIM_TEMPO t

            ON f.tempo_richiesta_key = t.tempo_key

        GROUP BY

            t.anno,
            t.mese

        ORDER BY

            t.anno,
            t.mese

    """

    df = execute_query(query)

    df["mese_nome"] = df["mese"].map(MESI)

    return df

# =====================================================
# DASHBOARD OPERATIVA
# =====================================================
def get_veicoli_utilizzati():

    conn = sqlite3.connect(DATABASE_FILE)

    query = """
        SELECT
            dv.tipo_veicolo,
            COUNT(*) AS spedizioni

        FROM FACT_SPEDIZIONI fs

        JOIN DIM_VEICOLO dv
            ON fs.veicolo_key = dv.veicolo_key

        GROUP BY dv.tipo_veicolo

        ORDER BY spedizioni DESC
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    totale = df["spedizioni"].sum()

    df["percentuale"] = (
        df["spedizioni"] / totale * 100
    ).round(1)

    return df

def get_merci_trasportate():

    conn = sqlite3.connect(DATABASE_FILE)

    query = """
        SELECT
            dm.categoria_merce,
            COUNT(*) AS spedizioni

        FROM FACT_SPEDIZIONI fs

        JOIN DIM_MERCE dm
            ON fs.merce_key = dm.merce_key

        GROUP BY dm.categoria_merce

        ORDER BY spedizioni DESC
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    totale = df["spedizioni"].sum()

    df["percentuale"] = (
        df["spedizioni"] / totale * 100
    ).round(1)

    return df

def get_top_trasportatori():

    conn = sqlite3.connect(DATABASE_FILE)

    query = """
        SELECT
            dt.ragione_sociale,
            COUNT(*) AS spedizioni

        FROM FACT_SPEDIZIONI fs

        JOIN DIM_TRASPORTATORE dt
            ON fs.trasportatore_key = dt.trasportatore_key

        GROUP BY dt.ragione_sociale

        ORDER BY spedizioni DESC

        LIMIT 10
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    totale = df["spedizioni"].sum()

    df["percentuale"] = (
        df["spedizioni"] / totale * 100
    ).round(1)

    return df


def get_distanza_media_veicolo():

    conn = sqlite3.connect(DATABASE_FILE)

    query = """
        SELECT

            dv.tipo_veicolo,

            ROUND(AVG(fs.distanza_km), 1) AS distanza_media

        FROM FACT_SPEDIZIONI fs

        JOIN DIM_VEICOLO dv

            ON fs.veicolo_key = dv.veicolo_key

        GROUP BY dv.tipo_veicolo

        ORDER BY distanza_media DESC
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    return df


def get_kpi_operativa():

    conn = sqlite3.connect(DATABASE_FILE)

    query = """
    SELECT

        (SELECT COUNT(*) FROM FACT_SPEDIZIONI) AS spedizioni,

        (SELECT COUNT(*) FROM DIM_VEICOLO) AS tipologie_veicolo,

        (SELECT COUNT(*) FROM DIM_MERCE) AS categorie_merce,

        (SELECT COUNT(*) FROM DIM_TRASPORTATORE) AS trasportatori

    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    return df

# =====================================================
# DASHBOARD GEOGRAFICA
# =====================================================
def get_destinazioni_spedizioni():

    conn = sqlite3.connect(DATABASE_FILE)

    query = """
        SELECT

            dl.comune,
            dl.provincia,
            dl.regione,
            dl.lat,
            dl.lon,

            COUNT(*) AS spedizioni

        FROM FACT_SPEDIZIONI fs

        JOIN DIM_LOCALITA dl
            ON fs.destinazione_key = dl.localita_key

        GROUP BY

            dl.comune,
            dl.provincia,
            dl.regione,
            dl.lat,
            dl.lon

        
        HAVING COUNT(*) >= 2
        
        ORDER BY spedizioni DESC
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    return df


def get_origini_spedizioni():
    conn = sqlite3.connect(DATABASE_FILE)

    query = """
        SELECT

            dl.comune,
            dl.provincia,
            dl.regione,
            dl.lat,
            dl.lon,

            COUNT(*) AS spedizioni

        FROM FACT_SPEDIZIONI fs

        JOIN DIM_LOCALITA dl
            ON fs.origine_key = dl.localita_key

        GROUP BY

            dl.comune,
            dl.provincia,
            dl.regione,
            dl.lat,
            dl.lon


        HAVING COUNT(*) >= 2

        ORDER BY spedizioni DESC
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    return df


def get_spedizioni_per_regione():

    conn = sqlite3.connect(DATABASE_FILE)

    query = """
        SELECT

            dl.regione,

            COUNT(*) AS spedizioni

        FROM FACT_SPEDIZIONI fs

        JOIN DIM_LOCALITA dl
            ON fs.destinazione_key = dl.localita_key

        GROUP BY dl.regione

        ORDER BY spedizioni DESC
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    return df


def get_commissioni_per_regione():

    conn = sqlite3.connect(DATABASE_FILE)

    query = """
        SELECT

            dl.regione,

            ROUND(SUM(fs.commissione), 2) AS commissioni

        FROM FACT_SPEDIZIONI fs

        JOIN DIM_LOCALITA dl
            ON fs.destinazione_key = dl.localita_key

        GROUP BY dl.regione

        ORDER BY commissioni DESC
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    return df

def get_numero_regioni():

    conn = sqlite3.connect(DATABASE_FILE)

    query = """
        SELECT COUNT(DISTINCT regione) AS regioni
        FROM DIM_LOCALITA
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    return int(df.iloc[0]["regioni"])


def get_numero_province():

    conn = sqlite3.connect(DATABASE_FILE)

    query = """
        SELECT COUNT(DISTINCT provincia) AS province
        FROM DIM_LOCALITA
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    return int(df.iloc[0]["province"])

def get_numero_comuni():

    conn = sqlite3.connect(DATABASE_FILE)

    query = """
        SELECT COUNT(DISTINCT comune) AS comuni
        FROM DIM_LOCALITA
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    return int(df.iloc[0]["comuni"])

def get_distanza_media():

    conn = sqlite3.connect(DATABASE_FILE)

    query = """
        SELECT ROUND(AVG(distanza_km),1) AS distanza
        FROM FACT_SPEDIZIONI
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    return float(df.iloc[0]["distanza"])


def get_top_clienti():

    conn = sqlite3.connect(DATABASE_FILE)

    query = """
        SELECT

            dc.ragione_sociale,

            COUNT(*) AS spedizioni,
            ROUND(COUNT(*) * 100.0 /
                (SELECT COUNT(*) FROM FACT_SPEDIZIONI), 1) AS percentuale

        FROM FACT_SPEDIZIONI fs

        JOIN DIM_CLIENTE dc
            ON fs.cliente_key = dc.cliente_key

        GROUP BY dc.ragione_sociale

        ORDER BY spedizioni DESC

        LIMIT 10
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    return df
def get_commissioni_clienti():

    conn = sqlite3.connect(DATABASE_FILE)

    query = """
        SELECT

            dc.ragione_sociale,

            ROUND(SUM(fs.commissione),2) AS commissioni

        FROM FACT_SPEDIZIONI fs

        JOIN DIM_CLIENTE dc
            ON fs.cliente_key = dc.cliente_key

        GROUP BY dc.ragione_sociale

        ORDER BY commissioni DESC

        LIMIT 10
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    return df


def get_clienti_per_regione():

    conn = sqlite3.connect(DATABASE_FILE)

    query = """
        SELECT

            regione,

            COUNT(*) AS clienti

        FROM DIM_CLIENTE

        GROUP BY regione

        ORDER BY clienti DESC
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    return df


def get_valore_spedizioni_clienti():

    conn = sqlite3.connect(DATABASE_FILE)

    query = """
        SELECT

            dc.ragione_sociale,

            ROUND(SUM(fs.importo_offerto), 2) AS valore

        FROM FACT_SPEDIZIONI fs

        JOIN DIM_CLIENTE dc
            ON fs.cliente_key = dc.cliente_key

        GROUP BY dc.ragione_sociale

        ORDER BY valore DESC

        LIMIT 10
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    return df


def get_commissioni_per_regione_cliente():

    conn = sqlite3.connect(DATABASE_FILE)

    query = """
        SELECT

            dc.regione,

            ROUND(SUM(fs.commissione),2) AS commissioni

        FROM FACT_SPEDIZIONI fs

        JOIN DIM_CLIENTE dc
            ON fs.cliente_key = dc.cliente_key

        GROUP BY dc.regione

        ORDER BY commissioni DESC
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    return df


def get_numero_clienti():

    conn = sqlite3.connect(DATABASE_FILE)

    query = """
        SELECT COUNT(*)
        FROM DIM_CLIENTE
    """

    valore = pd.read_sql_query(query, conn).iloc[0, 0]

    conn.close()

    return int(valore)

def get_spedizioni_medie_cliente():

    conn = sqlite3.connect(DATABASE_FILE)

    query = """
        SELECT
            ROUND(
                CAST(COUNT(*) AS FLOAT) /
                COUNT(DISTINCT cliente_key),
                2
            ) AS media
        FROM FACT_SPEDIZIONI
    """

    valore = pd.read_sql_query(query, conn).iloc[0, 0]

    conn.close()

    return valore

def get_commissione_media_cliente():

    conn = sqlite3.connect(DATABASE_FILE)

    query = """
        SELECT
            ROUND(
                SUM(commissione) /
                COUNT(DISTINCT cliente_key),
                2
            ) AS media
        FROM FACT_SPEDIZIONI
    """

    valore = pd.read_sql_query(query, conn).iloc[0, 0]

    conn.close()

    return valore

def get_numero_regioni_clienti():

    conn = sqlite3.connect(DATABASE_FILE)

    query = """
        SELECT COUNT(DISTINCT regione)
        FROM DIM_CLIENTE
    """

    valore = pd.read_sql_query(query, conn).iloc[0, 0]

    conn.close()

    return int(valore)

if __name__ == "__main__":

    df = get_commissioni_clienti()

    print(df)
