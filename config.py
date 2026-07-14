"""
Configurazione del progetto TruckFlow
"""

from datetime import datetime

# ==========================================
# GENERAZIONE DATI
# ==========================================

NUM_CLIENTI = 120
NUM_RICHIESTE = 500
NUM_TRASPORTATORI = 100
NUM_VEICOLI = 200

# ==========================================
# BUSINESS
# ==========================================

COMMISSIONE = 0.08

# ==========================================
# FAKER
# ==========================================

FAKER_LOCALE = "it_IT"
RANDOM_SEED = 42

# ==========================================
# CARTELLE
# ==========================================

DATA_FOLDER = "data"
SOURCE_FOLDER = "data/sorgenti"
ANAGRAFICHE_FOLDER = "data/anagrafiche"

# ==========================================
# AZIENDE
# ==========================================

COMPANY_PREFIX = [
    "Trasporti",
    "Autotrasporti",
    "Logistica",
    "Cargo",
    "Express"
]

COMPANY_SUFFIX = [
    "S.r.l.",
    "S.p.A."
]

# ==========================================
# MERCI
# ==========================================

CATEGORIE_MERCE = [
    "Alimentare",
    "Bevande",
    "Abbigliamento",
    "Elettronica",
    "Arredamento",
    "Materiale edile",
    "Carta",
    "Farmaceutico",
    "Container",
    "Liquidi"
]

# ==========================================
# VEICOLI
# ==========================================

TIPI_VEICOLO = [
    "Centinato",
    "Frigorifero",
    "Cassonato",
    "Portacontainer",
    "Cisterna"
]

# Compatibilità categoria -> veicolo

COMPATIBILITA_MERCE_VEICOLO = {

    "Alimentare": [
        "Frigorifero",
        "Centinato"
    ],

    "Bevande": [
        "Centinato",
        "Cassonato"
    ],

    "Abbigliamento": [
        "Centinato"
    ],

    "Elettronica": [
        "Centinato"
    ],

    "Arredamento": [
        "Centinato",
        "Cassonato"
    ],

    "Materiale edile": [
        "Cassonato"
    ],

    "Carta": [
        "Centinato",
        "Cassonato"
    ],

    "Farmaceutico": [
        "Frigorifero"
    ],

    "Container": [
        "Portacontainer"
    ],

    "Liquidi": [
        "Cisterna"
    ]
}


TEMPI_CONSEGNA = {

    "Alimentare": (0, 1),

    "Bevande": (1, 3),

    "Abbigliamento": (2, 5),

    "Elettronica": (2, 5),

    "Arredamento": (4, 7),

    "Materiale edile": (3, 7),

    "Carta": (2, 5),

    "Farmaceutico": (0, 2),

    "Container": (5, 10),

    "Liquidi": (2, 5)
}

CLIENT_COMPANY_PREFIX = {

    "Alimentare": [
        "Gusto",
        "Sapori",
        "Food",
        "Alimenti",
        "Delizie"
    ],

    "Bevande": [
        "Acqua",
        "Drink",
        "Beverage",
        "Fresh",
        "Viva"
    ],

    "Abbigliamento": [
        "Moda",
        "Fashion",
        "Style",
        "Trend",
        "Elegance"
    ],

    "Elettronica": [
        "Tech",
        "Digital",
        "Electro",
        "Smart",
        "Future"
    ],

    "Arredamento": [
        "Casa",
        "Arredo",
        "Living",
        "Design",
        "Home"
    ],

    "Materiale edile": [
        "Edil",
        "Costruzioni",
        "Building",
        "Cemento",
        "Inerti"
    ],

    "Carta": [
        "Paper",
        "Cartotecnica",
        "Grafica",
        "Print",
        "Office"
    ],

    "Farmaceutico": [
        "Pharma",
        "Medical",
        "Salus",
        "Bio",
        "Medica"
    ],

    "Container": [
        "Port Logistics",
        "Intermodal",
        "Terminal Cargo",
        "Sea Bridge",
        "Container Hub"
],

    "Liquidi": [
        "Oil",
        "Fluid",
        "Tank",
        "Energy",
        "Fuel"
    ]
}

CLIENT_COMPANY_SUFFIX = [
    "Italia",
    "Group",
    "Nord",
    "Sud"
]

COMPANY_LEGAL_FORM = [
    "S.r.l.",
    "S.p.A."
]

PESO_MERCE = {

    "Alimentare": (500, 28000),

    "Bevande": (1000, 30000),

    "Abbigliamento": (100, 8000),

    "Elettronica": (50, 4000),

    "Arredamento": (500, 20000),

    "Materiale edile": (1000, 30000),

    "Carta": (500, 28000),

    "Farmaceutico": (50, 12000),

    "Container": (10000, 30000),

    "Liquidi": (5000, 30000)
}



DATA_INIZIO = datetime(2026, 1, 1)

DATA_FINE = datetime(2026, 12, 31)


# Distribuzione stagionale delle richieste.
# Agosto presenta un forte calo per le ferie estive.
# Dicembre registra un'attività ridotta per le festività.
RICHIESTE_PER_MESE = {
    1: 0.06,
    2: 0.07,
    3: 0.09,
    4: 0.10,
    5: 0.10,
    6: 0.10,
    7: 0.09,
    8: 0.03,
    9: 0.10,
    10: 0.10,
    11: 0.10,
    12: 0.07
}

# ==========================================
# COSTI TRASPORTO
# ==========================================

COSTO_KM_MIN = 1.50
COSTO_KM_MAX = 2.50


STATI_RICHIESTA = [
    "COMPLETATA",
    "ACCETTATA",
    "ANNULLATA"
]

PESI_STATI_RICHIESTA = [
    80,
    10,
    10
]