<template>
  <v-container fluid>
    <div class="text-h5 mb-4">Detalle del Planificador</div>
    <div v-if="planificador" class="mb-4">
      <div><strong>Nombre:</strong> {{ planificador.nombre }}</div>
      <div><strong>Tipo:</strong> {{ planificador.tipo }}</div>
      <div><strong>Última modificación:</strong> {{ formatDate(planificador.fecha_modificacion) }}</div>
    </div>
    <v-row v-if="estructura && estructura.configuracion">
      <v-col cols="12">
        <div class="structure-title">Estructura: {{ estructura.nombre }}</div>
        <v-simple-table>
          <template v-slot:default>
            <thead>
              <tr>
                <th v-for="colIndex in estructura.configuracion.columnas" :key="'col-' + colIndex">
                  Columna {{ colIndex }}
                </th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="rowIndex in Array(estructura.configuracion.filas).fill().map((_, i) => i + 1)" :key="'row-' + rowIndex">
                <td v-for="colIndex in Array(estructura.configuracion.columnas).fill().map((_, i) => i + 1)" :key="'cell-' + rowIndex + '-' + colIndex">
                  <div v-if="celdasMap[rowIndex] && celdasMap[rowIndex][colIndex]">
                    <strong>Contenido:</strong> {{ celdasMap[rowIndex][colIndex].contenido }}
                    <div v-for="elemento in celdasMap[rowIndex][colIndex].elementos" :key="'elemento-' + elemento.id">
                      <strong>Elemento:</strong> {{ elemento.nombre }} - {{ elemento.descripcion }}
                    </div>
                  </div>
                  <div v-else>
                    Sin contenido
                  </div>
                </td>
              </tr>
            </tbody>
          </template>
        </v-simple-table>
      </v-col>
    </v-row>
    <div v-else>
      <div>No hay estructura asociada al planificador.</div>
    </div>
    <v-btn color="primary" @click="$router.push({ name: 'Planificadores' })">
      Volver a la lista
    </v-btn>
  </v-container>
</template>
<script>
export default {
  name: 'PlanificadorDetalle',
  data() {
    return {
      planificador: null,
      estructura: null,
      celdasMap: {}, // Mapeo de filas y columnas con sus celdas y elementos
    };
  },
  async mounted() {
    const id = this.$route.params.id;
    await this.fetchPlanificador(id);
    await this.fetchCeldas(id);
  },
  methods: {
    async fetchPlanificador(id) {
      try {
        const response = await fetch(`http://localhost:8000/planificadores/${id}/`);
        if (!response.ok) {
          throw new Error('Error al obtener los detalles del planificador');
        }
        this.planificador = await response.json();
        this.estructura = this.planificador.estructura;
      } catch (error) {
        console.error(error);
      }
    },
    async fetchCeldas(planificadorId) {
      try {
        const response = await fetch(`http://localhost:8000/celdas/?planificador=${planificadorId}`);
        if (!response.ok) {
          throw new Error('Error al obtener las celdas del planificador');
        }
        const data = await response.json();

        // Asegúrate de acceder al array dentro de `results`
        const celdas = data.results;
        this.mapCeldas(celdas);
      } catch (error) {
        console.error(error);
      }
    },

    mapCeldas(celdas) {
      const map = {};
      celdas.forEach(celda => {
        const { fila, columna } = celda; // Asegúrate de que `fila` y `columna` existen en tus datos
        if (!map[fila]) {
          map[fila] = {};
        }
        map[fila][columna] = celda;
      });
      this.celdasMap = map;
    },
  },

};
</script>
