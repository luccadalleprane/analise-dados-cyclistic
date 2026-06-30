# ==========================================================
# ESTUDO DE CASO - CYCLISTIC
# ETAPA 4 - ANALISAR (ANALYZE)
#
# Script: 04_05_hour.py
#
# Objetivo:
# Analisar a distribuição das viagens ao longo das horas do dia.
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

def tabela_horas(df):

    print("="*70)
    print("VIAGENS POR HORA")
    print("="*70)

    tabela = pd.crosstab(
        df["hour"],
        df["member_casual"]
    )

    percentual = pd.crosstab(
        df["hour"],
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
        linewidth=2.8,
        label="Member"
    )

    plt.plot(
        tabela.index,
        tabela["casual"],
        marker="o",
        linewidth=2.8,
        label="Casual"
    )

    plt.title(
        "Distribuição das Viagens por Hora",
        fontsize=18,
        fontweight="bold"
    )

    plt.xlabel("Hora do Dia")

    plt.ylabel("Número de Viagens")

    plt.xticks(range(24))

    plt.grid(alpha=0.3)

    plt.legend()

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            PASTA_GRAFICOS,
            "hour_line.png"
        ),
        dpi=300
    )

    plt.show()


# ==========================================================
# BARRAS AGRUPADAS
# ==========================================================

def grafico_barras(tabela):

    ax = tabela.plot(
        kind="bar",
        figsize=(15,6)
    )

    plt.title(
        "Viagens por Hora",
        fontsize=18,
        fontweight="bold"
    )

    plt.xlabel("Hora")

    plt.ylabel("Número de Viagens")

    plt.grid(axis="y", alpha=0.3)

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            PASTA_GRAFICOS,
            "hour_bar.png"
        ),
        dpi=300
    )

    plt.show()


# ==========================================================
# HEATMAP SIMPLES
# ==========================================================

def grafico_heatmap(percentual):

    plt.figure(figsize=(13,3))

    plt.imshow(
        percentual.T,
        aspect="auto"
    )

    plt.colorbar(label="% das viagens")

    plt.yticks([0,1],["Casual","Member"])

    plt.xticks(range(24))

    plt.xlabel("Hora")

    plt.title(
        "Distribuição Percentual por Hora",
        fontsize=16,
        fontweight="bold"
    )

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            PASTA_GRAFICOS,
            "hour_heatmap.png"
        ),
        dpi=300
    )

    plt.show()


# ==========================================================
# HORÁRIOS DE PICO
# ==========================================================

def horario_pico(df):

    print("\n")
    print("="*70)
    print("HORÁRIOS DE MAIOR MOVIMENTO")
    print("="*70)

    member = (
        df[df["member_casual"]=="member"]
        ["hour"]
        .value_counts()
        .sort_index()
    )

    casual = (
        df[df["member_casual"]=="casual"]
        ["hour"]
        .value_counts()
        .sort_index()
    )

    print()

    print(f"Maior horário (Member): {member.idxmax()} h")
    print(f"Viagens: {member.max():,}".replace(",", "."))

    print()

    print(f"Maior horário (Casual): {casual.idxmax()} h")
    print(f"Viagens: {casual.max():,}".replace(",", "."))


# ==========================================================
# RESUMO
# ==========================================================

def resumo(df):

    print("\n")
    print("="*70)
    print("RESUMO")
    print("="*70)

    print("\nTotal de viagens por grupo:\n")

    print(df["member_casual"].value_counts())

    print("\nHorário mais movimentado:")

    print(df["hour"].value_counts().sort_index().idxmax(), "h")

    print("="*70)

# ==========================================================
# MAIN
# ==========================================================

def main():

    df = carregar_base()

    tabela, percentual = tabela_horas(df)

    grafico_linhas(tabela)

    grafico_barras(tabela)

    grafico_heatmap(percentual)

    horario_pico(df)

    resumo(df)


if __name__ == "__main__":

    main()