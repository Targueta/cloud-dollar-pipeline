# cloud-dollar-pipeline

Pipeline automatizado de coleta, persistência e visualização da cotação USD/BRL.

## Visão geral

Coleta diária da cotação do dólar via API, persistência em PostgreSQL na AWS EC2 e dashboard público no Grafana com série histórica de 30 anos (1996–2026).

## Arquitetura

cron (Mac) → Python → PostgreSQL (AWS EC2) → Grafana (público)

## Stack

- Python · requests · psycopg2 · pandas · sqlalchemy
- PostgreSQL · AWS EC2 · Elastic IP
- Grafana · cron · SSH · SCP

## Dashboard público

[Acessar dashboard ao vivo](http://18.118.220.90:3000/public-dashboards/02cd7dfa1db84edc81d60c55bb71f8f0)

Painéis disponíveis:
- Cotação do dia (USD/BRL)
- Variação mensal 2025–2026
- Série histórica 1996–2026 (30 anos)

## Decisões técnicas

- Foco em USD/BRL para simplificar e aprofundar uma série histórica real
- Duas timestamps por registro: data da API e data de execução do script
- Grafana substituiu Metabase por restrição real de RAM na EC2
- Elastic IP para estabilizar o endereço público do dashboard
- Tratamento de erro 429 (quota da API) para evitar crash do pipeline

## Status atual

| Componente | Status |
|---|---|
| EC2 + PostgreSQL | ✅ no ar |
| Grafana público | ✅ no ar |
| Pipeline de ingestão | ⚠️ em manutenção — último dado: 2026-02-28 |

## Próximos passos

- Reativar e migrar o cron para a EC2
- Adicionar usuário read-only no PostgreSQL para o Grafana
- Revisar exposição de portas e segurança básica
