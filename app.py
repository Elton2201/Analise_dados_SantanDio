import streamlit as st
import pandas as pd
import plotly.express as px
import io

# 1. Configuração da Página e Estilo Customizado
st.set_page_config(page_title="Vendas Pro", layout="wide", initial_sidebar_state="expanded")

# Aplicando CSS para bordas, sombras e centralização
st.markdown("""
    <style>
    .block-container { padding-top: 2rem; }
    .stMetric { 
        background-color: #ffffff; 
        padding: 20px; 
        border-radius: 15px; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border: 1px solid #f0f2f6;
    }
    [data-testid="stMetricValue"] { color: #1f77b4; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÃO PARA CRIAR O MODELO CSV ---
def criar_csv_modelo():
    # Colunas exatas que o seu código processa
    colunas = ['data_vendas', 'produto', 'categoria', 'preco_unitario', 'quantidade_vendida']
    df_modelo = pd.DataFrame(columns=colunas)
    
    # Gerar arquivo em memória
    output = io.StringIO()
    df_modelo.to_csv(output, index=False)
    return output.getvalue()

# 2. Barra Lateral (Sidebar)
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3222/3222672.png", width=80)
    st.title("Configurações")
    
    # Botão de Download do Modelo (Inserido aqui)
    csv_modelo = criar_csv_modelo()
    st.download_button(
        label="📥 Baixar Modelo CSV",
        data=csv_modelo,
        file_name="modelo_vendas.csv",
        mime="text/csv",
        help="Baixe este modelo para garantir que as colunas estejam corretas."
    )
    
    st.markdown("---")
    
    # Upload do arquivo (aceitando CSV e Excel para facilitar no celular)
    arquivo = st.file_uploader("Importar Base de Vendas", type=["csv", "xlsx"])
    st.info("O sistema calcula o faturamento automaticamente multiplicando Preço x Quantidade.")

# 3. Tela Principal - Cabeçalho Centralizado
st.markdown("<h1 style='text-align: center;'>📊 Painel de Performance Comercial</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Análise estratégica de faturamento e volume de vendas</p>", unsafe_allow_html=True)
st.markdown("---")

# Lógica de Exibição
if arquivo is not None:
    # Processamento dos Dados
    try:
        if arquivo.name.endswith('.csv'):
            df = pd.read_csv(arquivo)
        else:
            df = pd.read_excel(arquivo)

        # Criação da coluna Faturamento (A mágica do Pandas)
        df['Faturamento'] = df['preco_unitario'] * df['quantidade_vendida']
        df['data_vendas'] = pd.to_datetime(df['data_vendas'])
        
        # KPIs em destaque
        total_faturamento = df['Faturamento'].sum()
        total_itens = df['quantidade_vendida'].sum()
        media_preco = df['preco_unitario'].mean()

        c1, c2, c3 = st.columns(3)
        c1.metric("Faturamento Acumulado", f"R$ {total_faturamento:,.2f}")
        c2.metric("Volume de Itens", f"{total_itens:,}")
        c3.metric("Preço Médio Unitário", f"R$ {media_preco:,.2f}")

        st.markdown("<br>", unsafe_allow_html=True)

        # Organização em Abas
        tab_grafico, tab_tabela, tab_analise = st.tabs(["📈 Gráfico Evolutivo", "📂 Tabela de Dados", "📝 Relatório IA"])

        with tab_grafico:
            st.markdown("<h3 style='text-align: center;'>Evolução Mensal de Receita</h3>", unsafe_allow_html=True)
            df_mensal = df.resample('ME', on='data_vendas')['Faturamento'].sum().reset_index()
            df_mensal['Mês'] = df_mensal['data_vendas'].dt.strftime('%b/%Y')
            
            fig = px.area(df_mensal, x='Mês', y='Faturamento', 
                          line_shape='spline',
                          color_discrete_sequence=['#007bff'])
            fig.update_layout(margin=dict(l=20, r=20, t=30, b=20), height=400)
            st.plotly_chart(fig, use_container_width=True)

        with tab_tabela:
            st.subheader("Base de Dados com Faturamento Calculado")
            st.dataframe(df, use_container_width=True, height=400)

        with tab_analise:
            st.subheader("Análise Automática")
            df_sorted = df_mensal.sort_values('data_vendas')
            if len(df_sorted) > 1:
                inicial = df_sorted['Faturamento'].iloc[0]
                final = df_sorted['Faturamento'].iloc[-1]
                delta = ((final - inicial) / inicial) * 100

                if delta > 0:
                    st.success(f"Crescimento positivo de **{delta:.2f}%** detectado no período.")
                else:
                    st.warning(f"Queda de faturamento de **{abs(delta):.2f}%**. Verifique o estoque.")
            else:
                st.info("Dados insuficientes para calcular tendência (necessário mais de 1 mês).")

    except Exception as e:
        st.error(f"Erro ao processar arquivo: Verifique se as colunas estão iguais ao modelo. Detalhe: {e}")

else:
    # Estado inicial centralizado
    st.markdown("""
        <div style='text-align: center; padding: 50px;'>
            <h2 style='color: #bdc3c7;'>Aguardando carregamento de dados...</h2>
            <p>Baixe o modelo na barra lateral e faça o upload para visualizar os gráficos.</p>
        </div>
        """, unsafe_allow_html=True)
