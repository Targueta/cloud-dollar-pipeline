import requests
import json
import csv
import psycopg2
from datetime import datetime


def main():
    print("Rodando script...")

    # data e hora em que o script foi executado
    data_execucao_script = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # conexão com o banco PostgreSQL
    conexao = psycopg2.connect(
        host="18.118.220.90",
        database="finance_db",
        user="postgres",
        password="postgres"
    )
    cursor = conexao.cursor()

    print("Conexão com o PostgreSQL funcionou.")

    # endereço da API com a cotação do dólar
    url = "https://economia.awesomeapi.com.br/json/last/USD-BRL"

    resposta = requests.get(url)
    status_code = resposta.status_code
    print(resposta.status_code)

    if status_code !=200:
        print("API retornou erro. Tente novamente mais tarde")
        return

    dados = resposta.json()

    # principais dados do dólar
    cotacao_dolar = float(dados["USDBRL"]["bid"])
    maior_valor_dolar = float(dados["USDBRL"]["high"])
    menor_valor_dolar = float(dados["USDBRL"]["low"])
    variacao_dolar = float(dados["USDBRL"]["pctChange"])
    nome_moeda_dolar = dados["USDBRL"]["name"]
    data_cotacao_dolar = dados["USDBRL"]["create_date"]

    # interpreta a variação do dólar
    if variacao_dolar > 0:
        mensagem_variacao_dolar = "O dólar subiu hoje."
    elif variacao_dolar < 0:
        mensagem_variacao_dolar = "O dólar caiu hoje."
    else:
        mensagem_variacao_dolar = "O dólar não mudou hoje."

    # registro que será salvo no histórico
    registro = {
        "data_execucao_script": data_execucao_script,
        "data_cotacao_api": data_cotacao_dolar,
        "cotacao_dolar": round(cotacao_dolar, 4),
        "maior_valor_dolar": round(maior_valor_dolar, 4),
        "menor_valor_dolar": round(menor_valor_dolar, 4),
        "variacao_dolar": round(variacao_dolar, 3),
        "nome_moeda_dolar": nome_moeda_dolar
    }

    # salva a cotação no PostgreSQL
    cursor.execute(
        """
        INSERT INTO cotacoes_dolar_v3 (
            data_execucao_script,
            data_cotacao_api,
            cotacao_dolar,
            maior_valor_dolar,
            menor_valor_dolar,
            variacao_dolar,
            nome_moeda_dolar
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,
        (
            data_execucao_script,
            data_cotacao_dolar,
            cotacao_dolar,
            maior_valor_dolar,
            menor_valor_dolar,
            variacao_dolar,
            nome_moeda_dolar
        )
    )   
            
    conexao.commit()
    print("Cotação salva no PostgreSQL!")

    # lê o histórico antigo ou começa uma lista vazia
    try:
        with open("historico_cotacao_dolar.json", "r", encoding="utf-8") as arquivo:
            historico = json.load(arquivo)
    except:
        historico = []

    # adiciona o novo registro ao histórico
    historico.append(registro)

    # salva o histórico em JSON
    with open("historico_cotacao_dolar.json", "w", encoding="utf-8") as arquivo:
        json.dump(historico, arquivo, ensure_ascii=False, indent=4)

    # salva o histórico em CSV
    with open("historico_cotacao_dolar.csv", "w", newline="", encoding="utf-8") as arquivo_csv:
        campos = [
            "data_execucao_script",
            "data_cotacao_api",
            "cotacao_dolar",
            "maior_valor_dolar",
            "menor_valor_dolar",
            "variacao_dolar",
            "nome_moeda_dolar"
        ]

        escritor = csv.DictWriter(arquivo_csv, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(historico)

    print(f"Quantidade de registros no histórico: {len(historico)}")
    print("----- COTAÇÃO DO DÓLAR -----")
    print(f"Cotação do dólar: R$ {cotacao_dolar:.2f}")
    print(f"Maior valor do dia: R$ {maior_valor_dolar:.2f}")
    print(f"Menor valor do dia: R$ {menor_valor_dolar:.2f}")
    print(f"Variação do dia: {variacao_dolar:.3f}%")
    print(f"Nome da moeda: {nome_moeda_dolar}")
    print(f"Data da cotação da API: {data_cotacao_dolar}")
    print(f"Data da execução do script: {data_execucao_script}")
    print(mensagem_variacao_dolar)

    cursor.close()
    conexao.close()


if __name__ == "__main__":
    main()
