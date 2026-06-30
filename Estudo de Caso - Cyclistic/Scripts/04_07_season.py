# ==========================================================
# ESTUDO DE CASO - CYCLISTIC
# ETAPA 4 - ANALISAR (ANALYZE)
#
# Script: 04_07_season.py
#
# Objetivo:
# Comparar o uso das bicicletas entre as estações do ano.
#
# Autor: Lucca Nascimento
# ==========================================================

import os
import pandas as pd
import matplotlib.pyplot as plt

# ==========================================================
# CONFIGURAÇÕES
# ==========================================================

PASTA_PROJETO = r"C:\Users\Lucca\Downloads\Estudo de Caso - Cyclistic"

ARQUIVO = os.path.join(
    PASTA_PROJETO,
    "Scripts",
    "cyclistic_clean.csv"
)

PASTA_GRAFICOS = os.path.join(
    PASTA_PROJETO,
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
# ORGANIZAR ESTAÇÕES
# ==========================================================

def preparar_estacoes(df):

    ordem = [

        "Winter",
        "Spring",
        "Summer",
        "Autumn"

    ]

    df["season"] = pd.Categorical(

        df["season"],

        categories=ordem,

        ordered=True

    )

    return df


# ==========================================================
# TABELA
# ==========================================================

def tabela_resumo(df):

    print("="*70)
    print("VIAGENS POR ESTAÇÃO")
    print("="*70)

    tabela = pd.crosstab(

        df["season"],

        df["member_casual"]

    )

    percentual = (

        pd.crosstab(

            df["season"],

            df["member_casual"],

            normalize="columns"

        ) * 100

    ).round(2)

    print("\nQuantidade\n")
    print(tabela)

    print("\nPercentual (%)\n")
    print(percentual)

    return tabela, percentual


# ==========================================================
# GRÁFICO DE BARRAS
# ==========================================================

def grafico_barras(tabela):

    tabela.plot(

        kind="bar",

        figsize=(10,6)

    )

    plt.title(

        "Quantidade de Viagens por Estação do Ano",

        fontsize=18,

        fontweight="bold"

    )

    plt.xlabel("Estação")

    plt.ylabel("Número de Viagens")

    plt.grid(axis="y", alpha=0.3)

    plt.tight_layout()

    plt.savefig(

        os.path.join(

            PASTA_GRAFICOS,

            "season_bar.png"

        ),

        dpi=300

    )

    plt.show()


# ==========================================================
# GRÁFICO EMPILHADO
# ==========================================================

def grafico_percentual(percentual):

    percentual.plot(

        kind="bar",

        stacked=True,

        figsize=(10,6)

    )

    plt.title(

        "Distribuição Percentual por Estação",

        fontsize=18,

        fontweight="bold"

    )

    plt.xlabel("Estação")

    plt.ylabel("Percentual (%)")

    plt.grid(axis="y", alpha=0.3)

    plt.legend(title="Usuário")

    plt.tight_layout()

    plt.savefig(

        os.path.join(

            PASTA_GRAFICOS,

            "season_percent.png"

        ),

        dpi=300

    )

    plt.show()
    
    # ==========================================================
# ESTAÇÃO FAVORITA
# ==========================================================

def estacao_favorita(tabela):

    print("\n")
    print("="*70)
    print("ESTAÇÃO FAVORITA")
    print("="*70)

    favorita_member = tabela["member"].idxmax()
    viagens_member = tabela["member"].max()

    favorita_casual = tabela["casual"].idxmax()
    viagens_casual = tabela["casual"].max()

    print(f"\nMember : {favorita_member}")
    print(f"Viagens: {viagens_member:,}".replace(",", "."))

    print(f"\nCasual : {favorita_casual}")
    print(f"Viagens: {viagens_casual:,}".replace(",", "."))


# ==========================================================
# RESUMO
# ==========================================================

def resumo(df, tabela):

    print("\n")
    print("="*70)
    print("RESUMO")
    print("="*70)

    print("\nTotal de viagens por grupo:\n")

    print(df["member_casual"].value_counts())

    total_estacao = tabela.sum(axis=1)

    print("\nEstação mais movimentada:")

    print(
        f"{total_estacao.idxmax()} "
        f"({total_estacao.max():,} viagens)".replace(",", ".")
    )

    print("\nEstação menos movimentada:")

    print(
        f"{total_estacao.idxmin()} "
        f"({total_estacao.min():,} viagens)".replace(",", ".")
    )

    diferenca = (
        total_estacao.max() - total_estacao.min()
    )

    print(
        f"\nDiferença entre maior e menor estação: "
        f"{diferenca:,} viagens".replace(",", ".")
    )

    percentual = (
        diferenca / total_estacao.max()
    ) * 100

    print(
        f"Redução em relação ao pico: {percentual:.2f}%"
    )

    print("="*70)


# ==========================================================
# PROGRAMA PRINCIPAL
# ==========================================================

def main():

    df = carregar_base()

    df = preparar_estacoes(df)

    tabela, percentual = tabela_resumo(df)

    grafico_barras(tabela)

    grafico_percentual(percentual)

    estacao_favorita(tabela)

    resumo(df, tabela)


if __name__ == "__main__":

    main()