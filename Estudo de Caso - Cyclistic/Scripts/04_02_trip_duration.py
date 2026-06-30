# ==========================================================
# ESTUDO DE CASO - CYCLISTIC
# ETAPA 4 - ANALISAR (ANALYZE)
#
# Script: 04_02_trip_duration.py
#
# Objetivo:
# Comparar a duração das viagens entre usuários
# Member e Casual.
#
# Autor: Lucca Nascimento
# ==========================================================

import os
import pandas as pd
import matplotlib.pyplot as plt

# ==========================================================
# CONFIGURAÇÕES
# ==========================================================

ARQUIVO = r"C:\Users\Lucca\Downloads\Estudo de Caso - Cyclistic\Scripts\cyclistic_clean.csv"

PASTA_GRAFICOS = r"C:\Users\Lucca\Downloads\Estudo de Caso - Cyclistic\Graficos"

os.makedirs(PASTA_GRAFICOS, exist_ok=True)

plt.rcParams["font.family"] = "Arial"
plt.rcParams["figure.dpi"] = 120

# ==========================================================
# CARREGAR BASE
# ==========================================================

def carregar_base():

    print("="*70)
    print("CARREGANDO BASE")
    print("="*70)

    df = pd.read_csv(ARQUIVO)

    print("Base carregada com sucesso.\n")

    return df

# ==========================================================
# ESTATÍSTICAS
# ==========================================================

def estatisticas(df):

    print("="*70)
    print("ESTATÍSTICAS DA DURAÇÃO DAS VIAGENS")
    print("="*70)

    tabela = (

        df.groupby("member_casual")["ride_length_min"]

        .agg(

            Quantidade="count",

            Média="mean",

            Mediana="median",

            Desvio_Padrão="std",

            Mínimo="min",

            Q1=lambda x: x.quantile(0.25),

            Q3=lambda x: x.quantile(0.75),

            Máximo="max"

        )

        .round(2)

    )

    print(tabela)

    return tabela

# ==========================================================
# BOXPLOT
# ==========================================================

def grafico_boxplot(df):

    plt.figure(figsize=(10,6))

    dados = [

        df[df["member_casual"]=="member"]["ride_length_min"],

        df[df["member_casual"]=="casual"]["ride_length_min"]

    ]

    plt.boxplot(

        dados,

        labels=["Member","Casual"],

        showfliers=False

    )

    plt.title(

        "Distribuição da Duração das Viagens",

        fontsize=18,

        fontweight="bold"

    )

    plt.ylabel("Minutos")

    plt.grid(alpha=0.3)

    plt.tight_layout()

    plt.savefig(

        os.path.join(

            PASTA_GRAFICOS,

            "duracao_boxplot.png"

        ),

        dpi=300,

        bbox_inches="tight"

    )

    plt.show()

# ==========================================================
# HISTOGRAMA
# ==========================================================

def grafico_histograma(df):

    dados = df[df["ride_length_min"] <= 180]

    plt.figure(figsize=(12,6))

    plt.hist(

        dados[dados["member_casual"]=="member"]["ride_length_min"],

        bins=50,

        alpha=0.6,

        label="Member"

    )

    plt.hist(

        dados[dados["member_casual"]=="casual"]["ride_length_min"],

        bins=50,

        alpha=0.6,

        label="Casual"

    )

    plt.title(

        "Distribuição da Duração das Viagens (até 180 min)",

        fontsize=18,

        fontweight="bold"

    )

    plt.xlabel("Duração (minutos)")

    plt.ylabel("Número de viagens")

    plt.legend()

    plt.grid(alpha=0.3)

    plt.tight_layout()

    plt.savefig(

        os.path.join(

            PASTA_GRAFICOS,

            "duracao_histograma.png"

        ),

        dpi=300,

        bbox_inches="tight"

    )

    plt.show()

# ==========================================================
# MÉDIA
# ==========================================================

def grafico_media(df):

    media = (

        df.groupby("member_casual")["ride_length_min"]

        .mean()

    )

    plt.figure(figsize=(8,6))

    barras = plt.bar(

        media.index,

        media.values

    )

    plt.title(

        "Tempo Médio das Viagens",

        fontsize=18,

        fontweight="bold"

    )

    plt.ylabel("Minutos")

    plt.grid(axis="y",alpha=0.3)

    for barra in barras:

        plt.text(

            barra.get_x()+barra.get_width()/2,

            barra.get_height(),

            f"{barra.get_height():.1f}",

            ha="center",

            va="bottom",

            fontsize=11

        )

    plt.tight_layout()

    plt.savefig(

        os.path.join(

            PASTA_GRAFICOS,

            "duracao_media.png"

        ),

        dpi=300,

        bbox_inches="tight"

    )

    plt.show()

# ==========================================================
# RESUMO
# ==========================================================

def resumo(df):

    print("\n")

    print("="*70)

    print("RESUMO")

    print("="*70)

    media = (

        df.groupby("member_casual")["ride_length_min"]

        .mean()

        .round(2)

    )

    print(media)

    print("="*70)

# ==========================================================
# PROGRAMA PRINCIPAL
# ==========================================================

def main():

    df = carregar_base()

    tabela = estatisticas(df)

    grafico_boxplot(df)

    grafico_histograma(df)

    grafico_media(df)

    resumo(df)

if __name__ == "__main__":

    main()
