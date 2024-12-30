<template>
  <div class="tarea-visualizacion" :style="tareaBackground">
    <div v-if="loading" class="loading">Cargando tarea...</div>
    <div v-else-if="error" class="error">Error al cargar la tarea.</div>
    <div v-else-if="!tarea.id" class="not-found">No se encontró la tarea.</div>
    <div v-else>
      <h3 :style="{ color: tarea.color }">
        {{ tarea.nombre }}{{ tarea.id }}
        <span v-if="tarea.esta_realizada" class="completada">
          (Completada)
        </span>
      </h3>
      <p v-if="tarea.descripcion" :style="{ color: tarea.color }">
        {{ tarea.descripcion }}
      </p>
      <p>Fecha límite: {{ formattedFechaLimite }}</p>
      <div class="color-indicator" :style="{ backgroundColor: tarea.color }"></div>
      <p>Estado: {{ tarea.estado ? tarea.estado.nombre : 'Sin Estado' }}</p>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    elemento: {
      type: Object,
      required: true,
    },
    editMode: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      tarea: {},
      loading: false,
      error: false,
    };
  },
  computed: {
    tareaBackground() {
      if (this.loading || this.error || !this.tarea.id) {
        return { backgroundColor: '#f9f9f9' };
      }
      if (!this.tarea.estado) {
        return { backgroundColor: '#f9f9f9' };
      }
      console.log(this.tarea)
      switch (this.tarea.estado.nombre) {
        case 'Completada':
          return { backgroundColor: '#e0ffe0' };
        case 'En Progreso':
          return { backgroundColor: '#ffffe0' };
        case 'Pendiente':
          return { backgroundColor: '#f2f2f2' };
        default:
          return { backgroundColor: '#f9f9f9' };
      }
    },
    formattedFechaLimite() {
      if (!this.tarea.fecha_limite) {
        return '';
      }
      const date = new Date(this.tarea.fecha_limite);
      const day = date.getDate().toString().padStart(2, '0');
      const month = (date.getMonth() + 1).toString().padStart(2, '0');
      const year = date.getFullYear();

      const monthNames = [
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
      ];

      const monthName = monthNames[date.getMonth()];

      return `${day}/${month}/${year}`; // Puedes descomentar la siguiente linea para usar el otro formato
      // return `${day} de ${monthName} de ${year}`;
    },
  },
  async created() {
    await this.fetchTarea();
  },
  watch: {
    elemento: {
      handler: 'fetchTarea',
      immediate: true,
    },
  },
  methods: {
    async fetchTarea() {
      this.loading = true;
      this.error = false;
      this.tarea = {};
      try {
        const response = await fetch(
          `http://localhost:8000/tareas/${this.elemento.object_id}/`
        );
        if (response.ok) {
          this.tarea = await response.json();
        } else {
          console.error('Error al cargar la tarea:', response.status);
          this.error = true;
        }
      } catch (error) {
        console.error('Error al cargar la tarea:', error);
        this.error = true;
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
.tarea-visualizacion {
  padding: 10px;
  border: 1px solid #ccc;
  margin-bottom: 10px;
  border-radius: 5px;
}

.loading,
.error,
.not-found {
  padding: 10px;
  text-align: center;
}

.error {
  color: red;
}

.color-indicator {
  width: 15px;
  height: 15px;
  border-radius: 50%;
  margin: 5px 0;
}

h3 {
  margin-top: 0;
}

.completada {
  font-size: 0.8em;
  color: #666;
  margin-left: 5px;
}
</style>