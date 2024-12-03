import streamlit as st
import yfinance as yf

#--------------------------------------------------------------------------------------------------

# config da página
st.set_page_config(
    page_title='Dashboard de ações - IBOVESPA',
    layout = 'wide'
)

#--------------------------------------------------------------------------------------------------

# titulo
st.header("**PAINEL DE ACMPANHAMENTO DE AÇÕES B3**")

#--------------------------------------------------------------------------------------------------

# opção para escolher o ticker - Itaú como default
ticker = st.text_input('Digite o ticker do ativo: ', 'ITUB4')
# adicionando automaticamente o .SA para o usuário não ter que escrever
empresa = yf.Ticker(f"{ticker}.SA")

#--------------------------------------------------------------------------------------------------

# periodo diario
# data inicial
# data final
tickerDF = empresa.history(period = '1d',
                           start = '2017-01-01',
                           end = '2024-10-17'
                           )

#--------------------------------------------------------------------------------------------------

# criando colunas
col1, col2, col3 = st.columns([1,1,1])

#preenchendo col1
with col1:
    st.write(f"**Empresa:** {empresa.info['longName']}") # nome da empresa longo

#preenchendo col2
with col2:
    st.write(f"**Mercado:** {empresa.info['industry']}") # área de atuação da empresa

#preenchendo col3
with col3:
    st.write(f"**Preço Atual:** R$ {empresa.info['currentPrice']}") # preço atual

#--------------------------------------------------------------------------------------------------

# gráfico de linhas
st.write('Fechamento ao longo do tempo:')
st.line_chart(tickerDF.Close)

# gráfico de barras
st.write('Dividendos:')
st.bar_chart(tickerDF.Dividends)
