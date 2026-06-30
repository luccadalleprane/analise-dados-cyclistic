# ==========================================================
# ESTUDO DE CASO - CYCLISTIC
# ETAPA 3 - PROCESSAR (PROCESS)
#
# Script: 03_process.py
#
# Objetivo:
# Limpar e transformar os dados para gerar uma base analítica.
#
# Autor: Lucca Nascimento
# ==========================================================

import os
import pandas as pd

# ==========================================================
# CONFIGURAÇÕES
# ==========================================================

PASTA_DADOS = r"C:\Users\Lucca\Downloads\Estudo de Caso - Cyclistic\Dados_manipulados"

ARQUIVO_SAIDA = "cyclistic_clean.csv"

# ==========================================================
# CARREGAMENTO DOS DADOS
# ==========================================================

def carregar_dados(pasta):

    print("=" * 70)
    print("CARREGANDO ARQUIVOS...")
    print("=" * 70)

    arquivos = sorted(
        [f for f in os.listdir(pasta) if f.endswith(".csv")]
    )

    lista_df = []

    for arquivo in arquivos:

        print(f"Lendo {arquivo}")

        caminho = os.path.join(pasta, arquivo)

        df = pd.read_csv(caminho)

        df["arquivo_origem"] = arquivo

        lista_df.append(df)

    dados = pd.concat(lista_df, ignore_index=True)

    print("\nTodos os arquivos carregados.")

    return dados

# ==========================================================
# CONVERSÃO DAS DATAS
# ==========================================================

def converter_datas(df):

    print("\nConvertendo datas...")

    df["started_at"] = pd.to_datetime(
        df["started_at"]
    )

    df["ended_at"] = pd.to_datetime(
        df["ended_at"]
    )

    return df

# ==========================================================
# REMOÇÃO DE RIDE_ID DUPLICADOS
# ==========================================================

def remover_ids_duplicados(df):

    print("\nRemovendo Ride_ID duplicados...")

    antes = len(df)

    df = df.drop_duplicates(
        subset="ride_id"
    )

    removidos = antes - len(df)

    print(f"{removidos} registros removidos.")

    return df

# ==========================================================
# DURAÇÃO DAS VIAGENS
# ==========================================================

def calcular_duracao(df):

    print("\nCalculando duração das viagens...")

    df["ride_length"] = (
        df["ended_at"] -
        df["started_at"]
    )

    df["ride_length_min"] = (
        df["ride_length"]
        .dt.total_seconds()
        / 60
    )

    return df

# ==========================================================
# REMOVER VIAGENS INVÁLIDAS
# ==========================================================

def remover_viagens_invalidas(df):

    print("\nRemovendo viagens com duração <= 0 minutos...")

    antes = len(df)

    df = df[
        df["ride_length_min"] > 0
    ]

    removidos = antes - len(df)

    print(f"{removidos} registros removidos.")

    return df

# ==========================================================
# ENGENHARIA DE ATRIBUTOS
# ==========================================================

def criar_variaveis_temporais(df):

    print("\nCriando variáveis temporais...")

    df["date"] = df["started_at"].dt.date

    df["year"] = df["started_at"].dt.year

    df["month"] = df["started_at"].dt.month

    df["month_name"] = df["started_at"].dt.month_name()
    
    df["quarter"] = df["started_at"].dt.quarter

    # Estação do ano
    estacoes = {
    12: "Winter", 1: "Winter", 2: "Winter",
    3: "Spring", 4: "Spring", 5: "Spring",
    6: "Summer", 7: "Summer", 8: "Summer",
    9: "Autumn", 10: "Autumn", 11: "Autumn"
    }

    df["season"] = df["month"].map(estacoes)

    df["day"] = df["started_at"].dt.day

    df["day_of_week"] = df["started_at"].dt.dayofweek

    df["day_name"] = df["started_at"].dt.day_name()

    df["hour"] = df["started_at"].dt.hour

    df["is_weekend"] = df["day_of_week"] >= 5

    return df

# ==========================================================
# ORGANIZAÇÃO DAS COLUNAS
# ==========================================================

def organizar_colunas(df):

    print("\nOrganizando colunas...")

    ordem = [

        "ride_id",

        "member_casual",

        "rideable_type",

        "started_at",

        "ended_at",

        "ride_length",

        "ride_length_min",

        "date",

        "year",

        "month",

        "month_name",
        
        "quarter",

        "season",

        "day",

        "day_of_week",

        "day_name",
        
        "is_weekend",

        "hour",

        "start_station_name",

        "start_station_id",

        "end_station_name",

        "end_station_id",

        "start_lat",

        "start_lng",

        "end_lat",

        "end_lng",

        "arquivo_origem"

    ]

    df = df[ordem]

    return df

# ==========================================================
# SALVAR BASE LIMPA
# ==========================================================

def salvar_base(df):

    print("\nSalvando base limpa...")

    df.to_csv(

        ARQUIVO_SAIDA,

        index=False,

        encoding="utf-8-sig"

    )

    print(f"Arquivo salvo: {ARQUIVO_SAIDA}")
    
# ==========================================================
# RESUMO
# ==========================================================

def resumo_final(df):

    print("\n")
    print("=" * 70)
    print("PROCESSAMENTO FINALIZADO")
    print("=" * 70)

    print(f"Registros finais : {len(df):,}".replace(",", "."))

    print(f"Colunas finais   : {df.shape[1]}")

    print(f"Tipos bicicleta  : {df['rideable_type'].nunique()}")

    print(f"Categorias       : {df['member_casual'].nunique()}")

    print("\nBase pronta para análise.")

    print("=" * 70)
    
# ==========================================================
# PROGRAMA PRINCIPAL
# ==========================================================

def main():

    df = carregar_dados(PASTA_DADOS)

    print(f"\nTotal inicial de registros: {len(df):,}".replace(",", "."))

    df = converter_datas(df)

    df = remover_ids_duplicados(df)

    df = calcular_duracao(df)

    df = remover_viagens_invalidas(df)

    df = criar_variaveis_temporais(df)

    df = organizar_colunas(df)

    salvar_base(df)

    resumo_final(df)


if __name__ == "__main__":

    main()
    
