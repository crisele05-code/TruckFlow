"""
load_staging.py

Carica le sorgenti CSV nelle tabelle di staging
del Data Warehouse TruckFlow.

Autore: Crisele Ariola
Project Work PW21
"""

from database import (
    create_connection,
    clear_table,
    load_dataframe
)

from extract import extract_all


# =====================================================
# STAGING
# =====================================================

def load_stg_app_clienti(conn, data):
    """
    Carica STG_APP_CLIENTI.
    """

    clear_table(
        conn,
        "STG_APP_CLIENTI"
    )

    load_dataframe(
        conn,
        data["app_clienti"],
        "STG_APP_CLIENTI"
    )

    print(f"✓ STG_APP_CLIENTI: {len(data['app_clienti'])} record")


def load_stg_partner(conn, data):
    """
    Carica STG_PARTNER.
    """

    clear_table(
        conn,
        "STG_PARTNER"
    )

    load_dataframe(
        conn,
        data["partner"],
        "STG_PARTNER"
    )

    print(f"✓ STG_PARTNER: {len(data['partner'])} record")


def load_stg_marketplace(conn, data):
    """
    Carica STG_MARKETPLACE.
    """

    clear_table(
        conn,
        "STG_MARKETPLACE"
    )

    load_dataframe(
        conn,
        data["marketplace"],
        "STG_MARKETPLACE"
    )

    print(f"✓ STG_MARKETPLACE: {len(data['marketplace'])} record")


# =====================================================
# MAIN
# =====================================================

def main():

    data = extract_all()

    conn = create_connection()

    print("\nCaricamento tabelle STAGING...\n")

    load_stg_app_clienti(
        conn,
        data
    )

    load_stg_partner(
        conn,
        data
    )

    load_stg_marketplace(
        conn,
        data
    )

    conn.commit()

    conn.close()

    print("\nCaricamento STAGING completato.\n")


if __name__ == "__main__":
    main()