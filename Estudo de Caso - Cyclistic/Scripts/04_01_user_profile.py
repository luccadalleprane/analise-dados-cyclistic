# ==========================================================
# ESTUDO DE CASO - CYCLISTIC
# ETAPA 4 - ANALISAR (ANALYZE)
#
# Script: 04_01_user_profile.py
#
# Objetivo:
# Analisar o perfil dos usuários da Cyclistic.
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
    print("CARREGANDO BASE...")
    print("="*70)

    df = pd.read_csv(ARQUIVO)

    print("Base carregada com sucesso.\n")

    return df

# ==========================================================
# TABELA RESUMO
# ==========================================================

def resumo_usuarios(df):

    print("="*70)
    print("PERFIL DOS USUÁRIOS")
    print("="*70)

    tabela = (

        df["member_casual"]

        .value_counts()

        .rename("Quantidade")

        .to_frame()

    )

    tabela["Percentual (%)"] = (

        tabela["Quantidade"]

        / tabela["Quantidade"].sum()

        *100

    ).round(2)

    print(tabela)

    return tabela

# ==========================================================
# GRÁFICO DE BARRAS
# ==========================================================

def grafico_barras(tabela):

    plt.figure(figsize=(10,6))

    barras = plt.bar(

        tabela.index,

        tabela["Quantidade"]

    )

    plt.title(

        "Quantidade de Usuários por Categoria",

        fontsize=18,

        fontweight="bold"

    )

    plt.xlabel("Categoria")

    plt.ylabel("Número de Viagens")

    plt.grid(

        axis="y",

        alpha=0.3

    )

    for barra in barras:

        altura = barra.get_height()

        plt.text(

            barra.get_x()+barra.get_width()/2,

            altura,

            f"{altura:,.0f}".replace(",", "."),

            ha="center",

            va="bottom",

            fontsize=11

        )

    plt.tight_layout()

    caminho = os.path.join(

        PASTA_GRAFICOS,

        "perfil_usuarios_barra.png"

    )

    plt.savefig(

        caminho,

        dpi=300,

        bbox_inches="tight"

    )

    plt.show()

# ==========================================================
# GRÁFICO DE PIZZA
# ==========================================================

def grafico_pizza(tabela):

    plt.figure(figsize=(8,8))

    plt.pie(

        tabela["Quantidade"],

        labels=tabela.index,

        autopct="%1.1f%%",

        startangle=90

    )

    plt.title(

        "Distribuição dos Usuários",

        fontsize=18,

        fontweight="bold"

    )

    plt.tight_layout()

    caminho = os.path.join(

        PASTA_GRAFICOS,

        "perfil_usuarios_pizza.png"

    )

    plt.savefig(

        caminho,

        dpi=300,

        bbox_inches="tight"

    )

    plt.show()

# ==========================================================
# RESUMO FINAL
# ==========================================================

def resumo_final(df):

    print("\n")

    print("="*70)

    print("RESUMO")

    print("="*70)

    print(f"Total de viagens : {len(df):,}".replace(",", "."))

    print(f"Members          : {(df['member_casual']=='member').sum():,}".replace(",", "."))

    print(f"Casual           : {(df['member_casual']=='casual').sum():,}".replace(",", "."))

    print("="*70)

# ==========================================================
# PROGRAMA PRINCIPAL
# ==========================================================

def main():

    df = carregar_base()

    tabela = resumo_usuarios(df)

    grafico_barras(tabela)

    grafico_pizza(tabela)

    resumo_final(df)

if __name__ == "__main__":

    main()