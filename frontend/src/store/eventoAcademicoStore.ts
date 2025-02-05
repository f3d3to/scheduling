import { defineStore } from 'pinia';
import { api } from '../services/apiServiceAuth';

// Interfaces
interface Categoria {
  categoria: string; // Nombre técnico del modelo (e.g., "eventoacademico")
  nombre: string; // Nombre legible para el usuario (e.g., "Evento Académico")
}

interface Elemento {
  id: number;
  nombre: string; // Nombre legible del elemento (e.g., "Clase de Matemáticas")
}

interface Recurrencia {
  id: number;
  frecuencia: string; // Diaria, semanal, mensual, anual
  intervalo: number; // Cada cuántas unidades se repite
  fin_recurrencia: string | null; // Fecha de fin de la recurrencia (ISO string)
}

interface TipoEvento {
  id: number;
  nombre: string; // Nombre del tipo de evento (e.g., "Clase", "Examen")
  descripcion: string; // Descripción del tipo de evento
}

interface EventoCalendarioAcademico {
  id?: number;
  titulo: string;
  descripcion?: string | null;
  inicio: string; // ISO datetime string (e.g., "2023-10-01T09:00:00")
  fin?: string | null; // ISO datetime string (e.g., "2023-10-01T11:00:00")
  todo_el_dia: boolean;
  color?: string | null;
  background_color?: string | null;
  border_color?: string | null;
  text_color?: string | null;
  url?: string | null;
  tipo: TipoEvento; // Objeto TipoEvento
  recurrencia?: Recurrencia | null; // Objeto Recurrencia
  content_type: string; // Nombre del modelo relacionado (e.g., "evento_academico.eventoacademico")
  object_id: number; // ID del objeto relacionado
  rrule?: string | null; // Regla de recurrencia generada dinámicamente por el backend
  display: string; // Modo de visualización (block, background, etc.)
  editable: boolean; // Indica si el evento es editable
  start_editable: boolean; // Indica si la fecha/hora de inicio es editable
  duration_editable: boolean; // Indica si la duración es editable
  resource_editable: boolean; // Indica si el evento puede moverse entre recursos
  exdate?: string | null; // Fechas excluidas de la recurrencia
  class_names?: string | null; // Clases CSS adicionales
}

export const useEventoAcademicoStore = defineStore('eventoAcademico', {
  state: () => ({
    // Eventos del calendario académico
    eventosCalendario: [] as EventoCalendarioAcademico[],
    // Categorías disponibles
    categorias: [] as Categoria[],
    // Elementos de una categoría específica
    elementos: [] as Elemento[],
    recurrencias: [] as Recurrencia[],
    tipos: [] as TipoEvento[],
  }),
  actions: {
    /**
     * Obtiene los tipos de eventos desde el backend.
     */
    async fetchTiposEvento() {
      try {
        const response = await api.get('tipos-evento/');
        this.tipos = response.data.results;
      } catch (error) {
        console.error('Error al cargar tipos de eventos:', error);
      }
    },

    /**
     * Obtiene las recurrencias disponibles desde el backend.
     */
    async fetchRecurrencias() {
      try {
        const response = await api.get('recurrencias/');
        this.recurrencias = response.data.results;
      } catch (error) {
        console.error('Error al cargar recurrencias:', error);
      }
    },

    /**
     * Obtiene los eventos del calendario académico desde el backend.
     */
    async fetchEventosCalendario() {
      try {
        const response = await api.get('eventos-calendario/');
        this.eventosCalendario = response.data.results; // Guardar los eventos en el estado
      } catch (error) {
        console.error('Error al cargar los eventos del calendario:', error);
      }
    },

    /**
     * Transforma las instancias de los modelos en eventos de FullCalendar.
     * @returns Un array de eventos compatibles con FullCalendar.
     */
    getFullCalendarEvents(): any[] {
      const events: any[] = [];
      if (Array.isArray(this.eventosCalendario)) {
        this.eventosCalendario.forEach((evento) => {
          console.log(evento.rrule, evento.todo_el_dia);
          events.push({
            id: `evento-calendario-${evento.id}`,
            title: evento.titulo,
            start: evento.inicio, // Fecha y hora de inicio
            end: evento.fin ?? evento.inicio, // Si no hay fin, usa el inicio
            allDay: evento.todo_el_dia, // Indica si es un evento de todo el día
            color: evento.background_color ?? '#378006', // Color de fondo
            textColor: evento.text_color ?? '#FFFFFF', // Color del texto
            borderColor: evento.border_color ?? '#000000', // Color del borde
            classNames: evento.class_names ? evento.class_names.split(' ') : ['calendar-event'], // Clases CSS personalizadas
            display: evento.display || 'block', // Modo de visualización (block, background, etc.)
            editable: evento.editable, // Indica si el evento es editable
            startEditable: evento.start_editable, // Indica si la fecha/hora de inicio es editable
            durationEditable: evento.duration_editable, // Indica si la duración es editable
            resourceEditable: evento.resource_editable, // Indica si el evento puede moverse entre recursos
            exdate: evento.exdate || null, // Fechas excluidas de la recurrencia
            rrule: evento.rrule || null, // Regla de recurrencia generada dinámicamente por el backend
            extendedProps: {
              type: 'evento-calendario',
              description: evento.descripcion,
              url: evento.url,
              recurrence: evento.recurrencia
                ? {
                    frecuencia: evento.recurrencia.frecuencia,
                    intervalo: evento.recurrencia.intervalo,
                    fin_recurrencia: evento.recurrencia.fin_recurrencia,
                  }
                : null, // Recurrencia completa
              tipo: evento.tipo, // Objeto TipoEvento completo
              relatedModel: evento.content_type, // Modelo relacionado
              relatedId: evento.object_id, // ID del objeto relacionado
            },
          });
        });
      }
      return events;
    },

    /**
     * Obtiene las categorías disponibles desde el backend.
     */
    async fetchCategorias() {
      try {
        const response = await api.get('categorias-disponibles/');
        this.categorias = response.data.map((item: any) => ({
          categoria: item.categoria, // Aseguramos que coincida con la interfaz
          nombre: item.nombre,
        }));
      } catch (error) {
        console.error('Error al cargar categorías:', error);
      }
    },

    /**
     * Obtiene los elementos de una categoría específica.
     * @param categoria - Nombre técnico de la categoría (e.g., "eventoacademico").
     */
    async fetchElementos(categoria: string) {
      try {
        const response = await api.get(`elementos/${categoria}/`);
        this.elementos = response.data; // Guardar los elementos en el estado
      } catch (error) {
        console.error('Error al cargar elementos:', error);
      }
    },

    /**
     * Crea un nuevo evento del calendario académico.
     * @param evento - Datos del nuevo evento.
     */
    async crearEvento(evento: any) {
      try {
        const payload = {
          ...evento,
          tipo: evento.tipo, // Enviar solo el ID del tipo
          recurrencia: evento.recurrencia?.id || null, // Enviar solo el ID de la recurrencia
        };
        console.log("Payload enviado al backend:", payload); // Depurar el payload
        await api.post('eventos-calendario/', payload);
        console.log('Evento creado exitosamente.');
        // Recargar los eventos después de crear uno nuevo
        await this.fetchEventosCalendario();
      } catch (error) {
        console.error('Error al crear el evento:', error);
        throw error; // Propagar el error para manejarlo en el componente
      }
    },

    /**
     * Obtiene los detalles de un evento por su ID.
     * @param eventoId - ID del evento.
     * @returns Detalles del evento o undefined si no se encuentra.
     */
    getDetallesPorId(eventoId: number): EventoCalendarioAcademico | undefined {
      return this.eventosCalendario.find((evento) => evento.id === eventoId);
    },
  },
});