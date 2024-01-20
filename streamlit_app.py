import streamlit as st
import pandas as pd
import numpy as np

st.title('Analise PROUNI')

df = pd.read_csv('cursos-prouni2.csv', sep=';')

st.dataframe(df)  # Same as st.write(df)

options = st.multiselect(
    'Curso',
    list(df['curso_busca'].unique()),
    )

st.write('Selecionados:', options)

