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

st.write(
    "O preço do petróleo desempenha um papel fundamental na economia global, "
    "influenciando mercados financeiros, políticas energéticas e estratégias corporativas em diversos setores. "
    "Por ser um dos principais indicadores econômicos, compreender sua dinâmica de variação ao longo do tempo é "
    "essencial para a tomada de decisões estratégicas em um ambiente econômico volátil e interconectado."
)

st.header("**Análise Exploratória dos Dados**")
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

# Dropdowns para selecionar os anos
ano_inicial = st.selectbox("Selecione o ano inicial:", range(1987, df_matriz_energica['Ano'].dt.year.max() + 1))
ano_final = st.selectbox("Selecione o ano final:", range(ano_inicial, 2024 + 1))

# Filtrar os dados com base nos anos selecionados
df_matriz_energica_filtrado = df_matriz_energica.loc[(df_matriz_energica['Ano'].dt.year >= ano_inicial) & (df_matriz_energica['Ano'].dt.year <= ano_final)]
df_preco_petroleo_filtrado = df_preco_petroleo.loc[(df_preco_petroleo['Data (Descending)'].dt.year >= ano_inicial) & (df_preco_petroleo['Data (Descending)'].dt.year <= ano_final)]

# Criar mensagens personalizadas para hover
hover_message_preco = [
    "Alta histórica" if 2008 <= data.year <= 2010 else
    "Queda significativa" if 2014 <= data.year <= 2016 else
    "Estável" for data in df_preco_petroleo_filtrado["Data (Descending)"]
]

hover_message_uso = [
    "Aumento do consumo" if ano.year <= 2005 else
    "Redução do consumo" if ano.year > 2005 else
    "Neutro" for ano in df_matriz_energica_filtrado['Ano']
]

# Criar o gráfico interativo com Plotly
fig = go.Figure()

# Plot do preço do petróleo com mensagens personalizadas
fig.add_trace(go.Scatter(
    x=df_preco_petroleo_filtrado["Data (Descending)"],
    y=df_preco_petroleo_filtrado["Preço - petróleo bruto - Brent (FOB)"],
    mode='lines',
    name="Preço",
    line=dict(color="black"),
    customdata=hover_message_preco,
    hovertemplate='<b>Preço do Petróleo</b><br>Ano: %{x}<br>Preço: %{y:.2f}<br>Mensagem: %{customdata}<extra></extra>'
))

# Plot do uso de petróleo com mensagens personalizadas
fig.add_trace(go.Scatter(
    x=df_matriz_energica_filtrado['Ano'],
    y=df_matriz_energica_filtrado['Petróleo'],
    mode='lines',
    name="Uso de Petróleo (%)",
    line=dict(color="blue", dash='dash'),
    customdata=hover_message_uso,
    hovertemplate='<b>Uso de Petróleo (%)</b><br>Ano: %{x}<br>Uso: %{y}%<br>Mensagem: %{customdata}<extra></extra>'
))

# Personalizar o gráfico
fig.update_layout(
    title="Comparação preço x uso",
    xaxis_title="Ano",
    yaxis_title="Valores",
    legend_title="Legenda",
    template="plotly_white"
)

# Exibir o gráfico interativo no Streamlit
st.plotly_chart(fig)

st.header("**Eventos que impactaram os preços:**")

st.write("
" * 1990-1991: Guerra do Golfo: Conflito no Oriente Médio elevou brevemente os preços, mas a recessão global limitou o impacto."
" * 2001: Ataques de 11 de Setembro: Aumento temporário nos preços e foco na segurança energética dos EUA."
" * 2003: Invasão do Iraque: Instabilidade geopolítica impulsionou preços durante crescimento global acelerado."
         ")
