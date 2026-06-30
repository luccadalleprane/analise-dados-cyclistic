# ==========================================================
# ESTUDO DE CASO - CYCLISTIC
# ETAPA 4 - ANALISAR (ANALYZE)
#
# Script: 04_08_weekend.py
#
# Objetivo:
# Comparar o uso das bicicletas entre dias úteis
# e finais de semana.
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
# PREPARAR DADOS
# ==========================================================

def preparar_dados(df):

    df["Tipo de Dia"] = df["is_weekend"].map({

        False: "Weekday",

        True: "Weekend"

    })

    return df


# ==========================================================
# TABELA
# ==========================================================

def tabela_resumo(df):

    print("="*70)
    print("DIAS ÚTEIS x FINAIS DE SEMANA")
    print("="*70)

    tabela = pd.crosstab(

        df["Tipo de Dia"],

        df["member_casual"]

    )

    percentual = (

        pd.crosstab(

            df["Tipo de Dia"],

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

        figsize=(8,6)

    )

    plt.title(

        "Viagens em Dias Úteis e Finais de Semana",

        fontsize=18,

        fontweight="bold"

    )

    plt.xlabel("Tipo de Dia")

    plt.ylabel("Número de Viagens")

    plt.grid(axis="y", alpha=0.3)

    plt.tight_layout()

    plt.savefig(

        os.path.join(

            PASTA_GRAFICOS,

            "weekend_bar.png"

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

        figsize=(8,6)

    )

    plt.title(

        "Distribuição Percentual das Viagens",

        fontsize=18,

        fontweight="bold"

    )

    plt.xlabel("Tipo de Dia")

    plt.ylabel("Percentual (%)")

    plt.grid(axis="y", alpha=0.3)

    plt.legend(title="Usuário")

    plt.tight_layout()

    plt.savefig(

        os.path.join(

            PASTA_GRAFICOS,

            "weekend_percent.png"

        ),

        dpi=300

    )

    plt.show()
    
# ==========================================================
# TIPO DE DIA FAVORITO
# ==========================================================

def tipo_dia_favorito(tabela):

    print("\n")
    print("="*70)
    print("TIPO DE DIA FAVORITO")
    print("="*70)

    favorito_member = tabela["member"].idxmax()
    viagens_member = tabela["member"].max()

    favorito_casual = tabela["casual"].idxmax()
    viagens_casual = tabela["casual"].max()

    print(f"\nMember : {favorito_member}")
    print(f"Viagens: {viagens_member:,}".replace(",", "."))

    print(f"\nCasual : {favorito_casual}")
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

    total = tabela.sum(axis=1)

    print("\nTipo de dia mais movimentado:")

    print(
        f"{total.idxmax()} "
        f"({total.max():,} viagens)".replace(",", ".")
    )

    print("\nTipo de dia menos movimentado:")

    print(
        f"{total.idxmin()} "
        f"({total.min():,} viagens)".replace(",", ".")
    )

    diferenca = total.max() - total.min()

    print(
        f"\nDiferença absoluta: "
        f"{diferenca:,} viagens".replace(",", ".")
    )

    percentual = (diferenca / total.max()) * 100

    print(
        f"Redução em relação ao maior movimento: "
        f"{percentual:.2f}%"
    )

    print("="*70)


# ==========================================================
# PROGRAMA PRINCIPAL
# ==========================================================

def main():

    df = carregar_base()

    df = preparar_dados(df)

    tabela, percentual = tabela_resumo(df)

    grafico_barras(tabela)

    grafico_percentual(percentual)

    tipo_dia_favorito(tabela)

    resumo(df, tabela)


if __name__ == "__main__":

    main()