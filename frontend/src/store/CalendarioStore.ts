// stores/calendarStore.js
import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { api } from '../services/apiServiceAuth';

export const useCalendarStore = defineStore("calendar", () => {
  // Estado
  const events = ref([]);
  const metas = ref([]);
  const recordatorios = ref([]);
  const planificaciones = ref([]);
  const currentDate = ref(new Date()); // Fecha sincronizada

  // Getters
  const formattedDate = computed(() =>
    currentDate.value.toISOString().split("T")[0]
  );

  // Actions
  const setCurrentDate = (date) => {
    currentDate.value = new Date(date); // Asegurar que sea una instancia de Date
  };

  const fetchEvents = async () => {
    try {
      // Cargar eventos académicos
      const responseEventos = await api.get("eventos-academicos/");
      const eventosAcademicos = responseEventos.data.map((evento) => ({
        id: `evento-academico-${evento.id}`,
        title: evento.descripcion || "Sin título",
        start: `${evento.dia}T${evento.hora_inicio}`,
        end: `${evento.dia}T${evento.hora_fin}`,
        allDay: false,
        extendedProps: {
          tipo: "academico",
          aula: evento.aula,
          profesor: evento.profesor,
          esObligatorio: evento.es_obligatorio,
          recursos: evento.recursos,
        },
      }));

      // Cargar metas
      const responseMetas = await api.get("metas/");
      const metasEventos = responseMetas.data.map((meta) => ({
        id: `meta-${meta.id}`,
        title: meta.descripcion || "Sin título",
        start: meta.fecha_limite,
        allDay: true,
        extendedProps: {
          tipo: "meta",
          estudiante: meta.estudiante,
          tipoMeta: meta.tipo,
          prioridad: meta.prioridad,
          completada: meta.completada,
        },
      }));

      // Cargar recordatorios
      const responseRecordatorios = await api.get("recordatorios/");
      const recordatoriosEventos = responseRecordatorios.data.map((recordatorio) => ({
        id: `recordatorio-${recordatorio.id}`,
        title: recordatorio.mensaje || "Sin título",
        start: recordatorio.fecha_hora,
        allDay: false,
        extendedProps: {
          tipo: "recordatorio",
          usuario: recordatorio.usuario,
          repetir: recordatorio.repetir,
          canal: recordatorio.canal,
        },
      }));

      // Cargar planificaciones
      const responsePlanificaciones = await api.get("planificaciones/");
      const planificacionesEventos = responsePlanificaciones.data.map((planificacion) => ({
        id: `planificacion-${planificacion.id}`,
        title: planificacion.nombre || "Sin título",
        start: new Date(planificacion.año, planificacion.semana - 1, 1), // Ajustar la fecha según la lógica
        allDay: true,
        extendedProps: {
          tipo: "planificacion",
          estudiante: planificacion.estudiante,
          tipoPlanificacion: planificacion.tipo,
          cuatrimestre: planificacion.cuatrimestre,
        },
      }));

      // Combinar todos los eventos en un solo array
      events.value = [
        ...eventosAcademicos,
        ...metasEventos,
        ...recordatoriosEventos,
        ...planificacionesEventos,
      ];
    } catch (error) {
      console.error("Error al cargar eventos:", error.message);
    }
  };

  return {
    events,
    metas,
    recordatorios,
    planificaciones,
    currentDate,
    formattedDate,
    setCurrentDate,
    fetchEvents,
  };
});
