<template>
<v-card class="pa-4">
    <div>
    <h2 class="mb-4">Añadir al planificador</h2>
    <FormKit
        type="form"
        @submit="enviarFormulario"
        :value="formulario"
        #default="{ value }"
        submit-label="Crear Elemento"
    >
        <FormKit
        type="hidden"
        name="elemento_nombre"
        :value="`Elemento de Celda ${celdaId}`"
        />

        <FormKit
        type="hidden"
        name="celda_id"
        :value="celdaId"
        />

        <FormKit
        type="select"
        name="estructura_id"
        label="Estructura"
        v-model="value.estructura_id"
        >
        <option :value="null">Sin Estructura</option>
        <option v-for="estructura in estructuras" :key="estructura.id" :value="estructura.id">
            {{ estructura.nombre }}
        </option>
        </FormKit>

        <FormKit
        type="textarea"
        name="descripcion"
        label="Descripción"
        v-model="value.descripcion"
        />

        <FormKit
        type="select"
        name="modelo_asociado"
        label="Modelo Asociado"
        v-model="value.modelo_asociado"
        >
        <option :value="null">Ninguno</option>
        <option v-for="modelo in modelosAsociables" :key="modelo" :value="modelo">
            {{ modelo }}
        </option>
        </FormKit>

        <ModeloFormulario
        v-if="value.modelo_asociado"
        :modelo-asociado="value.modelo_asociado"
        :estructura-modelos="estructuraModelos"
        :urls-modelos="urlsModelos"
        @update:modelo_asociado_id="(val) => formulario.modelo_asociado_id = val"
        @update:modelo_data="(val) => formulario[`${value.modelo_asociado}_data`] = val"
        />

        </FormKit>
    </div>
</v-card>
</template>

<script>
import ModeloFormulario from './ModeloFormulario.vue';
import { plugin, defaultConfig } from '@formkit/vue';
import '@formkit/themes/genesis';

export default {
    components: {
    ModeloFormulario,
    },
    props: {
    celdaId: {
        type: Number,
        required: true,
    },
    },
    data() {
    return {
        modelosAsociables: [],
        estructuraModelos: [],
        urlsModelos: [],
        estructuras: [],
        formulario: {
        elemento_nombre: '',
        celda_id: this.celdaId,
        estructura_id: null,
        descripcion: '',
        modelo_asociado: null,
        modelo_asociado_id: null,
        actividad_data: {},
        tarea_data: {},
        objetivo_data: {},
        comentario_data: {},
        etiqueta_data: {},
        evento_data: {},
        registro_progreso_data: {},
        recurrente_data: {},
        },
    };
    },
    watch: {
        celdaId: {
            handler(newVal) {
                this.formulario.celda_id = newVal; // Actualiza el valor de celda_id en formulario
            },
            immediate: true // Para que se ejecute el watcher al inicio
        }
    },
    async created() {
    try {
        const response = await fetch('http://localhost:8000/formulario-info-elemento/');
        if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        this.modelosAsociables = data.modelos_asociables;
        this.estructuraModelos = data.estructura_modelos;
        this.urlsModelos = data.urls_modelos;
        this.estructuras = data.estructuras;
    } catch (error) {
        console.error('Error al obtener la información del formulario:', error);
    }
    },
    methods: {
    async enviarFormulario(data) {
        try {
        // Actualizar el nombre del elemento aquí
        data.elemento_nombre = `Elemento de Celda ${this.celdaId}`;
        console.log(data)
        let datosAEnviar = {
            elemento_nombre: data.elemento_nombre,
            celda_id: data.celda_id,
            estructura_id: data.estructura_id,
            descripcion: data.descripcion,
            modelo_asociado: data.modelo_asociado,

        };

        if (data.modelo_asociado && !data.modelo_asociado_id) {
            datosAEnviar[`${data.modelo_asociado}_data`] = data[`${data.modelo_asociado}_data`];
        }else {
            datosAEnviar.modelo_asociado_id = data.modelo_asociado_id;
        }

        const response = await fetch('http://localhost:8000/formulario-crear-elemento/', {
            method: 'POST',
            headers: {
            'Content-Type': 'application/json',
            // Si es necesario, incluye aquí el token CSRF u otras cabeceras
            },
            body: JSON.stringify(datosAEnviar),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const responseData = await response.json();
        console.log('Elemento creado:', responseData);
        this.$emit('elemento-creado', responseData);
        // Aquí puedes redirigir al usuario o mostrar un mensaje de éxito
        // this.$router.push('/');
        } catch (error) {
        console.error('Error al crear el elemento:', error);
        // Aquí puedes manejar los errores y mostrar mensajes al usuario
        }
    },
    },
};
</script>