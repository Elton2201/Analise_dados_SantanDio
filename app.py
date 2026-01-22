import streamlit as st
import pandas as pd
import plotly.express as px
import io
import os

# 1. Configuração da Página
st.set_page_config(page_title="Vendas Pro", layout="wide")

# Estilo CSS para os Cards de Métricas e Layout
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

# --- FUNÇÃO PARA CARREGAR DADOS DE EXEMPLO (Segura contra erros) ---
def obter_dados_exemplo():
    caminho_arquivo = "vendas.csv"
    if os.path.exists(caminho_arquivo):
        return pd.read_csv(caminho_arquivo)
    return None

# 2. Barra Lateral (Sidebar)
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3222/3222672.png", width=80)
    st.title("Configurações")
    
    st.subheader("1. Seus Dados")
    arquivo_upload = st.file_uploader("Suba seu arquivo CSV ou Excel", type=["csv", "xlsx"])
    
    st.markdown("---")
    
    st.subheader("2. Dados de Teste")
    df_exemplo_base = obter_dados_exemplo()
    
    usar_exemplo = False
    if df_exemplo_base is not None:
        usar_exemplo = st.checkbox("Usar dados de exemplo (vendas.csv)", help="Ativa os dados reais do anexo.")
        
        # Botão para baixar o arquivo real que está no sistema
        dados_csv = df_exemplo_base.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Baixar Planilha de Exemplo", 
                           data=dados_csv, 
                           file_name="exemplo_vendas.csv", 
                           mime="text/csv")
    else:
        st.warning("Arquivo 'vendas.csv' não encontrado no GitHub.")

# 3. Lógica de Carregamento de Dados
df = None

if arquivo_upload is not None:
    try:
        if arquivo_upload.name.endswith('.csv'):
            df = pd.read_csv(arquivo_upload)
        else:
            df = pd.read_excel(arquivo_upload)
    except Exception as e:
        st.error(f"Erro ao processar arquivo: {e}")
elif usar_exemplo:
    df = df_exemplo_base

# 4. Exibição do Dashboard
if df is not None:
    # Cabeçalho Centralizado
    st.markdown("<h1 style='text-align: center;'>📊 Painel de Performance Comercial</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Validação automática de inventário e tendências</p>", unsafe_allow_html=True)
    st.markdown("---")

    # Processamento de Dados
    df['Faturamento'] = df['preco_unitario'] * df['quantidade_vendida']
    df['data_vendas'] = pd.to_datetime(df['data_vendas'])
    
    # KPIs principais
    c1, c2, c3 = st.columns(3)
    c1.metric("Faturamento Total", f"R$ {df['Faturamento'].sum():,.2f}")
    c2.metric("Qtd Vendida", f"{df['quantidade_vendida'].sum():,}")
    c3.metric("Ticket Médio", f"R$ {df['preco_unitario'].mean():,.2f}")

    st.markdown("<br>", unsafe_allow_html=True)

    # Organização em Abas
    tab_grafico, tab_tabela, tab_analise = st.tabs(["📈 Gráficos", "📂 Tabela", "📝 Relatório IA"])

    with tab_grafico:
        st.markdown("<h3 style='text-align: center;'>Evolução Mensal</h3>", unsafe_allow_html=True)
        df_mensal = df.resample('ME', on='data_vendas')['Faturamento'].sum().reset_index()
        df_mensal['Mês'] = df_mensal['data_vendas'].dt.strftime('%b/%Y')
        fig = px.area(df_mensal, x='Mês', y='Faturamento', line_shape='spline', color_discrete_sequence=['#007bff'])
        st.plotly_chart(fig, use_container_width=True)

    with tab_tabela:
        st.dataframe(df, use_container_width=True)

    with tab_analise:
        st.markdown("### 🤖 Insights e Validações da I.A.")
        
        # Validação 1: Tendência Comercial
        df_mensal_calc = df.resample('ME', on='data_vendas')['Faturamento'].sum().reset_index()
        if len(df_mensal_calc) > 1:
            v_inicial = df_mensal_calc['Faturamento'].iloc[0]
            v_final = df_mensal_calc['Faturamento'].iloc[-1]
            var = ((v_final - v_inicial) / v_inicial) * 100
            if var > 0:
                st.success(f"📈 **Crescimento:** O faturamento subiu **{var:.2f}%** no período analisado.")
            else:
                st.warning(f"📉 **Atenção:** Houve uma retração de **{abs(var):.2f}%** nas vendas.")

        # Validação 2: Estoque Crítico (Baseado no seu vendas.csv)
        if 'estoque' in df.columns:
            itens_baixos = df[df['estoque'] <= 5][['produto', 'estoque']].drop_duplicates()
            if not itens_baixos.empty:
                st.error("🚨 **Validação de Estoque:** Itens abaixo do nível de segurança (5 unid):")
                st.table(itens_baixos)
            else:
                st.info("✅ **Estoque:** Todos os itens possuem níveis de segurança adequados.")

        # Validação 3: Produto Estrela
        top_prod = df.groupby('produto')['Faturamento'].sum().idxmax()
        st.write(f"🏆 **Produto Destaque:** O item que mais gera receita é: **{top_prod}**.")

else:
    # Tela Inicial quando não há dados
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center;'>Bem-vindo ao Vendas Pro</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Escolha uma opção na barra lateral: suba seu arquivo ou use nossos dados de exemplo.</p>", unsafe_allow_html=True)
    st.image("https://cdn.dribbble.com/users/1238709/screenshots/5835438/media/765089776ec015949d8e7894a4805f15.gif", width=400)
