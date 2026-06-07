from sqlalchemy import create_engine, types
import pandas as pd

# Lê o CSV
df = pd.read_csv("export_series_dolar.csv")

# Renomeia as colunas
df.columns = ["data_cotacao", "cotacao_dolar"]

# Converte a coluna de Data para datetime
df["data_cotacao"] = pd.to_datetime(df["data_cotacao"], dayfirst=True)

# Converte cotacao_dolar para número (tira vírgula e transforma em float)
df["cotacao_dolar"] = (
    df["cotacao_dolar"]
    .astype(str)              # garante string
    .str.replace(",", ".")    # troca vírgula por ponto
    .astype(float)            # converte para float
)

print(df.dtypes)  # conferindo os tipos

# Conexão com o Postgres
engine = create_engine("postgresql+psycopg2://postgres:postgres@localhost:5432/finance_db")

# Exporta para a tabela, forçando o tipo DATE
df.to_sql(
    "serie_historica_dolar",
    engine,
    if_exists="replace",
    index=False,
    dtype={"data_cotacao": types.Date()}
)

print("Dados inseridos com sucesso no Postgres!")
