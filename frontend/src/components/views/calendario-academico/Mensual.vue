<template>
    <FullCalendar :options="calendarOptions" />
  </template>

  <script setup>
  import { computed } from "vue";
  import { useCalendarStore } from "@store/CalendarioStore";
  import FullCalendar from "@fullcalendar/vue3";
  import dayGridPlugin from "@fullcalendar/daygrid";
  import esLocale from '@fullcalendar/core/locales/es';
  import interactionPlugin from '@fullcalendar/interaction'

  const store = useCalendarStore();

  const calendarOptions = computed(() => ({
    plugins: [dayGridPlugin, interactionPlugin],
    initialView: "dayGridMonth",
    initialDate: store.formattedDate,
    locale: esLocale,
    editable: true,
    headerToolbar: { left: "prev,next today", center: "title", right: "" },
    events: [
      {
        title: 'simple event',
        start: '2025-01-28'
      },
      {
        title: 'event with URL',
        start: '2025-01-28'
      }
    ],
    datesSet: (arg) => store.setCurrentDate(arg.view.currentStart),
  }));
  </script>