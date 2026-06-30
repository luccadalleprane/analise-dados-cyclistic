# ==========================================================
# ESTUDO DE CASO - CYCLISTIC
# ETAPA 4 - ANALISAR (ANALYZE)
#
# Script: 04_04_weekday.py
#
# Objetivo:
# Analisar a distribuição das viagens por dia da semana.
#
# Autor: Lucca Nascimento
# ==========================================================

import os
import pandas as pd
import matplotlib.pyplot as plt

# ==========================================================
# CONFIGURAÇÕES
# ==========================================================

BASE_PROJETO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ARQUIVO = r"C:\Users\Lucca\Downloads\Estudo de Caso - Cyclistic\Scripts\cyclistic_clean.csv"

PASTA_GRAFICOS = os.path.join(
    BASE_PROJETO,
    "Graficos"
)

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
# PREPARAÇÃO
# ==========================================================

def preparar_dados(df):

    ordem = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]

    df["day_name"] = pd.Categorical(
        df["day_name"],
        categories=ordem,
        ordered=True
    )

    return df

# ==========================================================
# TABELA
# ==========================================================

def tabela_resumo(df):

    print("="*70)
    print("VIAGENS POR DIA DA SEMANA")
    print("="*70)

    tabela = pd.crosstab(
        df["day_name"],
        df["member_casual"]
    )

    percentual = pd.crosstab(
        df["day_name"],
        df["member_casual"],
        normalize="columns"
    ) * 100

    percentual = percentual.round(2)

    print("\nQuantidade\n")

    print(tabela)

    print("\nPercentual (%)\n")

    print(percentual)

    return tabela, percentual

# ==========================================================
# BARRAS AGRUPADAS
# ==========================================================

def grafico_barras(tabela):

    ax = tabela.plot(
        kind="bar",
        figsize=(12,6)
    )

    plt.title(
        "Viagens por Dia da Semana",
        fontsize=18,
        fontweight="bold"
    )

    plt.xlabel("Dia da Semana")

    plt.ylabel("Número de Viagens")

    plt.xticks(rotation=30)

    plt.grid(axis="y", alpha=0.3)

    for container in ax.containers:

        ax.bar_label(
            container,
            fontsize=8
        )

    plt.tight_layout()

    plt.savefig(

        os.path.join(
            PASTA_GRAFICOS,
            "weekday_bar.png"
        ),

        dpi=300

    )

    plt.show()

# ==========================================================
# LINHAS
# ==========================================================

def grafico_linhas(tabela):

    plt.figure(figsize=(12,6))

    plt.plot(

        tabela.index,

        tabela["member"],

        marker="o",

        linewidth=3,

        label="Member"

    )

    plt.plot(

        tabela.index,

        tabela["casual"],

        marker="o",

        linewidth=3,

        label="Casual"

    )

    plt.title(

        "Comportamento Semanal dos Usuários",

        fontsize=18,

        fontweight="bold"

    )

    plt.xlabel("Dia da Semana")

    plt.ylabel("Número de Viagens")

    plt.grid(alpha=0.3)

    plt.legend()

    plt.tight_layout()

    plt.savefig(

        os.path.join(

            PASTA_GRAFICOS,

            "weekday_line.png"

        ),

        dpi=300

    )

    plt.show()

# ==========================================================
# PERCENTUAL
# ==========================================================

def grafico_percentual(percentual):

    percentual.plot(

        kind="bar",

        figsize=(12,6),

        stacked=True

    )

    plt.title(

        "Distribuição Percentual das Viagens",

        fontsize=18,

        fontweight="bold"

    )

    plt.xlabel("Dia da Semana")

    plt.ylabel("Percentual (%)")

    plt.xticks(rotation=30)

    plt.tight_layout()

    plt.savefig(

        os.path.join(

            PASTA_GRAFICOS,

            "weekday_percentual.png"

        ),

        dpi=300

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

    member = (

        df[df["member_casual"]=="member"]

        ["day_name"]

        .value_counts()

        .sort_index()

    )

    casual = (

        df[df["member_casual"]=="casual"]

        ["day_name"]

        .value_counts()

        .sort_index()

    )

    print("\nDia favorito dos Members:")

    print(member.idxmax())

    print("\nDia favorito dos Casual:")

    print(casual.idxmax())

    print("="*70)

# ==========================================================
# MAIN
# ==========================================================

def main():

    df = carregar_base()

    df = preparar_dados(df)

    tabela, percentual = tabela_resumo(df)

    grafico_barras(tabela)

    grafico_linhas(tabela)

    grafico_percentual(percentual)

    resumo(df)

if __name__ == "__main__":

    main()