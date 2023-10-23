import streamlit as st
import plotly.express as px
from Modules.dados import puxar_df


st.set_page_config(layout="wide")
df = puxar_df()
col1 = st.columns(1)[0]
col2 = st.columns(1)[0]
col3, col4 = st.columns(2)

# --------------------GRÁFICO 01 - POR REGIÃO SECRETARIA--------------------#
# Criar uma lista de tipos de documento exclusivos
tipos_documento = ["Todos"] + df['tipo_documento'].unique().tolist()
# Adicionar um widget de seleção (dropdown) para escolher o tipo de documento
tipo_documento = col1.selectbox("Selecione o Tipo de Documento", tipos_documento)


# Filtrar o DataFrame com base na escolha do tipo de documento
if tipo_documento != "Todos":
    df_filtrado = df[df['tipo_documento'] == tipo_documento]
else:
    df_filtrado = df

# Calcular o quantitativo de dados por regiao_secretaria
quantitativo_por_regiao = df_filtrado['regiao_secretaria'].value_counts().reset_index()
quantitativo_por_regiao.columns = ['Região Secretaria', 'Quantitativo']

# Criar um mapeamento de cores personalizado
cores_personalizadas = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
cor_discrete_map = {regiao: cor for regiao, cor in zip(quantitativo_por_regiao['Região Secretaria'], cores_personalizadas)}

# Criar um gráfico de barras com Plotly e aplicar o mapeamento de cores
fig = px.bar(quantitativo_por_regiao, x='Região Secretaria', y='Quantitativo',
             labels={'Região Secretaria':'Região Secretaria', 'Quantitativo':'Quantitativo'},
             title=f"Quantitativo por Região Secretaria - 2022 ({tipo_documento})",
             text='Quantitativo', color='Região Secretaria',
             color_discrete_map=cor_discrete_map)

# Personalizar o layout do gráfico
fig.update_traces(texttemplate='%{text}', textposition='outside')
fig.update_layout(legend_title_text='Região')
fig.update_xaxes(categoryorder='total ascending')

# Exibir o gráfico no aplicativo Streamlit com um tamanho maior
col1.plotly_chart(fig, use_container_width=True)

# --------------------GRÁFICO 02 - POR ASSUNTO--------------------#
# Calcular o quantitativo de dados por assunto
quantitativo_por_assunto = df['assunto'].value_counts().reset_index()
quantitativo_por_assunto.columns = ['Assunto', 'Quantitativo']

# Criar um gráfico de barras com Plotly
fig = px.bar(quantitativo_por_assunto, x='Assunto', y='Quantitativo',
             color='Assunto',
             labels={'Assunto':'Assunto', 'Quantitativo':'Quantitativo'},
             title="Quantitativo por Assunto - 2022",
             text='Quantitativo')

# Personalizar o layout do gráfico
fig.update_traces(texttemplate='%{text}', textposition='outside')
fig.update_layout(legend_title_text='Assuntos')
fig.update_xaxes(categoryorder='total ascending')

# Exibir o gráfico no aplicativo Streamlit
col2.plotly_chart(fig, use_container_width=True)


# --------------------GRÁFICO 03 - Tipo Documento--------------------#
# Calcular o quantitativo de documentos por tipo de documento
quantitativo_por_tipo_documento = df['tipo_documento'].value_counts().reset_index()
quantitativo_por_tipo_documento.columns = ['Tipo de Documento', 'Quantitativo']

# Criar um gráfico de pizza com Plotly Express
fig = px.pie(quantitativo_por_tipo_documento, names='Tipo de Documento', values='Quantitativo',
             title="Quantitativo por Tipo de Documento - 2022")

# Exibir o gráfico no aplicativo Streamlit
col3.plotly_chart(fig, use_container_width=False)


# --------------------GRÁFICO 04 - Quantitativo Remetente--------------------#
# Substituir valores NaN (campos de interesse vazios) por "Não informado" na coluna "interesse"
df['interesse'].fillna("Não informado", inplace=True)

# Calcular o quantitativo de documentos por interesse
quantitativo_por_interesse = df['interesse'].value_counts().reset_index()
quantitativo_por_interesse.columns = ['Interesse', 'Quantitativo']

# Criar um gráfico de barras com Plotly Express
fig = px.bar(quantitativo_por_interesse, x='Interesse', y='Quantitativo',
             color='Interesse',
             labels={'Interesse':'Interesse', 'Quantitativo':'Quantitativo'},
             title="Quantitativo por Interesse (incluindo vazios)",
             text='Quantitativo')

# Personalizar o layout do gráfico
fig.update_traces(texttemplate='%{text}', textposition='outside')
fig.update_layout(legend_title_text='Interesse')
fig.update_xaxes(categoryorder='total ascending')

# Exibir o gráfico no aplicativo Streamlit
col4.plotly_chart(fig, use_container_width=False)
