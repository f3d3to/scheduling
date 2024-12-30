<template>
<div class="evento-asociado-visualizacion" v-if="evento">
    <h4>Evento Asociado:</h4>
    <h5>{{ evento.nombre }}</h5>
    <p v-if="evento.descripcion" class="descripcion">{{ evento.descripcion }}</p>
    <p>
    <strong>Fecha y Hora de Inicio:</strong>
    {{ formatFecha(evento.fecha_inicio) }} - {{ formatHora(evento.fecha_inicio) }}
    </p>
    <p>
    <strong>Fecha y Hora de Fin:</strong>
    {{ formatFecha(evento.fecha_fin) }} - {{ formatHora(evento.fecha_fin) }}
    </p>
    <p v-if="evento.ubicacion">
    <strong>Ubicación:</strong> {{ evento.ubicacion }}
    </p>
    <p v-if="evento.organizador">
    <strong>Organizador:</strong> {{ evento.organizador }}
    </p>
</div>
<div v-else>
    <p>No hay un evento asociado.</p>
</div>
</template>

<script>
export default {
props: {
    evento: {
    type: Object,
    required: true,
    },
},
methods: {
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
};
</script>

<style scoped>
.evento-asociado-visualizacion {
border: 1px solid #ccc;
border-radius: 5px;
padding: 10px;
margin-bottom: 10px;
background-color: #f8f8f8;
}

.evento-asociado-visualizacion h4 {
margin-top: 0;
}

.evento-asociado-visualizacion h5 {
margin: 5px 0;
}

.descripcion {
font-style: italic;
margin-bottom: 5px;
}

.evento-asociado-visualizacion p {
margin: 5px 0;
}
</style>