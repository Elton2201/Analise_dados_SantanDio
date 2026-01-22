import streamlit as st
import pandas as pd
import plotly.express as px
import io
import os

# 1. Configuração da Página
st.set_page_config(page_title="Vendas Pro", page_icon="📊", layout="wide")

# Estilo CSS para os Cards
st.markdown("""
    <style>
    .stMetric { 
        background-color: #ffffff; 
        padding: 20px; 
        border-radius: 15px; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.1); 
        border: 1px solid #f0f2f6; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÃO PARA CARREGAR DADOS DE EXEMPLO ---
def obter_dados_exemplo():
    caminho = "vendas.csv"
    if os.path.exists(caminho):
        return pd.read_csv(caminho)
    return None

# 2. Barra Lateral (Sidebar)
with st.sidebar:
    # Ícone Estável (Dashboard Icon)
    st.image("https://cdn-icons-png.flaticon.com/512/1162/1162456.png", width=80)
    st.title("Configurações")
    
    st.subheader("1. Seus Dados")
    arquivo_upload = st.file_uploader("Suba seu arquivo CSV ou Excel", type=["csv", "xlsx"])
    
    st.markdown("---")
    
    st.subheader("2. Dados de Teste")
    df_exemplo_base = obter_dados_exemplo()
    
    usar_exemplo = False
    if df_exemplo_base is not None:
        usar_exemplo = st.checkbox("Usar dados de exemplo (vendas.csv)")
        
        dados_csv = df_exemplo_base.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Baixar Planilha de Exemplo", 
                           data=dados_csv, 
                           file_name="exemplo_vendas.csv", 
                           mime="text/csv")
    else:
        st.warning("Arquivo 'vendas.csv' não encontrado no repositório.")

# 3. Lógica de Carregamento
df = None
if arquivo_upload is not None:
    try:
        if arquivo_upload.name.endswith('.csv'):
            df = pd.read_csv(arquivo_upload)
        else:
            df = pd.read_excel(arquivo_upload)
    except Exception as e:
        st.error(f"Erro: {e}")
elif usar_exemplo:
    df = df_exemplo_base

# 4. Exibição do Dashboard (AQUI ESTÁ A I.A.)
if df is not None:
    # Títulos
    st.markdown("<h1 style='text-align: center;'>📊 Painel de Performance Comercial</h1>", unsafe_allow_html=True)
    st.markdown("---")

    # Processamento
    df['Faturamento'] = df['preco_unitario'] * df['quantidade_vendida']
    df['data_vendas'] = pd.to_datetime(df['data_vendas'])
    
    # KPIs
    c1, c2, c3 = st.columns(3)
    c1.metric("Faturamento Total", f"R$ {df['Faturamento'].sum():,.2f}")
    c2.metric("Qtd Vendida", f"{df['quantidade_vendida'].sum():,}")
    c3.metric("Ticket Médio", f"R$ {df['preco_unitario'].mean():,.2f}")

    # CRIANDO AS ABAS (IMPORTANTE: A terceira aba é a IA)
    tab_grafico, tab_tabela, tab_ia = st.tabs(["📈 Gráficos", "📂 Tabela de Dados", "🤖 Relatório IA"])

    with tab_grafico:
        df_mensal = df.resample('ME', on='data_vendas')['Faturamento'].sum().reset_index()
        df_mensal['Mês'] = df_mensal['data_vendas'].dt.strftime('%b/%Y')
        fig = px.area(df_mensal, x='Mês', y='Faturamento', title="Evolução Mensal de Receita", line_shape='spline')
        st.plotly_chart(fig, use_container_width=True)

    with tab_tabela:
        st.subheader("Base de Dados Visual")
        st.dataframe(df, use_container_width=True)

    with tab_ia:
        st.markdown("### 🤖 Validação e Análise da I.A.")
        
        # Análise 1: Estoque (Baseado no seu arquivo vendas.csv)
        if 'estoque' in df.columns:
            criticos = df[df['estoque'] <= 5][['produto', 'estoque']].drop_duplicates()
            if not criticos.empty:
                st.error("🚨 **Alerta de Reposição:** Encontramos produtos com estoque crítico!")
                st.table(criticos)
            else:
                st.info("✅ **Saúde do Estoque:** Todos os itens estão com bons níveis.")

        # Análise 2: Performance
        df_mensal_ia = df.resample('ME', on='data_vendas')['Faturamento'].sum().reset_index()
        if len(df_mensal_ia) > 1:
            var = ((df_mensal_ia['Faturamento'].iloc[-1] - df_mensal_ia['Faturamento'].iloc[0]) / df_mensal_ia['Faturamento'].iloc[0]) * 100
            if var > 0:
                st.success(f"📈 **Tendência:** O faturamento cresceu **{var:.2f}%** no período.")
            else:
                st.warning(f"📉 **Tendência:** Queda de **{abs(var):.2f}%** no faturamento.")

        # Análise 3: Produto campeão
        campeao = df.groupby('produto')['Faturamento'].sum().idxmax()
        st.write(f"🏆 **Insight:** O produto **{campeao}** é o seu maior gerador de caixa.")

else:
    # Tela Inicial
    st.markdown("<div style='text-align: center; padding: 50px;'><h2>Aguardando Dados...</h2><p>Suba um arquivo ou use os dados de teste na lateral.</p></div>", unsafe_allow_html=True)
