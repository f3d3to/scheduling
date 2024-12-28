Este proyecto se compone de diferentes secciones: backend, frontend, mobile y deployment. El backend está desarrollado en Django y gestiona los modelos PlanDeEstudio y Materia. En este modelo, se utiliza una relación ManyToMany para manejar las correlativas entre las materias, lo que permite definir de manera flexible las asignaturas que son requisitos para cursar otras. Los datos de las materias se gestionan a través de estos modelos y se procesan dentro de la base de datos.

El frontend está basado en Vue.js con Vite. Utiliza componentes como App.vue y main.ts para estructurar la interfaz de usuario, mientras que TypeScript ayuda a proporcionar un tipado estático, lo cual mejora la calidad y mantenibilidad del código. Este enfoque permite una integración fluida entre los componentes de la aplicación, facilitando su escalabilidad y desarrollo.

La parte mobile está desarrollada con Flutter. En este caso, los archivos esenciales son main.dart y pubspec.yml, que permiten configurar la aplicación móvil y gestionar las dependencias necesarias para su funcionamiento. Flutter proporciona la capacidad de crear aplicaciones multiplataforma, lo que permite que el proyecto sea accesible tanto en dispositivos móviles Android como iOS.

En el deployment, se incluyen los archivos necesarios para configurar y desplegar la aplicación. Cada componente del proyecto (backend, frontend y mobile) tiene su propio Dockerfile para crear contenedores específicos para cada uno. Con el archivo docker-compose.yml se orquesta la ejecución de estos contenedores de manera conjunta, facilitando la gestión de los diferentes servicios. Además, se utiliza Nginx como servidor web para manejar las solicitudes HTTP, redirigiendo el tráfico a los contenedores correspondientes. Todo el sistema se puede levantar fácilmente con el comando docker-compose up, lo que permite iniciar y administrar el entorno de desarrollo o producción sin complicaciones.

.
├── backend
│   ├── core
│   │   ├── asgi.py
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── dbwait.py
│   ├── init.py
│   ├── manage.py
│   ├── plan_de_estudio
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── filters.py
│   │   ├── __init__.py
│   │   ├── materias.xlsx
│   │   ├── migrations
│   │   │   ├── 0001_initial.py
│   │   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tests.py
│   │   ├── tools.py
│   │   ├── urls.py
│   │   └── views.py
├── delete_pycache.sh
├── deployment
│   ├── backend.Dockerfile
│   ├── docker-compose.yml
│   ├── frontend.Dockerfile
│   ├── init.sh
│   ├── mobile.Dockerfile
│   ├── nginx.dockerfile
│   └── requirements.txt
├── frontend
│   ├── index.html
│   ├── package.json
│   ├── package-lock.json
│   ├── public
│   │   └── vite.svg
│   ├── README.md
│   ├── src
│   │   ├── App.vue
│   │   ├── assets
│   │   │   └── vue.svg
│   │   ├── components
│   │   │   └── HelloWorld.vue
│   │   ├── main.ts
│   │   ├── style.css
│   │   └── vite-env.d.ts
│   ├── tsconfig.app.json
│   ├── tsconfig.json
│   ├── tsconfig.node.json
│   ├── vite.config.js
│   └── vite.config.ts
├── mobile
│   ├── assets
│   ├── lib
│   │   └── main.dart
│   ├── pubspec.yml
│   ├── requirements.txt
│   └── web
│       └── index.html
├── readme.MD
└── show_dirs.sh


# TO-DO
- Dashboard de estado de carrera:finales debidos- NotificacionesSesiones compartidasCompartir entre usuariosMarcar horarios de materias para ver superpuestosOrganizacion por CuatrimestresPomodoro reporte por semana etcDashboard para una  materia y para mas de una a la vezEste es personal de inicio con lo que te queda pendiente etxModelo cursada notificacion por horario de inscripcion en el celu y mailBoton para mostrar aprobadas y color para las disponibles por corrlativas.Nivel de dificultad o materia densa o materia largaSistema de recomendacioneaCargar planes a manoplaRating de materiaCombinaciones mas comunesPromedio de finalizacion de carrera, cuando te recibis te felicita y cambia de coloresComo conectar entre estudiantes de distintaa carreras¡Eventos de carrera (PARA PENSAR)Plantilla para marcar qque laburas y en dondeOfrecer trabajo part time pero llenando donde y qué hacesProyectos a los que te podes sumarLaboratoriosMarcar promedios de la carrera ranking de estudiantesEncuestaMarcar que estudias y laburasCentro de estudiantes cuenta diferenciada para obtener mas gente

. Mi Panel Académico (Dashboard Personalizado):

    Visión General de Carrera:
        Estado de Carrera: Gráfico visual del avance, incluyendo materias aprobadas, en curso y pendientes.
        Finales Pendientes: Lista clara y concisa con fechas de los próximos finales, junto con notificaciones y recordatorios.
        Promedio de Finalización Estimado: Cálculo dinámico del tiempo estimado para la graduación, con un mensaje de felicitación al alcanzar la meta.
        Promedio Académico Actual: Visualización del promedio con ranking opcional entre estudiantes (privacidad configurable).
    Gestión de Materias:
        Vista por Materia: Información detallada de cada materia: programa, profesor, horarios, aula, y estado (aprobada, cursando, pendiente).
        Vista General de Materias: Comparación simultánea del estado y la información clave de múltiples materias, ideal para una rápida revisión.
        Nivel de Dificultad/Densidad/Longitud: Indicadores visuales o numéricos para evaluar la complejidad y la carga de trabajo de cada materia.
        Calificación de Materias (Rating): Sistema de estrellas o puntaje para que los estudiantes evalúen y compartan su experiencia.
        Materias Aprobadas: Listado con opción a ocultar y destacar, diferenciando las disponibles para cursar por correlatividades.
    Planificación y Organización:
        Organización por Cuatrimestres: Planificador para visualizar y organizar las materias a cursar en cada cuatrimestre, con sugerencias automáticas basadas en correlatividades y disponibilidad.
        Calendario Académico Personalizado: Integración de horarios de cursada, fechas de exámenes y eventos importantes, con opción de superposición de horarios para una mejor visualización.
        Técnica Pomodoro: Herramienta integrada para la gestión del tiempo de estudio, con reportes semanales del tiempo dedicado a cada materia.
        Carga Manual de Planes de Estudio: Opción para ingresar manualmente los planes de estudio en caso de que no estén pre-cargados.
    Notificaciones y Alertas:
        Recordatorios de Inscripción: Notificaciones push y por correo electrónico sobre fechas de inscripción a materias y exámenes.
        Notificaciones de Sesiones Compartidas Alertas cuando se programen sesiones colaborativas con otros usuarios.

2. Comunidad y Colaboración:

    Conexión entre Estudiantes:
        Búsqueda y Conexión: Perfiles de estudiantes con opciones para conectar con compañeros de la misma carrera o de otras afines.
        Mensajería Interna: Chat para comunicación directa entre estudiantes.
        Grupos de Estudio: Creación de grupos por materia o proyecto para facilitar el estudio colaborativo.
    Sesiones de Estudio Compartidas:
        Planificación y Reserva: Herramienta para programar y reservar sesiones de estudio grupales, con opción de compartir con otros usuarios.
    Recomendaciones Inteligentes:
        Sugerencias de Materias: Basadas en el rendimiento académico, intereses y calificaciones de otros usuarios.
        Recomendaciones de Grupos de Estudio: Sugerencias de grupos afines a las materias que se están cursando.
    Combinaciones Comunes (basado en datos anónimos): Visualización de las materias que los estudiantes suelen combinar en un cuatrimestre.

3. Centro de Estudiantes (Perfil Diferenciado):

    Difusión de Información: Canal para la publicación de noticias, eventos, y beneficios para los estudiantes.
    Encuestas y Sondeos: Herramienta para realizar encuestas a la comunidad estudiantil y recopilar feedback.
    Gestión de Afiliados: Herramienta para obtener más gente, mantener un registro de afiliados y facilitar la comunicación con ellos.

4. Integración Laboral y Profesional:

    Perfil Profesional:
        Registro de Experiencia Laboral: Espacio para detallar la experiencia laboral, incluyendo puesto, empresa y responsabilidades.
        Seguimiento Académico/Laboral: Opción para marcar si el estudiante está trabajando actualmente y en qué área, relacionándolo con sus estudios.
    Oportunidades Laborales:
        Bolsa de Trabajo: Ofertas de trabajos part-time y pasantías, con filtros de búsqueda por área de interés y habilidades requeridas.
        Postulación Simplificada: Proceso de postulación directa a través de la plataforma, con la información del perfil ya precargada.
    Proyectos y Laboratorios:
        Convocatorias a Proyectos: Publicación de proyectos de investigación y desarrollo a los que los estudiantes pueden postularse.
        Acceso a Laboratorios: Información sobre laboratorios disponibles y cómo acceder a ellos para proyectos académicos.

5. Recursos Adicionales:

    Eventos de Carrera: Calendario con eventos relevantes para el desarrollo profesional, como charlas, talleres y ferias de empleo (sección a desarrollar en el futuro).

Beneficios Clave:

    Mejor Organización y Planificación Académica.
    Seguimiento Detallado del Progreso.
    Facilita la Comunicación y Colaboración entre Estudiantes.
    Conexión con Oportunidades Laborales y Proyectos.
    Acceso a Información Relevante del Centro de Estudiantes.

Foros de Discusión por Materia: Espacios para debates, preguntas y respuestas sobre temas específicos de cada materia, moderados por estudiantes avanzados o profesores.


Ranking de apuntes "Mercado" de Apuntes y Resúmenes: Una plataforma donde los estudiantes puedan compartir, comprar o vender apuntes, resúmenes y material de estudio (con un sistema de verificación de calidad y reseñas).


Sistema de Feedback Directo a la Universidad: Un canal para que los estudiantes puedan enviar sugerencias, reportar problemas o expresar su opinión sobre diversos aspectos de la vida universitaria.

Dónde estudiar (MAPA): MAPITA CON BIBLIOTECAS VIRTUALES SEGÚN TU FACULTAD Y ALGUNOS LUGARES "IMPERDIBLES".

-HAY QUE PENSARLA MEJOR-Creador de CV y Portfolio: Asistentes para la creación de un CV atractivo y un portfolio digital que destaque las habilidades y proyectos del estudiante.

Networking con Empresas: Una sección que facilite el contacto con empresas para pasantías, prácticas profesionales y ofertas de empleo, con la posibilidad de organizar ferias de empleo virtuales.


DISEÑO:
- DEFINIR UN roadmap, PARA CREAR LAS FUNCIONALIDADES DE LA APLICACION


Seguimiento del Rendimiento Personalizado:

    Análisis de Progreso Académico: Visualización interactiva que muestre tendencias en el rendimiento, comparando semestres, materias o áreas de conocimiento.
    Identificación de Debilidades y Fortalezas: Informe automático que resalte las áreas donde el estudiante tiene dificultades y recomendaciones personalizadas para mejorar.

Integración con Herramientas Digitales:

    Sincronización con Apps Externas: Vinculación con Google Calendar, Notion o Trello para integrar el calendario académico con herramientas personales de gestión.
    Gestión de Documentos: Un repositorio personal en la nube para guardar apuntes, trabajos prácticos y exámenes pasados organizados por materia.

Interacción Gamificada:

    Logros Académicos: Sistema de medallas o insignias por objetivos cumplidos, como aprobar todas las materias de un cuatrimestre o participar en actividades extracurriculares.
    Ranking Colaborativo: Tablas que destaquen a los estudiantes más activos en foros, grupos de estudio o participación en eventos.

Asesoramiento Vocacional y Profesional:

   (CHUSMEAR ESTO) Pruebas de Orientación: Tests personalizados para descubrir áreas profesionales afines a los intereses del estudiante.
    Simulador de Trayectorias Laborales: Herramienta para explorar caminos profesionales según la carrera, combinando datos sobre empleabilidad, roles comunes y salarios promedio.

(CHUSMEAR ESTO) Mentoría Inversa: Espacio para que estudiantes jóvenes compartan habilidades digitales o conocimientos recientes con profesores o profesionales mayores.

(CELU) Herramienta de Control de Gastos: Herramienta para registrar gastos académicos (materiales, transporte, etc.) y sugerir formas de ahorrar.


(ELABORAR ESTO) Estrategias de Estudio Adaptativas :

    Guías Personalizadas: Creación automática de materiales de estudio según el progreso y rendimiento del estudiante en cada materia.
    Simuladores de Exámenes:

Recompensas por Participación: Un sistema de puntos canjeables por beneficios académicos (como extensiones de biblioteca, asesorías gratuitas o acceso a material premium) para incentivar el uso de la plataforma.

Optimización de Horarios: Algoritmos que sugieran la mejor combinación de materias y horarios según las preferencias del estudiante, como evitar días completos o maximizar mañanas libres.


# TO - DO

## GENERAL
- [ ]

## FRONTEND
- [ ]

## BACKEND
- [ ] AUTENTICACION
- [ ] SEGURIZACIÓN DE ENDPOINTS


## TIMER
- [ ] Poder des-seleccionar una tarea.
- [ ] Las sesiones deben decir cuando duran, en el dialog.
- [ ] Agregar más estilos.
- [ ] Al completar una Actividad es necesario una notificación.
- [ ] Al completar una Sesión cambiar de color a verde.
- [ ] Al completar una Tarea, una notificación.

## PLANES DE ESTUDIO
- [ ] FILTROS EN LA INTERFAZ SELECCIONABLES: PERIODO DE CARRERA, MATERIAS HECHAS, COLOR ESPECIFICO PARA LAS DISPONIBLES
- [ ] CUANDO SELECCIONO UNA MATERIA SE ABRE UN "DETALLE", ES UN DASHBOARD DE LA MATERIA, QUE TIENE MUCHAS OPCIONES CÓMO POR EJEMPLO
- [ ] El selector de planes debe estar en un dialog "arrastrable" junto con los filtros y se pueda.
- [ ] LAS MATERIAS OPTATIVAS DEBEN INICIAR "OCULTAS", DENTRO DEL DIALOGO SE PUEDEN
- [ ] DEBE HABER UNA FORMA DE EDITAR/ELIMINAR Y CREAR (CONECTAR,ETC) MATERIAS Y PLANES DE ESTUDIO.
- [ ] LOS PLANES DE ESTUDIO PUEDEN SER EXPORTABLES (HABRÍA QUE VER EN QUE FORMATO)
- [ ] AGREGAR CALIFICACIONES

## CARRERA
- [ ] DASHBOARD CON PROMEDIO, ETC

## PLANIFICADORES
- [ ] PREVISUALIZAR CON [Html Canvas](https://html2canvas.hertzen.com/)
- [ ] Edición de planificadores
- [ ] Creación de plantillas (calendario, Por tareas, etc)
- [ ] Exportar planificadores a PDF
- [ ]
- [ ]

## AGREGAR SISTEMA DE NOTAS
- [ ]


## MOBILE
- [ ] CONECTAR CON BACKEND
- [ ] AGREGAR FUNCIONALIDADES
- [ ]