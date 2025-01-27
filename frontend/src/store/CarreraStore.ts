import { defineStore } from "pinia";

interface PlanDeEstudio {
  id: string;
  nombre: string;
}

interface EstadoCarrera {
  estadisticas_generales: {
    total_creditos: number;
    creditos_aprobados: number;
    promedio: number | null;
  };
  desglose_ciclos: {
    materia__ciclo: string;
    total_creditos: number;
    obtenidos: number;
  }[];
  plan_actual: PlanDeEstudio;
  ultima_actualizacion: string;
}

interface CicloProgreso {
  nombre: string;
  porcentaje: number;
  creditos: string;
}

export const useCarreraStore = defineStore("graph", {
    state: () => ({
      estadoCarrera: null as EstadoCarrera | null,
      loading: false,
      error: null as string | null
    }),

    actions: {
      async fetchEstadoCarrera() {
        this.loading = true;
        try {
          const response = await api.get('carrera/estado/');
          this.estadoCarrera = response.data;
        } catch (error) {
          this.error = 'Error cargando estado de carrera';
        } finally {
          this.loading = false;
        }
      },

      async refreshEstado() {
        await this.fetchEstadoCarrera();
      }
    },

    getters: {
      creditosTotales: (state) => state.estadoCarrera?.estadisticas_generales.total_creditos || 0,
      creditosAprobados: (state) => state.estadoCarrera?.estadisticas_generales.creditos_aprobados || 0,
      promedio: (state) => state.estadoCarrera?.estadisticas_generales.promedio || 0,

      ciclosProgreso(): CicloProgreso[] {
        return this.estadoCarrera?.desglose_ciclos.map(c => ({
          nombre: c.materia__ciclo,
          porcentaje: (c.obtenidos / c.total_creditos) * 100,
          creditos: `${c.obtenidos}/${c.total_creditos}`
        })) || [];
      }
    }
  });

