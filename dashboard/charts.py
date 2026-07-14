"""
charts.py

Grafici della dashboard TruckFlow.

Autore: Crisele Ariola
Project Work PW21
"""

import pandas as pd
import plotly.express as px
from dashboard.repository import MESI
import plotly.graph_objects as go





# =====================================================
# RICHIESTE VS SPEDIZIONI
# =====================================================

def plot_richieste_spedizioni(
        richieste: pd.DataFrame,
        spedizioni: pd.DataFrame
):
    """
    Grafico dell'andamento mensile
    delle richieste e delle spedizioni.
    """

    df = richieste.merge(
        spedizioni,
        on=["anno", "mese"]
    )



    fig = px.line(

        df,

        x="mese_nome",

        y=[
            "richieste",
            "spedizioni"
        ],

        markers=True,

        color_discrete_map={
            "richieste": "#3366CC",
            "spedizioni": "#2E8B57"
        }

    )

    # Rinomina le serie
    fig.for_each_trace(

        lambda trace: trace.update(

            name="Richieste"
            if trace.name == "richieste"
            else "Spedizioni"

        )

    )

    fig.update_traces(

        line_width=3,

        marker=dict(
            size=9
        )

    )

    fig.update_layout(

        template="plotly_white",

        title=dict(

            text="Andamento mensile delle Richieste e delle Spedizioni",

            x=0.5,

            xanchor="center"

        ),

        xaxis_title="Mese",

        yaxis_title="Numero",

        legend=dict(

            orientation="h",

            yanchor="bottom",

            y=1.02,

            xanchor="right",

            x=1

        ),

        legend_title="",

        hovermode="x unified",

        font=dict(

            family="Arial",

            size=13

        ),

        margin=dict(

            t=80,

            l=50,

            r=20,

            b=50

        )

    )

    fig.update_yaxes(

        rangemode="tozero"

    )

    return fig

# =====================================================
# COMMISSIONI MENSILI
# =====================================================

def plot_commissioni_mensili(
        commissioni: pd.DataFrame
):
    """
    Grafico dell'andamento mensile
    delle commissioni.
    """

    fig = px.bar(

        commissioni,

        x="mese_nome",

        y="commissioni",

        text=commissioni["commissioni"].apply(
            lambda x: f"{x:,.0f} €".replace(",", ".")
        ),

        color_discrete_sequence=[
            "#2E8B57"
        ]

    )

    fig.update_traces(

        textposition="outside",

        hovertemplate=(
            "<b>%{x}</b><br>"
            "Commissioni: € %{y:,.2f}"
            "<extra></extra>"
        )

    )

    fig.update_layout(

        template="plotly_white",

        title=dict(

            text="Andamento mensile delle Commissioni",

            x=0.5,

            xanchor="center"

        ),

        xaxis_title="Mese",

        yaxis_title="Commissioni (€)",

        font=dict(

            family="Arial",

            size=13

        ),

        margin=dict(

            t=80,

            l=50,

            r=20,

            b=50

        )

    )

    fig.update_xaxes(

        showgrid=False

    )

    fig.update_yaxes(

        gridcolor="#ECECEC",

        rangemode="tozero"

    )

    return fig


# =====================================================
# VALORE SPEDIZIONI
# =====================================================

def plot_valore_spedizioni_mensile(
        valore_spedizioni: pd.DataFrame
):
    """
    Grafico del Valore delle Spedizioni.
    """

    fig = px.bar(

        valore_spedizioni,

        x="mese_nome",

        y="valore_spedizioni",

        text=valore_spedizioni["valore_spedizioni"].apply(
            lambda x: f"{x:,.0f} €".replace(",", ".")
        ),

        color_discrete_sequence=[
            "#3366CC"
        ]

    )

    fig.update_traces(

        textposition="outside",

        hovertemplate=(

            "<b>%{x}</b><br>"

            "Valore spedizioni: € %{y:,.2f}"

            "<extra></extra>"

        )

    )

    fig.update_layout(

        template="plotly_white",

        title=dict(

            text="Valore delle Spedizioni",

            x=0.5,

            xanchor="center"

        ),

        xaxis_title="Mese",

        yaxis_title="Valore (€)",

        font=dict(

            family="Arial",

            size=13

        ),

        margin=dict(

            t=80,

            l=50,

            r=20,

            b=50

        )

    )

    fig.update_xaxes(

        showgrid=False

    )

    fig.update_yaxes(

        gridcolor="#ECECEC",

        rangemode="tozero"

    )

    return fig





import plotly.express as px


def plot_veicoli_utilizzati(df):

    fig = px.bar(
        df,
        x="tipo_veicolo",
        y="spedizioni",
        text="spedizioni",
        color="spedizioni",
        color_continuous_scale="Blues",
        hover_data={
            "spedizioni": True,
            "percentuale": True
        }
    )

    fig.update_traces(
        textposition="outside"
    )

    fig.update_layout(
        title="🚚 Veicoli maggiormente utilizzati",
        xaxis_title="Tipologia di veicolo",
        yaxis_title="Numero spedizioni",
        template="plotly_dark",
        coloraxis_showscale=False,
        height=500,
        title_x=0.5
    )

    return fig


def plot_merci_trasportate(df):

    fig = px.bar(

        df,

        x="categoria_merce",
        y="spedizioni",

        text="spedizioni",

        color_discrete_sequence=["#F59E0B"],

        hover_data={
            "spedizioni": True,
            "percentuale": True
        }

    )

    fig.update_traces(

        width=0.72,

        textposition="outside"

    )

    fig.update_layout(

        title="📦 Merci maggiormente trasportate",

        title_x=0.5,

        xaxis_title="Categoria merce",

        yaxis_title="Numero spedizioni",

        template="plotly_dark",

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        height=500,

        margin=dict(
            l=10,
            r=10,
            t=60,
            b=10
        )

    )

    fig.update_xaxes(

        tickangle=-30,

        showgrid=False

    )

    fig.update_yaxes(

        showgrid=True,

        gridcolor="rgba(255,255,255,0.15)"

    )

    return fig

def plot_top_trasportatori(df):

    fig = px.bar(

        df,

        x="spedizioni",

        y="ragione_sociale",

        orientation="h",

        text="spedizioni",

        color_discrete_sequence=["#3B82F6"],

        hover_data={
            "spedizioni": True,
            "percentuale": True
        }

    )

    fig.update_traces(

        width=0.72,

        textposition="outside"

    )

    fig.update_layout(

        title="🏆 Top 10 Trasportatori",

        title_x=0.5,

        xaxis_title="Numero spedizioni",

        yaxis_title="",

        template="plotly_dark",

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        height=500,

        margin=dict(
            l=10,
            r=10,
            t=60,
            b=10
        )

    )

    fig.update_xaxes(

        showgrid=True,

        gridcolor="rgba(255,255,255,0.15)"

    )

    fig.update_yaxes(

        categoryorder="total ascending"

    )

    return fig


def plot_distanza_media_veicolo(df):

    fig = px.bar(

        df,

        x="tipo_veicolo",

        y="distanza_media",

        text="distanza_media",

        color_discrete_sequence=["#8B5CF6"]

    )

    fig.update_traces(

        width=0.72,

        texttemplate="%{text:.0f} km",

        textposition="outside"

    )

    fig.update_layout(

        title="🚚 Distanza media per tipologia di veicolo",

        title_x=0.5,

        xaxis_title="Tipologia di veicolo",

        yaxis_title="Distanza media (km)",

        template="plotly_dark",

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        height=500,

        margin=dict(
            l=10,
            r=10,
            t=60,
            b=10
        )

    )

    fig.update_yaxes(

        showgrid=True,

        gridcolor="rgba(255,255,255,0.15)"

    )

    return fig

def plot_mappa_spedizioni(df):

    fig = px.scatter_map(
        df,

        lat="lat",

        lon="lon",

        hover_name="comune",

        hover_data={
            "provincia": True,
            "regione": True
        },

        zoom=4.7,

        center={
            "lat": 42.5,
            "lon": 12.5
        },

        height=650
    )

    fig.update_layout(

        title="🗺️ Distribuzione geografica delle spedizioni",

        title_x=0.5,

        margin=dict(
            l=0,
            r=0,
            t=60,
            b=0
        )
    )

    return fig


def plot_mappa_spedizioni(df, tipo):

    colore = "#F39C12" if tipo == "Origini" else "#2563EB"

    fig = px.scatter_map(
        df,

        lat="lat",
        lon="lon",

        size="spedizioni",
        size_max=22,

        hover_name="comune",

        hover_data={
            "provincia": True,
            "regione": True,
            "spedizioni": True,
            "lat": False,
            "lon": False
        },

        zoom=4.8,

        center=dict(
            lat=42.5,
            lon=12.5
        ),

        height=700
    )

    fig.update_traces(

        marker=dict(
            color=colore,
            opacity=0.72
        )

    )

    fig.update_layout(

        title=f"🗺️ {tipo} delle spedizioni",

        title_x=0.5,

        map=dict(
            style="carto-positron"
        ),

        margin=dict(
            l=0,
            r=0,
            t=60,
            b=0
        )
    )

    return fig


def plot_spedizioni_per_regione(df):

    fig = px.bar(

        df,

        x="spedizioni",

        y="regione",

        orientation="h",

        text="spedizioni",

        color_discrete_sequence=["#3B82F6"]

    )

    fig.update_traces(

        textposition="outside",

        width=0.72

    )

    fig.update_layout(

        title="📦 Spedizioni per Regione",

        title_x=0.5,

        xaxis_title="Numero spedizioni",

        yaxis_title="",

        template="plotly_dark",

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        height=500,

        margin=dict(
            l=10,
            r=10,
            t=60,
            b=10
        )

    )

    fig.update_yaxes(

        categoryorder="total ascending"

    )

    return fig


def plot_commissioni_per_regione(df):

    fig = px.bar(

        df,

        x="commissioni",

        y="regione",

        orientation="h",

        text="commissioni",

        color_discrete_sequence=["#10B981"]

    )

    fig.update_traces(
        width=0.60,
        textposition="outside"
    )

    fig.update_layout(

        title="💶 Commissioni per Regione",

        title_x=0.5,

        xaxis_title="Commissioni (€)",

        yaxis_title="",

        template="plotly_dark",

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        height=500,

        margin=dict(
            l=10,
            r=10,
            t=60,
            b=10
        )

    )

    fig.update_yaxes(
        categoryorder="total ascending"
    )

    fig.update_xaxes(
        showgrid=True,
        gridcolor="rgba(255,255,255,0.15)"
    )

    return fig


def plot_top_clienti(df):

    fig = px.bar(

        df,

        x="spedizioni",

        y="ragione_sociale",

        orientation="h",

        text="spedizioni",

        color_discrete_sequence=["#2563EB"]

    )

    fig.update_traces(
        width=0.60,

        textposition="outside"
    )

    fig.update_layout(

        title="🏆 Top 10 Clienti",

        title_x=0.5,

        xaxis_title="Numero spedizioni",

        yaxis_title="",

        template="plotly_dark",

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        height=500,

        margin=dict(
            l=10,
            r=10,
            t=60,
            b=10
        )

    )

    fig.update_xaxes(
        showgrid=True,
        gridcolor="rgba(255,255,255,0.15)"
    )

    fig.update_yaxes(
        categoryorder="total ascending"
    )

    return fig

def plot_commissioni_clienti(df):

    fig = px.bar(

        df,

        x="commissioni",

        y="ragione_sociale",

        orientation="h",

        text="commissioni",

        color_discrete_sequence=["#10B981"]

    )

    fig.update_traces(

        texttemplate="€ %{x:,.0f}",

        textposition="outside",

        width=0.60

    )

    fig.update_layout(

        title="💶 Top 10 Clienti per Commissioni",

        title_x=0.5,

        xaxis_title="Commissioni (€)",

        yaxis_title="",

        template="plotly_dark",

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        height=500,

        margin=dict(
            l=10,
            r=10,
            t=60,
            b=10
        )

    )

    fig.update_xaxes(
        showgrid=True,
        gridcolor="rgba(255,255,255,0.15)"
    )

    fig.update_yaxes(
        categoryorder="total ascending"
    )

    return fig

def plot_clienti_per_regione(df):

    fig = px.bar(

        df,

        x="clienti",

        y="regione",

        orientation="h",

        text="clienti",

        color_discrete_sequence=["#8B5CF6"]

    )

    fig.update_traces(

        width=0.60,

        textposition="outside"

    )

    fig.update_layout(

        title="🌍 Clienti per Regione",

        title_x=0.5,

        xaxis_title="Numero clienti",

        yaxis_title="",

        template="plotly_dark",

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        height=500,

        margin=dict(
            l=10,
            r=10,
            t=60,
            b=10
        )

    )

    fig.update_xaxes(

        showgrid=True,

        gridcolor="rgba(255,255,255,0.15)"

    )

    fig.update_yaxes(

        categoryorder="total ascending"

    )

    return fig


def plot_valore_spedizioni_clienti(df):

    fig = px.bar(

        df,

        x="valore",

        y="ragione_sociale",

        orientation="h",

        text="valore",

        color_discrete_sequence=["#F59E0B"]

    )

    fig.update_traces(

        width=0.72,

        textposition="outside"

    )

    fig.update_layout(

        title="💰 Top 10 Clienti per Valore Spedizioni",

        title_x=0.5,

        xaxis_title="Valore spedizioni (€)",

        yaxis_title="",

        template="plotly_dark",

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        height=500,

        margin=dict(
            l=10,
            r=10,
            t=60,
            b=10
        )

    )

    fig.update_xaxes(

        showgrid=True,

        gridcolor="rgba(255,255,255,0.15)"

    )

    fig.update_yaxes(

        categoryorder="total ascending"

    )

    return fig


def plot_commissioni_per_regione(df):

    fig = px.bar(

        df,

        x="commissioni",

        y="regione",

        orientation="h",

        text="commissioni",

        color_discrete_sequence=["#10B981"]

    )

    fig.update_traces(

        texttemplate="€ %{x:,.0f}",

        textposition="outside",

        width=0.60

    )

    fig.update_layout(

        title="💰 Commissioni per Regione",

        title_x=0.5,

        xaxis_title="Commissioni (€)",

        yaxis_title="",

        template="plotly_dark",

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        height=500,

        margin=dict(
            l=10,
            r=10,
            t=60,
            b=10
        )

    )

    fig.update_xaxes(

        showgrid=True,

        gridcolor="rgba(255,255,255,0.15)"

    )

    fig.update_yaxes(

        categoryorder="total ascending"

    )

    return fig