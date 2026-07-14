"""
paths.py

Percorsi condivisi del progetto TruckFlow.
"""

from pathlib import Path


# =====================================================
# ROOT DEL PROGETTO
# =====================================================

BASE_DIR = Path(__file__).resolve().parent


# =====================================================
# CARTELLE DATI
# =====================================================

DATA_DIR = BASE_DIR / "data"

SOURCE_DIR = DATA_DIR / "sorgenti"

ANAGRAFICHE_DIR = DATA_DIR / "anagrafiche"

DATABASE_DIR = DATA_DIR / "database"

STAGING_DIR = DATA_DIR / "staging"

DW_DIR = DATA_DIR / "dw"