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
  height: 60px;
  background: linear-gradient(90deg, #2c2c3e, #1e1e2f);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 20px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}

.topbar input {
  width: 300px;
  padding: 10px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 5px;
  background-color: #1e1e2f;
  color: #fff;
  font-size: 1rem;
  outline: none;
  transition: border-color 0.3s ease;
}

.topbar input::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

.topbar input:focus {
  border-color: #535bf2;
}
  </style>
