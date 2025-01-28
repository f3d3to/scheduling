<template>
    <FullCalendar :options="calendarOptions" />
  </template>

  <script setup>
  import { computed } from "vue";
  import { useCalendarStore } from "@store/CalendarioStore";
  import FullCalendar from "@fullcalendar/vue3";
  import multiMonthPlugin from "@fullcalendar/multimonth";
  import interactionPlugin from "@fullcalendar/interaction";
  import esLocale from '@fullcalendar/core/locales/es';

  const store = useCalendarStore();

  const calendarOptions = computed(() => ({
    plugins: [multiMonthPlugin, interactionPlugin],
    initialView: "multiMonthYear",
    initialDate: '2025-01-28',
    headerToolbar: { left: "", center: "title", right: "" },
    editable: true,
    multiMonthMaxColumns: 1,
    locale: esLocale,
    events: [      {
        title: 'simple event',
        start: '2025-01-28'
      },
      {
        title: 'event with URL',
        url: 'https://www.google.com/',
        start: '2025-01-28'
      }
    ],

  }));
  </script>