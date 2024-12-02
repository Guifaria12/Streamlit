import pandas as pd
import numpy as np
import plotly.graph_objects as go
import streamlit as st
import xgboost as xgb
from sklearn.metrics import mean_absolute_error, mean_squared_error

st.title("Comparação de Preços do Petróleo - Treinamento, Teste e Previsões")

# Importar dados
url_preco_petroleo = 'https://docs.google.com/spreadsheets/d/1WSL2mbFwfnQR5vDF73UmcOK5_zf5NGelasCCo8_qCOk/export?format=csv'
df_preco_petroleo = pd.read_csv(url_preco_petroleo)

# Limpar e formatar dados
df_preco_petroleo['Data (Descending)'] = pd.to_datetime(df_preco_petroleo['Data (Descending)'])
df_preco_petroleo['y'] = df_preco_petroleo['Preço - petróleo bruto - Brent (FOB)'].str.replace(',', '.').astype(float)

df_preco_petroleo["year"] = df_preco_petroleo["Data (Descending)"].dt.year
df_preco_petroleo["month"] = df_preco_petroleo["Data (Descending)"].dt.month
df_preco_petroleo["day"] = df_preco_petroleo["Data (Descending)"].dt.day
df_preco_petroleo["dayofweek"] = df_preco_petroleo["Data (Descending)"].dt.dayofweek

# Seleção de intervalo de anos
ano_inicial = st.selectbox('Selecione o ano inicial:',
                           options=sorted(df_preco_petroleo["year"].unique()),
                           index=0)
ano_final = st.selectbox('Selecione o ano final:',
                         options=sorted(df_preco_petroleo["year"].unique()),
                         index=len(df_preco_petroleo["year"].unique()) - 1)

# Filtrar dados pelo intervalo selecionado
df_filtrado = df_preco_petroleo[(df_preco_petroleo["year"] >= ano_inicial) &
                                (df_preco_petroleo["year"] <= ano_final)]

# Divisão entre treinamento e teste
split_index = int(len(df_filtrado) * 0.7)
train = df_filtrado[:split_index]
test = df_filtrado[split_index:]

FEATURES = ["year", "month", "day", "dayofweek"]
TARGET = "y"

X_train, y_train = train[FEATURES], train[TARGET]
X_test, y_test = test[FEATURES], test[TARGET]

# Treinamento do modelo
reg = xgb.XGBRegressor(objective="reg:squarederror")
reg.fit(X_train, y_train)

# Previsões e métricas
preds = reg.predict(X_test)

mae = mean_absolute_error(y_test, preds)
mse = mean_squared_error(y_test, preds)
mape = np.mean(np.abs((y_test - preds) / y_test)) * 100

st.write(f"**MAE**: {mae:.2f}, **MSE**: {mse:.2f}, **MAPE**: {mape:.2f}%")

# Adicionar previsões ao conjunto de teste
test = test.reset_index(drop=True)
test['Predictions'] = preds

# Intervalo de confiança
errors = y_test - preds
std_error = np.std(errors)
confidence_interval = 1.96 * std_error
test['Upper_Bound'] = test['Predictions'] + confidence_interval
test['Lower_Bound'] = test['Predictions'] - confidence_interval

# Gráfico interativo com Plotly
fig = go.Figure()

# Adicionar dados de treinamento
fig.add_trace(go.Scatter(x=train['Data (Descending)'],
                         y=train[TARGET],
                         mode='lines',
                         name='Treinamento',
                         line=dict(color='blue', width=2)))

# Adicionar dados de teste
fig.add_trace(go.Scatter(x=test['Data (Descending)'],
                         y=test[TARGET],
                         mode='lines',
                         name='Teste',
                         line=dict(color='green', width=2)))

# Adicionar previsões
fig.add_trace(go.Scatter(x=test['Data (Descending)'],
                         y=test['Predictions'],
                         mode='lines',
                         name='Previsões',
                         line=dict(color='red', dash='dot', width=2)))

# Adicionar margem de confiança
fig.add_trace(go.Scatter(x=test['Data (Descending)'],
                         y=test['Upper_Bound'],
                         mode='lines',
                         name='Margem Superior',
                         line=dict(color='red', width=1, dash='dot')))
fig.add_trace(go.Scatter(x=test['Data (Descending)'],
                         y=test['Lower_Bound'],
                         mode='lines',
                         name='Margem Inferior',
                         line=dict(color='red', width=1, dash='dot')))

# Configurações do gráfico
fig.update_layout(title="Valores Reais, Previsões e Margem de Confiança",
                  xaxis_title="Data",
                  yaxis_title="Preço do Petróleo",
                  legend_title="Legenda",
                  template="plotly_white")

st.plotly_chart(fig)
