
# LAIKA: Motor de Búsqueda Inteligente para Biociencia Espacial

## Resumen del Proyecto

LAIKA es una plataforma de **Análisis de Conocimiento de Biología Espacial** impulsada por **Inteligencia Artificial**. Nuestro objetivo es transformar *datasets* masivos y desestructurados (como CSVs de publicaciones científicas) en **Inteligencia Accionable**, permitiendo a la comunidad científica y planificadores de misión priorizar el contenido que tiene el **mayor impacto científico y temático** de forma inmediata.

Hemos convertido la IA en un **Analista de Conocimiento Experto**, no en un generador de texto.

### Propuesta de Valor

| **Para la Investigación y Misiones** | **Para la Arquitectura de IA** | **Para la Misión (Global / Paraguay)** |
| :--- | :--- | :--- |
| **Acelera el Descubrimiento:** Prioriza los documentos que la IA califica como de mayor impacto. | **Uso Avanzado del LLM:** El modelo se usa como un módulo de inferencia para generar datos estructurados (prioridad temática). | **Inspiración Global:** Demuestra que la innovación técnica y el desarrollo de IA se hacen desde Paraguay. |
| **Optimiza Decisiones:** Reduce el tiempo de filtrado manual de miles de *papers* para planificadores de misiones. | **Resiliencia de Flujo:** Estrategia para mitigar las limitaciones de *throughput* de la API mediante el **CSV como caché dinámico**. | Fomenta la **curiosidad científica** y la participación en la exploración espacial en comunidades subrepresentadas. |

## Innovación Técnica y Algoritmos

El corazón de LAIKA es un sistema de procesamiento de lenguaje natural y una arquitectura de clasificación única:

### 1\. Inferencia Dirigida con Gemini (El "Analista de Conocimiento")

Utilizamos la **Gemini 2.5 Flash API** bajo el rol explícito de **"Knowledge Analyst"**.

  * **Función:** Generar **tres artefactos de conocimiento** por documento: **Resúmenes Abstractivos**, **Palabras Clave Paramétricas** y el **Índice de Relevancia Temática** (la métrica de importancia).

  * **Eficiencia:** El procesamiento es **secuencial** y resiliente (usando `start_row`), y los resultados se **reinyectan** al CSV original. Esto convierte el CSV en la **Base de Conocimiento Enriquecida** y resuelve las limitaciones de *throughput* de la API en tiempo de ejecución.

### 2\. Algoritmo de Doble Jerarquización (Priorización por Impacto)

El motor de búsqueda (desarrollado en Python con `sklearn`) va más allá de un simple *keyword search*.

  * **Paso 1: Afinidad Semántica:** Utilizamos **TF-IDF** y **Similitud Coseno** para calcular qué tan cerca está la *query* del significado real del documento (`score`).

  * **Paso 2: Prioridad Estratégica:** Los resultados se ordenan en dos fases cruciales:

    ```
    # Ordena: 1° por la importancia asignada por la IA, 2° por la afinidad semántica.
    resultados = resultados.sort_values(by=["Importancia", "score"], ascending=[False, False])


    ```

    **Resultado:** La plataforma siempre muestra primero los temas de **mayor impacto científico**, independientemente de las coincidencias superficiales.

### 3\. Despliegue Dinámico y Visualización

La aplicación **Flask** consume este CSV enriquecido para **generar la web dinámicamente** (`thelaika.earth`) y crear un **Grafo de Conocimiento** (usando Pyvis/NetworkX) en el instante de la consulta, ofreciendo una vista de alto nivel sobre las sinergias temáticas.

## Demo y Despliegue

  * **Plataforma Operativa:** [https://thelaika.earth](https://thelaika.earth)

  * **Estructura del Repositorio:**

      * `filter.py`: Contiene la lógica de scraping y la inferencia dirigida a la Gemini API.

      * `app.py`: El servidor Flask que aloja el **Motor de Búsqueda Jerárquico** y el *renderer* dinámico.

## Configuración y Ejecución Local

1.  **Clonar Repositorio:**

    ```
    git clone [https://github.com/Santiago027020/Laika.git](https://github.com/Santiago027020/Laika.git)
    cd Laika


    ```

2.  **Instalar Dependencias:**

    ```
    pip install pandas requests beautifulsoup4 scikit-learn nltk flask networkx pyvis google-genai


    ```

3.  **Configurar API Key:**

      * Crea una cuenta en Google AI Studio para obtener tu clave de Gemini API.

      * Añádela a tu entorno (`export GEMINI_API_KEY="..."`) o reemplaza la *placeholder* en el script `etl_processor.py`:

    <!-- end list -->

    ```
    # Configuración de la API de Gemini
    # REEMPLAZAR con su clave de API
    genai.configure(api_key="TU_CLAVE_AQUI") 


    ```

4.  **Ejecutar la Plataforma:**

    ```
    python app.py


    ```

    (Accede a `http://127.0.0.1:5000` en tu navegador.)

## La Misión de LAIKA

Este proyecto es la prueba de que el ingenio técnico no tiene fronteras. LAIKA busca ser el catalizador para que la juventud de Paraguay se involucre en la biología y exploración espacial. Nuestra IA no solo procesa datos; está diseñada para **inspirar, acelerar y dejar una marca** en la historia de la contribución científica global.

Laika es una aplicación creada para aportar al desarrollo de la biología espacial, sin fines comerciales.
