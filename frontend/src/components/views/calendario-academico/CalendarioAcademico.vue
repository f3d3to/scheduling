<template>
  <div>
    <!-- Calendario FullCalendar -->
    <FullCalendar :options="calendarOptions" />
    <!-- Detalles del evento seleccionado -->
    <EventosAcademicosDetalles
      v-if="eventoSeleccionado"
      :evento="eventoSeleccionado"
      @cerrar="cerrarDetalles"
    />
    <!-- Formulario de creación de eventos -->
    <CrearEventosAcademicos
      v-if="mostrarFormulario"
      :fechaSeleccionada="fechaSeleccionada"
      @cerrar="cerrarFormulario"
      @eventoCreado="recargarEventos"
    />
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref } from "vue";
import FullCalendar from "@fullcalendar/vue3";
import dayGridPlugin from "@fullcalendar/daygrid";
import timeGridPlugin from "@fullcalendar/timegrid";
import interactionPlugin from "@fullcalendar/interaction";
import multiMonthPlugin from "@fullcalendar/multimonth";
import listPlugin from "@fullcalendar/list";
import esLocale from "@fullcalendar/core/locales/es";
import rrulePlugin from '@fullcalendar/rrule';
import { useEventoAcademicoStore } from "@store/eventoAcademicoStore";
import EventosAcademicosDetalles from "./EventosAcademicosDetalle.vue";
import CrearEventosAcademicos from "./CrearEventosAcademicos.vue";

export default defineComponent({
  components: {
    FullCalendar,
    EventosAcademicosDetalles,
    CrearEventosAcademicos,
  },
  setup() {
    const eventoAcademicoStore = useEventoAcademicoStore();
    const eventoSeleccionado = ref<any>(null);
    const mostrarFormulario = ref(false); // Controla la visibilidad del formulario
    const fechaSeleccionada = ref<string | null>(null); // Fecha seleccionada en el calendario

    // Opciones del calendario
    const calendarOptions = ref({
      plugins: [dayGridPlugin, timeGridPlugin, interactionPlugin, multiMonthPlugin, listPlugin, rrulePlugin],
      initialView: "multiMonthYear", // Vista inicial de varios meses
      multiMonthMaxColumns: 1,
      timeZone: "UTC",
      headerToolbar: {
        left: "prev,next today crearEvento", // Agregamos el botón "crearEvento"
        center: "title",
        right: "multiMonthYear,dayGridMonth,timeGridWeek,timeGridDay,listWeek", // Botones de vista
      },
      customButtons: {
        crearEvento: {
          text: "Crear Evento", // Texto del botón
          click: () => {
            abrirFormulario(); // Abrir el formulario de creación de eventos
          },
        },
      },
      locale: esLocale,
      editable: false, // Desactivar edición
      selectable: true, // Permitir selección de fechas
      events: [], // Los eventos se cargarán desde el store
      dateClick: (arg: any) => {
        // Abrir el formulario de creación de eventos con la fecha seleccionada
        abrirFormularioConFecha(arg.dateStr);
      },
      eventClick: (info: any) => {
        const eventoId = info.event.id; // Obtener el ID del evento clickeado
        const detalles = eventoAcademicoStore.getDetallesPorId(eventoId); // Obtener detalles completos
        eventoSeleccionado.value = { ...detalles, type: info.event.id }; // Guardar los detalles con el tipo
      },
    });

    // Cargar datos del store y asignarlos como eventos del calendario
    onMounted(async () => {
      try {
        // Cargar eventos del calendario académico desde el store
        await eventoAcademicoStore.fetchEventosCalendario();
        calendarOptions.value.events = eventoAcademicoStore.getFullCalendarEvents();
      } catch (error) {
        console.error("Error al cargar datos:", error);
      }
    });

    // Cerrar el panel de detalles
    const cerrarDetalles = () => {
      eventoSeleccionado.value = null;
    };

    // Abrir el formulario de creación de eventos
    const abrirFormulario = () => {
      mostrarFormulario.value = true;
      fechaSeleccionada.value = null; // Limpiar la fecha seleccionada
    };

    // Abrir el formulario con una fecha preseleccionada
    const abrirFormularioConFecha = (fecha: string) => {
      mostrarFormulario.value = true;
      fechaSeleccionada.value = fecha; // Pasar la fecha seleccionada al formulario
    };

    // Cerrar el formulario de creación de eventos
    const cerrarFormulario = () => {
      mostrarFormulario.value = false;
      fechaSeleccionada.value = null; // Limpiar la fecha seleccionada
    };

    // Recargar eventos después de crear uno nuevo
    const recargarEventos = async () => {
      try {
        await eventoAcademicoStore.fetchEventosCalendario();
        calendarOptions.value.events = eventoAcademicoStore.getFullCalendarEvents();
      } catch (error) {
        console.error("Error al recargar eventos:", error);
      }
    };

    return {
      calendarOptions,
      cerrarDetalles,
      eventoSeleccionado,
      abrirFormulario,
      cerrarFormulario,
      recargarEventos,
      mostrarFormulario,
      fechaSeleccionada,
    };
  },
});
</script>

<style>
/* Estilos para eventos académicos */
.calendar-event {
  border-radius: 5px;
  font-style: italic;
}
/* Estilos para eventos de todo el día */
.calendar-event[allDay] {
  opacity: 0.8;
}
/* Estilos para recordatorios */
.reminder-event {
  border: 2px solid #ff4500;
  font-size: 14px;
}
</style>