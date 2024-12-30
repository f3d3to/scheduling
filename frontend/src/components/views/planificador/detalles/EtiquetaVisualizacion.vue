<template>
    <div class="etiqueta-visualizacion" v-if="etiqueta" @click.stop="$emit('abrir-dialogo', elemento)">
      <span
        class="etiqueta-badge"
        :style="{ backgroundColor: etiqueta.color, color: getTextColor(etiqueta.color) }"
      >
        <i class="fas fa-tag etiqueta-icono" v-if="!dialogOpen"></i>
        <span class="etiqueta-nombre">{{ etiqueta.nombre }}</span>
      </span>
      <div v-if="dialogOpen" class="detalles">
        <p v-if="etiqueta.descripcion" class="descripcion">
          {{ etiqueta.descripcion }}
        </p>
        <p v-if="etiqueta.usuario" class="usuario">
          <strong>Usuario:</strong> {{ etiqueta.usuario }}
        </p>
      </div>
    </div>
    <p v-else>Cargando datos de la etiqueta...</p>
</template>


<script>
export default {
  props: {
    elemento: {
      type: Object,
      required: true,
    },
    dialogOpen: { // Prop para saber si el diálogo está abierto
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      etiqueta: null,
      mostrarDetalles: false,
    };
  },
  async mounted() {
    await this.fetchEtiqueta();
  },
  methods: {
    async fetchEtiqueta() {
      try {
        const response = await fetch(`http://localhost:8000/etiquetas/${this.elemento.object_id}/`);
        if (response.ok) {
          const data = await response.json();
          this.etiqueta = {
            nombre: data.nombre || "Sin nombre",
            descripcion: data.descripcion || "Sin descripción",
            usuario: data.usuario || "Sin usuario",
            color: data.color,
          };
        } else {
          console.error("Error al cargar la etiqueta:", response.statusText);
        }
      } catch (error) {
        console.error("Error al hacer fetch de la etiqueta:", error);
      }
    },
    getTextColor(bgColor) {
      const color = bgColor.charAt(0) === "#" ? bgColor.substring(1, 7) : bgColor;
      const r = parseInt(color.substring(0, 2), 16);
      const g = parseInt(color.substring(2, 4), 16);
      const b = parseInt(color.substring(4, 6), 16);
      const luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255;
      return luminance > 0.5 ? "#000000" : "#FFFFFF";
    },
    toggleDetalles() {
      this.mostrarDetalles = !this.mostrarDetalles;
    },
  },
  watch: {
    elemento: {
      handler: "fetchEtiqueta",
      immediate: true,
      deep: true,
    },
    dialogOpen: {
      handler: function (newVal) {
        if (newVal) {
          this.mostrarDetalles = true; // Mostrar detalles si el diálogo está abierto
        } else {
          this.mostrarDetalles = false; // Ocultar detalles si el diálogo está cerrado o se cierra
        }
      },
      immediate: true,
    },
  },
};
</script>

<style scoped>
.etiqueta-visualizacion {
  display: inline-block;
  margin-right: 5px;
  margin-bottom: 5px;
}

.etiqueta-badge {
  display: inline-flex;
  align-items: center;
  padding: 3px 8px;
  border-radius: 5px;
  font-weight: 500;
  font-size: 0.9em;
  box-shadow: inset 0px -2px 3px rgba(0, 0, 0, 0.2);
  cursor: pointer; /* Indica que se puede ক্লিক করতে */
}

.etiqueta-icono {
  margin-right: 5px;
  font-size: 0.9em;
}

.etiqueta-nombre {
  white-space: nowrap;
}

.detalles {
  padding: 5px;
  margin-top: 5px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: #f8f8f8;
}

.descripcion {
  font-style: italic;
  margin: 2px 0;
}

.usuario {
  font-size: 0.9em;
  margin: 2px 0;
}
</style>