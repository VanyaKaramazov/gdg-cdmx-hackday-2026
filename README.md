# Sistema de Triaje Clínico Inteligente y Análisis de Población\n**Digitalización e Inferencia de Expedientes Médicos con Gemma 4**\n\n**Categoría:** Equidad e Inclusión Digitales  \n**Fecha:** 1 de agosto de 2026\n\n## Resumen\nEste proyecto presenta una solución integral para entornos de salud con conectividad limitada o registros físicos. Mediante la captura de historias clínicas físicas en PDF, el sistema utiliza el modelo Gemma 4 local para extraer datos estructurados, predecir el nivel de riesgo de triaje y alimentar una base de datos relacional SQLite. Adicionalmente, habilita un motor conversacional de consultas inteligentes en lenguaje natural que permite responder preguntas operativas como la identificación de pacientes con obesidad, adultos mayores o niveles de glucosa elevada.\n\n## 1. El Problema\nEn clínicas comunitarias y centros de salud con infraestructura digital limitada, el registro de atención se realiza en papel o archivos escaneados. Esto acarrea graves inconsistencias:
- Falta de estructuración: Los datos de signos vitales, antecedentes y síntomas quedan atrapados en formatos no estructurados, imposibilitando un seguimiento automatizado.
- Estratificación de riesgo manual: La evaluación del nivel de urgencia o riesgo metabólico depende totalmente del criterio manual inmediato, aumentando el margen de error bajo sobrecarga de trabajo.
- Incapacidad de realizar análisis epidemiológicos: Extraer métricas como 'pacientes adultos mayores atendidos ayer', 'lista de personas con obesidad o glucosa alterada' requiere la revisión física manual de cientos de expedientes.\n\n## 2. Nuestra Solución y Arquitectura\nSe desarrolló un sistema de expediente clínico inteligente que opera completamente de forma local, sin depender de servicios en la nube. El objetivo es digitalizar expedientes clínicos en formato PDF, estructurar automáticamente la información médica mediante inteligencia artificial y almacenarla en una base de datos relacional para facilitar su consulta y análisis posterior.

A diferencia de una digitalización convencional, el sistema no solamente extrae información del expediente, sino que también realiza una primera inferencia clínica sobre los datos obtenidos, permitiendo identificar indicadores relevantes para el personal de enfermería.\n\n## 2.1. Flujo General del Sistema\nEl funcionamiento del sistema se divide en cinco etapas:
1. Carga del expediente clínico: El usuario proporciona un expediente clínico en formato PDF. Se eligió este formato debido a que conserva mejor la estructura del documento y evita los problemas de calidad presentes en fotografías o imágenes escaneadas.
2. Extracción del contenido: Mediante la biblioteca PyPDF2 se obtiene automáticamente todo el texto contenido en el expediente.
3. Procesamiento mediante Gemma 4: El texto extraído es enviado al modelo Gemma 4 ejecutado localmente mediante Ollama. El modelo identifica la información clínica relevante y genera un objeto JSON estructurado que contiene datos como: Nombre del paciente, Edad, Sexo, Presión arterial, Frecuencia cardiaca, Frecuencia respiratoria, Peso, Talla, Circunferencia de cintura, Glucosa, Temperatura, Saturación de oxígeno (SpO2), Motivo de consulta, Diagnósticos previos, Observaciones clínicas. Además, Gemma realiza una inferencia clínica preliminar generando automáticamente un nivel de alerta (Alta, Media o Baja) acompañado de una breve justificación médica basada en la información disponible.
4. Almacenamiento estructurado: La información obtenida se almacena en una base de datos SQLite organizada mediante un modelo relacional compuesto por las tablas de pacientes y registros de triaje. Esta estructura permite mantener el historial clínico de cada paciente y facilita futuras consultas sobre la información almacenada.
5. Consulta inteligente: Finalmente, el sistema incorpora un asistente conversacional que permite al personal de enfermería realizar preguntas en lenguaje natural. Por ejemplo: ¿Qué pacientes presentan glucosa elevada?, ¿Quiénes tienen sobrepeso u obesidad?, Muéstrame los pacientes con alerta alta, ¿Qué personas presentan hipertensión? Gemma traduce automáticamente estas preguntas a consultas SQL, ejecuta la búsqueda sobre SQLite y devuelve una respuesta comprensible para el usuario.\n\n## 2.2. Código Fuente del Prototipo Final\nA continuación se presenta el código que integra la carga de documentos, la estructuración JSON con Gemma 4 y el almacenamiento relacional:\n\n```python\nimport sqlite3
import PyPDF2
import requests
import json
import pandas as pd

#1. Creacion e inicializacion de la Base de Datos Relacional
def inicializar_bd_final():
    conexion = sqlite3.connect('clinica_local.db')
    cursor = conexion.cursor()
    cursor.execute("DROP TABLE IF EXISTS pacientes")
    cursor.execute("DROP TABLE IF EXISTS registros_triage")
    cursor.execute('''CREATE TABLE pacientes (
        id_paciente INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_completo TEXT,
        curp TEXT,
        edad INTEGER,
        sexo TEXT)''')
    cursor.execute('''CREATE TABLE registros_triage (
        id_registro INTEGER PRIMARY KEY AUTOINCREMENT,
        id_paciente INTEGER,
        pa_sistolica INTEGER, pa_diastolica INTEGER,
        frec_cardiaca INTEGER, frec_respiratoria INTEGER,
        peso REAL, talla REAL, cintura REAL,
        glucosa INTEGER, temperatura REAL, spo2 INTEGER,
        condicion_glucosa TEXT, diagnosticos_previos TEXT,
        motivo_consulta TEXT, observaciones TEXT,
        nivel_alerta TEXT, justificacion_clinica TEXT,
        FOREIGN KEY (id_paciente) REFERENCES pacientes (id_paciente)
    )''')
    conexion.commit()
    conexion.close()

inicializar_bd_final()

#2. Extraccion del texto desde el documento PDF
ruta_pdf = "Historia-clinica.pdf"
texto_pdf = ""
with open(ruta_pdf, "rb") as archivo:
    lector_pdf = PyPDF2.PdfReader(archivo)
    for pagina in lector_pdf.pages:
        texto_pdf += pagina.extract_text() + "\n"

#3. Inferencia y estructuracion con Gemma 4 via Ollama
url_local = "http://localhost:11434/api/generate"
prompt_maestro = f"""Eres un motor de inferencia clinica y estructuracion de datos.
Analiza este texto extraido de un expediente medico: \"{texto_pdf}\"
TAREAS:
1. EXTRACCION Y LIMPIEZA: Extrae datos a formato numerico/texto o null
2. INFERENCIA CLINICA: Evalua el riesgo. Define \"nivel_alerta\" (ALTA, MEDIA, BAJA) y redacta \"justificacion_clinica\".
Devuelve UNICAMENTE un objeto JSON valido con la estructura solicitada"""

payload = {
    "model": "gemma",
    "prompt": prompt_maestro,
    "stream": False,
    "format": "json"
}
respuesta = requests.post(url_local, json=payload)
resultado_crudo = respuesta.json().get("response", "")

#4. Insercion de registros procesados
if resultado_crudo:
    datos = json.loads(resultado_crudo.strip().strip("```json").strip("```"))
    conexion = sqlite3.connect('clinica_local.db')
    cursor = conexion.cursor()
    cursor.execute('''INSERT INTO pacientes (nombre_completo, curp, edad, sexo)
                      VALUES (?, ?, ?, ?)''',
                   (datos.get('nombre_completo'), datos.get('curp'), datos.get('edad'), datos.get('sexo')))
    id_pac = cursor.lastrowid
    
    cursor.execute('''INSERT INTO registros_triage (
        id_paciente, pa_sistolica, pa_diastolica, frec_cardiaca, frec_respiratoria,
        peso, talla, cintura, glucosa, temperatura, spo2, condicion_glucosa,
        diagnosticos_previos, motivo_consulta, observaciones, nivel_alerta, justificacion_clinica
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (
        id_pac, datos.get('pa_sistolica'), datos.get('pa_diastolica'), datos.get('frec_cardiaca'),
        datos.get('frec_respiratoria'), datos.get('peso'), datos.get('talla'), datos.get('cintura'),
        datos.get('glucosa'), datos.get('temperatura'), datos.get('spo2'), datos.get('condicion_glucosa'),
        datos.get('diagnosticos_previos'), datos.get('motivo_consulta'), datos.get('observaciones'),
        datos.get('nivel_alerta'), datos.get('justificacion_clinica')
    ))
    conexion.commit()
    conexion.close()\n```\n\n## 3. Integración de Gemma 4\nGemma 4 constituye el núcleo inteligente del sistema y participa en dos etapas diferentes del flujo de trabajo.

3.1. Extracción y estructuración de información: A partir del texto extraído del expediente clínico en formato PDF, Gemma identifica automáticamente los datos clínicos relevantes y los organiza en un objeto JSON estructurado. Cuando algún dato no se encuentra presente en el documento, el modelo asigna el valor null, garantizando consistencia en el almacenamiento de la información.

3.2. Inferencia clínica: Además de extraer datos, Gemma realiza una evaluación preliminar del estado del paciente utilizando los signos vitales, los antecedentes médicos y el motivo de consulta. Como resultado genera: Nivel de alerta clínica (Alta, Media o Baja), Clasificación de la condición de glucosa, Justificación clínica de la decisión.

3.3. Consultas inteligentes: Una vez almacenada la información en SQLite, Gemma permite interactuar con la base de datos mediante lenguaje natural. El modelo traduce automáticamente las preguntas realizadas por el personal de enfermería a consultas SQL, ejecuta dichas consultas y presenta los resultados en lenguaje claro, facilitando la identificación de pacientes con características específicas, como glucosa elevada, sobrepeso, obesidad, hipertensión o cualquier otro criterio almacenado en la base de datos.\n\n## 4. Desafíos Superados\nDurante la jornada del Hackday se resolvieron los siguientes retos técnicos:
- Procesamiento de respuestas en formato Markdown/JSON: Creación de parsers de limpieza para aislar el objeto JSON nativo devuelto por el LLM antes de pasarlo a json.loads().
- Normalización de esquemas relacionales: Separación eficiente entre los datos fijos del paciente (pacientes) y la historia clínica dinámica de la visita (registros_triage).
- Evaluación de triaje y consultas Text-to-SQL offline: Configuración de prompts maestros que ejecutan la evaluación clínica y la traducción de preguntas en lenguaje natural a código SQL ejecutable localmente.\n\n## 5. Enlaces del Proyecto\nRepositorio Público: https://github.com/VanyaKaramazov/gdg-cdmx-hackday-2026\n\n
