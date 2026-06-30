# ==========================================================
# ESTUDO DE CASO - CYCLISTIC
# ETAPA 4 - ANALISAR (ANALYZE)
#
# Script: 04_03_bike_type.py
#
# Objetivo:
# Comparar o tipo de bicicleta utilizado pelos
# usuários Member e Casual.
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
# TABELA RESUMO
# ==========================================================

def tabela_resumo(df):

    print("="*70)
    print("TIPO DE BICICLETA")
    print("="*70)

    tabela = pd.crosstab(
        df["member_casual"],
        df["rideable_type"]
    )

    percentual = pd.crosstab(
        df["member_casual"],
        df["rideable_type"],
        normalize="index"
    ) * 100

    percentual = percentual.round(2)

    print("\nQuantidade\n")
    print(tabela)

    print("\nPercentual (%)\n")
    print(percentual)

    return tabela, percentual

# ==========================================================
# GRÁFICO DE BARRAS
# ==========================================================

def grafico_barras(tabela):

    ax = tabela.plot(
        kind="bar",
        figsize=(10,6)
    )

    plt.title(
        "Tipo de Bicicleta por Categoria de Usuário",
        fontsize=18,
        fontweight="bold"
    )

    plt.xlabel("Categoria")

    plt.ylabel("Número de viagens")

    plt.xticks(rotation=0)

    plt.grid(axis="y", alpha=0.3)

    for container in ax.containers:
        ax.bar_label(
            container,
            fmt='%.0f',
            fontsize=10
        )

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            PASTA_GRAFICOS,
            "bike_type_bar.png"
        ),
        dpi=300
    )

    plt.show()

# ==========================================================
# GRÁFICO EMPILHADO
# ==========================================================

def grafico_empilhado(percentual):

    percentual.plot(
        kind="bar",
        stacked=True,
        figsize=(10,6)
    )

    plt.title(
        "Distribuição Percentual do Tipo de Bicicleta",
        fontsize=18,
        fontweight="bold"
    )

    plt.xlabel("Categoria")

    plt.ylabel("Percentual (%)")

    plt.xticks(rotation=0)

    plt.legend(title="Tipo")

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            PASTA_GRAFICOS,
            "bike_type_percentual.png"
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

    print("Tipos de bicicleta disponíveis:")

    for tipo in df["rideable_type"].unique():

        qtd = (df["rideable_type"] == tipo).sum()

        print(f"{tipo}: {qtd:,}".replace(",", "."))

    print("="*70)

# ==========================================================
# PROGRAMA PRINCIPAL
# ==========================================================

def main():

    df = carregar_base()

    tabela, percentual = tabela_resumo(df)

    grafico_barras(tabela)

    grafico_empilhado(percentual)

    resumo(df)

if __name__ == "__main__":

    main()