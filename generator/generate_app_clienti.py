import random
from datetime import timedelta
import calendar
import pandas as pd

from config import (
    NUM_CLIENTI,
    NUM_RICHIESTE,
    RANDOM_SEED,
    CATEGORIE_MERCE,
    CLIENT_COMPANY_PREFIX,
    CLIENT_COMPANY_SUFFIX,
    COMPANY_LEGAL_FORM,
    COMPATIBILITA_MERCE_VEICOLO,
    PESO_MERCE,
    TEMPI_CONSEGNA,
    DATA_INIZIO,
    DATA_FINE,
    RICHIESTE_PER_MESE, STATI_RICHIESTA, PESI_STATI_RICHIESTA
)

from generator.utils import (
    generate_id,
    generate_partita_iva,
    load_comuni,
    save_csv,
    random_date
)

random.seed(RANDOM_SEED)

# =====================================================
# GENERAZIONE CLIENTI
# =====================================================

def generate_customer(customer_number: int,
                      comuni: pd.DataFrame) -> dict:
    """
    Genera un cliente.
    """

    categoria = random.choice(CATEGORIE_MERCE)

    prefix = random.choice(
        CLIENT_COMPANY_PREFIX[categoria]
    )

    suffix = random.choice(
        CLIENT_COMPANY_SUFFIX
    )

    legal_form = random.choice(
        COMPANY_LEGAL_FORM
    )

    sede = comuni.sample(1).iloc[0]

    profilo = random.choices(
        population=[
            "top",
            "standard",
            "occasionale"
        ],
        weights=[
            20,
            60,
            20
        ],
        k=1
    )[0]

    return {

        "id_cliente": generate_id(
            "C",
            customer_number
        ),

        "ragione_sociale":
            f"{prefix} {suffix} {legal_form}",

        "partita_iva":
            generate_partita_iva(),

        "categoria_prevalente":
            categoria,

        "comune":
            sede["comune"],

        "provincia":
            sede["provincia"],

        "sigla":
            sede["sigla"],

        "regione":
            sede["regione"],

        "profilo":
            profilo
    }


def generate_customers() -> list[dict]:
    """
    Genera tutti i clienti.
    """

    comuni = load_comuni()

    clienti = []

    ragioni_sociali = set()

    partite_iva = set()

    for i in range(
            1,
            NUM_CLIENTI + 1
    ):

        while True:

            cliente = generate_customer(
                i,
                comuni
            )

            if (

                cliente["ragione_sociale"]
                not in ragioni_sociali

                and

                cliente["partita_iva"]
                not in partite_iva

            ):

                ragioni_sociali.add(
                    cliente["ragione_sociale"]
                )

                partite_iva.add(
                    cliente["partita_iva"]
                )

                clienti.append(cliente)

                break

    return clienti


# =====================================================
# FUNZIONI DI SUPPORTO
# =====================================================

def choose_customer(clienti: list[dict]) -> dict:
    """
    Seleziona un cliente in base al suo profilo.
    """

    weights = []

    for cliente in clienti:

        if cliente["profilo"] == "top":
            weights.append(10)

        elif cliente["profilo"] == "standard":
            weights.append(4)

        else:
            weights.append(1)

    return random.choices(
        population=clienti,
        weights=weights,
        k=1
    )[0]


def choose_categoria_merce(cliente: dict) -> str:
    """
    Nell'80% dei casi il cliente spedisce la propria
    categoria prevalente.
    """

    if random.random() < 0.80:
        return cliente["categoria_prevalente"]

    categorie = [

        categoria

        for categoria in CATEGORIE_MERCE

        if categoria != cliente["categoria_prevalente"]

    ]

    return random.choice(categorie)


def choose_tipo_veicolo_richiesto(categoria: str) -> str:
    """
    Seleziona un veicolo compatibile con la merce.
    """

    return random.choice(
        COMPATIBILITA_MERCE_VEICOLO[categoria]
    )


def generate_peso(categoria: str) -> int:
    """
    Genera il peso della spedizione.
    """

    minimo, massimo = PESO_MERCE[categoria]

    return random.randint(
        minimo,
        massimo
    )


def choose_origine(
        cliente: dict,
        comuni: pd.DataFrame
) -> dict:
    """
    L'origine coincide con la sede del cliente
    nell'80% dei casi.
    """

    if random.random() < 0.80:

        return {

            "comune": cliente["comune"],
            "provincia": cliente["provincia"],
            "sigla": cliente["sigla"],
            "regione": cliente["regione"]

        }

    stessa_regione = comuni[
        comuni["regione"] == cliente["regione"]
    ]

    origine = stessa_regione.sample(1).iloc[0]

    return {

        "comune": origine["comune"],
        "provincia": origine["provincia"],
        "sigla": origine["sigla"],
        "regione": origine["regione"]

    }


def choose_destinazione(
        origine: dict,
        comuni: pd.DataFrame
) -> dict:
    """
    Seleziona un comune di destinazione diverso
    dall'origine.
    """

    while True:

        destinazione = comuni.sample(1).iloc[0]

        if destinazione["comune"] != origine["comune"]:

            return {

                "comune": destinazione["comune"],
                "provincia": destinazione["provincia"],
                "sigla": destinazione["sigla"],
                "regione": destinazione["regione"]

            }


def generate_date(
        categoria: str
) -> tuple:
    """
    Genera la data della richiesta e la data
    di consegna prevista.
    """

    data_richiesta = generate_data_richiesta()

    giorni_min, giorni_max = TEMPI_CONSEGNA[categoria]

    giorni = random.randint(
        giorni_min,
        giorni_max
    )

    data_consegna = (
        data_richiesta +
        timedelta(days=giorni)
    )

    return (
        data_richiesta,
        data_consegna
    )


# =====================================================
# GENERAZIONE RICHIESTE
# =====================================================

def generate_data_richiesta():
    """
    Genera una data richiesta
    con stagionalità.
    """

    mese = random.choices(
        population=list(RICHIESTE_PER_MESE.keys()),
        weights=list(RICHIESTE_PER_MESE.values()),
        k=1
    )[0]

    ultimo_giorno = calendar.monthrange(
        DATA_INIZIO.year,
        mese
    )[1]

    giorno = random.randint(
        1,
        ultimo_giorno
    )

    return DATA_INIZIO.replace(
        month=mese,
        day=giorno
    )


# =====================================================
# STATO RICHIESTA
# =====================================================

def generate_stato_richiesta() -> str:
    """
    Genera lo stato della richiesta.
    """

    return random.choices(
        population=STATI_RICHIESTA,
        weights=PESI_STATI_RICHIESTA,
        k=1
    )[0]


def generate_request(
        request_number: int,
        clienti: list,
        comuni: pd.DataFrame
):
    """
    Genera una richiesta.
    """

    cliente = choose_customer(clienti)

    categoria = choose_categoria_merce(cliente)

    tipo_veicolo = choose_tipo_veicolo_richiesto(
        categoria
    )

    origine = choose_origine(
        cliente,
        comuni
    )

    destinazione = choose_destinazione(
        origine,
        comuni
    )

    peso = generate_peso(
        categoria
    )

    data_richiesta, data_consegna = generate_date(
        categoria
    )

    stato_richiesta = generate_stato_richiesta()

    return {

        "id_richiesta":
            generate_id(
                "R",
                request_number
            ),

        "id_cliente":
            cliente["id_cliente"],

        "data_richiesta":
            data_richiesta.strftime("%Y-%m-%d"),

        "data_consegna_prevista":
            data_consegna.strftime("%Y-%m-%d"),

        "comune_origine":
            origine["comune"],

        "provincia_origine":
            origine["provincia"],

        "regione_origine":
            origine["regione"],

        "comune_destinazione":
            destinazione["comune"],

        "provincia_destinazione":
            destinazione["provincia"],

        "regione_destinazione":
            destinazione["regione"],

        "categoria_merce":
            categoria,

        "tipo_veicolo":
            tipo_veicolo,

        "peso_kg":
            peso,

        "stato_richiesta":
            stato_richiesta
    }

# =====================================================
# GENERAZIONE DATAFRAME
# =====================================================

def generate() -> pd.DataFrame:
    """
    Genera tutte le richieste dell'App Clienti.
    """

    comuni = load_comuni()

    clienti = generate_customers()

    richieste = []

    df_clienti = pd.DataFrame(clienti)

    # Il profilo serve solo per la generazione,
    # non è una sorgente del DW.
    df_clienti = df_clienti.drop(columns=["profilo"])

    save_csv(
        df_clienti,
        "clienti.csv"
    )

    for i in range(1, NUM_RICHIESTE + 1):

        richiesta = generate_request(
            request_number=i,
            clienti=clienti,
            comuni=comuni
        )

        richieste.append(richiesta)

    df = pd.DataFrame(richieste)

    save_csv(
        df,
        "app_clienti.csv"
    )

    return df_clienti, df


# =====================================================
# MAIN
# =====================================================

def main():

    df_clienti, df_richieste = generate()

    print(f"\nClienti generati: {len(df_clienti)}")

    print(f"Richieste generate: {len(df_richieste)}")

    print("\nPrime 10 richieste:\n")

    print(df_clienti.head(10))


if __name__ == "__main__":
    main()