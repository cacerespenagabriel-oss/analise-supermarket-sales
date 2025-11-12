import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
import seaborn as sns
import numpy as np

# --- Configuração da Página ---
st.set_page_config(layout="wide", page_title="Supermarket Sales Dashboard")

# --------------------------------------- 
# 0. CARREGAMENTO E PRÉ-PROCESSAMENTO DE DADOS
# ---------------------------------------

@st.cache_data
def load_data():
    try:
        df = pd.read_excel('supermarket_sales.xlsx')
    except FileNotFoundError:
        st.error("ERRO: Arquivo 'supermarket_sales.xlsx' não encontrado. Por favor, verifique o caminho.")
        df = pd.DataFrame({
            'Invoice ID': np.arange(100),
            'Branch': np.random.choice(['A', 'B', 'C'], 100),
            'City': np.random.choice(['Mandalay', 'Naypyitaw', 'Yangon'], 100),
            'Customer type': np.random.choice(['Member', 'Normal'], 100),
            'Gender': np.random.choice(['Female', 'Male'], 100),
            'Product line': np.random.choice(['Food and beverages', 'Fashion accessories', 'Electronic accessories'], 100),
            'Unit price': np.random.uniform(10, 100, 100),
            'Quantity': np.random.randint(1, 10, 100),
            'Total': np.random.uniform(100, 500, 100),
            'Date': pd.to_datetime(pd.date_range('2023-01-01', periods=100, freq='D')),
            'gross income': np.random.uniform(10, 50, 100),
            'Rating': np.random.uniform(1, 10, 100)
        })
        
    df1 = df.copy()

    # Limpando a coluna Date e criando colunas de tempo
    df1['Date'] = pd.to_datetime(df1['Date'], errors='coerce')
    df1['Dia_Semana'] = df1['Date'].dt.day_name(locale='pt_BR') # Tenta localizar para português
    df1['Mes'] = df1['Date'].dt.month_name(locale='pt_BR')
    df1['Date'] = df1['Date'].dt.date
    
    return df1

df1 = load_data()


# --------------------------------------- 
# 1. FUNÇÕES DE PÁGINAS
# ---------------------------------------

def pagina_inicial():
    st.title("🏠 Página Inicial | Supermarket Sales Dashboard")

    st.markdown('''
    Seja muito bem-vindo(a)!

    Me chamo Gabriel Cáceres Pena, tenho 20 anos e atualmente curso Engenharia da Computação na UNIVESP.

    Para exercitar meus conhecimentos em análise de dados, desenvolvi este projeto chamado Supermarket Sales, no qual realizo uma exploração completa de um conjunto de dados de vendas de supermercado, disponível no DataSet Supermarket Sales no Kaggle.

    O objetivo é analisar informações sobre vendas, clientes, satisfação, impostos, lucros e tendências ao longo do tempo, transformando dados brutos em insights úteis e visualmente intuitivos.

    Aqui, você poderá interagir com dashboards dinâmicos, visualizar gráficos e entender como as decisões baseadas em dados podem ajudar a melhorar o desempenho e a estratégia de um negócio.

    Aproveite a navegação e boa análise!🤗
    ''')
    st.markdown("---")
    st.subheader("Amostra do DataSet")
    st.dataframe(df1.head(), use_container_width=True)


def pagina_vendas(df):
    st.title('📈 Métricas de Vendas')
    st.markdown('''##### Para uma melhor noção a respeito dos dados, confira o DataSet completo abaixo:''')
    st.dataframe(df, use_container_width=True)
    st.markdown('##### Vamos Responder a Perguntas de Negócios relacionados a Vendas:')
    st.markdown('''
1. Qual é o total de receita (gross income) gerado por cada filial (Branch)?
2. Qual filial teve a maior média de vendas?
3. Qual é o produto mais vendido (por Product line)?
4. Qual é o dia da semana com maior volume de vendas?
5. Qual é o mês com maior receita total?
''')
    
    st.markdown('##### Respostas:')

    # 1. Receita total por filial
    st.markdown('1. Qual é o total de receita (gross income) gerado por cada filial (Branch)?')
    resultado = df.loc[: , ['Branch', 'gross income']].groupby('Branch').sum().reset_index()
    st.dataframe(resultado, use_container_width=True)
    # Exemplo de resposta baseada nos dados
    st.info(f"O maior faturamento foi da Branch {resultado.sort_values('gross income', ascending=False).iloc[0]['Branch']} com R$ {resultado['gross income'].max():,.2f}.")
    st.markdown('---')

    # 2. Filial com maior média de vendas
    st.markdown('2. Qual filial teve a maior média de vendas?')
    resultado = df.loc[: , ['Branch', 'Total']].groupby('Branch').mean().sort_values('Total', ascending=False).reset_index()
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(resultado['Branch'], resultado['Total'], color='orange')
    ax.set_title('Média de Vendas por Filial')
    ax.set_xlabel('Filial')
    ax.set_ylabel('Média de Vendas (R$)')
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    min_total = resultado['Total'].min()
    ax.set_ylim(bottom=min_total - 10)
    st.pyplot(fig)
    st.dataframe(resultado, use_container_width=True)
    st.info('A Branch com maior média de faturamento foi a Branch {}, com R${:.2f} de média'.format(resultado.loc[0, 'Branch'], resultado.loc[0, 'Total']))
    st.markdown('---')
    
    # 3. Produto mais vendido (por Product line)
    st.markdown('3. Qual é o produto mais vendido (por Product line)?')
    resultado = df.loc[: , ['Product line', 'Quantity']].groupby('Product line').sum().sort_values('Quantity', ascending=False).reset_index()
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(resultado['Product line'], resultado['Quantity'], color='green')
    ax.set_title('Produtos Mais Vendidos')
    ax.set_xlabel('Linha de Produto')
    ax.set_ylabel('Quantidade Vendida')
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    plt.xticks(rotation=45, ha='right')
    min_total = resultado['Quantity'].min()
    ax.set_ylim(bottom=min_total - 50)
    fig.tight_layout()
    st.pyplot(fig)
    st.dataframe(resultado, use_container_width=True)
    st.info('O produto com maior número de vendas foi o produto {}, com {} vendas.'.format(resultado.loc[0, 'Product line'], resultado.loc[0, 'Quantity']))
    st.markdown('---')
    
    # 4. Dia da semana com maior volume de vendas
    st.markdown('4. Qual é o dia da semana com maior volume de vendas?')
    resultado = df.loc[:, ['Dia_Semana', 'Invoice ID']].groupby('Dia_Semana').count().sort_values('Invoice ID', ascending=False).reset_index()
    fig, ax= plt.subplots(figsize=(8, 4))
    ax.bar(resultado['Dia_Semana'], resultado['Invoice ID'], color='purple')
    ax.set_title('Volume de Vendas por Dia da Semana')
    ax.set_xlabel('Dia')
    ax.set_ylabel('Total de Vendas')
    plt.xticks(rotation=45, ha='right')
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    menor_valor = resultado['Invoice ID'].min()
    ax.set_ylim(bottom=(menor_valor-10))
    fig.tight_layout()
    st.pyplot(fig)
    st.dataframe(resultado, use_container_width=True)
    st.info('O dia da semana que mais realizou vendas foi o dia {}, realizando {} vendas.'.format(resultado.loc[0, 'Dia_Semana'], resultado.loc[0, 'Invoice ID']))
    st.markdown('---')

    # 5. Mês com maior receita total
    st.markdown('5. Qual é o mês com maior receita total?')
    resultado = df.loc[:, ['Mes', 'Total']].groupby('Mes').sum().sort_values('Total', ascending=False).reset_index()
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(resultado['Mes'], resultado['Total'], marker='o', color='red')
    ax.set_title('Receita Total por Mês')
    ax.set_xlabel('Mês')
    ax.set_ylabel('Receita Total (R$)')
    ax.grid(True, linestyle='--', alpha=0.7)
    # Adiciona todos os meses no eixo X
    ax.set_xticks(resultado['Mes'])
    fig.tight_layout()
    st.pyplot(fig)
    st.dataframe(resultado, use_container_width=True)
    st.info('O mês com maior faturamento foi o mês de {}, com R${:,.2f} de faturamento.'.format(resultado.loc[0, 'Mes'], resultado.loc[0, 'Total']))
    st.markdown('---')


def pagina_clientes(df):
    st.title('👤 Métricas sobre Comportamento do Cliente')
    st.markdown('''##### Para uma melhor noção a respeito dos dados, confira o DataSet completo abaixo:''')
    st.dataframe(df, use_container_width=True)
    st.markdown('##### Vamos Responder a Perguntas de Negócios relacionados ao comportamento do cliente:')
    st.markdown('''
1. Qual gênero (Gender) mais compra em cada filial?
2. Clientes de qual tipo (`Customer Type`: Member / Normal) gastam mais em média?
3. Há diferença no valor médio de compra entre clientes de diferentes cidades?
4. Qual método de pagamento é mais usado?
5. Clientes que usam cartões ou dinheiro gastam mais em média?
''')
    
    st.markdown('##### Respostas:')
    
    # 1. Gênero que mais compra em cada filial (Plotly)
    st.markdown('1. Qual gênero (Gender) mais compra em cada filial?')
    resultado = df.loc[:, ['Gender', 'Branch', 'Invoice ID']].groupby(['Branch', 'Gender']).count().reset_index()
    resultado = resultado.rename(columns={'Invoice ID': 'Contagem de Compras'})
    
    cores = {'Female': 'deeppink', 'Male': 'dodgerblue'}
    fig = px.bar(
        resultado, 
        x='Branch',           # Eixo X: Filiais
        y='Contagem de Compras', # Eixo Y: Quantidade de compras
        color='Gender',       # Agrupa e colore por Gênero
        barmode='group',      # Configura o modo como 'lado a lado'
        title='Volume de Compras por Filial e Gênero',
        labels={
            'Branch': 'Filial', 
            'Contagem de Compras': 'Número de Compras (Invoice ID)', 
            'Gender': 'Gênero'
        },
        color_discrete_map=cores # Aplica as cores personalizadas
    )
    fig.update_layout(
        xaxis_title='Filial',
        yaxis_title='Contagem de Compras',
        legend_title='Gênero',
        font=dict(size=12),
        hovermode='x unified'
    )
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(resultado, use_container_width=True)
    st.markdown('---')
    
    # 2. Gasto médio por tipo de cliente
    st.markdown('2. Clientes de qual tipo (`Customer Type`: Member / Normal) gastam mais em média?')
    resultado = df.loc[:, ['Customer type', 'Total']].groupby('Customer type').mean().reset_index()
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(resultado['Customer type'], resultado['Total'])
    ax.set_title('Gasto em média de Tipos de Clientes')
    ax.set_ylabel('Gasto em Média (R$)')
    ax.set_xlabel('Tipo de Cliente')
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    min_value = resultado['Total'].min()
    ax.set_ylim(bottom=(min_value-10))
    st.pyplot(fig)
    resultado = resultado.rename(columns={'Total': 'Média de Gastos'})
    st.dataframe(resultado, use_container_width=True)
    st.info('Clientes do tipo Member costumam gastar mais do que clientes Normal, com médias respectivamente de {:.4f} e {:.4f}.'.format(resultado[resultado['Customer type'] == 'Member']['Média de Gastos'].iloc[0], resultado[resultado['Customer type'] == 'Normal']['Média de Gastos'].iloc[0]))
    st.markdown('---')
    
    # 3. Diferença no valor médio de compra entre cidades
    st.markdown('3. Há diferença no valor médio de compra entre clientes de diferentes cidades?')
    resultado = df.loc[:, ['City', 'Total']].groupby('City').mean().reset_index()
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(resultado['City'], resultado['Total'], color='lightgreen')
    ax.set_title('Valor Médio de Compra por Cidade')
    ax.set_xlabel('Cidade')
    ax.set_ylabel('Ticket Médio (R$)')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    valor_minimo = resultado['Total'].min()
    ax.set_ylim(bottom=(valor_minimo-10))
    st.pyplot(fig)
    st.dataframe(resultado, use_container_width=True)
    
    maior_cidade = resultado.sort_values('Total', ascending=False).iloc[0]['City']
    maior_media = resultado.sort_values('Total', ascending=False).iloc[0]['Total']
    st.info(f"O Ticket Médio mais alto é na cidade de {maior_cidade}, com uma média de R$ {maior_media:.4f}.")
    st.markdown('---')
    
    # Adicione a lógica para as perguntas 4 e 5 aqui...

def pagina_satisfacao(df):
    st.title('⭐ Métricas de Satisfação')
    st.warning("Esta seção está em desenvolvimento.")
    # Adicione sua lógica de satisfação e gráficos aqui

def pagina_impostos_lucros(df):
    st.title('💰 Impostos e Lucros')
    st.warning("Esta seção está em desenvolvimento.")
    # Adicione sua lógica de impostos e lucros e gráficos aqui

def pagina_temporal(df):
    st.title('⏳ Análise Temporal')
    st.warning("Esta seção está em desenvolvimento.")
    # Adicione sua lógica de análise temporal e gráficos aqui


# --------------------------------------- 
# 2. BARRA LATERAL (MENU DE NAVEGAÇÃO)
# ---------------------------------------

st.sidebar.title("Menu de Análise")

# Trocando o st.selectbox/checkbox pelo st.radio
PAGES = {
    "Página Inicial": pagina_inicial,
    "Vendas": pagina_vendas,
    "Clientes": pagina_clientes,
    "Satisfação": pagina_satisfacao,
    "Impostos e Lucros": pagina_impostos_lucros,
    "Temporal": pagina_temporal
}

selecao_pagina = st.sidebar.radio("Selecione a Seção", list(PAGES.keys()))

# --------------------------------------- 
# 3. LÓGICA DE ROTEAMENTO
# ---------------------------------------

# Chama a função correspondente à página selecionada
if selecao_pagina in ["Página Inicial"]:
    PAGES[selecao_pagina]() # Não precisa passar o df1
else:
    PAGES[selecao_pagina](df1) # Passa o df1 para as páginas de análise
    