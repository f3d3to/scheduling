<template>
  <div class="actividad-visualizacion" v-if="actividad" :style="{ borderColor: actividad.color }">
    <h3 :style="{ color: actividad.color }">{{ actividad.nombre }}</h3>
    <p v-if="actividad.descripcion" class="descripcion">{{ actividad.descripcion }}</p>
    <p v-if="actividad.fecha_inicio">
      <strong>Inicio:</strong> {{ formatFecha(actividad.fecha_inicio) }}
    </p>
    <p v-if="actividad.fecha_fin">
      <strong>Fin:</strong> {{ formatFecha(actividad.fecha_fin) }}
    </p>
    <p v-if="actividad.estado">
      <strong>Estado:</strong> <span :style="{ color: actividad.estadoColor }">{{ actividad.estado }}</span>
    </p>
  </div>
  <div v-else>
    <p>Cargando datos de la actividad...</p>
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
      actividad: null, // Aquí se almacenará la instancia completa de la actividad
    };
  },
  async mounted() {
    await this.fetchActividad();
  },
  methods: {
    async fetchActividad() {
      try {
        const response = await fetch(
          `http://localhost:8000/actividades/${this.elemento.object_id}/`
        );
        if (response.ok) {
          const data = await response.json();
          this.actividad = {
            nombre: data.nombre || "Sin nombre",
            descripcion: data.descripcion || "Sin descripción",
            fecha_inicio: data.fecha_inicio,
            fecha_fin: data.fecha_fin,
            color: data.color || "#000000",
            estado: data.estado?.nombre || "Sin estado",
            estadoColor: data.estado?.color || "#000000",
          };
        } else {
          console.error("Error al cargar la actividad:", response.statusText);
        }
      } catch (error) {
        console.error("Error al hacer fetch de la actividad:", error);
      }
    },
    formatFecha(fecha) {
      if (!fecha) return "Sin fecha";
      const opciones = { year: "numeric", month: "long", day: "numeric" };
      return new Date(fecha).toLocaleDateString("es-ES", opciones);
    },
  },
};
</script>

<style scoped>
.actividad-visualizacion {
  border: 2px solid;
  border-radius: 6px;
  padding: 10px;
  margin: 1px 0;
  background-color: #f9f9f9;
  transition: box-shadow 0.3s ease;
}

.actividad-visualizacion:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

h3 {
  margin: 0;
}

.descripcion {
  font-style: italic;
  margin: 5px 0;
}

p {
  margin: 5px 0;
}

strong {
  font-weight: bold;
}
</style>
