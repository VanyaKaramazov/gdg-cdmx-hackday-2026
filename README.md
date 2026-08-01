# 🏥 Sistema de Triaje Clínico Inteligente y Análisis de Población

**Digitalización, Inferencia Clínica y Consultas NL2SQL con Gemma 4**

**Categoría:** Equidad e Inclusión Digitales  
**Fecha:** 31 de Julio de 2026  
**Desarrolladores:** Ivan Cabrera Herrera, Tonatiuh Cabrera Gonzales y José Uriel Vidal Cruz

---
## 💡 1. Inspiración: El Problema Local
En las clínicas comunitarias y centros de salud con infraestructura digital limitada, el registro de la atención a los pacientes se sigue realizando en papel o en archivos escaneados de forma deficiente. Esto conlleva graves inconsistencias que afectan directamente la salud pública:
*   **Falta de estructuración:** Los datos vitales quedan atrapados en texto plano.
*   **Estratificación de riesgo manual:** La evaluación del triaje depende del criterio humano inmediato, susceptible a errores por sobrecarga de trabajo.
*   **Incapacidad analítica:** Es imposible realizar análisis epidemiológicos rápidos.
*   **Desperdicio de recursos:** Se gasta tiempo y dinero valiosos en gestionar bases de datos complejas.
*   **Brecha técnica:** Las herramientas de software actuales son poco intuitivas y frustrantes para el personal médico no técnico.

Nuestro proyecto ataca directamente esta brecha de inclusión digital, democratizando el acceso al análisis de datos sin necesidad de saber programar ni requerir costosos servidores en la nube.

---

## ⚙️ 2. Cómo lo construimos (Arquitectura y Tecnología)
El sistema opera 100% de forma local, priorizando la privacidad del paciente. Utilizamos **Gemma 4 (versión 7B)** ejecutado localmente a través de **Ollama**. 

En lugar de utilizar RAG o Fine-tuning, el núcleo lógico del proyecto se basa en **Prompt Engineering avanzado**. 
1.  **Ingesta y Extracción:** A través de la biblioteca `PyPDF2`, el sistema extrae la información de los expedientes médicos en formato PDF.
2.  **Estructuración JSON:** El texto extraído se envía al modelo Gemma 4, el cual identifica la información clínica relevante y genera un objeto JSON puramente estructurado, inferiendo incluso el nivel de urgencia clínica.
3.  **Almacenamiento Relacional:** Este JSON se normaliza y se inserta automáticamente en una base de datos SQL (`SQLite`).
4.  **Motor NL2SQL:** Para resolver la brecha técnica del personal, implementamos un agente conversacional. El personal de salud puede hacer consultas en lenguaje natural (ej. *"¿Cuántos pacientes varones tienen glucosa alta?"*), Gemma 4 traduce esto a consultas SQL bajo el capó, y devuelve la información requerida en un formato claro y humano o agrega nuevos registros según sea el caso.

---

## 🚧 3. Desafíos a los que nos enfrentamos
Construir un pipeline de datos de extremo a extremo en 24 horas presentó varios retos técnicos importantes:

*   **Reconocimiento de escritura a mano (OCR):** Inicialmente intentamos procesar expedientes llenados a mano mediante fotografías. Sin embargo, Gemma 4 presentaba dificultades para registrar correctamente los valores numéricos de los manuscritos. Tomamos la decisión técnica de limitarnos al reconocimiento de archivos PDF nativos para garantizar la precisión médica del prototipo, dejando el soporte OCR avanzado para futuras iteraciones.
*   **Control de Alucinaciones y Formato:** Lograr que un LLM devuelva un JSON estricto sin incluir introducciones conversacionales (formato Markdown) requirió iteraciones intensivas en el diseño del prompt maestro y scripts de limpieza (parsers) en Python.
*   **Orquestación de Entornos Efímeros:** Lograr que un evaluador pudiera ejecutar el modelo local (Ollama) dentro de la máquina virtual temporal de Google Colab requirió resolver dependencias de compresión de Linux (`zstd`) y levantar procesos en segundo plano nativamente.

---

## 🚀 4. Instalación y Uso (Reproducibilidad)

El proyecto está diseñado para ser "Plug & Play", facilitando su revisión por parte de los jueces:

### Opción A: Ejecución en Google Colab (Recomendado)
El cuaderno incluye un script de configuración automatizada que prepara el entorno.
1. Abre el archivo `.ipynb` en Google Colab.
2. En el menú, ve a **Entorno de ejecución > Cambiar tipo de entorno** y selecciona **T4 GPU**.
3. Ejecuta la **Celda 0**. El script instalará dependencias, levantará Ollama en segundo plano y descargará el modelo Gemma:7b automáticamente.
4. Ejecuta el resto de las celdas secuencialmente. Se te preguntará si deseas usar los PDFs de prueba del repositorio o subir los tuyos propios.

### Opción B: Ejecución Local
1. Instala [Ollama](https://ollama.com/) en tu equipo local.
2. Descarga el modelo: `ollama pull gemma:7b` y arranca el servidor: `ollama serve`.
3. Ejecuta el archivo `.ipynb` en VS Code o Jupyter, **omitiendo la Celda 0**.

---

## 🔗 5. Enlaces del Proyecto
*   **Repositorio Público:** [https://github.com/VanyaKaramazov/gdg-cdmx-hackday-2026](https://github.com/VanyaKaramazov/gdg-cdmx-hackday-2026)
*   **Video Demo:** [https://youtu.be/ZNO8vsMAlqU](https://youtu.be/ZNO8vsMAlqU)
