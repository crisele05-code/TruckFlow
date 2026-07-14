import streamlit as st

from dashboard.views.executive import show_executive
from dashboard.views.operativa import show_operativa
from dashboard.views.geografica import show_geografica
from dashboard.views.clienti import show_clienti


st.set_page_config(
    page_title="TruckFlow",
    page_icon="🚛",
    layout="wide"
)

with st.sidebar:

    st.title("🚛 TruckFlow")

    st.markdown("---")

    pagina = st.radio(

        "Dashboard",

        [

            "Executive",

            "Operativa",

            "Geografica",

            "Clienti"

        ]

    )

    st.markdown("---")

    st.caption("Versione 1.0")

    st.caption("Data Warehouse 2026")


if pagina == "Executive":

    show_executive()

elif pagina == "Operativa":

    show_operativa()

elif pagina == "Geografica":

    show_geografica()

else:

    show_clienti()