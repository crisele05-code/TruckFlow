import streamlit as st

from dashboard.repository import (
    get_kpi_operativa,
    get_veicoli_utilizzati,
    get_merci_trasportate,
    get_top_trasportatori,
    get_distanza_media_veicolo
)

from dashboard.charts import (
    plot_veicoli_utilizzati,
    plot_merci_trasportate,
    plot_top_trasportatori,
    plot_distanza_media_veicolo
)

from dashboard.utils import metric_card


def show_operativa():

    st.title("🚛 Dashboard Operativa")

    st.caption(
        "Monitoraggio delle attività operative della piattaforma TruckFlow"
    )

    st.markdown("---")

    # ==========================================================
    # KPI
    # ==========================================================

    kpi = get_kpi_operativa().iloc[0]

    col1, col2, col3, col4 = st.columns(4)

    metric_card(
        col1,
        "🚛 Spedizioni concluse",
        int(kpi["spedizioni"])
    )

    metric_card(
        col2,
        "🚚 Tipologie veicolo",
        int(kpi["tipologie_veicolo"])
    )

    metric_card(
        col3,
        "📦 Categorie merce",
        int(kpi["categorie_merce"])
    )

    metric_card(
        col4,
        "🤝 Trasportatori attivi",
        int(kpi["trasportatori"])
    )


    # ==========================================================
    # GRAFICI
    # ==========================================================

    col1, col2 = st.columns(2)

    with col1:

        st.plotly_chart(
            plot_veicoli_utilizzati(
                get_veicoli_utilizzati()
            ),
            use_container_width=True
        )

    with col2:

        st.plotly_chart(
            plot_merci_trasportate(
                get_merci_trasportate()
            ),
            use_container_width=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    col3, col4 = st.columns(2)

    with col3:

        st.plotly_chart(
            plot_top_trasportatori(
                get_top_trasportatori()
            ),
            use_container_width=True
        )

    with col4:

        st.plotly_chart(
            plot_distanza_media_veicolo(
                get_distanza_media_veicolo()
            ),
            use_container_width=True
        )