import pandas as pd
import streamlit as st
import plotly.graph_objs as go
import statsmodels.api as sm

# Carregar dados
url = 'https://docs.google.com/spreadsheets/d/1WSL2mbFwfnQR5vDF73UmcOK5_zf5NGelasCCo8_qCOk/export?format=csv'
df_preco_petroleo = pd.read_csv(url)

# Preprocessamento
df_preco_petroleo['Date'] = pd.to_datetime(df_preco_petroleo['Data (Descending)'])
df_preco_petroleo['y'] = df_preco_petroleo['Preço - petróleo bruto - Brent (FOB)'].str.replace(',', '.').astype(float)
df_preco_petroleo = df_preco_petroleo.sort_values(by='Date')

# Definir a data mais recente e o ponto de corte para 3 meses atrás
last_date = df_preco_petroleo['Date'].max()
three_months_ago = last_date - pd.DateOffset(months=3)

# Dividir em treino e teste
test = df_preco_petroleo[df_preco_petroleo['Date'] >= three_months_ago]
train = df_preco_petroleo[df_preco_petroleo['Date'] < three_months_ago]

# Renomear as colunas para o formato exigido pelo SARIMAX
train.rename(columns={'Date': 'ds', 'y': 'y'}, inplace=True)
test.rename(columns={'Date': 'ds', 'y': 'y'}, inplace=True)

# Criar o modelo SARIMAX
model = sm.tsa.statespace.SARIMAX(
    train["y"], order=(1, 1, 1), seasonal_order=(1, 1, 1, 12)
)
results = model.fit()

# Previsões
forecast = results.get_forecast(steps=len(test))
preds = forecast.predicted_mean
conf_int = forecast.conf_int()

# Ajustar o índice das previsões para corresponder às datas de teste
preds.index = test["ds"]
conf_int.index = test["ds"]

# Criar dropdowns para selecionar o intervalo de ano
years = df_preco_petroleo['Date'].dt.year.unique()
start_year = st.selectbox('Selecione o Ano Inicial:', years, index=0)
end_year = st.selectbox('Selecione o Ano Final:', years, index=len(years)-1)

# Filtrar os dados com base nos anos selecionados
df_filtered = df_preco_petroleo[
    (df_preco_petroleo['Date'].dt.year >= start_year) &
    (df_preco_petroleo['Date'].dt.year <= end_year)
]

# Dividir em treino e teste novamente após o filtro
test_filtered = df_filtered[df_filtered['Date'] >= three_months_ago]
train_filtered = df_filtered[df_filtered['Date'] < three_months_ago]

# Ajustar as colunas para o modelo
train_filtered.rename(columns={'Date': 'ds', 'y': 'y'}, inplace=True)
test_filtered.rename(columns={'Date': 'ds', 'y': 'y'}, inplace=True)

# Criar o modelo SARIMAX novamente com os dados filtrados
model_filtered = sm.tsa.statespace.SARIMAX(
    train_filtered["y"], order=(1, 1, 1), seasonal_order=(1, 1, 1, 12)
)
results_filtered = model_filtered.fit()

# Previsões
forecast_filtered = results_filtered.get_forecast(steps=len(test_filtered))
preds_filtered = forecast_filtered.predicted_mean
conf_int_filtered = forecast_filtered.conf_int()

# Ajustar o índice das previsões para corresponder às datas de teste
preds_filtered.index = test_filtered["ds"]
conf_int_filtered.index = test_filtered["ds"]

# Plotar os resultados com Plotly
fig = go.Figure()

# Adicionar linha de treinamento
fig.add_trace(go.Scatter(x=train_filtered['ds'], y=train_filtered['y'], mode='lines', name='Treinamento', line=dict(color='blue')))

# Adicionar linha de teste
fig.add_trace(go.Scatter(x=test_filtered['ds'], y=test_filtered['y'], mode='lines', name='Teste', line=dict(color='green')))

# Adicionar previsões
fig.add_trace(go.Scatter(x=preds_filtered.index, y=preds_filtered, mode='lines', name='Previsões', line=dict(color='red', dash='dash')))

# Adicionar intervalo de confiança
fig.add_trace(go.Scatter(
    x=conf_int_filtered.index,
    y=conf_int_filtered.iloc[:, 0],
    fill=None,
    mode='lines',
    line=dict(color='red', width=0),
    showlegend=False
))
fig.add_trace(go.Scatter(
    x=conf_int_filtered.index,
    y=conf_int_filtered.iloc[:, 1],
    fill='tonexty',
    mode='lines',
    line=dict(color='red', width=0),
    name='Margem de Confiança',
    fillcolor='rgba(255, 0, 0, 0.2)'
))

# Adicionar título e rótulos
fig.update_layout(
    title="Previsões de Preço do Petróleo (Modelo SARIMAX)",
    xaxis_title="Data",
    yaxis_title="Preço do Petróleo",
    template="plotly_dark"
)

# Mostrar o gráfico
st.plotly_chart(fig)
