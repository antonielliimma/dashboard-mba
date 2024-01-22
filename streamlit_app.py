import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px 

st.title('Analise Reclame Aqui')

dfn = pd.read_csv('RECLAMEAQUI_NAGEM.csv', sep=';')
dfh = pd.read_csv('RECLAMEAQUI_HAPVIDA.csv', sep=';')
dfi = pd.read_csv('RECLAMEAQUI_IBYTE.csv', sep=';')

def apply_uf(value):
    uf = value.split('-')[1].strip()
    return uf if len(uf) == 2 else None

def count_words(value):
    return len(value.split())


dfi['UF'] =  dfi['LOCAL'].apply(apply_uf)
dfn['UF'] =  dfn['LOCAL'].apply(apply_uf)
dfh['UF'] =  dfh['LOCAL'].apply(apply_uf)

dfi['WORDS'] =  dfi['DESCRICAO'].apply(count_words)
dfn['WORDS'] =  dfn['DESCRICAO'].apply(count_words)
dfh['WORDS'] =  dfh['DESCRICAO'].apply(count_words)

dfi['TEMPO'] = pd.to_datetime(dfi['TEMPO'])
dfn['TEMPO'] = pd.to_datetime(dfn['TEMPO'])
dfh['TEMPO'] = pd.to_datetime(dfh['TEMPO'])

dfi['EMPRESA'] = 'IBYTE'
dfn['EMPRESA'] = 'NAGEM'
dfh['EMPRESA'] = 'HAPVIDA'

df = pd.concat([dfi, dfn, dfh], ignore_index=True)

df = df.dropna()

with st.sidebar:
    empresas = st.multiselect(
        'Empresa',
        list(df['EMPRESA'].unique()),
        list(df['EMPRESA'].unique())
        )
    ufs = st.multiselect(
        'Estados',
        list(df['UF'].unique()),
        list(df['UF'].unique()),
        )

    status = st.multiselect(
        'Status',
        list(df['STATUS'].unique()),
        list(df['STATUS'].unique()),
        )
    
    size = st.slider(
        'Tamanho da descrição',
        0, 2000, 0)    


copy = df.copy()
df_filter = copy[(copy['EMPRESA'].isin(empresas)) & (copy['UF'].isin(ufs)) & (copy['STATUS'].isin(status)) & (copy['WORDS'] >= size)]

#1. Série temporal do número de reclamações. 
series = df_filter.copy()
series['MES_ANO'] = df_filter['TEMPO'].dt.strftime('%b/%Y')
dfs = series.groupby('MES_ANO').size().reset_index(name='Numero_Reclamacoes')
fig = px.bar(dfs, x='MES_ANO', y='Numero_Reclamacoes', title='Reclamações Mensais',
             labels={'MES_ANO': 'Mês/Ano', 'Numero_Reclamacoes': 'Número de Reclamações'})
fig.update_layout(xaxis=dict(tickangle=60))
st.plotly_chart(fig)

#2. Frequência de reclamações por estado. 
dff_uf = df_filter.copy()
dff_uf = dff_uf.groupby('UF')['CASOS'].agg(['sum']).reset_index().rename({'sum':"frequencia"}, axis=1)
fig = px.bar(dff_uf, x='UF', y='frequencia', title='Frequência de Reclamações por Estado',
             labels={'UF': 'Estado', 'frequencia': 'Número de Reclamações'})

st.plotly_chart(fig)

#3. Frequência de cada tipo de **STATUS**

dff_status = df_filter.copy()
dff_status = dff_status.groupby('STATUS')['CASOS'].agg(['sum']).reset_index().rename({'sum':"FREQUENCIA"}, axis=1)
fig = px.bar(dff_status, x='STATUS', y='FREQUENCIA', title='Frequência de Reclamações por Status',
             labels={'STATUS': 'Status', 'FREQUENCIA': 'Número de Reclamações'})             
fig.update_layout(xaxis=dict(tickangle=60))
st.plotly_chart(fig)

#4. Distribuição do tamanho do texto (coluna **DESCRIÇÃO**) 

dff_words = df_filter.copy()
fig = px.histogram(dff_words, x='WORDS', title='Distribuição de caracteres da "DESCRIÇÃO"',
                   labels={'WORDS': 'Quantidade de caracteres', 'count': 'Número de Reclamações'})

fig.update_layout(bargap=0.1)
st.plotly_chart(fig)
