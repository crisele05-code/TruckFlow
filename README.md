# 🚚 TruckFlow

> Sistema di Business Intelligence per il monitoraggio delle performance di un marketplace logistico.

## 📖 Descrizione

TruckFlow è un progetto sviluppato nell'ambito del Project Work PW21 del Corso di Laurea in Informatica per le Aziende Digitali.

L'obiettivo del progetto è progettare e implementare una soluzione completa di **Business Intelligence** in grado di trasformare dati provenienti da differenti sorgenti informative in informazioni strategiche a supporto del processo decisionale.

Il sistema comprende:

- generazione di dati sintetici;
- pipeline ETL;
- Data Warehouse multidimensionale;
- query SQL;
- dashboard interattive.

---

# 🏗 Architettura del sistema

```
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

# 🚀 Tecnologie utilizzate

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

# 📂 Struttura del progetto

```text
TruckFlow
│
├── dashboard/
│   ├── app.py
│   ├── repository.py
│   ├── charts.py
│   ├── utils.py
│   └── views/
│
├── generator/
│
├── etl/
│
├── data/
│
├── dw/
│
├── requirements.txt
│
└── README.md
```

---

# 📊 Dashboard

Il sistema mette a disposizione quattro dashboard dedicate all'analisi delle performance aziendali.

### 📈 Executive Dashboard

Consente di monitorare i principali KPI economici e operativi.

- Richieste
- Spedizioni
- Commissioni
- Ricavi

---

### 🚛 Dashboard Operativa

Analizza le attività operative della piattaforma.

- Veicoli utilizzati
- Merci trasportate
- Top trasportatori
- Distanza media

---

### 🌍 Dashboard Geografica

Permette di analizzare la distribuzione territoriale delle spedizioni.

- Mappa interattiva
- Spedizioni per regione
- Commissioni per regione

---

### 👥 Dashboard Clienti

Consente di monitorare il comportamento della clientela.

- Top clienti
- Top commissioni
- Clienti per regione
- Commissioni per regione

---

# ▶️ Avvio del progetto

Installare le dipendenze:

```bash
pip install -r requirements.txt
```

Avviare la dashboard:

```bash
python -m streamlit run dashboard/app.py
```

---

# 📚 Project Work

Corso di Laurea

**Informatica per le Aziende Digitali**

Project Work PW21

**Business Intelligence**

---

# 👩‍💻 Autore

**Crisele Ariola**

Anno Accademico 2025/2026