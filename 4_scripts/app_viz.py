import streamlit as st
import pandas as pd
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np

st.write("**DADOS DA EMPRESA ESCOLHIDA**")
st.sidebar.header("Trending Tickers neste momento:")

#landing page e seleção
df = pd.read_csv("./1_bases_tratadas/basestratadas.csv", sep=";", encoding="utf-8")
empresas = df["empresas"].drop_duplicates()
empresa_escolhida = st.sidebar.selectbox("Escolha uma empresa", empresas)

df2 = df.loc[df["empresas"] == empresa_escolhida]
st.write(f"Empresa escolhida: {empresa_escolhida}")

#dados da empresa (a esquerda)
col1, col2, col3 = st.columns(3)
col1.metric("Valor atual", value=df2.valor.iloc[0])
col2.metric("Variação ($)", value=df2.change.iloc[0])
col3.metric("Variação (%)", value=df2.change2.iloc[0])

np.random.seed(42)
data = np.random.normal(loc=50, scale=10, size=100)
data = np.append(data, [100, 110, 120, 20, 10])


#graficos do grupo de empresas

#boxplot
media = np.mean(data)
mediana = np.median(data)
desvio_padrao = np.std(data)

df_boxplot = pd.DataFrame({"Valores": data})

fig1, ax1 = plt.subplots(figsize=(8, 6))
sns.boxplot(data=df_boxplot, y="Valores", color="lightblue", width=0.5, ax=ax1)
ax1.axhline(media, color="red", linestyle="--", label=f"Média: {media:.2f}")
ax1.axhline(mediana, color="black", linestyle="-", label=f"Mediana: {mediana:.2f}")
ax1.axhline(
    media + desvio_padrao,
    color="orange",
    linestyle="-.",
    label=f"Média + 1 Desvio Padrão: {media + desvio_padrao:.2f}",
)
ax1.axhline(
    media - desvio_padrao,
    color="purple",
    linestyle="-.",
    label=f"Média - 1 Desvio Padrão: {media - desvio_padrao:.2f}",
)
ax1.legend()
ax1.set_title("Boxplot de TODAS as empresas Trending Tickers, no momento")
ax1.set_ylabel("Valores")
ax1.grid(axis="y", linestyle="--", alpha=0.7)
st.pyplot(fig1)

#grafico barras
faixas = [0.47, 4.814, 9.628, 14.442, 19.256, 24.07]
labels = ["faixa1", "faixa2", "faixa3", "faixa4", "faixa5"]
df["faixa"] = pd.cut(df["change2"], bins=faixas, labels=labels, include_lowest=True)

st.subheader("Gráfico de Barras")
fig2, ax2 = plt.subplots(figsize=(12, 6))
sns.barplot(data=df, x="empresas", y="valor", ax=ax2, palette="viridis")
ax2.set_title("Valor da ação por empresa", fontsize=16)
ax2.set_xlabel("Empresas", fontsize=14)
ax2.set_ylabel("Valores ($)", fontsize=14)
ax2.set_xticklabels(
    ax2.get_xticklabels(), rotation=45, ha="right"
)
st.pyplot(fig2)

#histograma
st.subheader("Histograma")
fig3, ax3 = plt.subplots(figsize=(12, 6))
sns.histplot(
    data=df,
    x="change2",
    hue="faixa",
    multiple="stack",
    palette="viridis",
    kde=False,
    bins=10,
    ax=ax3,
)
ax3.set_title("Histograma: Quantidade de empresas por % de Variação do valor da ação", fontsize=16)
ax3.set_xlabel("Variação (%)", fontsize=14)
ax3.set_ylabel("Frequência (Empresas)", fontsize=14)
ax3.grid(axis="y", linestyle="--", alpha=0.7)
st.pyplot(fig3)

#dispersão
st.subheader("Gráfico de Dispersão")
fig4, ax4 = plt.subplots(figsize=(12, 6))
sns.scatterplot(data=df,
                x="valor",
                y="change",
                hue="empresas",
                style="empresas",
                palette="bright",
                markers=["o", "s", "D"],
                sizes=(20, 200),
                ax=ax4)

# Adicionando título e rótulos
ax4.set_title("Gráfico de Dispersão: Valor x Variação ($)", fontsize=16)
ax4.set_xlabel("Valor ($)", fontsize=14)
ax4.set_ylabel("Variação ($)", fontsize=14)

# Adicionando legenda
plt.legend(title="Empresas")

st.pyplot(fig4)
