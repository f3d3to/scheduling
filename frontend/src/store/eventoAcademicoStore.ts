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
  ultima_actualizacion: string;
  porcentaje_completado: number | null;
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
            color: '#FFA500', // Naranja para metas
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

      // Transformar Progreso de Materias en eventos
      if (Array.isArray(this.progresos)) {
        this.progresos.forEach((progreso) => {
          events.push({
            id: `progreso-${progreso.id}`,
            title: `📊 Progreso: ${progreso.materia_estudiante} - ${progreso.porcentaje_completado}%`,
            start: progreso.ultima_actualizacion, // Fecha de la última actualización
            color: '#007BFF', // Azul para progreso
            textColor: '#FFFFFF',
            classNames: ['progress-event'],
            extendedProps: {
              type: 'progreso',
              completedPercentage: progreso.porcentaje_completado,
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
            start: recordatorio.fecha_hora, // Fecha y hora del recordatorio
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

      // Transformar Eventos Académicos en eventos
      if (Array.isArray(this.eventosAcademicos)) {
        this.eventosAcademicos.forEach((evento) => {
          events.push({
            id: `evento-${evento.id}`,
            title: `📚 ${evento.tipo}: ${evento.materia} - ${evento.profesor}`,
            start: getFormattedDate(evento.dia, evento.hora_inicio),
            end: getFormattedDate(evento.dia, evento.hora_fin),
            color: '#378006', // Verde para eventos académicos
            textColor: '#FFFFFF',
            classNames: ['academic-event'],
            extendedProps: {
              type: 'evento',
              classroom: evento.aula,
              mandatory: evento.es_obligatorio,
            },
            display: 'block',
          });
        });
      }

      // Transformar Planificaciones Académicas en eventos
      if (Array.isArray(this.planificaciones)) {
        this.planificaciones.forEach((planificacion) => {
          let endDate;
          if (planificacion.tipo === 'SEMANAL') {
            endDate = new Date(planificacion.año, 0, (planificacion.semana || 1) * 7); // Fin de la semana
          } else if (planificacion.tipo === 'CUATRIMESTRAL') {
            endDate = new Date(planificacion.año, (planificacion.cuatrimestre === '1' ? 5 : 11), 0); // Fin del cuatrimestre
          } else if (planificacion.tipo === 'ANUAL') {
            endDate = new Date(planificacion.año + 1, 0, 0); // Fin del año
          }

          events.push({
            id: `planificacion-${planificacion.id}`,
            title: `📅 ${planificacion.tipo}`,
            start: new Date(planificacion.año, 0, 1), // Inicio del año
            end: endDate,
            color: '#999ef59f', // Amarillo para planificaciones
            textColor: '#000000',
            allDay: true,
            classNames: ['planning-event'],
            extendedProps: {
              type: 'planificacion',
              planningType: planificacion.tipo,
              workload: planificacion,
            },
            display: 'background',
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
              title: `${actividad.completada ? '✅' : '❌'} Actividad: ${evento.tipo}`,
              start: getFormattedDate(evento.dia, evento.hora_inicio),
              end: getFormattedDate(evento.dia, evento.hora_fin),
              color: actividad.completada ? '#4CAF50' : '#e65f50',
              textColor: '#000000',
              classNames: ['planned-activity'],
              extendedProps: {
                type: 'actividad',
                completed: actividad.completada,
              },
              display: 'block',
            });
          }
        });
      }

      return events;
    },
    getDetallesPorId(id: string): any | null {
      const [tipo, idNumerico] = id.split('-'); // Extraer el tipo y el ID numérico
      const idNum = parseInt(idNumerico, 10);

      switch (tipo) {
        case 'meta':
          return this.metas.find((meta) => meta.id === idNum);
        case 'progreso':
          return this.progresos.find((progreso) => progreso.id === idNum);
        case 'recordatorio':
          return this.recordatorios.find((recordatorio) => recordatorio.id === idNum);
        case 'evento':
          return this.eventosAcademicos.find((evento) => evento.id === idNum);
        case 'planificacion':
          return this.planificaciones.find((planificacion) => planificacion.id === idNum);
        case 'actividad':
          return this.actividadesAcademicas.find((actividad) => actividad.id === idNum);
        default:
          console.warn(`Tipo de evento desconocido: ${tipo}`);
          return null;
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