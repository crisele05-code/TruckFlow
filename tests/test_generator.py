from pathlib import Path

import pandas as pd

from config import (
    NUM_RICHIESTE,
    COMPATIBILITA_MERCE_VEICOLO,
    PESO_MERCE
)

# =====================================================
# CARICAMENTO CSV
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

CSV_FILE = BASE_DIR / "data" / "sorgenti" / "app_clienti.csv"

assert CSV_FILE.exists(), f"File non trovato: {CSV_FILE}"

df = pd.read_csv(CSV_FILE)

print("=" * 60)
print("VALIDAZIONE APP_CLIENTI.CSV")
print("=" * 60)

# =====================================================
# NUMERO RICHIESTE
# =====================================================

assert len(df) == NUM_RICHIESTE

print(f"✓ Numero richieste: {len(df)}")

# =====================================================
# ID RICHIESTA UNIVOCI
# =====================================================

assert df["id_richiesta"].is_unique

print("✓ ID richiesta univoci")

# =====================================================
# ORIGINE != DESTINAZIONE
# =====================================================

assert (
    df["comune_origine"]
    !=
    df["comune_destinazione"]
).all()

print("✓ Origine diversa dalla destinazione")

# =====================================================
# DATE
# =====================================================

df["data_richiesta"] = pd.to_datetime(
    df["data_richiesta"]
)

df["data_consegna_prevista"] = pd.to_datetime(
    df["data_consegna_prevista"]
)

assert (
    df["data_consegna_prevista"]
    >=
    df["data_richiesta"]
).all()

print("✓ Date corrette")

# =====================================================
# COMPATIBILITA' MERCE - VEICOLO
# =====================================================

for _, row in df.iterrows():

    categoria = row["categoria_merce"]

    veicolo = row["tipo_veicolo"]

    assert (
        veicolo
        in
        COMPATIBILITA_MERCE_VEICOLO[categoria]
    )

print("✓ Compatibilità merce-veicolo")

# =====================================================
# PESO
# =====================================================

for _, row in df.iterrows():

    minimo, massimo = PESO_MERCE[
        row["categoria_merce"]
    ]

    assert (
        minimo
        <=
        row["peso_kg"]
        <=
        massimo
    )

print("✓ Peso corretto")

# =====================================================
# STATO RICHIESTA
# =====================================================

assert (
    df["stato_richiesta"] == "Pubblicata"
).all()

print("✓ Stato richiesta corretto")

# =====================================================
# ID CLIENTE
# =====================================================

assert df["id_cliente"].notnull().all()

print("✓ ID cliente valorizzato")

# =====================================================
# RIEPILOGO
# =====================================================

print("\n" + "=" * 60)
print("VALIDAZIONE COMPLETATA CON SUCCESSO")
print("=" * 60)