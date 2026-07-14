"""
database.py

Funzioni comuni per la gestione del database SQLite.
"""

import sqlite3

import pandas as pd

from paths import DATABASE_DIR


DATABASE_FILE = DATABASE_DIR / "TruckFlow.db"


def create_connection() -> sqlite3.Connection:
    """
    Crea una connessione al database.
    """

    return sqlite3.connect(DATABASE_FILE)


def clear_table(
        conn: sqlite3.Connection,
        table_name: str
) -> None:
    """
    Svuota una tabella.
    """

    conn.execute(
        f"DELETE FROM {table_name}"
    )


def load_dataframe(
        conn: sqlite3.Connection,
        df: pd.DataFrame,
        table_name: str
) -> None:
    """
    Carica un DataFrame in una tabella SQLite.
    """

    df.to_sql(
        table_name,
        conn,
        if_exists="append",
        index=False
    )