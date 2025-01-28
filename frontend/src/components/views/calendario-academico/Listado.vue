<template>
    <FullCalendar :options="calendarOptions" />
  </template>

  <script setup>
  import { computed } from "vue";
  import { useCalendarStore } from "@store/CalendarioStore";
  import FullCalendar from "@fullcalendar/vue3";
  import listPlugin from "@fullcalendar/list";
  import esLocale from '@fullcalendar/core/locales/es';
  const store = useCalendarStore();

  const calendarOptions = computed(() => ({
    plugins: [ listPlugin ],
    initialView: 'listWeek',
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