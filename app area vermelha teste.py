import streamlit as st
import pandas as pd

# ==============================
# CONFIGURAÇÃO DA PÁGINA
# ==============================
st.set_page_config(
    page_title="Sistema de Tags",
    layout="wide"
)

# ==============================
# LOGIN SIMPLES
# ==============================
USUARIO = "admin"
SENHA = "123456789"

if "logado" not in st.session_state:
    st.session_state.logado = False

def tela_login():
    st.title("🔐 Login do Sistema APP ARÉA VERMELHA")

    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        if usuario == USUARIO and senha == SENHA:
            st.session_state.logado = True
            st.rerun()
        else:
            st.error("Usuário ou senha incorretos")

if not st.session_state.logado:
    tela_login()
    st.stop()

# ==============================
# LINK GOOGLE SHEETS CSV
# ==============================
url = "https://docs.google.com/spreadsheets/d/1Ph9SQ1gjeUdQYeUqAq2xIaxaBtuMQxyqtAYtVI2530c/export?format=csv&gid=0"

# ==============================
# CARREGAR DADOS
# ==============================
@st.cache_data(ttl=60)
def carregar():
    df = pd.read_csv(url)
    df.columns = df.columns.str.upper()
    return df

df = carregar()

# ==============================
# INTERFACE PRINCIPAL
# ==============================
st.title("📊 Sistema de Pesquisa de Tags")

col1, col2 = st.columns(2)

with col1:
    busca_tag = st.text_input("🔎 Pesquisar por TAG")

with col2:
    busca_local = st.text_input("📍 Pesquisar por LOCAL")

# ==============================
# FILTROS AUTOMÁTICOS
# ==============================
resultado = df.copy()

if busca_tag:
    resultado = resultado[resultado["TAG"].astype(str).str.contains(busca_tag, case=False)]

if busca_local:
    resultado = resultado[resultado["LOC."].astype(str).str.contains(busca_local, case=False)]

# ==============================
# RESULTADO PRINCIPAL
# ==============================
st.subheader("Resultados")

if resultado.empty:
    st.warning("Nenhum resultado encontrado")
else:
    st.dataframe(resultado, use_container_width=True)

# ==============================
# DETALHE DE UMA TAG
# ==============================
st.subheader("Consulta rápida")

tag_escolhida = st.selectbox(
    "Selecionar TAG",
    [""] + list(df["TAG"].dropna().unique())
)

if tag_escolhida:
    linha = df[df["TAG"] == tag_escolhida].iloc[0]

    st.success(f"""
    LOCAL: {linha["LOC."]}
    ÁREA: {linha["AREA"]}
    """)

# ==============================
# LOGOUT
# ==============================
if st.button("Sair"):
    st.session_state.logado = False

    st.rerun()
