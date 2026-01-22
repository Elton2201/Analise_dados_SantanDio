import streamlit as st
import pandas as pd
import plotly.express as px
import io

# 1. Configuração da Página
st.set_page_config(page_title="Vendas Pro", layout="wide")

# CSS para Estilo
st.markdown("""
    <style>
    .stMetric { background-color: #000; padding: 20px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); border: 1px solid #f0f2f6; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÃO PARA CARREGAR O CSV REAL DO SEU ANEXO ---
def obter_dados_exemplo():
    return pd.read_csv("vendas.csv")

# 2. Barra Lateral (Sidebar)
with st.sidebar:

    st.markdown("<h1 style='text-align: center;'>📦</h1>", unsafe_allow_html=True)
    st.title("Configurações")
    
    # ... resto do código
    
    st.subheader("1. Seus Dados")
    arquivo_upload = st.file_uploader("Suba seu arquivo CSV ou Excel", type=["csv", "xlsx"])
    
    st.markdown("---")
    
    st.subheader("2. Dados de Teste")
    usar_exemplo = st.checkbox("Usar dados de exemplo (vendas.csv)", help="Marque esta opção para testar o dashboard sem subir um arquivo.")
    
    # Botão de download caso ele queira ver como é o arquivo
    dados_download = obter_dados_exemplo().to_csv(index=False).encode('utf-8')
    st.download_button("📥 Baixar Planilha de Exemplo", data=dados_download, file_name="exemplo_vendas.csv", mime="text/csv")

# 3. Lógica de Decisão de Dados
df = None

if arquivo_upload is not None:
    # Se ele subiu um arquivo, damos prioridade total a ele
    if arquivo_upload.name.endswith('.csv'):
        df = pd.read_csv(arquivo_upload)
    else:
        df = pd.read_excel(arquivo_upload)
    st.success("✅ Usando seus dados enviados!")

elif usar_exemplo:
    # Se ele marcou a caixinha de exemplo
    try:
        df = obter_dados_exemplo()
        st.info("💡 Usando dados de exemplo para demonstração.")
    except:
        st.error("Erro: O arquivo 'vendas.csv' não foi encontrado no servidor.")

# 4. Exibição do Dashboard (Só acontece se houver um DF carregado)
if df is not None:
    # Título Centralizado
    st.markdown("<h1 style='text-align: center;'>📊 Painel de Performance Comercial</h1>", unsafe_allow_html=True)
    
    # Processamento
    df['Faturamento'] = df['preco_unitario'] * df['quantidade_vendida']
    df['data_vendas'] = pd.to_datetime(df['data_vendas'])
    
    # KPIs
    c1, c2, c3 = st.columns(3)
    c1.metric("Faturamento Total", f"R$ {df['Faturamento'].sum():,.2f}")
    c2.metric("Qtd Vendida", f"{df['quantidade_vendida'].sum():,}")
    c3.metric("Ticket Médio", f"R$ {df['preco_unitario'].mean():,.2f}")

    # Abas
    tab1, tab2 = st.tabs(["📈 Gráficos", "📂 Tabela"])
    
    with tab1:
        df_mensal = df.resample('ME', on='data_vendas')['Faturamento'].sum().reset_index()
        df_mensal['Mês'] = df_mensal['data_vendas'].dt.strftime('%b/%Y')
        fig = px.area(df_mensal, x='Mês', y='Faturamento', title="Evolução Mensal", line_shape='spline')
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.dataframe(df, use_container_width=True)

else:
    # Tela de espera caso nada tenha sido selecionado
    st.markdown("<h1 style='text-align: center;'>Bem-vindo ao Vendas Pro</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Escolha uma opção na barra lateral para começar.</p>", unsafe_allow_html=True)
    

