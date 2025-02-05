<template>
  <div>
    <v-btn
        variant="plain
        "v-if="!isVisible"
        v-ripple="false"
        @click="toggleVisibility" color="primary" size="x-large"
        title="Mostrar más detalle del plan de estudios" >
      Mostrar más
      <v-icon >
        mdi mdi-chevron-up
      </v-icon>
    </v-btn>
    <!-- Componente condicional -->
    <v-container v-if="isVisible" class="graph-estado-carrera" fluid>
      <v-row align="center" justify="space-between" class="h-100">
        <v-col cols="1" class="py-0">
          <v-icon @click="toggleVisibility" size="50px" color="primary" class="mb-4">
            {{ isVisible ? 'mdi-chevron-down' : 'mdi-chevron-down' }}
          </v-icon>
        </v-col>

        <!-- Primera columna: Créditos -->
        <v-col cols="1" class="py-0">
          <div class="creditos">
            <span class="icon">🎓</span>
            <div class="info">
              <span class="creditos-obtenidos">{{ creditos.obtenidos }} de {{ creditos.total }}</span>
              <span class="porcentaje" :style="{ color: colorPorcentaje }">{{ creditos.porcentaje }}%</span>
            </div>
          </div>
        </v-col>

        <!-- Segunda columna: Barras de progreso por ciclos -->
        <v-col cols="8" class="py-0">
          <div class="barras-ciclos">
            <div
              v-for="(ciclo, index) in ciclos"
              :key="index"
              class="barra-ciclo"
              @mouseover="mostrarDetalleCiclo(ciclo)"
              @mouseleave="ocultarDetalleCiclo"
            >
              <div class="nombre-ciclo">{{ ciclo.nombre }}</div>
              <div class="barra-progreso-ciclo">
                <div
                  class="progreso"
                  :style="{
                    width: `${ciclo.porcentaje}%`,
                    backgroundColor: coloresCiclos[index]
                  }"
                ></div>
                <span class="porcentaje-ciclo">{{ ciclo.porcentaje }}%</span>
              </div>
            </div>
          </div>
          <div v-if="detalleCiclo" class="detalle-ciclo">
            <p><strong>{{ detalleCiclo.nombre}}</strong>: {{ detalleCiclo.creditos_obtenidos }} de {{ detalleCiclo.total_creditos }} créditos/materias</p>
          </div>
          <div v-else class="detalle-ciclo">
            <p><strong>Ciclos y/o materias promocionadas.</strong></p>
          </div>
        </v-col>

        <!-- Tercera columna: Promedio -->
        <v-col cols="2" class="py-0">
          <div class="promedio">
            <span class="icon">🏆</span>
            <span class="valor-promedio">{{ promedio.valor }}</span>
          </div>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from "vue";
import { useGraphStore } from "@store/GraphStore";

export default {
  name: "GraphEstadoCarrera",
  setup() {
    const store = useGraphStore();
    const creditos = ref({ obtenidos: 0, total: 0, porcentaje: 0 });
    const ciclos = ref([]);
    const promedio = ref({ valor: 0, materias_cursadas: 0 });
    const detalleCiclo = ref(null);
    const selectedPlan = computed(() => store.selectedPlan);
    const isVisible = ref(true); // Variable para controlar la visibilidad
    // Colores para los ciclos
    const coloresCiclos = ["#FF6B6B", "#4ECDC4", "#FFD166", "#06D6A0", "#118AB2"];

    // Obtener datos del estado de la carrera
    const obtenerEstadoCarrera = async () => {
      try {
        if (!selectedPlan.value) return;
        const response = await store.fetchEstadoCarrera(selectedPlan.value);
        creditos.value = response.creditos;
        ciclos.value = response.ciclos;
        promedio.value = response.promedio;
        console.log(response.plan_actual.nombre)
      } catch (error) {
        console.error("Error obteniendo el estado de la carrera:", error);
      }
    };

    // Observar cambios en selectedPlan
    watch(selectedPlan, (newVal) => {
      if (newVal) obtenerEstadoCarrera();
    });

    // Mostrar detalles del ciclo al hacer hover
    const mostrarDetalleCiclo = (ciclo) => {
      detalleCiclo.value = ciclo;
    };

    // Ocultar detalles del ciclo al salir del hover
    const ocultarDetalleCiclo = () => {
      detalleCiclo.value = null;
    };

    // Color dinámico para el porcentaje de créditos
    const colorPorcentaje = computed(() => {
      const porcentaje = creditos.value.porcentaje;
      if (porcentaje < 33) return "#FF6B6B";
      if (porcentaje < 66) return "#FFD166";
      return "#06D6A0";
    });

    // Alternar visibilidad del componente
    const toggleVisibility = () => {
      isVisible.value = !isVisible.value;
    };

    // Cargar datos al montar el componente
    onMounted(() => {
      obtenerEstadoCarrera();
    });

    return {
      creditos,
      ciclos,
      promedio,
      detalleCiclo,
      coloresCiclos,
      colorPorcentaje,
      mostrarDetalleCiclo,
      ocultarDetalleCiclo,
      isVisible,
      toggleVisibility,
    };
  },
};
</script>

<style scoped>
.graph-estado-carrera {
  background: linear-gradient(180deg, #2c2c3e, #1e1e2f);
  color: #fff;
  border-radius: 0 0 12px 12px;
  padding: 10px 20px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
  height: 120px; /* Altura reducida */
  width: 100%;
}

.creditos,
.promedio {
  display: flex;
  align-items: center;
  gap: 8px;
}

.icon {
  font-size: 22px;
}

.info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.creditos-obtenidos {
  font-size: 14px;
  font-weight: bold;
}

.porcentaje {
  font-size: 12px;
  font-weight: bold;
}

.barras-ciclos {
  display: flex;
  flex-direction: row;
  gap: 15px;
  height: 70px;
}

.barra-ciclo {
  display: flex;
  flex-direction: column;
  gap: 4px;
  flex: 1;
  min-width: 80px;
}

.nombre-ciclo {
  font-size: 12px;
  font-weight: bold;
  text-align: center;
  margin-bottom: 2px;
}

.barra-progreso-ciclo {
  display: flex;
  align-items: center;
  width: 100%;
  height: 16px;
  background-color: #3a3a4e;
  border-radius: 8px;
  overflow: hidden;
  position: relative;
}

.progreso {
  height: 100%;
  transition: width 0.3s ease;
}

.porcentaje-ciclo {
  font-size: 10px;
  color: #fff;
  position: absolute;
  right: 4px;
  mix-blend-mode: difference;
}

.detalle-ciclo {
  bottom: 5px;
  width: 100%;
  font-size: 15px;
  text-align: center;
}

.promedio .valor-promedio {
  font-size: 22px;
  font-weight: bold;
}
.h-100 {
  height: 100%;
}
</style>