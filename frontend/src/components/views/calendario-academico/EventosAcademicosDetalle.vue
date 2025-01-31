<template>
  <div v-if="evento" class="detalle-evento">
    <h3>Detalles del Evento</h3>
    <div class="detalle-contenido">
      <p v-for="(value, key) in evento" :key="key">
        <strong>{{ key }}:</strong> {{ value }}
      </p>
    </div>
    <div class="botones">
      <button @click="editarEvento">Editar</button>
      <button @click="eliminarEvento">Eliminar</button>
      <button @click="cerrar">Cerrar</button>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { useEventoAcademicoStore } from "@store/eventoAcademicoStore";

export default defineComponent({
  props: {
    evento: {
      type: Object,
      required: true,
    },
  },
  emits: ["cerrar"],
  setup(props) {
    const eventoAcademicoStore = useEventoAcademicoStore();

    // Función para editar el evento
    const editarEvento = () => {
      const id = props.evento.id; // Obtener el ID directamente del evento

      // Redirigir a un formulario de edición o abrir un modal de edición
      console.log(`Editar evento con ID: ${id}`);
      alert(`Editar evento con ID: ${id}`);
      // Aquí puedes implementar la lógica para abrir un formulario de edición
    };

    // Función para eliminar el evento
    const eliminarEvento = async () => {
      const id = props.evento.id; // Obtener el ID directamente del evento
      const tipo = props.evento.type.split("-")[0] || "desconocido"; // Obtener el tipo del evento
      console.log(tipo)
      try {
        switch (tipo) {
          case "meta":
            await eventoAcademicoStore.deleteMeta(id);
            break;
          case "progreso":
            await eventoAcademicoStore.deleteProgreso(id);
            break;
          case "recordatorio":
            await eventoAcademicoStore.deleteRecordatorio(id);
            break;
          case "evento-academico":
            await eventoAcademicoStore.deleteEventoAcademico(id);
            break;
          case "planificacion":
            await eventoAcademicoStore.deletePlanificacion(id);
            break;
          case "actividad":
            await eventoAcademicoStore.deleteActividadAcademica(id);
            break;
          default:
            console.warn(`Tipo de evento desconocido: ${tipo}`);
        }
        console.log(`${tipo.charAt(0).toUpperCase() + tipo.slice(1)} eliminado exitosamente.`);
      } catch (error) {
        console.error(`Error al eliminar evento:`, error);
        console.log(`Error al eliminar el evento.`);
      }
    };

    return {
      editarEvento,
      eliminarEvento,
    };
  },
  methods: {
    cerrar() {
      this.$emit("cerrar");
    },
  },
});
</script>

<style scoped>
.detalle-evento {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  z-index: 1000;
}
.detalle-contenido {
  margin-bottom: 10px;
}
.botones {
  display: flex;
  gap: 10px;
}
button {
  padding: 5px 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
button:nth-child(1) {
  background-color: #28a745; /* Verde para Editar */
  color: white;
}
button:nth-child(2) {
  background-color: #dc3545; /* Rojo para Eliminar */
  color: white;
}
button:nth-child(3) {
  background-color: #007bff; /* Azul para Cerrar */
  color: white;
}
button:hover {
  opacity: 0.9;
}
</style>
