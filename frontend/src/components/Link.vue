<template>
    <line :x1="x1" :y1="y1" :x2="x2" :y2="y2" stroke="#FFD700" stroke-width="2" />
  </template>

  <script>
  export default {
    props: {
      x1: Number,
      y1: Number,
      x2: Number,
      y2: Number,
    },
  };
  </script>
