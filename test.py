import os
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import google.generativeai as genai

# Configuración de la API de Gemini
genai.configure(api_key="AIzaSyDEWIWq8mTVKxsox1JQriLPFeCf_3Id_S0")
model = genai.GenerativeModel("gemini-2.5-flash")

# --------- Funciones ---------
def extract_text_from_url(url):
    headers = {
        'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                       'AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/58.0.3029.110 Safari/537.3')
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        text = ' '.join([p.get_text() for p in paragraphs])
        cleaned_text = re.sub(r'\[.*?\]', '', text)
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
        return cleaned_text
    except Exception as e:
        print(f"❌ Error al acceder a {url}: {e}")
        return None

def process_row(index, url, doc):
    """Procesa una fila de forma secuencial"""
    full_text = extract_text_from_url(url)
    if not full_text:
        print(f"Fila {index}: ❌ No se pudo extraer texto de {url}")
        return

    try:
        summary = model.generate_content(
            f"Escribe un resumen breve del siguiente texto. "
            f"Devuélvelo solo como texto corrido, sin títulos ni explicaciones:\n\n{full_text[:15000]}"
        )

        # Guardar resultados en el mismo DataFrame
        doc.at[index, "Resumen"] = summary.text.strip()

        print(f"✅ Fila {index} procesada correctamente")

    except Exception as e:
        print(f"⚠️ Error en Gemini para {url}: {e}")

# --------- Programa principal ---------
if __name__ == "__main__":
    # Cargar CSV original
    csv_path = r"Laika V1.csv"
    doc = pd.read_csv(csv_path)

    # Definir desde qué fila arrancar
    start_row = 512   # 👈 cámbialo al número que quieras

    # Procesar desde esa fila en adelante
    for index, row in doc.iloc[start_row:].iterrows():
        url = row.get("Link")
        process_row(index, url, doc)

        # Guardar en el mismo archivo original
        doc.to_csv(csv_path, index=False)

    print(f"✅ Proceso completado desde la fila {start_row} en adelante. Resultados guardados en el mismo CSV")
