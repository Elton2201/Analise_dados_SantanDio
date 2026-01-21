import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuração da Página e Estilo Customizado
st.set_page_config(page_title="Vendas Pro", layout="wide", initial_sidebar_state="expanded")

# No topo do seu arquivo, logo após o st.set_page_config

# Título Principal Centralizado
st.markdown("<h1 style='text-align: center;'>📊 Painel de Performance Comercial</h1>", unsafe_allow_html=True)

# Subtítulo ou descrição centralizada
st.markdown("<p style='text-align: center; color: gray;'>Análise estratégica de faturamento e volume de vendas</p>", unsafe_allow_html=True)

st.markdown("---")

# Se quiser centralizar os títulos das seções mais abaixo:
st.markdown("<h3 style='text-align: center;'>Evolução Mensal</h3>", unsafe_allow_html=True)

# Aplicando um "tema" via CSS para bordas arredondadas e sombras
st.markdown("""
    <style>
    .block-container { padding-top: 2rem; }
    .stMetric { 
        background-color: #000; 
        padding: 20px; 
        border-radius: 15px; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border: 1px solid #f0f2f6;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Barra Lateral (Sidebar) - Limpa a tela principal
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3222/3222672.png", width=80)
    st.title("Configurações")
    arquivo = st.file_uploader("Importar Base de Vendas", type="csv")
    st.info("O sistema processa automaticamente o faturamento com base no arquivo vendas.csv.")

# 3. Tela Principal
if arquivo is not None:
    # Processamento silencioso
    df = pd.read_csv(arquivo)
    df['Faturamento'] = df['preco_unitario'] * df['quantidade_vendida']
    df['data_vendas'] = pd.to_datetime(df['data_vendas'])
    
    st.title("📊 Painel de Performance Comercial")
    
    # KPIs em destaque
    total_faturamento = df['Faturamento'].sum()
    total_itens = df['quantidade_vendida'].sum()
    media_preco = df['preco_unitario'].mean()

    c1, c2, c3 = st.columns(3)
    c1.metric("Faturamento Acumulado", f"R$ {total_faturamento:,.2f}")
    c2.metric("Volume de Itens", f"{total_itens:,}")
    c3.metric("Preço Médio Unitário", f"R$ {media_preco:,.2f}")

    st.markdown("---")

    # Organização em Abas (Tabs) - Melhora muito a interface
    tab_grafico, tab_tabela, tab_analise = st.tabs(["📈 Gráfico Evolutivo", "📂 Tabela de Dados", "📝 Relatório IA"])

    with tab_grafico:
        df_mensal = df.resample('ME', on='data_vendas')['Faturamento'].sum().reset_index()
        df_mensal['Mês'] = df_mensal['data_vendas'].dt.strftime('%b/%Y')
        
        fig = px.area(df_mensal, x='Mês', y='Faturamento', 
                      title='Fluxo de Caixa Mensal',
                      line_shape='spline',
                      color_discrete_sequence=['#007bff'])
        fig.update_layout(margin=dict(l=20, r=20, t=50, b=20), height=400)
        st.plotly_chart(fig, use_container_width=True)

    with tab_tabela:
        st.subheader("Base de Dados Completa")
        st.dataframe(df, use_container_width=True, height=300)

    with tab_analise:
        st.subheader("Conclusões do Sistema")
        # Lógica de comparação (Ex: primeiro vs último mês do CSV)
        df_sorted = df_mensal.sort_values('data_vendas')
        inicial = df_sorted['Faturamento'].iloc[0]
        final = df_sorted['Faturamento'].iloc[-1]
        delta = ((final - inicial) / inicial) * 100

        if delta > 0:
            st.success(f"Crescimento positivo de **{delta:.2f}%** detectado no período.")
        else:
            st.warning(f"Queda de faturamento de **{abs(delta):.2f}%**. Recomenda-se revisão de estoque.")

else:
    # Estado inicial "Vazio" elegante
    st.empty()
    st.markdown("""
        <div style='text-align: center; padding: 100px;'>
            <h2 style='color: #bdc3c7;'>Aguardando carregamento de dados...</h2>
            <p>Utilize a barra lateral para fazer o upload do seu arquivo CSV.</p>
        </div>
        """, unsafe_allow_html=True)