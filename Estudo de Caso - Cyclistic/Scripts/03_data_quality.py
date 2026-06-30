# ==========================================================
# ESTUDO DE CASO - CYCLISTIC
# ETAPA 3 - PROCESSAR (PROCESS)
#
# Script: 02_data_quality.py
#
# Objetivo:
# Realizar uma auditoria da qualidade dos dados antes da limpeza.
#
# Autor: Lucca Nascimento
# ==========================================================

import os
import pandas as pd

# ==========================================================
# CONFIGURAÇÕES
# ==========================================================

PASTA_DADOS = r"C:\Users\Lucca\Downloads\Estudo de Caso - Cyclistic\Dados_manipulados"

# ==========================================================
# CARREGAMENTO DOS DADOS
# ==========================================================

def carregar_dados(pasta):

    arquivos = sorted(
        [f for f in os.listdir(pasta) if f.endswith(".csv")]
    )

    lista_df = []

    for arquivo in arquivos:

        caminho = os.path.join(pasta, arquivo)

        df = pd.read_csv(caminho)

        df["arquivo_origem"] = arquivo

        lista_df.append(df)

    dados = pd.concat(lista_df, ignore_index=True)

    return dados, arquivos


# ==========================================================
# ESTRUTURA DA BASE
# ==========================================================

def verificar_estrutura(df):

    print("\n")
    print("="*70)
    print("ESTRUTURA DA BASE")
    print("="*70)

    print(f"Linhas : {df.shape[0]:,}".replace(",", "."))
    print(f"Colunas: {df.shape[1]}")

    print("\nTipos das variáveis:\n")
    print(df.dtypes)


# ==========================================================
# VALORES AUSENTES
# ==========================================================

def verificar_nulos(df):

    print("\n")
    print("="*70)
    print("VALORES AUSENTES")
    print("="*70)

    nulos = pd.DataFrame({

        "Valores Ausentes": df.isnull().sum(),

        "%": round(
            df.isnull().mean()*100,
            2
        )

    })

    print(nulos)

    return nulos


# ==========================================================
# DUPLICATAS
# ==========================================================

def verificar_duplicatas(df):

    duplicatas = df.duplicated().sum()

    print("\n")
    print("="*70)
    print("DUPLICATAS")
    print("="*70)

    print(f"Duplicatas encontradas: {duplicatas:,}".replace(",", "."))

    return duplicatas


# ==========================================================
# IDs REPETIDOS
# ==========================================================

def verificar_ids(df):

    ids_repetidos = df["ride_id"].duplicated().sum()

    print("\n")
    print("="*70)
    print("RIDE_ID")
    print("="*70)

    print(f"IDs repetidos: {ids_repetidos:,}".replace(",", "."))

    return ids_repetidos

# ==========================================================
# VERIFICAÇÃO DAS DATAS E DURAÇÃO DAS VIAGENS
# ==========================================================

def verificar_datas(df):

    print("\n")
    print("="*70)
    print("VERIFICAÇÃO DAS DATAS")
    print("="*70)

    # Conversão para datetime
    df["started_at"] = pd.to_datetime(
        df["started_at"],
        errors="coerce"
    )

    df["ended_at"] = pd.to_datetime(
        df["ended_at"],
        errors="coerce"
    )

    datas_inicio_invalidas = df["started_at"].isna().sum()
    datas_fim_invalidas = df["ended_at"].isna().sum()

    print(f"Datas inválidas (started_at): {datas_inicio_invalidas}")
    print(f"Datas inválidas (ended_at)  : {datas_fim_invalidas}")

    # Duração da viagem
    df["ride_length"] = (
        df["ended_at"] - df["started_at"]
    ).dt.total_seconds() / 60

    viagens_invalidas = (df["ride_length"] <= 0).sum()

    print(f"\nViagens com duração <= 0 minutos: {viagens_invalidas:,}".replace(",", "."))

    return df, viagens_invalidas

# ==========================================================
# INVESTIGAÇÃO DOS RIDE_ID DUPLICADOS
# ==========================================================

def investigar_ids_duplicados(df):

    print("\n")
    print("="*70)
    print("INVESTIGAÇÃO DOS RIDE_ID DUPLICADOS")
    print("="*70)

    duplicados = df[
        df["ride_id"].duplicated(keep=False)
    ].sort_values("ride_id")

    print(f"Total de registros encontrados: {len(duplicados)}")

    if len(duplicados) > 0:

        nome_arquivo = "ride_ids_duplicados.csv"

        duplicados.to_csv(
            nome_arquivo,
            index=False,
            encoding="utf-8-sig"
        )

        print(f"\nArquivo '{nome_arquivo}' salvo com sucesso.")

    return duplicados

# ==========================================================
# CATEGORIAS
# ==========================================================

def verificar_categorias(df):

    print("\n")
    print("="*70)
    print("TIPOS DE BICICLETA")
    print("="*70)

    print(df["rideable_type"].value_counts())

    print("\n")
    print("="*70)
    print("TIPOS DE USUÁRIO")
    print("="*70)

    print(df["member_casual"].value_counts())


# ==========================================================
# COORDENADAS
# ==========================================================

def verificar_coordenadas(df):

    print("\n")
    print("="*70)
    print("COORDENADAS INVÁLIDAS")
    print("="*70)

    lat_inicio = (
        (df["start_lat"] < -90) |
        (df["start_lat"] > 90)
    ).sum()

    lon_inicio = (
        (df["start_lng"] < -180) |
        (df["start_lng"] > 180)
    ).sum()

    lat_final = (
        (df["end_lat"] < -90) |
        (df["end_lat"] > 90)
    ).sum()

    lon_final = (
        (df["end_lng"] < -180) |
        (df["end_lng"] > 180)
    ).sum()

    print(f"Latitude inicial inválida : {lat_inicio}")
    print(f"Longitude inicial inválida: {lon_inicio}")
    print(f"Latitude final inválida   : {lat_final}")
    print(f"Longitude final inválida  : {lon_final}")


# ==========================================================
# ESTATÍSTICAS
# ==========================================================

def estatisticas(df):

    print("\n")
    print("="*70)
    print("ESTATÍSTICAS DAS COORDENADAS")
    print("="*70)

    print(
        df[
            [
                "start_lat",
                "start_lng",
                "end_lat",
                "end_lng"
            ]
        ].describe()
    )


# ==========================================================
# RESUMO FINAL
# ==========================================================

def resumo(df, arquivos, duplicatas, ids_repetidos):

    print("\n")
    print("="*70)
    print("RESUMO DA AUDITORIA")
    print("="*70)

    print(f"Arquivos analisados : {len(arquivos)}")

    print(f"Total de viagens    : {len(df):,}".replace(",", "."))

    print(f"Total de colunas    : {df.shape[1]}")

    print(f"Duplicatas          : {duplicatas}")

    print(f"IDs repetidos       : {ids_repetidos}")
    
    print(f"Viagens <= 0 min    : {(df['ride_length'] <= 0).sum():,}".replace(",", "."))

    print(f"Tipos de bicicleta  : {df['rideable_type'].nunique()}")

    print(f"Categorias usuário  : {df['member_casual'].nunique()}")

    print(
        f"Valores ausentes    : {df.isnull().sum().sum():,}".replace(",", ".")
    )

    print("="*70)


# ==========================================================
# PROGRAMA PRINCIPAL
# ==========================================================

def main():

    df, arquivos = carregar_dados(PASTA_DADOS)

    verificar_estrutura(df)

    verificar_nulos(df)

    duplicatas = verificar_duplicatas(df)

    ids = verificar_ids(df)

    verificar_categorias(df)

    verificar_coordenadas(df)

    estatisticas(df)

    # NOVAS AUDITORIAS
    df, viagens_invalidas = verificar_datas(df)

    investigar_ids_duplicados(df)

    resumo(df, arquivos, duplicatas, ids)

if __name__ == "__main__":

    main()