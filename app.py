# Importação das bibliotecas
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
from datetime import timedelta

metrics = {
    'Métrica': ['MAE', 'MSE', 'RMSE', 'R2'],
    'Valor': [2.27, 9.37, 3.06, -0.10]
}

# Criar um DataFrame
df_metrics = pd.DataFrame(metrics)

# Carregar os dados de preço do petróleo
url_preco_petroleo = 'https://docs.google.com/spreadsheets/d/1WSL2mbFwfnQR5vDF73UmcOK5_zf5NGelasCCo8_qCOk/export?format=csv'

df_preco_petroleo = pd.read_csv(url_preco_petroleo)
df_preco_petroleo = df_preco_petroleo.rename(columns={'Data (Descending)': 'Date', 'Preço - petróleo bruto - Brent (FOB)': 'price'})
df_preco_petroleo['Date'] = pd.to_datetime(df_preco_petroleo['Date'])
df_preco_petroleo['price'] = df_preco_petroleo['price'].str.replace(',', '.', regex=False)
df_preco_petroleo['price'] = pd.to_numeric(df_preco_petroleo['price'])

# Carregar o modelo salvo com joblib
model_filename = "Modelo/best_xgboost_model.joblib"
reg_best = joblib.load(model_filename)

FEATURES = ['day_of_week', 'month', 'day_of_month', 'rolling_mean', 'time_index']
TARGET = 'price'  # Ajuste para o nome da variável que está sendo prevista

# Título e introdução
st.markdown('<style>div[role="listbox"] ul{background-color: #6e42ad}; </style>', unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; '> Previsão de Preço de Petróleo (Machine Learning)</h1>", unsafe_allow_html=True)
st.warning('Indique quantos Meses pretende prever e depois clique no botão **PREVER** no final da página.')

# Obter a quantidade de dias para prever
input_days = int(st.slider('Selecione a quantidade de MESES para previsão', 1, 12))

# Exibir os dias selecionados
st.write(f"Você selecionou prever para {input_days} meses.")

# Botão para gerar as previsões
if st.button('Prever'):
    # Gerar previsões
    input_days = input_days * 30
    future_dates = pd.date_range(start=df_preco_petroleo['Date'].max() + timedelta(days=1), periods=input_days, freq='D')
    
    # Gerar características para os dados futuros com as colunas esperadas pelo modelo
    future_features = pd.DataFrame(index=future_dates)
    future_features['Date'] = future_features.index

    # Adicionar as características conforme esperado pelo modelo
    future_features['year'] = future_features['Date'].dt.year
    future_features['month'] = future_features['Date'].dt.month
    future_features['day'] = future_features['Date'].dt.day
    future_features['dayofweek'] = future_features['Date'].dt.dayofweek

    # Calcular a média rolante para a nova feature
    future_features['rolling_mean'] = df_preco_petroleo['price'].rolling(window=30).mean().iloc[-1]  # Ajuste conforme necessário

    # Criar o time_index
    future_features['time_index'] = range(len(future_features))

    # Gerar as previsões
    future_features['Predictions'] = reg_best.predict(future_features[['year', 'month', 'day', 'dayofweek']])

    # Filtrar os últimos 365 dias de dados reais
    last_year_data = df_preco_petroleo[df_preco_petroleo['Date'] > df_preco_petroleo['Date'].max() - timedelta(days=365)]

    window_size = 7
    future_features['Predictions_smooth'] = future_features['Predictions'].rolling(window=window_size).mean()

    # Plotar os dados reais e as previsões
    plt.figure(figsize=(14, 7))

    # Plotar os dados reais (último ano)
    plt.plot(last_year_data['Date'], last_year_data['price'], label='Dados Reais (último ano)', color='blue', alpha=0.6)

    # Plotar as previsões futuras
    plt.plot(future_features['Date'], future_features['Predictions_smooth'], label='Previsões Futuras', color='purple', linestyle='--', alpha=0.8)

    plt.xlabel('Data')
    plt.ylabel('Preço Previsto')
    plt.title(f'Previsões e Dados Reais para o Preço do Petróleo')
    plt.legend()
    plt.grid(True)
    
    # Exibir gráfico no Streamlit
    st.pyplot(plt)

    st.write("Métricas modelo:")
    st.write(df_metrics[['Métrica', 'Valor']])
