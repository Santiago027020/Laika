import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
import nltk

# Descargar stopwords (solo la primera vez)
nltk.download("stopwords")

# Cargar lista de stopwords en español
spanish_stopwords = stopwords.words("spanish")

# Ahora sí, usar la lista
vectorizer = TfidfVectorizer(stop_words=spanish_stopwords)

try:
    from rapidfuzz import fuzz
    _HAS_RAPIDFUZZ = True
except ImportError:
    _HAS_RAPIDFUZZ = False


def normalize_text(s: str) -> str:
    return str(s).lower().strip() if s is not None else ""

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
import nltk

# Descargar stopwords si no están
nltk.download("stopwords")
spanish_stopwords = stopwords.words("spanish")

def buscador_avanzado(ruta_archivo, query, top_n=10):
    # Cargar archivo (Excel o CSV)
    if ruta_archivo.endswith(".xlsx"):
        df = pd.read_excel(ruta_archivo)
    else:
        df = pd.read_csv(ruta_archivo)
    
    # Combinar columnas relevantes
    df["combined"] = (
        df["Title"].astype(str) + " " +
        df["Keywords"].astype(str) + " " +
        df["Resumen"].astype(str)
    )

    # Vectorizar texto
    vectorizer = TfidfVectorizer(stop_words=spanish_stopwords)
    X = vectorizer.fit_transform(df["combined"])

    # Vectorizar consulta
    q_vec = vectorizer.transform([query])

    # Similaridad coseno
    similitudes = cosine_similarity(q_vec, X).flatten()

    # Top N resultados
    mejores_idx = similitudes.argsort()[::-1][:top_n]
    resultados = df.iloc[mejores_idx].copy()
    resultados["score"] = similitudes[mejores_idx]

    return resultados[["Title", "Link", "Keywords", "Resumen", "Importancia", "score"]]

if __name__ == "__main__":
    archivo = "Laika V1.csv"  # cambia si es .csv
    query = input("Ingrese término de búsqueda: ")
    resultados = buscador_avanzado(archivo, query, top_n=10)

    if resultados.empty:
        print("No se encontraron coincidencias.")
    else:
        print(resultados.to_string(index=False))