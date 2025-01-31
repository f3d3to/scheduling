import { defineStore } from 'pinia';
import { api } from '../services/apiServiceAuth';
import dayjs from 'dayjs';

// Tipos para los modelos
interface Meta {
  id?: number;
  estudiante: number;
  descripcion: string;
  tipo: string;
  fecha_limite: string;
  prioridad: number;
  completada: boolean;
  relacion_materia?: number | null;
}

interface ProgresoMateria {
  id?: number;
  materia_estudiante: number;
  horas_estudiadas: number;
  temas_completados: number;
  ejercicios_resueltos: number;
  autoevaluaciones: number;
}

interface RecordatorioPersonalizado {
  id?: number;
  usuario: number;
  mensaje: string;
  fecha_hora: string;
  repetir: string;
  canal: string;
  relacion_evento?: number | null;
}

interface EventoAsociado {
  id?: number;
  evento_origen: number;
  evento_destino: number;
  tipo_relacion: string;
  peso: number;
}

interface EventoAcademico {
  id?: number;
  dia: string;
  hora_inicio: string;
  hora_fin: string;
  descripcion_horario: string;
  materia: number;
  tipo: string;
  aula: string;
  profesor: string;
  es_obligatorio: boolean;
  recursos: string;
}

interface PlanificacionAcademica {
  id?: number;
  estudiante: number;
  tipo: string;
  cuatrimestre?: string | null;
  año: number;
  semana?: number | null;
  nombre: string;
}

interface ActividadPlanificada {
  id?: number;
  planificacion: number;
  evento: number;
  completada: boolean;
}

export const useEventoAcademicoStore = defineStore('eventoAcademico', {
  state: () => ({
    metas: [] as Meta[],
    progresos: [] as ProgresoMateria[],
    recordatorios: [] as RecordatorioPersonalizado[],
    eventosAsociados: [] as EventoAsociado[],
    eventosAcademicos: [] as EventoAcademico[],
    planificaciones: [] as PlanificacionAcademica[],
    actividadesAcademicas: [] as ActividadPlanificada[],
  }),
  actions: {
    // Metas
    async fetchMetas() {
      const { data } = await api.get('metas/');
      this.metas = data.results;
    },
    async fetchMeta(id: number) {
      const { data } = await api.get(`metas/${id}/`);
      return data.results;
    },
    async createMeta(meta: Omit<Meta, 'id'>) {
      const { data } = await api.post('metas/', meta);
      this.metas.push(data);
    },
    async updateMeta(id: number, meta: Partial<Meta>) {
      const { data } = await api.put(`metas/${id}/`, meta);
      const index = this.metas.findIndex((m) => m.id === id);
      if (index !== -1) this.metas[index] = { ...this.metas[index], ...data };
    },
    async deleteMeta(id: number) {
      await api.delete(`metas/${id}/`);
      this.metas = this.metas.filter((meta) => meta.id !== id);
    },

    // Progreso
    async fetchProgresos() {
      const { data } = await api.get('progreso/');
      this.progresos = data.results;
    },
    async fetchProgreso(id: number) {
      const { data } = await api.get(`progreso/${id}/`);
      return data.results;
    },
    async createProgreso(progreso: Omit<ProgresoMateria, 'id'>) {
      const { data } = await api.post('progreso/', progreso);
      this.progresos.push(data.results);
    },
    async updateProgreso(id: number, progreso: Partial<ProgresoMateria>) {
      const { data } = await api.put(`progreso/${id}/`, progreso);
      const index = this.progresos.findIndex((p) => p.id === id);
      if (index !== -1) this.progresos[index] = { ...this.progresos[index], ...data.results };
    },
    async deleteProgreso(id: number) {
      await api.delete(`progreso/${id}/`);
      this.progresos = this.progresos.filter((progreso) => progreso.id !== id);
    },

    // Recordatorios
    async fetchRecordatorios() {
      const { data } = await api.get('recordatorios/');
      this.recordatorios = data.results;
    },
    async fetchRecordatorio(id: number) {
      const { data } = await api.get(`recordatorios/${id}/`);
      return data.results;
    },
    async createRecordatorio(recordatorio: Omit<RecordatorioPersonalizado, 'id'>) {
      const { data } = await api.post('recordatorios/', recordatorio);
      this.recordatorios.push(data.results);
    },
    async updateRecordatorio(id: number, recordatorio: Partial<RecordatorioPersonalizado>) {
      const { data } = await api.put(`recordatorios/${id}/`, recordatorio);
      const index = this.recordatorios.findIndex((r) => r.id === id);
      if (index !== -1) this.recordatorios[index] = { ...this.recordatorios[index], ...data.results };
    },
    async deleteRecordatorio(id: number) {
      await api.delete(`recordatorios/${id}/`);
      this.recordatorios = this.recordatorios.filter((recordatorio) => recordatorio.id !== id);
    },

    // Eventos Asociados
    async fetchEventosAsociados() {
      const { data } = await api.get('eventos-asociados/');
      this.eventosAsociados = data.results;
    },
    async fetchEventoAsociado(id: number) {
      const { data } = await api.get(`eventos-asociados/${id}/`);
      return data.results;
    },
    async createEventoAsociado(evento: Omit<EventoAsociado, 'id'>) {
      const { data } = await api.post('eventos-asociados/', evento);
      this.eventosAsociados.push(data.results);
    },
    async updateEventoAsociado(id: number, evento: Partial<EventoAsociado>) {
      const { data } = await api.put(`eventos-asociados/${id}/`, evento);
      const index = this.eventosAsociados.findIndex((e) => e.id === id);
      if (index !== -1) this.eventosAsociados[index] = { ...this.eventosAsociados[index], ...data.results };
    },
    async deleteEventoAsociado(id: number) {
      await api.delete(`eventos-asociados/${id}/`);
      this.eventosAsociados = this.eventosAsociados.filter((evento) => evento.id !== id);
    },

    // Eventos Académicos
    async fetchEventosAcademicos() {
      const { data } = await api.get('eventos-academicos/');
      this.eventosAcademicos = data.results;
    },
    async fetchEventoAcademico(id: number) {
      const { data } = await api.get(`eventos-academicos/${id}/`);
      return data.results;
    },
    async createEventoAcademico(evento: Omit<EventoAcademico, 'id'>) {
      const { data } = await api.post('eventos-academicos/', evento);
      this.eventosAcademicos.push(data.results);
    },
    async updateEventoAcademico(id: number, evento: Partial<EventoAcademico>) {
      const { data } = await api.put(`eventos-academicos/${id}/`, evento);
      const index = this.eventosAcademicos.findIndex((e) => e.id === id);
      if (index !== -1) this.eventosAcademicos[index] = { ...this.eventosAcademicos[index], ...data.results };
    },
    async deleteEventoAcademico(id: number) {
      await api.delete(`eventos-academicos/${id}/`);
      this.eventosAcademicos = this.eventosAcademicos.filter((evento) => evento.id !== id);
    },

    // Planificaciones
    async fetchPlanificaciones() {
      const { data } = await api.get('planificaciones/');
      // console.log('Datos de planificaciones:', data.results); // Depuración
      this.planificaciones = data.results;
    },
    async fetchPlanificacion(id: number) {
      const { data } = await api.get(`planificaciones/${id}/`);
      return data.results;
    },
    async createPlanificacion(planificacion: Omit<PlanificacionAcademica, 'id'>) {
      const { data } = await api.post('planificaciones/', planificacion);
      this.planificaciones.push(data.results);
    },
    async updatePlanificacion(id: number, planificacion: Partial<PlanificacionAcademica>) {
      const { data } = await api.put(`planificaciones/${id}/`, planificacion);
      const index = this.planificaciones.findIndex((p) => p.id === id);
      if (index !== -1) this.planificaciones[index] = { ...this.planificaciones[index], ...data.results };
    },
    async deletePlanificacion(id: number) {
      await api.delete(`planificaciones/${id}/`);
      this.planificaciones = this.planificaciones.filter((planificacion) => planificacion.id !== id);
    },

    // Actividades Académicas
    async fetchActividadesAcademicas() {
      const { data } = await api.get('actividades-academicas/');
      this.actividadesAcademicas = data.results;
    },
    async fetchActividadAcademica(id: number) {
      const { data } = await api.get(`actividades-academicas/${id}/`);
      return data.results;
    },
    async createActividadAcademica(actividad: Omit<ActividadPlanificada, 'id'>) {
      const { data } = await api.post('actividades-academicas/', actividad);
      this.actividadesAcademicas.push(data.results);
    },
    async updateActividadAcademica(id: number, actividad: Partial<ActividadPlanificada>) {
      const { data } = await api.put(`actividades-academicas/${id}/`, actividad);
      const index = this.actividadesAcademicas.findIndex((a) => a.id === id);
      if (index !== -1) this.actividadesAcademicas[index] = { ...this.actividadesAcademicas[index], ...data.results };
    },
    async deleteActividadAcademica(id: number) {
      await api.delete(`actividades-academicas/${id}/`);
      this.actividadesAcademicas = this.actividadesAcademicas.filter((actividad) => actividad.id !== id);
    },
    /**
     * Transforma las instancias de los modelos en eventos de FullCalendar.
     * @returns Un array de eventos compatibles con FullCalendar.
     */
    getFullCalendarEvents(): any[] {
      const events: any[] = [];

      // Transformar Metas en eventos
      if (Array.isArray(this.metas)) {
        this.metas.forEach((meta) => {
          events.push({
            id: `meta-${meta.id}`,
            title: `🎯 Meta: ${meta.descripcion}`,
            start: meta.fecha_creacion || new Date(), // Fecha de creación o actual
            end: meta.fecha_limite,
            color: '#FFA500',
            textColor: '#000000',
            classNames: ['meta-event'],
            extendedProps: {
              type: 'meta',
              priority: meta.prioridad,
              completed: meta.completada,
            },
            display: 'block',
          });
        });
      }

      // Transformar Eventos Académicos en eventos
      if (Array.isArray(this.eventosAcademicos)) {
        this.eventosAcademicos.forEach((evento) => {
          events.push({
            id: `evento-academico-${evento.id}`,
            title: `📚 ${evento.tipo}: ${evento.materia.nombre} - ${evento.profesor}`,
            start: getFormattedDate(evento.dia, evento.hora_inicio),
            end: getFormattedDate(evento.dia, evento.hora_fin),
            color: '#378006', // Verde para eventos académicos
            textColor: '#FFFFFF',
            classNames: ['academic-event'],
            extendedProps: {
              type: 'evento-academico',
              classroom: evento.aula,
              mandatory: evento.es_obligatorio,
            },
            display: 'block',
          });
        });
      }

      // Transformar Recordatorios en eventos
      if (Array.isArray(this.recordatorios)) {
        this.recordatorios.forEach((recordatorio) => {
          events.push({
            id: `recordatorio-${recordatorio.id}`,
            title: `🔔 Recordatorio: ${recordatorio.mensaje}`,
            start: recordatorio.fecha_hora,
            color: '#FF4500', // Rojo para recordatorios
            textColor: '#FFFFFF',
            classNames: ['reminder-event'],
            extendedProps: {
              type: 'recordatorio',
              channel: recordatorio.canal,
              frequency: recordatorio.repetir,
            },
            display: 'list-item',
          });
        });
      }

      // Transformar Actividades Planificadas en eventos
      if (Array.isArray(this.actividadesAcademicas)) {
        this.actividadesAcademicas.forEach((actividad) => {
          const evento = this.eventosAcademicos.find((e) => e.id === actividad.evento);
          if (evento) {
            events.push({
              id: `actividad-${actividad.id}`,
              title: `Actividad: ${evento.tipo}`,
              start: getFormattedDate(evento.dia, evento.hora_inicio), // Fecha y hora de inicio
              end: getFormattedDate(evento.dia, evento.hora_fin), // Fecha y hora de fin
              color: actividad.completada ? '#4CAF50' : '#FF9800', // Verde si está completada, naranja si no
              textColor: '#000000', // Texto negro
              classNames: ['planned-activity'], // Clase CSS personalizada
              extendedProps: { type: 'actividad', completada: actividad.completada },
              display: 'block', // Muestra como bloque
            });
          }
        });
      }

      return events;
    },
    async fetchEventoDetailsById(id: number, type: string) {
      try {
        let endpoint = '';
        switch (type) {
          case 'meta-':
            endpoint = `metas/${id}/`;
            break;
          case 'evento-academico-':
            endpoint = `eventos-academicos/${id}/`;
            break;
          case 'recordatorio-':
            endpoint = `recordatorios/${id}/`;
            break;
          case 'actividad':
            console.log(id, type)
            endpoint = `actividades-academicas/${id}/`;
            console.log(endpoint)
            break;
          default:
            throw new Error(`Tipo de evento desconocido: ${type}`);
        }
        const { data } = await api.get(endpoint);
        return data; // Devuelve los datos del evento
      } catch (error) {
        console.error('Error al obtener los detalles del evento:', error);
        throw error;
      }
    },
  },
});

function getFormattedDate(dia: string, hora: string): string {
  const diasSemana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'];
  const hoy = dayjs(); // Fecha actual
  const diaSemanaActual = hoy.day(); // Día de la semana actual (0 = Domingo, 1 = Lunes, ..., 6 = Sábado)
  const indiceDia = diasSemana.indexOf(dia); // Índice del día proporcionado

  // Calcular la fecha correspondiente al día de la semana
  let fecha = hoy;
  if (indiceDia !== -1) {
    fecha = hoy.add(indiceDia - diaSemanaActual, 'day');
  }

  // Combinar la fecha con la hora
  return fecha.format('YYYY-MM-DD') + 'T' + hora;
}