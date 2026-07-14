"""
main.py

Pipeline ETL del progetto TruckFlow.

Autore: Crisele Ariola
Project Work PW21
"""

from create_dw import main as create_dw
from load_staging import main as load_staging
from load import main as load_dimensions


def main():

    print("\n" + "=" * 60)
    print("TRUCKFLOW - ETL")
    print("=" * 60)

    print("\n[1/3] Creazione Data Warehouse...")
    create_dw()

    print("\n[2/3] Caricamento Staging...")
    load_staging()

    print("\n[3/3] Caricamento Dimensioni...")
    load_dimensions()

    print("\n" + "=" * 60)
    print("PIPELINE ETL COMPLETATA")
    print("=" * 60)


if __name__ == "__main__":
    main()