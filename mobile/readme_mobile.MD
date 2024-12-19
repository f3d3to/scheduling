# **Mobile**

## **Descripción**
La aplicación es una herramienta móvil diseñada para estudiantes, que combina funcionalidades clave para la organización y el registro académico. Permite transcribir grabaciones de clases mediante el uso de modelos avanzados de reconocimiento de voz como OpenAI Whisper, generando texto editable y almacenable en archivos locales. También incorpora un canvas interactivo para escribir notas matemáticas a mano alzada, reconociendo símbolos y ecuaciones que son automáticamente convertidos a formato LaTeX, con soporte para exportación en `.txt` y `.tex`.

La aplicación está integrada con una plataforma web que permite a los usuarios visualizar:
1. **Planificadores académicos**: Tablas interactivas que organizan tareas y fechas.
2. **Planes de estudio**: Grafos que representan relaciones y estructuras entre materias o módulos académicos.

---

## **Herramientas y Arquitectura**
- **Transcripción de audio**:
  - **Backend**: Implementado en Python con FastAPI, utilizando el modelo OpenAI Whisper.
  - **Almacenamiento**: Archivos de texto generados en formato `.txt` para consulta posterior.

- **Reconocimiento de notas matemáticas**:
  - **Canvas interactivo**: Implementado con Flutter usando `CustomPainter` para capturar trazos.
  - **Conversión a LaTeX**: API de Mathpix para transformar trazos en ecuaciones matemáticas exportables.
  - **Renderización**: Uso de la biblioteca `flutter_math_fork` para mostrar ecuaciones en tiempo real.

- **Visualización de planificadores y grafos**:
  - **Integración con la web**: Sincronización con la plataforma para cargar datos en formato de tablas y grafos.
  - **Frontend**: Flutter, con interfaces dinámicas para explorar tareas y estructuras académicas.

---

## **Despliegue de Entorno**
1. **Backend**:
   - **Lenguaje**: Python 3.8+.
   - **Framework**: FastAPI.
   - **Dependencias principales**:
     - `faster-whisper` para transcripción.
     - `uvicorn` para el servidor web.
   - **Ejecución**:
     ```bash
     uvicorn main:app --reload
     ```

2. **Mobile**:
   - **Framework**: Flutter.
   - **Dependencias**:
     - `flutter_math_fork` para renderización LaTeX.
     - `http` para consumo de API.
   - **Ejecución**:
     ```bash
     flutter run
     ```

3. **Integración con la Web**:
   - La sincronización con el frontend web se realiza a través de APIs RESTful y una base de datos compartida.

---

## **Consideraciones**
1. **Compatibilidad**:
   - La app está diseñada para dispositivos Android e iOS.
   - Requiere conexión a internet para sincronización y uso de servicios como Mathpix y la transcripción.
2. **Ampliaciones futuras**:
   -
   - Visualización de avance académico en la sección de planificadores.

