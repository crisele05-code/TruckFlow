# TruckFlow

> Sistema di Business Intelligence per il monitoraggio delle performance di un marketplace logistico.

## Descrizione

TruckFlow è un progetto sviluppato nell'ambito del Project Work PW21 del Corso di Laurea in Informatica per le Aziende Digitali.

L'obiettivo del progetto è progettare e implementare una soluzione completa di **Business Intelligence** in grado di trasformare dati provenienti da differenti sorgenti informative in informazioni strategiche a supporto del processo decisionale.

Il sistema comprende:

- generazione di dati sintetici;
- pipeline ETL;
- Data Warehouse multidimensionale;
- query SQL;
- dashboard interattive.

---

# Architettura del sistema

```text
Sorgenti dati
│
├── App Clienti
├── Marketplace
├── Gestionale Partner
└── Archivio Partner
        │
        ▼
 Pipeline ETL
        │
        ▼
 Data Warehouse (SQLite)
        │
        ▼
 Query SQL
        │
        ▼
 Dashboard Streamlit
```

---

# Tecnologie utilizzate

| Tecnologia | Utilizzo |
|------------|----------|
| Python | Linguaggio principale |
| SQLite | Data Warehouse |
| Pandas | ETL e manipolazione dati |
| Faker | Generazione dati sintetici |
| Streamlit | Dashboard |
| Plotly | Grafici interattivi |
| Draw.io | Diagrammi |

---

# Struttura del progetto

```text
TruckFlow
│
├── dashboard/                         # Dashboard e interfaccia Streamlit
│   ├── app.py
│   ├── charts.py
│   ├── repository.py
│   ├── utils.py
│   ├── test_chart.py
│   └── views/
│       ├── clienti.py
│       ├── executive.py
│       ├── geografica.py
│       └── operativa.py
│
├── generator/                         # Generazione dei dati sintetici
│   ├── distance.py
│   ├── generate_app_clienti.py
│   ├── generate_archivio_partner.py
│   ├── generate_marketplace.py
│   └── utils.py
│
├── etl/                               # Pipeline ETL e Data Warehouse
│   ├── build_fact.py
│   ├── create_dw.py
│   ├── database.py
│   ├── extract.py
│   ├── load.py
│   ├── load_staging.py
│   ├── main.py
│   └── transform.py
│
├── data/                              # Dati utilizzati dal progetto
│   ├── anagrafiche/
│   ├── database/
│   └── sorgenti/
│
├── tests/                             # Test e controlli
│
├── requirements.txt                   # Dipendenze Python
│
└── README.md                          # Documentazione del progetto
```

---

# Dashboard

Il sistema mette a disposizione quattro dashboard dedicate all'analisi delle performance aziendali.

### Executive Dashboard

Consente di monitorare i principali KPI economici e operativi.

- Richieste
- Spedizioni
- Commissioni
- Ricavi

---

### Dashboard Operativa

Analizza le attività operative della piattaforma.

- Veicoli utilizzati
- Merci trasportate
- Top trasportatori
- Distanza media

---

### Dashboard Geografica

Permette di analizzare la distribuzione territoriale delle spedizioni.

- Mappa interattiva
- Spedizioni per regione
- Commissioni per regione

---

### Dashboard Clienti

Consente di monitorare il comportamento della clientela.

- Top clienti
- Top commissioni
- Clienti per regione
- Commissioni per regione

---

# Riproduzione del progetto

Il progetto può essere riprodotto in ambiente locale seguendo una sequenza di passaggi che comprende l'installazione delle dipendenze, la generazione dei dati sintetici, l'esecuzione della pipeline ETL e l'avvio della dashboard.

## Requisiti

- Python 3.13
- Git

## 1. Clonazione del repository

Clonare il repository e accedere alla cartella del progetto:

```bash
git clone https://github.com/crisele05-code/TruckFlow.git
cd TruckFlow
```

## 2. Installazione delle dipendenze

Installare le librerie richieste dal progetto:

```bash
pip install -r requirements.txt
```

## 3. Generazione dei dati sintetici

Eseguire gli script per generare le principali sorgenti dati utilizzate dal progetto:

```bash
python generator/generate_app_clienti.py
python generator/generate_archivio_partner.py
python generator/generate_marketplace.py
```

## 4. Esecuzione della pipeline ETL

Avviare il processo di creazione e caricamento del Data Warehouse:

```bash
python etl/main.py
```

## 5. Avvio della dashboard

Avviare l'applicazione Streamlit:

```bash
python -m streamlit run dashboard/app.py
```

Una volta avviata, la dashboard sarà disponibile nel browser all'indirizzo indicato da Streamlit.

---

# Project Work

Corso di Laurea

**Informatica per le Aziende Digitali**

Project Work PW21

**Business Intelligence**

---

# Autore

**Crisele Ariola**

Anno Accademico 2025/2026
