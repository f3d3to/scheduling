<template>
  <FullCalendar :options='calendarOptions'>
    <template v-slot:eventContent='arg'>
      <b>{{ arg.timeText }}</b>
      <i>{{ arg.event.title }}</i>
    </template>
  </FullCalendar>
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
    plugins: [timeGridPlugin, interactionPlugin],
    initialView: "timeGridDay",
    initialDate: '2025-01-28',
    editable: true,
    timeZone: 'UTC',
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

  }));
  </script>