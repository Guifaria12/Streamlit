import pandas as pd
import plotly.graph_objects as go
import streamlit as st



# Carregar os dados de preço do petróleo
url_preco_petroleo = 'https://docs.google.com/spreadsheets/d/1WSL2mbFwfnQR5vDF73UmcOK5_zf5NGelasCCo8_qCOk/export?format=csv'
df_preco_petroleo = pd.read_csv(url_preco_petroleo)

# Converter a coluna 'Data (Descending)' para o formato de data
df_preco_petroleo['Data (Descending)'] = pd.to_datetime(df_preco_petroleo['Data (Descending)'])

# Ajustar a coluna 'Preço - petróleo bruto - Brent (FOB)' para valores numéricos
df_preco_petroleo['Preço - petróleo bruto - Brent (FOB)'] = df_preco_petroleo['Preço - petróleo bruto - Brent (FOB)'].str.replace(',', '.').astype(float)

# Carregar os dados da matriz energética
url_matriz_energica = 'https://docs.google.com/spreadsheets/d/1SjoisxQ5WqMsWFCIJ9NgzaQZuNmJ0UPxkG2cBXkW5PM/export?format=csv'
df_matriz_energica = pd.read_csv(url_matriz_energica)

# Processar e limpar os dados da matriz energética
df_matriz_energica = df_matriz_energica[['Ano', 'Petróleo']]
df_matriz_energica['Ano'] = pd.to_datetime(df_matriz_energica['Ano'], format='%Y')
df_matriz_energica['Petróleo'] = df_matriz_energica['Petróleo'].str.replace('%', '').astype(int)

# Filtrar dados após o ano de 1987
df_matriz_energica = df_matriz_energica.loc[df_matriz_energica['Ano'] >= '1987']

st.header("**Introdução**")

st.writer("O preço do petróleo desempenha um papel fundamental na economia global, influenciando mercados financeiros, políticas energéticas e estratégias corporativas em diversos setores. Por ser um dos principais indicadores econômicos, compreender sua dinâmica de variação ao longo do tempo é essencial para a tomada de decisões estratégicas em um ambiente econômico volátil e interconectado.
Este projeto foi desenvolvido como parte de uma consultoria especializada, com o objetivo de atender à demanda de um cliente do segmento energético. A proposta consiste na criação de um dashboard interativo que permita visualizar, explorar e gerar insights sobre o comportamento histórico do preço do petróleo Brent. Além disso, foi solicitado o desenvolvimento de um modelo de Machine Learning para previsão de preços diários, fornecendo uma ferramenta preditiva para auxiliar em decisões informadas e antecipação de tendências. ")
