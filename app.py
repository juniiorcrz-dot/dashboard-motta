import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.title("📊 Dashboard MOTTA - Quebra de Peso")

arquivo = st.file_uploader("📂 Carregar Base Excel", type=["xlsx"])

if arquivo:
    df = pd.read_excel(arquivo)
    st.write(df.columns)

    # Normalizar nomes (caso venham diferentes)
    df.columns = df.columns.str.strip().str.lower()

    # KPIs
    st.subheader("Indicadores")
    c1, c2, c3, c4 = st.columns(4)

    # Corrigir nomes de colunas
df.columns = df.columns.str.strip().str.lower()

# Funções seguras
def safe_sum(df, col):
    if col in df.columns:
        return df[col].sum()
    return 0

def safe_mean(df, col):
    if col in df.columns:
        return df[col].mean()
    return 0

# KPIs
c1.metric("Cabeças", int(safe_sum(df, "cabecas")))
c2.metric("Peso Compra", round(safe_mean(df, "peso_compra"),1))
c3.metric("Peso Chegada", round(safe_mean(df, "peso_chegada"),1))
c4.metric("Peso Balancinha", round(safe_mean(df, "peso_balancinha"),1))

    # Cálculos (só se as colunas existirem)
    if all(col in df.columns for col in ["peso_compra","peso_chegada","km"]):
        df["quebra_kg"] = df["peso_chegada"] - df["peso_compra"]
        df["quebra_%"] = (df["quebra_kg"] / df["peso_compra"]) * 100
        df["kg_100km"] = df["quebra_kg"] / df["km"] * 100

        st.metric("Kg / 100km", f"{df['kg_100km'].mean():.2f}")

        # Gráfico por unidade (se existir)
        if "unidade" in df.columns:
            st.subheader("Comparativo por Unidade")
            fig = px.bar(df, x="unidade", y="quebra_kg", color="unidade")
            st.plotly_chart(fig, use_container_width=True)

        # Ranking compradores (se existir)
        if "comprador" in df.columns:
            st.subheader("Ranking Compradores")
            ranking = df.groupby("comprador")["kg_100km"].mean().sort_values()
            st.dataframe(ranking)

    st.subheader("Base Completa")
    st.dataframe(df)

else:
    st.info("Faça upload do Excel para visualizar o dashboard")
