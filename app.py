import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# Configuração da Página
st.set_page_config(page_title="Portal de Indicações", layout="wide")

# Estilo customizado para o fundo e fontes
st.markdown("""
    <style>
    .main { background-color: #F9F9F9; }
    h1 { color: #2C3E50; font-family: 'Segoe UI'; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏆 Ranking de Indicações - Top 10 Clientes")

# Sidebar para Upload de Arquivo
st.sidebar.header("📁 Carregar Dados")
uploaded_file = st.sidebar.file_uploader("Faça upload do arquivo Excel", type=['xlsx', 'xls'])

# Função para carregar e processar dados
def carregar_dados(arquivo):
    try:
        if arquivo is not None:
            df = pd.read_excel(arquivo)
        else:
            # Tenta carregar o arquivo padrão ranking.xlsx
            if os.path.exists("ranking.xlsx"):
                df = pd.read_excel("ranking.xlsx")
            else:
                st.error("❌ Arquivo 'ranking.xlsx' não encontrado. Por favor, faça upload de um arquivo.")
                return None
        
        # Limpeza de dados
        # Remover linhas onde CLIENTE está vazio
        df = df[df['CLIENTE'].notna()]
        df = df[df['CLIENTE'].astype(str).str.strip() != '']
        
        # Converter INDICAÇÕES para numérico e remover valores <= 0
        df['INDICAÇÕES'] = pd.to_numeric(df['INDICAÇÕES'], errors='coerce')
        df = df[df['INDICAÇÕES'] > 0]
        
        return df
    except Exception as e:
        st.error(f"❌ Erro ao carregar arquivo: {str(e)}")
        return None

# Carregar dados
df = carregar_dados(uploaded_file)

if df is not None and len(df) > 0:
    # Ordenar e pegar o Top 10
    df_ranking = df.sort_values(by='INDICAÇÕES', ascending=False).head(10)
    
    # Criar gráfico
    fig, ax = plt.subplots(figsize=(10, 6), facecolor='#F9F9F9')
    ax.set_facecolor('#F9F9F9')
    
    # Cores de Medalha
    cores = []
    for i in range(len(df_ranking)):
        if i == 0: 
            cores.append('#D4AF37')  # Ouro
        elif i == 1: 
            cores.append('#BFC1C2')  # Prata
        elif i == 2: 
            cores.append('#A0522D')  # Bronze
        else: 
            cores.append('#34495E')  # Azul Marinho Corporativo
    
    # Criar barras horizontais
    barras = ax.barh(df_ranking['CLIENTE'], df_ranking['INDICAÇÕES'], color=cores, height=0.7)
    ax.invert_yaxis()
    
    # Remover bordas e eixos
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.get_xaxis().set_visible(False)
    ax.tick_params(left=False)
    
    # Adicionar valores nas barras
    for barra in barras:
        width = barra.get_width()
        ax.text(width + 0.3, barra.get_y() + barra.get_height()/2, 
                f'{int(width)}', va='center', fontweight='bold', fontsize=11)
    
    # Layout do Site - Métricas e Gráfico
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.metric("📊 Total de Indicações", int(df['INDICAÇÕES'].sum()))
    
    with col2:
        lider = df_ranking.iloc[0]['CLIENTE']
        st.metric("👑 Líder do Ranking", lider)
    
    st.markdown("---")
    
    # Exibir gráfico
    st.pyplot(fig)
    
    # Mostrar tabela de dados (opcional)
    with st.expander("📋 Ver Dados Completos do Top 10"):
        st.dataframe(df_ranking.reset_index(drop=True), use_container_width=True)
    
else:
    st.warning("⚠️ Nenhum dado válido encontrado. Por favor, carregue um arquivo Excel com as colunas 'CLIENTE' e 'INDICAÇÕES'.")
    
    # Mostrar exemplo de formato esperado
    st.info("""
    **Formato esperado do arquivo Excel:**
    
    | CLIENTE | INDICAÇÕES |
    |---------|-----------|
    | João Silva | 15 |
    | Maria Santos | 12 |
    | Pedro Costa | 8 |
    """)