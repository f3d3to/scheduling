Este proyecto se compone de diferentes secciones: backend, frontend, mobile y deployment. El backend está desarrollado en Django y gestiona los modelos PlanDeEstudio y Materia. En este modelo, se utiliza una relación ManyToMany para manejar las correlativas entre las materias, lo que permite definir de manera flexible las asignaturas que son requisitos para cursar otras. Los datos de las materias se gestionan a través de estos modelos y se procesan dentro de la base de datos.

El frontend está basado en Vue.js con Vite. Utiliza componentes como App.vue y main.ts para estructurar la interfaz de usuario, mientras que TypeScript ayuda a proporcionar un tipado estático, lo cual mejora la calidad y mantenibilidad del código. Este enfoque permite una integración fluida entre los componentes de la aplicación, facilitando su escalabilidad y desarrollo.

La parte mobile está desarrollada con Flutter. En este caso, los archivos esenciales son main.dart y pubspec.yml, que permiten configurar la aplicación móvil y gestionar las dependencias necesarias para su funcionamiento. Flutter proporciona la capacidad de crear aplicaciones multiplataforma, lo que permite que el proyecto sea accesible tanto en dispositivos móviles Android como iOS.

En el deployment, se incluyen los archivos necesarios para configurar y desplegar la aplicación. Cada componente del proyecto (backend, frontend y mobile) tiene su propio Dockerfile para crear contenedores específicos para cada uno. Con el archivo docker-compose.yml se orquesta la ejecución de estos contenedores de manera conjunta, facilitando la gestión de los diferentes servicios. Además, se utiliza Nginx como servidor web para manejar las solicitudes HTTP, redirigiendo el tráfico a los contenedores correspondientes. Todo el sistema se puede levantar fácilmente con el comando docker-compose up, lo que permite iniciar y administrar el entorno de desarrollo o producción sin complicaciones.

.
├── backend
│   ├── core
│   │   ├── asgi.py
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-310.pyc
│   │   │   ├── settings.cpython-310.pyc
│   │   │   ├── urls.cpython-310.pyc
│   │   │   └── wsgi.cpython-310.pyc
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
│   │   │   └── __pycache__
│   │   │       ├── 0001_initial.cpython-310.pyc
│   │   │       └── __init__.cpython-310.pyc
│   │   ├── models.py
│   │   ├── __pycache__
│   │   │   ├── admin.cpython-310.pyc
│   │   │   ├── apps.cpython-310.pyc
│   │   │   ├── filters.cpython-310.pyc
│   │   │   ├── __init__.cpython-310.pyc
│   │   │   ├── models.cpython-310.pyc
│   │   │   ├── serializers.cpython-310.pyc
│   │   │   ├── urls.cpython-310.pyc
│   │   │   └── views.cpython-310.pyc
│   │   ├── serializers.py
│   │   ├── tests.py
│   │   ├── tools.py
│   │   ├── urls.py
│   │   └── views.py
│   └── __pycache__
│       └── dbwait.cpython-310.pyc
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
