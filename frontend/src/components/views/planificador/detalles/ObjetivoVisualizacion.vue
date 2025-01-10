<template>
<div class="objetivo-visualizacion" v-if="objetivo">
    <h3>{{ objetivo.nombre }}</h3>
    <p v-if="objetivo.descripcion" class="descripcion">{{ objetivo.descripcion }}</p>
    <p>
    <strong>Estado:</strong>
    <span :style="{ color: getColorEstado(objetivo.estado) }">{{ objetivo.estado }}</span>
    </p>
    <p v-if="objetivo.fecha_limite">
    <strong>Fecha Límite:</strong> {{ formatFecha(objetivo.fecha_limite) }}
    </p>
    <p v-if="objetivo.progreso">
        <strong>Progreso: </strong> {{ objetivo.progreso }} %
    </p>
</div>
<div v-else>
    <p>Cargando datos del objetivo...</p>
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
    objetivo: null,
    };
},
async mounted() {
    await this.fetchObjetivo();
},
methods: {
    async fetchObjetivo() {
    try {
        const response = await fetch(
        `http://localhost:8000/objetivos/${this.elemento.object_id}/`
        ); // Ajusta la URL a tu endpoint de objetivos
        if (response.ok) {
        const data = await response.json();
        this.objetivo = {
            nombre: data.nombre || "Sin nombre",
            descripcion: data.descripcion || "Sin descripción",
            estado: data.estado || "Pendiente",
            fecha_limite: data.fecha_limite,
            progreso: data.progreso || 0,
        };
        } else {
        console.error("Error al cargar el objetivo:", response.statusText);
        }
    } catch (error) {
        console.error("Error al hacer fetch del objetivo:", error);
    }
    },
    formatFecha(fecha) {
    if (!fecha) return "";
    const date = new Date(fecha);
    const options = { year: "numeric", month: "long", day: "numeric" };
    return date.toLocaleDateString("es-ES", options);
    },
    getColorEstado(estado) {
    const mapping = {
        Pendiente: "gray",
        "En Progreso": "blue",
        Completado: "green",
        Fallido: "red",
        // ... añade más estados y colores si es necesario
    };
    return mapping[estado] || "black";
    },
},
watch: {
    elemento: {
    handler: "fetchObjetivo",
    immediate: true,
    deep: true,
    },
},
};
</script>

<style scoped>
.objetivo-visualizacion {
border: 1px solid #ccc;
border-radius: 5px;
padding: 10px;
margin-bottom: 10px;
background-color: #f8f8f8;
}

.objetivo-visualizacion h3 {
margin-top: 0;
}

.descripcion {
font-style: italic;
margin-bottom: 5px;
}

.objetivo-visualizacion p {
margin: 5px 0;
}
</style>