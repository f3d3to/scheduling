<template>
  <v-btn @click="modoEdicion = !modoEdicion">
    {{ modoEdicion ? "Desactivar Edición" : "Activar Edición" }}
  </v-btn>
  <v-btn v-if="modoEdicion" @click="guardarCambios">Guardar Cambios</v-btn>
  <FullCalendar :options="calendarOptions" />
  <EventosAcademicosDetalles
    v-if="eventoSeleccionado"
    :evento="eventoSeleccionado"
    @cerrar="cerrarDetalles"
  />
</template>

<script lang="ts">
import { defineComponent, onMounted, ref } from "vue";
import FullCalendar from "@fullcalendar/vue3";
import dayGridPlugin from "@fullcalendar/daygrid";
import timeGridPlugin from "@fullcalendar/timegrid";
import interactionPlugin from "@fullcalendar/interaction";
import multiMonthPlugin from "@fullcalendar/multimonth";
import listPlugin from "@fullcalendar/list";
import esLocale from '@fullcalendar/core/locales/es';
import { useEventoAcademicoStore } from "@store/eventoAcademicoStore";
import EventosAcademicosDetalles from "./EventosAcademicosDetalle.vue";

export default defineComponent({
  components: {
    FullCalendar,
    EventosAcademicosDetalles,
  },
  setup() {
    const eventoAcademicoStore = useEventoAcademicoStore();
    const eventoSeleccionado = ref<any>(null);
    const modoEdicion = ref(false); // Estado para activar/desactivar el modo edición
    const eventosTemporales = ref<any[]>([]); // Eventos creados/modificados temporalmente

    const calendarOptions = ref({
      plugins: [dayGridPlugin, timeGridPlugin, interactionPlugin, multiMonthPlugin, listPlugin],
      initialView: "multiMonthYear", // Vista inicial de varios meses
      multiMonthMaxColumns: 1,
      timeZone: 'UTC',
      headerToolbar: {
        left: "prev,next today",
        center: "title",
        right: "multiMonthYear,dayGridMonth,timeGridWeek,timeGridDay,listWeek", // Botones de vista
      },
      locale: esLocale,
      editable: true,
      selectable: true,
      selectMirror: true,
      events: [], // Los eventos se cargarán desde el store
      dateClick: (arg: any) => {
        if (modoEdicion.value) {
          // Crear un nuevo evento temporal al hacer clic en una fecha
          const nuevoEvento = {
            id: `temp-${Date.now()}`, // ID temporal único
            title: "Nuevo Evento",
            start: arg.dateStr,
            end: arg.dateStr,
            allDay: true,
          };
          eventosTemporales.value.push(nuevoEvento);
          calendarOptions.value.events = [
            ...eventoAcademicoStore.getFullCalendarEvents(),
            ...eventosTemporales.value,
          ];
        }
      },
      eventClick: (info: any) => {
        const eventoId = info.event.id; // Obtener el ID del evento clickeado
        const detalles = eventoAcademicoStore.getDetallesPorId(eventoId); // Obtener detalles completos
        eventoSeleccionado.value = { ...detalles, type: info.event.id }; // Guardar los detalles con el tipo
      },
    });

    // Cargar datos del store y asignarlos como eventos del calendario
    onMounted(async () => {
      // Cargar datos desde el backend
      await eventoAcademicoStore.fetchMetas();
      await eventoAcademicoStore.fetchEventosAcademicos();
      await eventoAcademicoStore.fetchRecordatorios();
      await eventoAcademicoStore.fetchActividadesAcademicas();
      await eventoAcademicoStore.fetchPlanificaciones();
      await eventoAcademicoStore.fetchProgresos();

      // Obtener eventos transformados desde el store
      calendarOptions.value.events = eventoAcademicoStore.getFullCalendarEvents();
    });

    const cerrarDetalles = () => {
      eventoSeleccionado.value = null; // Cerrar el panel de detalles
    };
    // Actualizar eventos temporales en el calendario
    const actualizarEventosTemporales = () => {
      calendarOptions.value.events = [
        ...eventoAcademicoStore.getFullCalendarEvents(),
        ...eventosTemporales.value,
      ];
    };

    // Guardar todos los eventos al backend
    const guardarCambios = async () => {
      try {
        // Filtrar eventos temporales para enviar solo los nuevos/modificados
        const eventosParaGuardar = eventosTemporales.value.map((evento) => ({
          title: evento.title,
          start: evento.start,
          end: evento.end,
          allDay: evento.allDay,
        }));

        // Enviar solicitud al backend
        await eventoAcademicoStore.guardarEventosBatch(eventosParaGuardar);

        // Limpiar eventos temporales y desactivar modo edición
        eventosTemporales.value = [];
        modoEdicion.value = false;

        // Recargar eventos desde el backend
        await eventoAcademicoStore.fetchEventosAcademicos();
        calendarOptions.value.events = eventoAcademicoStore.getFullCalendarEvents();
      } catch (error) {
        console.error("Error al guardar eventos:", error);
      }
    };

    return {
      calendarOptions,
      cerrarDetalles,
      eventoSeleccionado,
      modoEdicion,
      eventosTemporales,
      guardarCambios,
    };
  },
});
</script>

<style>
/* Estilos para metas */
.meta-event {
  border-radius: 5px;
  font-weight: bold;
}
/* Estilos para eventos académicos */
.academic-event {
  border-radius: 5px;
  font-style: italic;
}
/* Estilos para recordatorios */
.reminder-event {
  border: 2px solid #FF4500;
  font-size: 14px;
}
/* Estilos para actividades planificadas */
.planned-activity {
  opacity: 0.8;
  font-size: 12px;
}
</style>