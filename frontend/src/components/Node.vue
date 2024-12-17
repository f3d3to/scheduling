<template>
    <circle
      :r="20"
      :fill="color"
      @click="$emit('node-clicked', id)"
    ></circle>
  </template>

  <script>
  export default {
    props: {
      id: String,
      color: String,
    },
  };
  </script>
