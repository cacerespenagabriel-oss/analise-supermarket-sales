import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
import seaborn as sns
import numpy as np

df = pd.read_excel('supermarket_sales.xlsx')

df1 = df.copy()

df1['Date'] = pd.to_datetime(df1['Date'], errors='coerce')
df1['Dia_Semana'] = df1['Date'].dt.day_name()
df1['Mes'] = df1['Date'].dt.month_name()
df1['Date'] = df1['Date'].dt.date

plt.style.use('dark_background')



# -----------------------------------------------------------------------
# Barra de Navegação
# -----------------------------------------------------------------------

PAGES = [
    "Página Inicial",
    "Vendas",
    "Clientes",
    "Satisfação",
    "Impostos e Lucros",
    "Temporal"
]

with st.sidebar:
    st.title("Menu de Navegação")
    selected_page = st.radio(
        "Selecione a Página",
        PAGES
    )

if selected_page == "Página Inicial":
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
    st.dataframe(df1.head(10), use_container_width=True)

elif selected_page == "Vendas":
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
    resultado = df1.loc[: , ['Branch', 'gross income']].groupby('Branch').sum().reset_index()
    st.dataframe(resultado, use_container_width=True)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(resultado['Branch'], resultado['gross income'], color='mediumseagreen')
    ax.set_title('Receita Total (Gross Income) por Filial', fontsize=16)
    ax.set_xlabel('Receita Total (R$)', fontsize=12)
    ax.set_ylabel('Filial (Branch)', fontsize=12)
    ax.grid(axis='x', linestyle='--', alpha=0.7)
    min_valor = resultado['gross income'].min()
    novo_limite_min = min_valor * 0.95 
    ax.set_xlim(novo_limite_min)
    st.pyplot(fig)
    st.info(f"O maior faturamento foi da Branch {resultado.sort_values('gross income', ascending=False).iloc[0]['Branch']} com R$ {resultado['gross income'].max():,.2f}.")
    st.markdown('---')

    # 2. Filial com maior média de vendas
    st.markdown('2. Qual filial teve a maior média de vendas?')
    resultado = df1.loc[: , ['Branch', 'Total']].groupby('Branch').mean().sort_values('Total', ascending=False).reset_index()
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
    resultado = df1.loc[: , ['Product line', 'Quantity']].groupby('Product line').sum().sort_values('Quantity', ascending=False).reset_index()
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
    resultado = df1.loc[:, ['Dia_Semana', 'Invoice ID']].groupby('Dia_Semana').count().sort_values('Invoice ID', ascending=False).reset_index()
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
    resultado = df1.loc[:, ['Mes', 'Total']].groupby('Mes').sum().sort_values('Total', ascending=False).reset_index()
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

elif selected_page == "Clientes":
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
    st.info('O gênero dominante varia em cada filial, mas por uma diferença estreita, indicando que ambos os gêneros são importantes nas três unidades')
    st.markdown('---')
    
    # 2. Gasto médio por tipo de cliente
    st.markdown('2. Clientes de qual tipo (`Customer Type`: Member / Normal) gastam mais em média?')
    resultado = df.loc[:, ['Customer type', 'Total']].groupby('Customer type').mean().reset_index()
    # fig, ax = plt.subplots(figsize=(8, 4))
    # ax.bar(resultado['Customer type'], resultado['Total'])
    #ax.set_title('Gasto em média de Tipos de Clientes')
    # ax.set_ylabel('Gasto em Média (R$)')
    #ax.set_xlabel('Tipo de Cliente')
    #ax.grid(axis='y', linestyle='--', alpha=0.7)
    #min_value = resultado['Total'].min()
    #ax.set_ylim(bottom=(min_value-10))
    #st.pyplot(fig)

    fig, ax = plt.subplots(figsize=(10, 6))
    cores = ['#66c2a5', '#fc8d62'] # Uma paleta de cores bonita
    ax.bar(resultado['Customer type'], resultado['Total'], color=cores)
    ax.set_title('Gasto Médio por Tipo de Cliente', fontsize=18, color='white') # Título maior e branco
    ax.set_ylabel('Gasto Médio (R$)', fontsize=14, color='lightgray') # Eixos com fonte clara
    ax.set_xlabel('Tipo de Cliente', fontsize=14, color='lightgray')
    for index, value in enumerate(resultado['Total']):
        ax.text(index, value + 2, f'R$ {value:,.2f}', ha='center', va='bottom', color='white', fontsize=12)
    ax.grid(axis='y', linestyle='--', alpha=0.5, color='gray') # Grade mais discreta
    min_value = resultado['Total'].min()
    ax.set_ylim(bottom=(min_value * 0.95))
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('lightgray')
    ax.spines['bottom'].set_color('lightgray')

    # 4. Exibição no Streamlit
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

    st.markdown('4. Qual método de pagamento é mais usado?')
    resultado = df1.loc[:, ['Payment', 'Invoice ID']].groupby('Payment').count().reset_index()
    resultado.rename(columns={'Invoice ID': 'Quantidade de Compras'}, inplace=True)
    fig = px.treemap(
    resultado, 
    path=['Payment'],  # Categoria principal (Método de Pagamento)
    values='Quantidade de Compras', 
    color='Quantidade de Compras', # Colore com base na quantidade (para contraste visual)
    title='Uso de Métodos de Pagamento',
    color_continuous_scale='Sunset' # Escolha de cores
    )

    # 2. Exibição interativa no Streamlit
    st.plotly_chart(fig, use_container_width=True)
    st.write(resultado)
    st.info("O método de Pagamento mais utilizado é Ewallet, pois foi utilizado 345 vezes. Isso é claramente visível no Treemap, onde o Ewallet corresponde à maior área do gráfico, indicando sua dominância na contagem de compras.")
    st.markdown('---')
    
    st.markdown('5. Clientes que usam cartões ou dinheiro gastam mais em média?')
    resultado = df1.loc[:, ['Payment', 'Total']].groupby('Payment').mean().reset_index()
    
    # Mude apenas a função para px.violin
    fig = px.violin(
        df1, 
        x='Payment',     
        y='Total',       
        title='Densidade de Gasto Total por Método de Pagamento (Violin Plot)',
        box=True, # Opcional: mantém o Box Plot dentro do violino
        points="all", # Opcional: mostra todos os pontos de dados
        color='Payment'
    )

    st.plotly_chart(fig, use_container_width=True)
    st.write(resultado)
    st.info('Clientes que usam dinheiro gastam mais em média. No Violin Plot, isso é refletido pela linha da mediana e a área central da densidade que estão posicionadas em um patamar visivelmente mais alto em comparação com os outros métodos.')
    st.markdown('---')


elif selected_page == "Satisfação":
    st.title('⭐ Métricas sobre satisfação do cliente')
    st.markdown('''##### Para uma melhor noção a respeito dos dados, confira o DataSet completo abaixo:''')
    st.dataframe(df, use_container_width=True)
    st.markdown('##### Vamos Responder a Perguntas de Negócios relacionados a satisfação do cliente:')
    st.markdown('''
1. Qual é a média geral de avaliação (`Rating`)?
2. Existe correlação entre `Rating` e `Total` (clientes que gastam mais avaliam melhor)?
3. Qual linha de produto tem a maior média de avaliação?
''')
    
    st.markdown('---')
    st.markdown('1. Qual é a média geral de avaliação (`Rating`)?')
    resultado = df1.loc[:, 'Rating'].mean()
    fig, ax = plt.subplots()
    ax.hist(df1['Rating'], bins=10, color='plum', edgecolor='black')
    ax.set_title('Distribuição das Avaliações')
    ax.set_xlabel('Avaliação')
    ax.set_ylabel('Frequência')
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(fig)
    st.info('A média geral de rating é {}'.format(resultado))
    st.markdown('---')

    st.markdown('2. Existe correlação entre Rating e Total (clientes que gastam mais avaliam melhor)?')
    fig, ax = plt.subplots()
    ax.scatter(df1['Total'], df1['Rating'], alpha=0.6, color='teal')
    ax.set_title('Correlação entre Total Gasto e Avaliação')
    ax.set_xlabel('Total Gasto')
    ax.set_ylabel('Avaliação')
    plt.grid(True, linestyle='--', alpha=0.7)
    st.pyplot(fig)
    st.markdown('---')

    st.markdown('3. Qual linha de produto tem a maior média de avaliação?')
    resultado = df1.loc[:, ['Product line', 'Rating']].groupby('Product line').mean().sort_values('Rating', ascending=False).reset_index()
    fig, ax = plt.subplots()
    ax.plot(resultado['Product line'], resultado['Rating'], marker='o', color='red')
    ax.set_title('Média de rating por Produto')
    ax.set_xlabel('Produto')
    ax.set_ylabel('Rating')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)
    st.write(resultado)
    st.info('O produto com maior média de avaliação é Food_and_beverages')

elif selected_page == "Impostos e Lucros":
    st.title('💸 Impostos e Lucros')
    st.markdown('''##### Para uma melhor noção a respeito dos dados, confira o DataSet completo abaixo:''')
    st.dataframe(df, use_container_width=True)
    st.markdown('##### Vamos Responder a Perguntas de Negócios relacionados a impostos e lucros:')
    st.markdown('''
1. Qual é o total de imposto (`Tax 5%`) recolhido por cidade?
2. Qual categoria de produto gera mais lucro bruto (`gross income`)?
3. Qual foi o ticket médio (valor médio de compra) por cidade?
''')
    
    st.markdown('---')
    st.markdown("1. Qual é o total de imposto (`Tax 5%`) recolhido por cidade?")
    resultado = df1.loc[:, ['City', 'Tax 5%']].groupby('City').sum().sort_values('Tax 5%', ascending=False).reset_index()
    st.write(resultado)

    fig, ax = plt.subplots(figsize=(8, 5))
    # Dados
    cidades = resultado['City']
    impostos = resultado['Tax 5%']
    # 2. Desenho do Gráfico
    # Desenha as hastes (linhas horizontais) com cores padrão
    ax.hlines(y=cidades, xmin=0, xmax=impostos, color='skyblue')
    # Desenha os pontos (o 'picolé') com cores padrão
    ax.scatter(impostos, cidades, color='blue', s=100) 
    # 3. Rótulos e Título (Formato padrão)
    ax.set_title('Total de Imposto Recolhido por Cidade (R$)')
    ax.set_xlabel('Total de Imposto (R$)')
    ax.set_ylabel('Cidade')
    # Grade padrão (apenas no eixo X)
    ax.grid(axis='x', linestyle='--', alpha=0.6) 
    # Adição de Rótulos de Dados básicos (para ter alguma leitura)
    for index, value in enumerate(impostos.values):
        # Adiciona o valor no final do "picolé"
        ax.text(value, index, f' R$ {value:,.0f}', ha='left', va='center', fontsize=9)
    # Ajuste do Eixo X (para acomodar os rótulos de dados)
    ax.set_xlim(right=impostos.max() * 1.15) 
    # 4. Exibição
    st.pyplot(fig)
    st.info('A cidade Naypyitaw foi a cidade com mais imposto recolhido, com R\\$5.265 em impostos')
    st.markdown('---')


    st.markdown('2. Qual categoria de produto gera mais lucro bruto (`gross income`)?')
    resultado = df1.loc[:, ['Product line', 'gross income']].groupby('Product line').sum().sort_values('gross income', ascending=False).reset_index()
    # 1. Criação da Figura
    fig, ax = plt.subplots(figsize=(8, 6))
    # Dados
    categorias = resultado['Product line']
    lucro = resultado['gross income']
    # 2. Desenho do Gráfico (Barra Horizontal)
    ax.barh(categorias, lucro, color='teal') 
    # 3. Rótulos e Título
    ax.set_title('Lucro Bruto Total por Categoria de Produto', fontsize=14)
    ax.set_xlabel('Lucro Bruto (R$)')
    ax.set_ylabel('Categoria de Produto')
    # Grade padrão no eixo X
    ax.grid(axis='x', linestyle='--', alpha=0.6) 
    # Adição de Rótulos de Dados básicos (opcional, mas recomendado para ranking)
    for index, value in enumerate(lucro.values):
        # Coloca o rótulo no final da barra
        ax.text(value, index, f' R$ {value:,.0f}', ha='left', va='center', fontsize=9)
    # Ajuste do Eixo X
    ax.set_xlim(right=lucro.max() * 1.1) 

    # 4. Exibição
    st.pyplot(fig)
    st.write(resultado)
    st.info('O produto com maior lucro bruto foi Food_and_beverages, com R\\$2.673,5')
    st.markdown('---')

    st.markdown('Qual foi o ticket médio (valor médio de compra) por cidade?')
    resultado = df1.loc[:, ['City', 'Total']].groupby('City').mean().sort_values('Total').reset_index()
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(resultado['City'], resultado['Total'], color='lightseagreen')
    ax.set_title('Ticket Médio por Cidade', fontsize=16)
    ax.set_xlabel('Ticket Médio', fontsize=12)
    ax.set_ylabel('Cidade', fontsize=12)
    ax.grid(axis='x', linestyle='--', alpha=0.7)
    # Ajustar layout para evitar cortes
    plt.tight_layout()
    st.pyplot(fig)
    st.write(resultado)
    st.info('O ticket médio de cidade de Naypyitaw foi de 337, em Mandalay foi 319, e em Yangon foi 312.')

elif selected_page == "Temporal":
    st.title('📅 Métricas sobre variações de dados em função do tempo')
    st.markdown('''##### Para uma melhor noção a respeito dos dados, confira o DataSet completo abaixo:''')
    st.dataframe(df1, use_container_width=True)
    st.markdown('##### Vamos Responder a Perguntas de Negócios relacionados ao fator temporal:')
    st.markdown('''
1. Qual foi a média de vendas brutas (Gross Income) registrada a cada mês do ano?
2. Qual é a variação (Desvio Padrão - Standard Deviation) no valor total das vendas (Total) em cada hora do dia?
3. Qual é o dia da semana (Day of the Week) que registra o maior número de transações (Moda/Mais Frequente)?
''')
    
    st.markdown("---")
    st.markdown('1. Qual foi a média de vendas brutas (Gross Income) registrada a cada mês do ano?')
    resultado = df1.loc[:, ['Mes', 'gross income']].groupby('Mes').mean().sort_values('gross income', ascending=False).reset_index()
    fig, ax = plt.subplots(figsize=(10, 6))

    # 1. Plotar o gráfico de linha
    # O Eixo X é o nome do mês (Nome_Mes) e o Eixo Y é a média de vendas brutas
    ax.plot(
        resultado['Mes'],
        resultado['gross income'],
        marker='o',             # Adiciona círculos nos pontos de dados
        color='#0077B6',        # Cor da linha (azul escuro)
        linestyle='-',          # Tipo de linha (sólida)
        linewidth=2
    )

    # 2. Configurações do Título e Eixos
    ax.set_title('Média de Vendas Brutas (Gross Income) por Mês', fontsize=16, weight='bold')
    ax.set_xlabel('Mês', fontsize=12)
    ax.set_ylabel('Média de Vendas Brutas ($)', fontsize=12)

    # 3. Adicionar uma linha de grade no Eixo Y para facilitar a leitura dos valores
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    # 4. Rotacionar os rótulos do Eixo X se necessário (para evitar sobreposição)
    plt.xticks(rotation=0) # Mantenho a 0 pois os nomes curtos não se sobrepõem

    # 5. Adicionar anotações de texto no ponto mais alto (pico) para destaque (Opcional)
    pico = resultado.loc[resultado['gross income'].idxmax()]
    ax.annotate(
        f'Pico: ${pico["gross income"]:.2f}',
        xy=(pico['Mes'], pico['gross income']),
        xytext=(5, -15), # Deslocamento do texto
        textcoords='offset points',
        arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2", color='red'),
        fontsize=10,
        color='red'
    )

    # 6. Ajustar layout para evitar cortes
    plt.tight_layout()

    # Exibir o gráfico no Streamlit
    st.pyplot(fig)
    st.write(resultado)
    st.markdown('---')  


    st.markdown("Qual é a variação (Desvio Padrão - Standard Deviation) no valor total das vendas (Total) em cada hora do dia?")
    df1['Hour'] = pd.to_datetime(df1['Time'], format='%H:%M:%S').dt.hour
    variacao_por_hora = df1.groupby('Hour')['Total'].std().reset_index(name='Desvio_Padrao_Total')
    variacao_por_hora = variacao_por_hora.sort_values(by='Hour')
    fig, ax = plt.subplots(figsize=(10, 6))

    # 1. Plotar o gráfico de linha
    ax.plot(
        variacao_por_hora['Hour'],
        variacao_por_hora['Desvio_Padrao_Total'],
        marker='o',             # Adiciona círculos nos pontos de dados
        color='darkorange',     # Cor da linha
        linestyle='-',          # Tipo de linha (sólida)
        linewidth=2
    )

    # 2. Configurações do Título e Eixos
    ax.set_title('Variação (Desvio Padrão) das Vendas por Hora do Dia', fontsize=16, weight='bold')
    ax.set_xlabel('Hora do Dia (HH)', fontsize=12)
    ax.set_ylabel('Desvio Padrão do Total de Vendas ($)', fontsize=12)

    # 3. Ajustar os ticks do Eixo X para mostrar apenas as horas inteiras
    ax.set_xticks(variacao_por_hora['Hour'])

    # 4. Adicionar uma linha de grade no Eixo Y para facilitar a leitura dos valores
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    # 5. Adicionar anotações de texto no ponto mais alto (Opcional: Destaque a hora mais volátil)
    pico = variacao_por_hora.loc[variacao_por_hora['Desvio_Padrao_Total'].idxmax()]
    ax.annotate(
        f'Máxima Volatilidade: {pico["Hour"]}h',
        xy=(pico['Hour'], pico['Desvio_Padrao_Total']),
        xytext=(-30, 15), # Deslocamento do texto
        textcoords='offset points',
        arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2", color='red'),
        fontsize=10,
        color='red'
    )

    # 6. Ajustar layout para evitar cortes
    plt.tight_layout()

    # Exibir o gráfico no Streamlit
    st.pyplot(fig)
    st.write(variacao_por_hora)
    st.markdown("---")


    st.markdown('3. Qual é o dia da semana (Day of the Week) que registra o maior número de transações (Moda/Mais Frequente)?')
    resultado = df1.loc[:, ['Dia_Semana', 'Invoice ID']].groupby('Dia_Semana').count().sort_values('Invoice ID', ascending=False).reset_index()
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(resultado['Dia_Semana'], resultado['Invoice ID'], color='lightgreen')
    ax.set_title('Número de Transações por Dia da Semana')
    ax.set_xlabel('Dia da Semana')
    ax.set_ylabel('Número de Transações')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    valor_minimo = resultado['Invoice ID'].min()
    ax.set_ylim(bottom=(valor_minimo-10))
    st.pyplot(fig)
    st.write(resultado)
    st.info('O dia da semana com amior moda é Terça-feira, com 159 registros.')
