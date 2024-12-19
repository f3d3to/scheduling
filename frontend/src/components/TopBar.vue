<template>
    <div class="topbar">
      <input
        type="text"
        v-model="filterText"
        @input="applyFilter"
        placeholder="Filtrar..."
      />
    </div>
  </template>

  <script>
  export default {
    name: "TopBar",
    data() {
      return {
        filterText: "",
      };
    },
    methods: {
      applyFilter() {
        this.$emit("filter-change", this.filterText);
      },
    },
  };
  </script>

  <style scoped>
  .topbar {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 10px;
    background-color: #f5f5f5;
    border-bottom: 1px solid #ddd;
  }

  input {
    width: 300px;
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  </style>
