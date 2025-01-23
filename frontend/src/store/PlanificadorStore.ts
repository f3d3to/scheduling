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

interface Elemento {
  id: number;
  nombre: string;
  color: string;
  celda: number;
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
    elementos: [] as Elemento[], // Nuevo estado para elementos
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

    async saveLayoutCelda(planificadorId: string, data: any) {
      try {
        const tablaActualizada: Record<string, any> = {};

        data.layout.forEach(item => {
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
          columnas: data.columnas,
          filas: data.filas,
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
          estructura: template.id,
        });
        await this.fetchPlanners();
      } catch (error) {
        console.error('Error creating from template:', error);
        throw error;
      }
    },

    // Nuevas acciones para manejar elementos
    async updateCelda(planificadorId: string, celdaId: number, data: any) {
      try {
        await api.patch(`planificadores/${planificadorId}/celdas/${celdaId}/`, data);
      } catch (error) {
        console.error('Error updating cell:', error);
        throw error;
      }
    },

    async fetchElementos(celdaId: number) {
      try {
        const response = await api.get(`elementos/?celda=${celdaId}`);
        this.elementos = response.data.results || [];
      } catch (error) {
        console.error('Error fetching elementos:', error);
        throw error;
      }
    },
    async fetchElementoDetalle(contentType: string, objectId: number) {
      try {
        const response = await api.get(`elementos/detalle/${contentType}/${objectId}/`);
        return response.data;
      } catch (error) {
        console.error('Error fetching elemento detalle:', error);
        throw error;
      }
    },

    async eliminarElemento(elementoId: number) {
      try {
        await api.delete(`elementos/${elementoId}/`);
      } catch (error) {
        console.error('Error deleting elemento:', error);
        throw error;
      }
    },
    async fetchModels() {
      try {
        const response = await api.get("models/");
        return response.data; // Asegúrate de que la API devuelva los resultados en `results`
      } catch (error) {
        console.error('Error fetching models:', error);
        throw error;
      }
    },

    async createInstance(data: any) {
      try {
        const response = await api.post("models/", data);
        return response;
      } catch (error) {
        console.error('Error creating instance:', error);
        throw error;
      }
    },

    async asociarElemento(planificadorId: number, celdaId: number, instanciaId: number, model: string) {
      try {
        const response = await api.post(`celdas/${planificadorId}/${celdaId}/elementos/`, {
          instancia_id: instanciaId,
          model: model,
        });
        return response.data;
      } catch (error) {
        console.error('Error asociando elemento:', error);
        throw error;
      }
    },
    async updateEstructura(planificadorId: string, data: any) {
      try {
          const response = await api.post(`planificador/estructura/actualizar/${planificadorId}/`, {
              filas: data.filas,
              columnas: data.columnas,
              tabla: data.tabla,
              celdas: data.celdas
          });

          // Actualizar estado local
          await this.fetchData(planificadorId);
          return response.data;
      } catch (error) {
          console.error('Error actualizando estructura:', error);
          throw error;
      }
  },

  },

  getters: {
    getCeldaById: (state) => (id: string) => {
      return state.celdas.find(celda => celda.id === parseInt(id));
    },

    // Nuevo getter para obtener elementos por celdaId
    getElementosByCeldaId: (state) => (celdaId: number) => {
      return state.elementos.filter(elemento => elemento.celda === celdaId);
    },
  },
});