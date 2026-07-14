import streamlit as st


def format_currency(value):
    return f"€ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def format_number(value):
    return f"{value:,.0f}".replace(",", ".")


def format_percentage(value):
    return f"{value:.1f}%"


def format_days(value):
    return f"{value:.1f} giorni".replace(".", ",")


def format_km(value):
    return f"{value:,.0f} km".replace(",", ".")


def metric_card(col, titolo, valore):
    with col:
        st.metric(
            label=titolo,
            value=valore,
            border=True
        )