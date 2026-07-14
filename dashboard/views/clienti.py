import streamlit as st

from dashboard.charts import (plot_top_clienti,
                              plot_commissioni_clienti, plot_clienti_per_regione, plot_valore_spedizioni_clienti,
                              plot_commissioni_per_regione)
from dashboard.repository import (get_top_clienti,
                                  get_commissioni_clienti, get_clienti_per_regione, get_valore_spedizioni_clienti,
                                  get_commissioni_per_regione_cliente, get_numero_clienti, get_spedizioni_medie_cliente,
                                  get_commissione_media_cliente, get_numero_regioni_clienti)
from dashboard.utils import format_number, metric_card


def show_clienti():

    st.title("👥 Dashboard Clienti")

    st.caption("Analisi della clientela della piattaforma TruckFlow")

    col1, col2, col3, col4 = st.columns(4)

    metric_card(
        col1,
        "👥 Clienti attivi",
        get_numero_clienti()
    )

    metric_card(
        col2,
        "📦 Spedizioni medie",
        f"{get_spedizioni_medie_cliente():.1f}"
    )

    metric_card(
        col3,
        "💶 Commissione media",
        f"€ {get_commissione_media_cliente():,.0f}"
    )

    metric_card(
        col4,
        "🌍 Regioni servite",
        get_numero_regioni_clienti()
    )
    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(
            plot_top_clienti(
                get_top_clienti()
            ),
            use_container_width=True
        )

    with col2:
        st.plotly_chart(
            plot_commissioni_clienti(
                get_commissioni_clienti()
            ),
            use_container_width=True
        )

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(
            plot_clienti_per_regione(
                get_clienti_per_regione()
            ),
            use_container_width=True
        )

    with col2:
        st.plotly_chart(
            plot_commissioni_per_regione(
                get_commissioni_per_regione_cliente()
            ),
            use_container_width=True
        )