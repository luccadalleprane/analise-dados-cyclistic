# ==========================================================
# ESTUDO DE CASO - CYCLISTIC
# ETAPA 4 - ANALISAR (ANALYZE)
#
# Script: 04_06_month.py
#
# Objetivo:
# Analisar a evolução das viagens ao longo dos meses.
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
# ORGANIZAR MESES
# ==========================================================

def preparar_meses(df):

    ordem = [

        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
        "January",
        "February",
        "March",
        "April",
        "May",
        "June"

    ]

    df["month_name"] = pd.Categorical(

        df["month_name"],

        categories=ordem,

        ordered=True

    )

    return df


# ==========================================================
# TABELA
# ==========================================================

def tabela_resumo(df):

    print("="*70)
    print("VIAGENS POR MÊS")
    print("="*70)

    tabela = pd.crosstab(

        df["month_name"],

        df["member_casual"]

    )

    percentual = pd.crosstab(

        df["month_name"],

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
# GRÁFICO DE LINHAS
# ==========================================================

def grafico_linhas(tabela):

    plt.figure(figsize=(13,6))

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

        "Evolução das Viagens ao Longo dos Meses",

        fontsize=18,

        fontweight="bold"

    )

    plt.xlabel("Mês")

    plt.ylabel("Número de Viagens")

    plt.grid(alpha=0.3)

    plt.legend()

    plt.tight_layout()

    plt.savefig(

        os.path.join(

            PASTA_GRAFICOS,

            "month_line.png"

        ),

        dpi=300

    )

    plt.show()


# ==========================================================
# GRÁFICO DE BARRAS
# ==========================================================

def grafico_barras(tabela):

    ax = tabela.plot(

        kind="bar",

        figsize=(13,6)

    )

    plt.title(

        "Quantidade de Viagens por Mês",

        fontsize=18,

        fontweight="bold"

    )

    plt.xlabel("Mês")

    plt.ylabel("Número de Viagens")

    plt.grid(axis="y", alpha=0.3)

    plt.tight_layout()

    plt.savefig(

        os.path.join(

            PASTA_GRAFICOS,

            "month_bar.png"

        ),

        dpi=300

    )

    plt.show()
    
    # ==========================================================
# GRÁFICO PERCENTUAL
# ==========================================================

def grafico_percentual(percentual):

    percentual.plot(

        kind="bar",

        stacked=True,

        figsize=(13,6)

    )

    plt.title(

        "Distribuição Percentual das Viagens por Mês",

        fontsize=18,

        fontweight="bold"

    )

    plt.xlabel("Mês")

    plt.ylabel("Percentual (%)")

    plt.grid(axis="y", alpha=0.3)

    plt.legend(title="Usuário")

    plt.tight_layout()

    plt.savefig(

        os.path.join(

            PASTA_GRAFICOS,

            "month_percent.png"

        ),

        dpi=300

    )

    plt.show()


# ==========================================================
# MÊS DE MAIOR MOVIMENTO
# ==========================================================

def maior_mes(tabela):

    print("\n")
    print("="*70)
    print("MÊS DE MAIOR MOVIMENTO")
    print("="*70)

    maior_member = tabela["member"].idxmax()
    viagens_member = tabela["member"].max()

    maior_casual = tabela["casual"].idxmax()
    viagens_casual = tabela["casual"].max()

    print(f"\nMember : {maior_member}")
    print(f"Viagens: {viagens_member:,}".replace(",", "."))

    print(f"\nCasual : {maior_casual}")
    print(f"Viagens: {viagens_casual:,}".replace(",", "."))


# ==========================================================
# RESUMO
# ==========================================================

def resumo(df, tabela):

    print("\n")
    print("="*70)
    print("RESUMO")
    print("="*70)

    print("\nTotal de viagens:\n")

    print(

        df["member_casual"]

        .value_counts()

    )

    total_mes = tabela.sum(axis=1)

    print("\nMês mais movimentado:")

    print(
        f"{total_mes.idxmax()} "
        f"({total_mes.max():,} viagens)".replace(",", ".")
    )

    print("\nMês menos movimentado:")

    print(
        f"{total_mes.idxmin()} "
        f"({total_mes.min():,} viagens)".replace(",", ".")
    )

    crescimento = (

        (total_mes.iloc[-1] - total_mes.iloc[0])

        / total_mes.iloc[0]

    ) * 100

    print(f"\nVariação Julho → Junho: {crescimento:.2f}%")

    print("="*70)


# ==========================================================
# PROGRAMA PRINCIPAL
# ==========================================================

def main():

    df = carregar_base()

    df = preparar_meses(df)

    tabela, percentual = tabela_resumo(df)

    grafico_linhas(tabela)

    grafico_barras(tabela)

    grafico_percentual(percentual)

    maior_mes(tabela)

    resumo(df, tabela)


if __name__ == "__main__":

    main()