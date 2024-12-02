import pandas as pd
from prophet import Prophet
import plotly.graph_objects as go
import streamlit as st

# Carregar dados
url = 'https://docs.google.com/spreadsheets/d/1WSL2mbFwfnQR5vDF73UmcOK5_zf5NGelasCCo8_qCOk/export?format=csv'
df_preco_petroleo = pd.read_csv(url)

# Preprocessamento
df_preco_petroleo['Date'] = pd.to_datetime(df_preco_petroleo['Data (Descending)'])
df_preco_petroleo['y'] = df_preco_petroleo['Preço - petróleo bruto - Brent (FOB)'].str.replace(',', '.').astype(float)
df_preco_petroleo = df_preco_petroleo.sort_values(by='Date')

# Dropdowns para selecionar os anos
ano_inicial = st.selectbox("Selecione o ano inicial:", range(df_preco_petroleo['Date'].dt.year.min(), df_preco_petroleo['Date'].dt.year.max() + 1))
ano_final = st.selectbox("Selecione o ano final:", range(ano_inicial, df_preco_petroleo['Date'].dt.year.max() + 1))

# Filtrar os dados com base nos anos selecionados
df_preco_petroleo_filtrado = df_preco_petroleo.loc[(df_preco_petroleo['Date'].dt.year >= ano_inicial) & (df_preco_petroleo['Date'].dt.year <= ano_final)]

# Dividir em treino e teste
last_date = df_preco_petroleo_filtrado['Date'].max()
three_months_ago = last_date - pd.DateOffset(months=3)

test_prophet = df_preco_petroleo_filtrado[df_preco_petroleo_filtrado['Date'] >= three_months_ago]
train_prophet = df_preco_petroleo_filtrado[df_preco_petroleo_filtrado['Date'] < three_months_ago]

# Ajustar colunas para o Prophet
train_prophet = train_prophet[['Date', 'y']].rename(columns={'Date': 'ds', 'y': 'y'})
test_prophet = test_prophet[['Date', 'y']].rename(columns={'Date': 'ds', 'y': 'y'})

# Treinamento do modelo
model = Prophet(daily_seasonality=True)
model.fit(train_prophet)

# Criar previsões
future = model.make_future_dataframe(periods=len(test_prophet))
forecast = model.predict(future)

# Filtrar previsões para o período de teste
forecast_filtered = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(len(test_prophet))
forecast_filtered = forecast_filtered.set_index("ds")

# Ajustar y_test
y_test = test_prophet.set_index("ds")["y"]

# Título do gráfico
st.write(f"### Comparação entre Valores Reais, Previsões e Margem de Confiança a partir de 2021 (Modelo Prophet)")

# Criar o gráfico interativo com Plotly
fig = go.Figure()

# Plot do treino
fig.add_trace(go.Scatter(
    x=train_prophet['ds'],
    y=train_prophet['y'],
    mode='lines',
    name='Treinamento',
    line=dict(color='blue'),
    hovertemplate='<b>Treinamento</b><br>Data: %{x}<br>Preço: %{y:.2f}<extra></extra>'
))

# Plot do teste
fig.add_trace(go.Scatter(
    x=test_prophet['ds'],
    y=test_prophet['y'],
    mode='lines',
    name='Teste',
    line=dict(color='green'),
    hovertemplate='<b>Teste</b><br>Data: %{x}<br>Preço: %{y:.2f}<extra></extra>'
))

# Plot das previsões
fig.add_trace(go.Scatter(
    x=forecast_filtered.index,
    y=forecast_filtered['yhat'],
    mode='lines',
    name='Previsões',
    line=dict(color='red', dash='dash'),
    hovertemplate='<b>Previsões</b><br>Data: %{x}<br>Preço previsto: %{y:.2f}<extra></extra>'
))

# Intervalo de confiança
fig.add_trace(go.Scatter(
    x=forecast_filtered.index,
    y=forecast_filtered['yhat_upper'],
    fill=None,
    mode='lines',
    line=dict(color='red', width=0),
    showlegend=False,
    hovertemplate='Margem de Confiança Superior: %{y:.2f}<extra></extra>'
))

fig.add_trace(go.Scatter(
    x=forecast_filtered.index,
    y=forecast_filtered['yhat_lower'],
    fill='tonexty',
    mode='lines',
    line=dict(color='red', width=0),
    showlegend=False,
    hovertemplate='Margem de Confiança Inferior: %{y:.2f}<extra></extra>'
))

# Personalizar layout
fig.update_layout(
    title="Comparação entre Valores Reais, Previsões e Margem de Confiança",
    xaxis_title="Data",
    yaxis_title="Valor",
    template="plotly_white",
    hovermode="closest"  # Habilitar hovermode para mostrar os valores
)

# Exibir o gráfico interativo no Streamlit
st.plotly_chart(fig)
