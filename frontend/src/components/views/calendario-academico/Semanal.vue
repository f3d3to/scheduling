<template>
    <FullCalendar :options="calendarOptions" />
  </template>

  <script setup>
  import { computed } from "vue";
  import { useCalendarStore } from "@store/CalendarioStore";
  import FullCalendar from "@fullcalendar/vue3";
  import timeGridPlugin from "@fullcalendar/timegrid";
  import esLocale from '@fullcalendar/core/locales/es';
  import interactionPlugin from '@fullcalendar/interaction'
  const store = useCalendarStore();



  const calendarOptions = computed(() => ({
    plugins: [timeGridPlugin,],
    editable: true,
    initialView: "timeGridWeek",
    initialDate: store.formattedDate,
    locale: esLocale,
    headerToolbar: { left: "prev,next today", center: "title", right: "" },
    events: [
      {
        title: 'simple event',
        start: '2025-01-28'
      },
      {
        title: 'event with URL',
        url: 'https://www.google.com/',
        start: '2025-01-28'
      }
    ],
    datesSet: (arg) => store.setCurrentDate(arg.view.currentStart),
  }));
  </script>