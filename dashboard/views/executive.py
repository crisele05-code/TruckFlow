import streamlit as st

from dashboard.repository import (
    get_kpi,
    get_richieste_mensili,
    get_spedizioni_mensili,
    get_commissioni_mensili,
    get_valore_spedizioni_mensile
)

from dashboard.charts import (
    plot_richieste_spedizioni,
    plot_commissioni_mensili,
    plot_valore_spedizioni_mensile
)

from dashboard.utils import (
    metric_card,
    format_currency,
    format_percentage,
    format_days
)


def show_executive():

    # =====================================================
    # CARICAMENTO DATI
    # =====================================================

    kpi = get_kpi().iloc[0]

    richieste = get_richieste_mensili()

    spedizioni = get_spedizioni_mensili()

    commissioni = get_commissioni_mensili()

    valore_spedizioni = get_valore_spedizioni_mensile()

    # =====================================================
    # TITOLO
    # =====================================================

    st.title("📊 Executive Dashboard")

    st.caption(
        "Panoramica delle performance della piattaforma TruckFlow"
    )

    # =====================================================
    # KPI
    # =====================================================

    col1, col2, col3 = st.columns(3)

    metric_card(
        col1,
        "📦 Richieste",
        int(kpi["richieste"])
    )

    metric_card(
        col2,
        "🚛 Spedizioni",
        int(kpi["spedizioni"])
    )

    metric_card(
        col3,
        "📈 Conversione",
        format_percentage(kpi["conversione"])
    )

    col4, col5, col6 = st.columns(3)

    metric_card(
        col4,
        "💶 Commissioni",
        format_currency(kpi["commissioni"])
    )

    metric_card(
        col5,
        "💰 Valore spedizioni",
        format_currency(kpi["valore_spedizioni"])
    )

    metric_card(
        col6,
        "⏱️ Tempo medio",
        format_days(kpi["tempo_medio"])
    )

    # =====================================================
    # GRAFICO PRINCIPALE
    # =====================================================

    st.markdown("## 📈 Richieste e Spedizioni")

    fig = plot_richieste_spedizioni(
        richieste,
        spedizioni
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # =====================================================
    # GRAFICI ECONOMICI
    # =====================================================

    st.markdown("## 💼 Andamento economico")

    col1, col2 = st.columns(2)

    with col1:

        fig = plot_commissioni_mensili(
            commissioni
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        fig = plot_valore_spedizioni_mensile(
            valore_spedizioni
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )