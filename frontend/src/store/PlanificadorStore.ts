// PlanificadorStore.ts
import { defineStore } from 'pinia';
import { api } from '../services/apiServiceAuth';

// Interfaces para TypeScript
interface Celda {
  id: number;
  contenido: string;
  w: number;
  h: number;
  coordenadas: string;
}

interface LayoutItem {
  i: string;
  x: number;
  y: number;
  w: number;
  h: number;
}

export const usePlanificadorStore = defineStore('planificador', {
  state: () => ({
    layout: [] as LayoutItem[],
    celdas: [] as Celda[],
    columnas: 7,
    layoutGenerado: false,
    isEditing: false,
    nombre: '',
    showAddCeldaDialog: false,
    originalLayout: [] as LayoutItem[],
    nombrePlanificador: '',
    filas: 0,
    anchoColumna: 0,

    planners: [] as any[],
    templates: [] as any[],
    templateTypes: [] as string[],
  }),

  actions: {
    async fetchData(planificadorId: string) {
      try {
        const response = await api.get(`estructuras-planificador/${planificadorId}/`);
        const data = response.data;

        // Actualizar estado
        this.columnas = data.columnas;
        this.nombre = data.nombre;
        this.nombrePlanificador = data.nombre;
        this.filas = data.filas;
        this.anchoColumna = data.ancho_columna;

        // Procesar celdas
        this.celdas = Object.entries(data.tabla).map(([coordenadas, celda]: [string, any]) => ({
          ...celda,
          coordenadas,
        }));

        // Generar layout
        this.layout = this.celdas.map(celda => {
          const [fila, columna] = celda.coordenadas.split(',').map(Number);
          return {
            i: String(celda.id),
            x: columna - 1,
            y: fila - 1,
            w: celda.w,
            h: celda.h,
          };
        });

        this.layoutGenerado = true;
      } catch (error) {
        console.error('Error fetching planner data:', error);
        throw error;
      }
    },

    toggleEditMode() {
      if (!this.isEditing) {
        this.originalLayout = JSON.parse(JSON.stringify(this.layout));
      }
      this.isEditing = !this.isEditing;
    },

    cancelChanges() {
      this.layout = JSON.parse(JSON.stringify(this.originalLayout));
      this.isEditing = false;
    },

    async eliminarCelda(planificadorId: string, celdaId: number) {
      try {
        await api.delete(`planificadores/${planificadorId}/celdas/${celdaId}/`);

        // Actualizar estado local
        this.layout = this.layout.filter(item => item.i !== String(celdaId));
        this.celdas = this.celdas.filter(celda => celda.id !== celdaId);
      } catch (error) {
        console.error('Error deleting cell:', error);
        throw error;
      }
    },

    async saveLayout(planificadorId: string) {
      try {
        const tablaActualizada: Record<string, any> = {};

        this.layout.forEach(item => {
          const celda = this.getCeldaById(item.i);
          if (celda) {
            tablaActualizada[`${item.y + 1},${item.x + 1}`] = {
              id: celda.id,
              contenido: celda.contenido,
              w: celda.w,
              h: celda.h,
            };
          }
        });

        const requestBody = {
          tabla: tablaActualizada,
          nombre: this.nombrePlanificador,
          columnas: this.columnas,
          filas: this.filas,
          ancho_columna: this.anchoColumna,
        };

        await api.patch(`estructuras-planificador/${planificadorId}/`, requestBody);
        this.isEditing = false;
      } catch (error) {
        console.error('Error saving layout:', error);
        throw error;
      }
    },

    handleLayoutUpdate() {
      this.showAddCeldaDialog = false;
    },
    async fetchPlanners() {
        try {
          const response = await api.get('planificadores/');
          this.planners = response.data.results || [];
        } catch (error) {
          console.error('Error fetching planners:', error);
          throw error;
        }
      },

      async fetchTemplates() {
        try {
          const response = await api.get('estructuras-planificador/');
          this.templates = response.data.results || [];
          this.templateTypes = this.templates.map(t => t.nombre);
        } catch (error) {
          console.error('Error fetching templates:', error);
          throw error;
        }
      },

      async createPlanner(data: any) {
        try {
          await api.post('planificadores/', data);
          await this.fetchPlanners();
        } catch (error) {
          console.error('Error creating planner:', error);
          throw error;
        }
      },

      async updatePlanner(id: string, data: any) {
        try {
          await api.patch(`planificadores/${id}/`, data);
          await this.fetchPlanners();
        } catch (error) {
          console.error('Error updating planner:', error);
          throw error;
        }
      },

      async deletePlanner(id: string) {
        try {
          await api.delete(`planificadores-eliminar/${id}/`);
          await this.fetchPlanners();
        } catch (error) {
          console.error('Error deleting planner:', error);
          throw error;
        }
      },

      async createFromTemplate(template: any) {
        try {
          await api.post('planificadores/', {
            nombre: `Planificador - ${template.nombre}`,
            tipo: template.nombre,
            estructura: template.id
          });
          await this.fetchPlanners();
        } catch (error) {
          console.error('Error creating from template:', error);
          throw error;
        }
      }

  },

  getters: {
    getCeldaById: (state) => (id: string) => {
      return state.celdas.find(celda => celda.id === parseInt(id));
    },
  },
});