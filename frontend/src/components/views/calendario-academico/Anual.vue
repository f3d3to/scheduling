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
    initialDate: store.formattedDate,
    headerToolbar: { left: "", center: "title", right: "" },
    multiMonthMaxColumns: 1,
    locale: esLocale,
    events: store.events,
    datesSet: (arg) => store.setCurrentDate(arg.view.currentStart),
  }));
  </script>