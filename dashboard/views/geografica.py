import streamlit as st
from dashboard.utils import metric_card, format_km, format_number

from dashboard.repository import (
    get_origini_spedizioni,
    get_destinazioni_spedizioni,
    get_spedizioni_per_regione,
    get_commissioni_per_regione,
    get_numero_regioni,
    get_numero_province,
    get_numero_comuni,
    get_distanza_media,
)

from dashboard.charts import (
    plot_mappa_spedizioni,
    plot_spedizioni_per_regione,
    plot_commissioni_per_regione
)


def show_geografica():

    st.title("🌍 Dashboard Geografica")

    st.subheader("🗺️ Distribuzione geografica delle spedizioni")

    col1, col2, col3, col4 = st.columns(4)

    metric_card(
        col1,
        "🌍 Regioni servite",
        get_numero_regioni()
    )

    metric_card(
        col2,
        "🏛 Province servite",
        get_numero_province()
    )

    metric_card(
        col3,
        "📍 Comuni serviti",
        format_number(get_numero_comuni())
    )

    metric_card(
        col4,
        "🚚 Distanza media",
        format_km(get_distanza_media())
    )
    tipo = st.radio(
        "Visualizza",
        ["Origini", "Destinazioni"],
        horizontal=True
    )

    if tipo == "Origini":
        df = get_origini_spedizioni()
    else:
        df = get_destinazioni_spedizioni()

    fig = plot_mappa_spedizioni(df, tipo)

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:

        fig = plot_spedizioni_per_regione(
            get_spedizioni_per_regione()
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:

        fig = plot_commissioni_per_regione(
            get_commissioni_per_regione()
        )

        st.plotly_chart(fig, use_container_width=True)