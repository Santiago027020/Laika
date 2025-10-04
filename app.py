import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
import nltk
from flask import Flask, render_template, request
import networkx as nx
from pyvis.network import Network
import os

# Descargar stopwords (solo la primera vez)
nltk.download("stopwords")
spanish_stopwords = stopwords.words("spanish")

app = Flask(__name__)

# ---------- Función de búsqueda ----------
def buscador_avanzado(ruta_archivo, query, top_n=10):
    if ruta_archivo.endswith(".xlsx"):
        df = pd.read_excel(ruta_archivo)
    else:
        df = pd.read_csv(ruta_archivo)
    
    # Texto combinado
    df["combined"] = (
        df["Title"].astype(str) + " " +
        df["Keywords"].astype(str) + " " +
        df["Resumen"].astype(str)
    )

    # Vectorización TF-IDF
    vectorizer = TfidfVectorizer(stop_words=spanish_stopwords)
    X = vectorizer.fit_transform(df["combined"])

    # Similitud coseno con la query
    q_vec = vectorizer.transform([query])
    similitudes = cosine_similarity(q_vec, X).flatten()

    # Mejores resultados
    mejores_idx = similitudes.argsort()[::-1][:top_n]
    resultados = df.iloc[mejores_idx].copy()
    resultados["score"] = similitudes[mejores_idx]
    resultados = resultados.sort_values(by=["Importancia", "score"], ascending=[False, False])


    return resultados[["Title", "Link", "Keywords", "Resumen", "Importancia", "score"]]


def generar_grafo_conocimiento(df_resultados):
    from pyvis.network import Network

    net = Network(height="600px", width="100%", bgcolor="#f8f9fa", font_color="black")
    net.barnes_hut()

    for _, row in df_resultados.iterrows():
        net.add_node(row["Title"], label=row["Title"], title=row["Resumen"], color="lightblue")
        for kw in str(row["Keywords"]).split(","):
            kw = kw.strip()
            if kw:
                net.add_node(kw, label=kw, color="lightgreen")
                net.add_edge(row["Title"], kw)

    grafo_path = "static/grafo.html"
    net.write_html(grafo_path)
    return grafo_path


# ---------- Ruta principal ----------
@app.route("/", methods=["GET", "POST"])
def index():
    resultados = []
    query = ""
    grafo_url = None
    if request.method == "POST":
        query = request.form.get("query")
        if query:
            df_resultados = buscador_avanzado("Laika V1.csv", query, top_n=10)
            resultados = df_resultados.to_dict(orient="records")
            grafo_url = generar_grafo_conocimiento(df_resultados)
    return render_template("index.html", resultados=resultados, query=query, grafo_url=grafo_url)
if __name__ == "__main__":
    app.run(debug=True)
