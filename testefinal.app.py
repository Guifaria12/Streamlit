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

st.write("""
    O preço do petróleo desempenha um papel fundamental na economia global, influenciando mercados financeiros, políticas energéticas e estratégias corporativas em diversos setores, até mesmo em aspectos micro da sociedade (i.e. o preço da gasolina no posto que cotidianamente se abastece o carro para ir ao trabalho). Por ser um dos principais indicadores econômicos, sociais e políticos, compreender sua dinâmica de variação ao longo do tempo é essencial para a tomada de decisões estratégicas em um ambiente econômico volátil e interconectado.
""")

st.markdown("<hr style='border:1px solid #000000;'>", unsafe_allow_html=True)

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

st.subheader("**Eventos que impactaram os preços:**")

st.write("""
 * **1990-1991:** Guerra do Golfo: Conflito no Oriente Médio elevou brevemente os preços, mas a recessão global limitou o impacto.
 * **2001:** Ataques de 11 de Setembro: Aumento temporário nos preços e foco na segurança energética dos EUA.
 * **2003:** Invasão do Iraque: Instabilidade geopolítica impulsionou preços durante crescimento global acelerado.
 * **2008:** Crise Financeira Global: Recessão mundial derrubou a demanda e fez os preços caírem drasticamente.
 * **2014-2016:** Petróleo de Xisto: Excesso de oferta dos EUA levou a queda histórica nos preços.
 * **2016:** Acordo da OPEP+: Cortes coordenados de produção estabilizaram e recuperaram os preços.
 * **2020:** Pandemia da COVID-19: Lockdowns globais colapsaram a demanda, levando a preços negativos.
 * **2022:** Guerra na Ucrânia: Sanções à Rússia dispararam preços devido à insegurança no fornecimento global.
""")

st.markdown("<hr style='border:1px solid #000000;'>", unsafe_allow_html=True)


st.header("**Insights:**")
st.write (""" 
**1° Insight: Geopolítica e Preços do Petróleo: Um Ciclo de Alta e Baixa** - 
Os picos de preços e quedas são fortemente ligados a guerras, instabilidades e acordos (como o da OPEP+ em 2016), confirmando a correlação entre geopolítica e mercado.

**2° Insight: Crescimento Econômico Global como Motor da Demanda** - 
Períodos de alta de preços coincidem com fases de crescimento econômico (como em 2003 e pré-2008), enquanto recessões resultam em quedas significativas.

**3° Insight: Impacto de Inovações e Excesso de Oferta** - 
O primeiro gráfico (comparação preço x uso) reflete uma queda significativa em 2014-2016, relacionada à ascensão do petróleo de xisto, evidenciando o impacto das inovações tecnológicas.

**4° Insight: Estabilização e Disrupções:** - 
A queda extrema de 2020 é exemplificada pela pandemia de COVID-19, que abalou o equilíbrio de oferta e demanda. A recuperação gradual nos anos subsequentes, vista no segundo gráfico, reflete intervenções e ajustes no mercado.
""")

st.markdown("<hr style='border:1px solid #000000;'>", unsafe_allow_html=True)

st.header("**Modelos de Machine Learning:**")

st.subheader ("Modelos utilizados ")

st.write ("""

**ARIMA (AutoRegressive Integrated Moving Average)**

* Este modelo foi escolhido por sua robustez na análise de séries temporais com dados estacionários ou transformados para estacionaridade.
Vantagens:
Excelente para capturar padrões sazonais e tendências históricas de curto prazo.
Permite modelar a autocorrelação entre observações.

Desempenho:
Funcionou bem em séries com padrões previsíveis, mas apresentou limitações ao lidar com dados mais complexos ou não estacionários, especialmente onde mudanças estruturais ocorrem.


**Prophet**
* O Prophet foi escolhido por sua capacidade de modelar séries temporais com sazonalidades variadas e componentes exógenos, como feriados e eventos especiais.
Vantagens:
Fácil de implementar e ajustar, com bom suporte para sazonalidade e eventos externos.
Robusto contra dados ausentes e outliers.

Desempenho:
Superou o ARIMA ao capturar padrões mais complexos e oferecer previsões confiáveis. Além disso, gerou intervalos de confiança úteis para análise de riscos.


**XGBoost Regressor**
* O XGBoost foi construído para explorar padrões mais complexos nos dados, utilizando um modelo baseado em árvores de decisão com técnicas de boosting.
Vantagens:
Capacidade de capturar relações não lineares e interações complexas.
Resistente a overfitting devido ao uso de regularização e boosting.

Desempenho:
Superou todos os outros modelos, apresentando a menor taxa de erro e a melhor capacidade de generalização. Mostrou-se ideal para séries temporais onde fatores externos têm grande influência.

""")
st.markdown("<hr style='border:1px solid #000000;'>", unsafe_allow_html=True)


st.subheader ("Avaliação dos Modelos")

st.write ("""
As métricas utilizadas para avaliar os modelos foram:

* **MAE (Erro Médio Absoluto):** Mede a média absoluta dos erros.
* **Mean Squared Error (MSE):** Para medir a precisão do modelo em prever valores numéricos.
* **MAPE (Erro Percentual Absoluto Médio):** Expressa o erro em termos percentuais.
* **R² (Coeficiente de Determinação):** Para avaliar a proporção da variação dos dados explicada pelo modelo.
""")
st.text ("""
Os resultados foram os seguintes:

XGBoost Metrics:
MAE: 2.2787702026367187.
MSE: 9.370494869745423.
RMSE: 3.0611264053850213.
R2: -0.1074362651768701.

Prophet Metrics:
MAE: 15.746337317234484.
MSE: 257.57486298101446.
MAPE: 20.8705505543171.

SARIMAX Metrics:
MAE: 6.588024306967685.
MSE: 52.2327502612595.
MAPE: 8.89090381557282.
""")

st.markdown("<hr style='border:1px solid #000000;'>", unsafe_allow_html=True)

st.header ("Gráfico de Previsão de Preço de Petróleo (Machine Learning)")

# Importação das bibliotecas
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go
from datetime import timedelta

# Importação e processamento dos dados
metrics = {
    'Métrica': ['MAE', 'MSE', 'RMSE', 'R2'],
    'Valor': [2.27, 9.37, 3.06, -0.10]
}

df_metrics = pd.DataFrame(metrics)

url_preco_petroleo = 'https://docs.google.com/spreadsheets/d/1WSL2mbFwfnQR5vDF73UmcOK5_zf5NGelasCCo8_qCOk/export?format=csv'

df_preco_petroleo = pd.read_csv(url_preco_petroleo)
df_preco_petroleo = df_preco_petroleo.rename(columns={'Data (Descending)': 'Date', 'Preço - petróleo bruto - Brent (FOB)': 'price'})
df_preco_petroleo['Date'] = pd.to_datetime(df_preco_petroleo['Date'])
df_preco_petroleo['price'] = df_preco_petroleo['price'].str.replace(',', '.', regex=False)
df_preco_petroleo['price'] = pd.to_numeric(df_preco_petroleo['price'])

model_filename = "Modelo/best_xgboost_model.joblib"
reg_best = joblib.load(model_filename)

FEATURES = ['day_of_week', 'month', 'day_of_month', 'rolling_mean', 'time_index']
TARGET = 'price'

# Interface Streamlit
st.markdown('<style>div[role="listbox"] ul{background-color: #6e42ad}; </style>', unsafe_allow_html=True)
st.warning('Indique quantos Meses pretende prever e depois clique no botão **PREVER** no final da página.')

input_days = int(st.slider('Selecione a quantidade de MESES para previsão', 1, 12))
st.write(f"Você selecionou prever para {input_days} meses.")

if st.button('Prever'):
    input_days = input_days * 30
    future_dates = pd.date_range(start=df_preco_petroleo['Date'].max() + timedelta(days=1), periods=input_days, freq='D')
    
    future_features = pd.DataFrame(index=future_dates)
    future_features['Date'] = future_features.index

    future_features['year'] = future_features['Date'].dt.year
    future_features['month'] = future_features['Date'].dt.month
    future_features['day'] = future_features['Date'].dt.day
    future_features['dayofweek'] = future_features['Date'].dt.dayofweek
    future_features['rolling_mean'] = df_preco_petroleo['price'].rolling(window=30).mean().iloc[-1]
    future_features['time_index'] = range(len(future_features))

    future_features['Predictions'] = reg_best.predict(future_features[['year', 'month', 'day', 'dayofweek']])

    last_year_data = df_preco_petroleo[df_preco_petroleo['Date'] > df_preco_petroleo['Date'].max() - timedelta(days=365)]

    window_size = 7
    future_features['Predictions_smooth'] = future_features['Predictions'].rolling(window=window_size).mean()

    # Criar gráfico interativo com Plotly
    fig = go.Figure()

    # Adicionar dados reais (último ano)
    fig.add_trace(go.Scatter(
        x=last_year_data['Date'],
        y=last_year_data['price'],
        mode='lines',
        name='Dados Reais (último ano)',
        line=dict(color='blue', width=2),
        opacity=0.6
    ))

    # Adicionar previsões futuras suavizadas
    fig.add_trace(go.Scatter(
        x=future_features['Date'],
        y=future_features['Predictions_smooth'],
        mode='lines',
        name='Previsões Futuras',
        line=dict(color='purple', width=2, dash='dot'),
        opacity=0.8
    ))

    # Configurar layout do gráfico
    fig.update_layout(
        title='Previsões e Dados Reais para o Preço do Petróleo',
        xaxis_title='Data',
        yaxis_title='Preço',
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
        template='plotly_white',
        hovermode='x unified'  # Exibe todos os valores ao passar o mouse
    )

    # Exibir gráfico no Streamlit
    st.plotly_chart(fig, use_container_width=True)

    # Exibir métricas
    st.write("**Métricas do modelo:**")
    st.write(df_metrics[['Métrica', 'Valor']])

st.markdown("<hr style='border:1px solid #000000;'>", unsafe_allow_html=True)


st.header ("Conclusão")

st.write ("""
Com os dados apresentados, é possível entender que estar atento aos acontecimentos geopolíticos é fundamental para compreender a variação do preço do barril de petróleo. Além disso, analisar a sua variação e projeção permite que, em um ambiente de negócios, decisões estratégicas sejam tomadas de forma mais planejada e eficiente. Por exemplo, a abertura e o sucesso de um novo empreendimento estão intimamente relacionados a esses fatores, uma vez que influenciam diretamente a logística de abastecimento, a atração de clientes e outros aspectos essenciais para a operação do negócio.

Por fim, explorar esses dados exige uma compreensão não apenas de sua variação histórica, mas também da conexão com questões geopolíticas, econômicas e ambientais que impactam o mercado global de energia. Esse conhecimento permite uma visão mais ampla e assertiva, essencial para antecipar tendências e minimizar riscos no desenvolvimento de estratégias empresariais.

""")
