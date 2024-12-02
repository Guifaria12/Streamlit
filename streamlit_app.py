import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objs as go
import statsmodels.api as sm
import xgboost as xgb
from sklearn.metrics import mean_absolute_error, mean_squared_error

st.title("Comparação de Preços do Petróleo - Modelos SARIMAX e XGBoost")

# Carregar dados
url = 'https://docs.google.com/spreadsheets/d/1WSL2mbFwfnQR5vDF73UmcOK5_zf5NGelasCCo8_qCOk/export?format=csv'
df_preco_petroleo = pd.read_csv(url)

# ----------- Preprocessamento de Dados -----------
df_preco_petroleo['Data (Descending)'] = pd.to_datetime(df_preco_petroleo['Data (Descending)'])
df_preco_petroleo['y'] = df_preco_petroleo['Preço - petróleo bruto - Brent (FOB)'].str.replace(',', '.').astype(float)

# Colunas adicionais para o modelo XGBoost
df_preco_petroleo["year"] = df_preco_petroleo["Data (Descending)"].dt.year
df_preco_petroleo["month"] = df_preco_petroleo["Data (Descending)"].dt.month
df_preco_petroleo["day"] = df_preco_petroleo["Data (Descending)"].dt.day
df_preco_petroleo["dayofweek"] = df_preco_petroleo["Data (Descending)"].dt.dayofweek

# ----------- Seletor de Anos -----------
years = sorted(df_preco_petroleo["year"].unique())
start_year = st.selectbox("Selecione o Ano Inicial:", options=years, index=0)
end_year = st.selectbox("Selecione o Ano Final:", options=years, index=len(years) - 1)

df_filtered = df_preco_petroleo[(df_preco_petroleo["year"] >= start_year) & (df_preco_petroleo["year"] <= end_year)]

# Divisão em treino e teste
split_index = int(len(df_filtered) * 0.7)
train = df_filtered[:split_index]
test = df_filtered[split_index:]

# ----------- Gráfico 1: SARIMAX -----------
train_sarimax = train.copy()
test_sarimax = test.copy()

model_sarimax = sm.tsa.statespace.SARIMAX(
    train_sarimax["y"], order=(1, 1, 1), seasonal_order=(1, 1, 1, 12)
)
results_sarimax = model_sarimax.fit()

forecast_sarimax = results_sarimax.get_forecast(steps=len(test_sarimax))
preds_sarimax = forecast_sarimax.predicted_mean
conf_int_sarimax = forecast_sarimax.conf_int()

preds_sarimax.index = test_sarimax["Data (Descending)"]
conf_int_sarimax.index = test_sarimax["Data (Descending)"]

fig_sarimax = go.Figure()
fig_sarimax.add_trace(go.Scatter(x=train_sarimax["Data (Descending)"], y=train_sarimax["y"], mode="lines", name="Treinamento", line=dict(color="blue")))
fig_sarimax.add_trace(go.Scatter(x=test_sarimax["Data (Descending)"], y=test_sarimax["y"], mode="lines", name="Teste", line=dict(color="green")))
fig_sarimax.add_trace(go.Scatter(x=preds_sarimax.index, y=preds_sarimax, mode="lines", name="Previsões", line=dict(color="red", dash="dash")))

# ----------- Gráfico 2: XGBoost -----------
FEATURES = ["year", "month", "day", "dayofweek"]
TARGET = "y"

X_train, y_train = train[FEATURES], train[TARGET]
X_test, y_test = test[FEATURES], test[TARGET]

reg = xgb.XGBRegressor(objective="reg:squarederror")
reg.fit(X_train, y_train)

preds_xgb = reg.predict(X_test)
errors_xgb = y_test - preds_xgb
std_error_xgb = np.std(errors_xgb)
confidence_interval_xgb = 1.96 * std_error_xgb

test["Predictions"] = preds_xgb
test["Upper_Bound"] = preds_xgb + confidence_interval_xgb
test["Lower_Bound"] = preds_xgb - confidence_interval_xgb

fig_xgb = go.Figure()
fig_xgb.add_trace(go.Scatter(x=train["Data (Descending)"], y=train["y"], mode="lines", name="Treinamento", line=dict(color="blue")))
fig_xgb.add_trace(go.Scatter(x=test["Data (Descending)"], y=test["y"], mode="lines", name="Teste", line=dict(color="green")))
fig_xgb.add_trace(go.Scatter(x=test["Data (Descending)"], y=test["Predictions"], mode="lines", name="Previsões", line=dict(color="red", dash="dot")))

# ----------- Layout com st.columns -----------
col1, col2 = st.columns(2)

with col1:
    st.subheader("Gráfico SARIMAX")
    st.plotly_chart(fig_sarimax, use_container_width=True)

with col2:
    st.subheader("Gráfico XGBoost")
    st.plotly_chart(fig_xgb, use_container_width=True)
