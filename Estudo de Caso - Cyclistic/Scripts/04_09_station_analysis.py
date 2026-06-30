# ==========================================================
# ESTUDO DE CASO - CYCLISTIC
# ETAPA 4 - ANALISAR (ANALYZE)
#
# Script: 04_09_station_analysis.py
#
# Objetivo:
# Analisar as estações mais utilizadas pelos usuários.
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
# TOP 10 ORIGEM
# ==========================================================

def top_origem(df):

    print("="*70)
    print("TOP 10 ESTAÇÕES DE ORIGEM")
    print("="*70)

    origem = (

        df.groupby("start_station_name")

        .size()

        .sort_values(ascending=False)

        .head(10)

    )

    print(origem)

    return origem


# ==========================================================
# TOP 10 DESTINO
# ==========================================================

def top_destino(df):

    print("\n")
    print("="*70)
    print("TOP 10 ESTAÇÕES DE DESTINO")
    print("="*70)

    destino = (

        df.groupby("end_station_name")

        .size()

        .sort_values(ascending=False)

        .head(10)

    )

    print(destino)

    return destino


# ==========================================================
# TOP ORIGEM POR USUÁRIO
# ==========================================================

def origem_usuario(df):

    print("\n")
    print("="*70)
    print("TOP 10 ORIGEM - MEMBER")
    print("="*70)

    member = (

        df[df["member_casual"]=="member"]

        .groupby("start_station_name")

        .size()

        .sort_values(ascending=False)

        .head(10)

    )

    print(member)

    print("\n")
    print("="*70)
    print("TOP 10 ORIGEM - CASUAL")
    print("="*70)

    casual = (

        df[df["member_casual"]=="casual"]

        .groupby("start_station_name")

        .size()

        .sort_values(ascending=False)

        .head(10)

    )

    print(casual)

    return member, casual


# ==========================================================
# GRÁFICO ORIGEM
# ==========================================================

def grafico_origem(origem):

    origem.sort_values().plot(

        kind="barh",

        figsize=(10,6)

    )

    plt.title(

        "Top 10 Estações de Origem",

        fontsize=18,

        fontweight="bold"

    )

    plt.xlabel("Número de viagens")

    plt.tight_layout()

    plt.grid(axis="x", alpha=0.3)

    plt.savefig(

        os.path.join(

            PASTA_GRAFICOS,

            "top_origin.png"

        ),

        dpi=300

    )

    plt.show()


# ==========================================================
# GRÁFICO DESTINO
# ==========================================================

def grafico_destino(destino):

    destino.sort_values().plot(

        kind="barh",

        figsize=(10,6)

    )

    plt.title(

        "Top 10 Estações de Destino",

        fontsize=18,

        fontweight="bold"

    )

    plt.xlabel("Número de viagens")

    plt.tight_layout()

    plt.grid(axis="x", alpha=0.3)

    plt.savefig(

        os.path.join(

            PASTA_GRAFICOS,

            "top_destination.png"

        ),

        dpi=300

    )

    plt.show()
    
    # ==========================================================
# GRÁFICO TOP ORIGEM - MEMBER
# ==========================================================

def grafico_member(member):

    member.sort_values().plot(

        kind="barh",

        figsize=(10,6),

        color="royalblue"

    )

    plt.title(

        "Top 10 Estações de Origem - Members",

        fontsize=18,

        fontweight="bold"

    )

    plt.xlabel("Número de viagens")

    plt.grid(axis="x", alpha=0.3)

    plt.tight_layout()

    plt.savefig(

        os.path.join(

            PASTA_GRAFICOS,

            "top_origin_member.png"

        ),

        dpi=300

    )

    plt.show()


# ==========================================================
# GRÁFICO TOP ORIGEM - CASUAL
# ==========================================================

def grafico_casual(casual):

    casual.sort_values().plot(

        kind="barh",

        figsize=(10,6),

        color="darkorange"

    )

    plt.title(

        "Top 10 Estações de Origem - Casual",

        fontsize=18,

        fontweight="bold"

    )

    plt.xlabel("Número de viagens")

    plt.grid(axis="x", alpha=0.3)

    plt.tight_layout()

    plt.savefig(

        os.path.join(

            PASTA_GRAFICOS,

            "top_origin_casual.png"

        ),

        dpi=300

    )

    plt.show()


# ==========================================================
# RESUMO
# ==========================================================

def resumo(df, origem, destino):

    print("\n")
    print("="*70)
    print("RESUMO")
    print("="*70)

    print(f"\nTotal de viagens analisadas: {len(df):,}".replace(",", "."))

    print("\nEstação de origem mais utilizada:")

    print(
        f"{origem.idxmax()} "
        f"({origem.max():,} viagens)".replace(",", ".")
    )

    print("\nEstação de destino mais utilizada:")

    print(
        f"{destino.idxmax()} "
        f"({destino.max():,} viagens)".replace(",", ".")
    )

    print("\nQuantidade de estações distintas:")

    print(
        f"Origem : {df['start_station_name'].nunique()}"
    )

    print(
        f"Destino: {df['end_station_name'].nunique()}"
    )

    print("="*70)


# ==========================================================
# PROGRAMA PRINCIPAL
# ==========================================================

def main():

    df = carregar_base()

    origem = top_origem(df)

    destino = top_destino(df)

    member, casual = origem_usuario(df)

    grafico_origem(origem)

    grafico_destino(destino)

    grafico_member(member)

    grafico_casual(casual)

    resumo(df, origem, destino)


if __name__ == "__main__":

    main()