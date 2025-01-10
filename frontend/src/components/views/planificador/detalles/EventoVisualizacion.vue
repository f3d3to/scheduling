<template>
<div class="evento-visualizacion" v-if="evento">
    <h3>{{ evento.nombre }}</h3>
    <p v-if="evento.descripcion" class="descripcion">
    {{ evento.descripcion }}
    </p>
    <p>
    <strong>Fecha y Hora:</strong>
    {{ formatFecha(evento.fecha_hora) }} - {{ formatHora(evento.fecha_hora) }}
    </p>
    <p v-if="evento.usuario">
    <strong>Usuario:</strong> {{ evento.usuario }}
    </p>
</div>
<div v-else>
    <p>Cargando datos del evento...</p>
</div>
</template>

<script>
export default {
props: {
    elemento: {
    type: Object,
    required: true,
    },
},
data() {
    return {
    evento: null,
    };
},
async mounted() {
    await this.fetchEvento();
},
methods: {
    async fetchEvento() {
    try {
        const response = await fetch(
        `http://localhost:8000/eventos/${this.elemento.object_id}/`
        ); // Ajusta la URL a tu endpoint de eventos
        if (response.ok) {
        const data = await response.json();
        this.evento = {
            nombre: data.nombre || "Sin nombre",
            descripcion: data.descripcion || "Sin descripción",
            fecha_hora: data.fecha_hora,
            usuario: data.usuario || null,
            // ... añade aquí el resto de los campos de tu modelo de datos
        };
        } else {
        console.error("Error al cargar el evento:", response.statusText);
        }
    } catch (error) {
        console.error("Error al hacer fetch del evento:", error);
    }
    },
    formatFecha(fecha) {
    if (!fecha) return "";
    const date = new Date(fecha);
    const options = { year: "numeric", month: "long", day: "numeric" };
    return date.toLocaleDateString("es-ES", options);
    },
    formatHora(fecha) {
    if (!fecha) return "";
    const date = new Date(fecha);
    const options = { hour: "2-digit", minute: "2-digit" };
    return date.toLocaleTimeString("es-ES", options);
    },
},
watch: {
    elemento: {
    handler: "fetchEvento",
    immediate: true,
    deep: true,
    },
},
};
</script>

<style scoped>
.evento-visualizacion {
border: 1px solid #ccc;
border-radius: 5px;
padding: 10px;
margin-bottom: 10px;
background-color: #f8f8f8;
}

.evento-visualizacion h3 {
margin-top: 0;
}

.descripcion {
font-style: italic;
margin-bottom: 5px;
}

.evento-visualizacion p {
margin: 5px 0;
}
</style>