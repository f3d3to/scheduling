<template>
<div class="comentario-visualizacion" v-if="comentario">
    <p class="comentario-autor">
    <strong>{{ comentario.autor }}:</strong>
    </p>
    <p class="comentario-texto">
    {{ comentario.texto }}
    </p>
    <p class="comentario-fecha">
    {{ formatFecha(comentario.fecha_creacion) }}
    </p>
</div>
<div v-else>
    <p>Cargando comentario...</p>
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
    comentario: null,
    };
},
async mounted() {
    await this.fetchComentario();
},
methods: {
    async fetchComentario() {
    try {
        const response = await fetch(
        `http://localhost:8000/comentarios/${this.elemento.object_id}/`
        ); // Ajusta la URL a tu endpoint de comentarios
        if (response.ok) {
        const data = await response.json();
        this.comentario = {
            autor: data.autor || "Anónimo",
            texto: data.texto,
            fecha_creacion: data.fecha_creacion,
        };
        } else {
        console.error("Error al cargar el comentario:", response.statusText);
        }
    } catch (error) {
        console.error("Error al hacer fetch del comentario:", error);
    }
    },
    formatFecha(fecha) {
    if (!fecha) return "";
    const date = new Date(fecha);
    const options = {
        year: "numeric",
        month: "long",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
    };
    return date.toLocaleDateString("es-ES", options);
    },
},
watch: {
    elemento: {
    handler: "fetchComentario",
    immediate: true,
    deep: true,
    },
},
};
</script>

<style scoped>
.comentario-visualizacion {
border: 1px solid #ccc;
border-radius: 5px;
padding: 10px;
margin-bottom: 10px;
background-color: #f8f8f8;
}

.comentario-autor {
margin: 0 0 5px 0;
}

.comentario-texto {
margin: 0 0 5px 0;
white-space: pre-wrap; /* Respeta los saltos de línea */
}

.comentario-fecha {
font-size: 0.8em;
color: #777;
margin: 0;
}
</style>