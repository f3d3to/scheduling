<template>
  <div v-if="planificador" class="planificador">
    <h1 class="titulo">{{ planificador.nombre }}</h1>
    <p class="tipo">Tipo: {{ planificador.tipo }}</p>
    {{ planificador.estructura }}
    <!-- Representación dinámica de la grilla -->
    <div class="planificador-grid" :style="gridStyle">
      <div
        v-for="celda in planificador.celdas"
        :key="celda.id"
        class="celda"
      >
        <h3 class="titulo-celda">{{ celda.contenido }}</h3>
        <ul class="elementos">
          <li v-for="elemento in celda.elementos" :key="elemento.id" class="elemento">
            <strong>{{ elemento.nombre }}</strong>: {{ elemento.descripcion }}
          </li>
        </ul>
      </div>
    </div>
  </div>
  <div v-else class="cargando">
    <p>Cargando planificador...</p>
  </div>
</template>

<script>
export default {
  props: {
    id: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      planificador: null,
    };
  },
  computed: {
    gridStyle() {
      if (!this.planificador) return {};
      const filas = this.planificador.estructura?.configuracion?.filas || 1;
      const columnas = this.planificador.estructura?.configuracion?.columnas || 1;
      return {
        display: "grid",
        gridTemplateRows: `repeat(${filas}, 1fr)`,
        gridTemplateColumns: `repeat(${columnas}, 1fr)`,
        gap: "10px",
      };
    },
  },
  methods: {
    async fetchPlanificador() {
      if (!this.id) {
        console.error("id no está definido");
        return;
      }
      try {
        const response = await fetch(
          `http://localhost:8000/planificadores/${this.id}/`
        );
        if (!response.ok) {
          throw new Error("Error al cargar el planificador");
        }
        this.planificador = await response.json();
      } catch (error) {
        console.error("Error al cargar el planificador:", error);
      }
    },
  },
  mounted() {
    this.fetchPlanificador();
  },
};
</script>

<style scoped>
.planificador {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
}

.titulo {
  text-align: center;
  font-size: 2rem;
  margin-bottom: 10px;
  color: #007BFF;
}

.tipo {
  text-align: center;
  font-size: 1.2rem;
  margin-bottom: 20px;
}

.planificador-grid {
  display: grid;
  background: #f7f7f7;
  padding: 10px;
  border-radius: 8px;
}

.celda {
  background: #fff;
  border: 1px solid #ddd;
  border-radius: 5px;
  padding: 15px;
  display: flex;
  flex-direction: column;
}

.titulo-celda {
  font-size: 1.1rem;
  font-weight: bold;
  margin-bottom: 10px;
}

.elementos {
  list-style: none;
  padding: 0;
  margin: 0;
}

.elemento {
  font-size: 0.9rem;
  border-bottom: 1px solid #ddd;
  padding: 5px;
}

.elemento:last-child {
  border-bottom: none;
}

.cargando {
  text-align: center;
  margin-top: 50px;
  font-size: 1.2rem;
  color: #777;
}
</style>
