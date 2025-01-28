// stores/calendarStore.js
import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { api } from '../services/apiServiceAuth';

export const useCalendarStore = defineStore("calendar", () => {
  // Estado
  const events = ref([]);
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
      // Usar el servicio `api` para realizar la solicitud GET
      const response = await api.get("eventos-academicos/");

      // Transformar datos a formato de FullCalendar
      events.value = response.data.map((evento) => ({
        id: evento.id,
        title: evento.descripcion || "Sin título",
        start: `${evento.dia}T${evento.hora_inicio}`,
        end: `${evento.dia}T${evento.hora_fin}`,
        allDay: false, // Ajustar según la lógica del evento
        extendedProps: {
          aula: evento.aula,
          profesor: evento.profesor,
          esObligatorio: evento.es_obligatorio,
          recursos: evento.recursos,
        },
      }));
    } catch (error) {
      console.error("Error al cargar eventos:", error.message);
    }
  };

  return {
    events,
    currentDate,
    formattedDate,
    setCurrentDate,
    fetchEvents,
  };
});
