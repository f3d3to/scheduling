import { defineStore } from 'pinia';
import { api } from '../services/apiServiceAuth';

// Interfaces para TypeScript
interface EventoAcademico {
  id: number;
  nombre: string;
  tipo: string;
  dia: string;
  hora_inicio: string;
  hora_fin: string;
  descripcion: string;
  profesor: string;
  aula: string;
  es_obligatorio: boolean;
  recursos: string;
}

interface PlanificacionAcademica {
  id: number;
  estudiante: number;
  tipo: string;
  cuatrimestre: string;
  año: number;
  semana: number;
  nombre: string;
  actividades: EventoAcademico[];
}

interface LayoutItem {
  i: string;
  x: number;
  y: number;
  w: number;
  h: number;
}

export const usePlanificadorAcademicoStore = defineStore('planificadorAcademico', {
  state: () => ({
    layout: [] as LayoutItem[],
    eventos: [] as EventoAcademico[],
    planificaciones: [] as PlanificacionAcademica[],
    isEditing: false,
    showAddEventoDialog: false,
    originalLayout: [] as LayoutItem[],
    nombrePlanificador: '',
    columnas: 7,
    filas: 0,
    anchoColumna: 0,
  }),

  actions: {
    async fetchData(planificadorId: string) {
      try {
        const response = await api.get(`planificadores-academicos/${planificadorId}/`);
        const data = response.data;

        // Actualizar estado
        this.columnas = data.columnas;
        this.nombrePlanificador = data.nombre;
        this.filas = data.filas;
        this.anchoColumna = data.ancho_columna;

        // Procesar eventos
        this.eventos = data.eventos;

        // Generar layout
        this.layout = this.eventos.map(evento => {
          const [fila, columna] = evento.dia.split(',').map(Number);
          return {
            i: String(evento.id),
            x: columna - 1,
            y: fila - 1,
            w: 1,
            h: 1,
          };
        });

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

    async eliminarEventoAcademico(planificadorId: string, eventoId: number) {
      try {
        await api.delete(`planificadores-academicos/${planificadorId}/eventos/${eventoId}/`);

        // Actualizar estado local
        this.layout = this.layout.filter(item => item.i !== String(eventoId));
        this.eventos = this.eventos.filter(evento => evento.id !== eventoId);
      } catch (error) {
        console.error('Error deleting event:', error);
        throw error;
      }
    },

    async saveLayoutEvento(planificadorId: string, data: any) {
      try {
        const tablaActualizada: Record<string, any> = {};

        data.layout.forEach(item => {
          const evento = this.getEventoById(item.i);
          if (evento) {
            tablaActualizada[`${item.y + 1},${item.x + 1}`] = {
              id: evento.id,
              nombre: evento.nombre,
              tipo: evento.tipo,
              dia: evento.dia,
              hora_inicio: evento.hora_inicio,
              hora_fin: evento.hora_fin,
              descripcion: evento.descripcion,
              profesor: evento.profesor,
              aula: evento.aula,
              es_obligatorio: evento.es_obligatorio,
              recursos: evento.recursos,
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

        await api.patch(`planificadores-academicos/${planificadorId}/`, requestBody);
        this.isEditing = false;
      } catch (error) {
        console.error('Error saving layout:', error);
        throw error;
      }
    },

    async fetchPlanificaciones() {
      try {
        const response = await api.get('planificaciones-academicas/');
        this.planificaciones = response.data.results || [];
      } catch (error) {
        console.error('Error fetching planificaciones:', error);
        throw error;
      }
    },

    async createPlanificacion(data: any) {
      try {
        await api.post('planificaciones-academicas/', data);
        await this.fetchPlanificaciones();
      } catch (error) {
        console.error('Error creating planificacion:', error);
        throw error;
      }
    },

    async updatePlanificacion(id: string, data: any) {
      try {
        await api.patch(`planificaciones-academicas/${id}/`, data);
        await this.fetchPlanificaciones();
      } catch (error) {
        console.error('Error updating planificacion:', error);
        throw error;
      }
    },

    async deletePlanificacion(id: string) {
      try {
        await api.delete(`planificaciones-academicas-eliminar/${id}/`);
        await this.fetchPlanificaciones();
      } catch (error) {
        console.error('Error deleting planificacion:', error);
        throw error;
      }
    },

    async fetchEventos(planificadorId: string) {
      try {
        const response = await api.get(`planificadores-academicos/${planificadorId}/eventos/`);
        this.eventos = response.data.results || [];
      } catch (error) {
        console.error('Error fetching eventos:', error);
        throw error;
      }
    },

    async createEvento(planificadorId: string, data: any) {
      try {
        await api.post(`planificadores-academicos/${planificadorId}/eventos/`, data);
        await this.fetchEventos(planificadorId);
      } catch (error) {
        console.error('Error creating evento:', error);
        throw error;
      }
    },

    async updateEvento(planificadorId: string, eventoId: number, data: any) {
      try {
        await api.patch(`planificadores-academicos/${planificadorId}/eventos/${eventoId}/`, data);
      } catch (error) {
        console.error('Error updating evento:', error);
        throw error;
      }
    },

    async eliminarEvento(planificadorId: string, eventoId: number) {
      try {
        await api.delete(`planificadores-academicos/${planificadorId}/eventos/${eventoId}/`);
        await this.fetchEventos(planificadorId);
      } catch (error) {
        console.error('Error deleting evento:', error);
        throw error;
      }
    },
  },

  getters: {
    getEventoById: (state) => (id: string) => {
      return state.eventos.find(evento => evento.id === parseInt(id));
    },

    getEventosByDia: (state) => (dia: string) => {
      return state.eventos.filter(evento => evento.dia === dia);
    },
  },
});