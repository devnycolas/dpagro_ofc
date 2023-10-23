import pandas as pd

def puxar_df():
    # Leitura da tabela Excel "ListaCompleta.xlsx"
    df_lista_completa = pd.read_excel("ListaCompleta.xlsx", engine="openpyxl")

    # Leitura da tabela Excel "PaisesCompare.xlsx"
    df_paises_compare = pd.read_excel("PaisesCompare.xlsx", engine="openpyxl")

    # Filtro para manter apenas os registros do ano de 2022 com base na coluna "data_documento"
    df_lista_completa = df_lista_completa[df_lista_completa['data_documento'].dt.year == 2022]

    # Fazer a correspondência entre as tabelas com base na coluna "paises_ois" e "País/OI"
    df_resultante = df_lista_completa.merge(df_paises_compare, left_on="paises_ois", right_on="País/OI", how="left")

    # Preencher a coluna "regiao_secretaria" com base na correspondência da coluna "Continente"
    df_resultante["regiao_secretaria"] = df_resultante["Continente"]

    # Preencher os valores em branco na coluna "regiao_secretaria" com "Vários Países"
    df_resultante["regiao_secretaria"].fillna("Vários Países", inplace=True)

    # Remover colunas temporárias usadas para a correspondência
    df_resultante.drop(columns=["País/OI", "Continente"], inplace=True)

    return df_resultante
