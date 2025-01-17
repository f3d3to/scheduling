import { defineStore } from "pinia";

export const useGraphStore = defineStore("graphStore", {
  state: () => ({
    materias: [] as any[], // Datos del plan de estudios
    materiasEstudiantes: [] as any[], // Datos específicos del estudiante
    nodos: [] as any[], // Nodos para la representación visual
    links: [] as any[], // Enlaces entre los nodos
    filters: {} as Record<string, any>, // Configuración de filtros dinámicos
  }),

  getters: {
    getActiveFilters(state) {
      // Devuelve solo los filtros que están aplicados
      return Object.values(state.filters).filter((filter) => filter.applied);
    },
    getNodeById(state) {
      // Encuentra un nodo por su ID
      return (id: string) => state.nodos.find((node) => node.id === id);
    },
    getLinkBySource(state) {
      // Encuentra enlaces que parten de un nodo específico
      return (sourceId: string) =>
        state.links.filter((link) => link.source === sourceId);
    },
  },

  actions: {
    // Carga los datos de las materias desde el endpoint
    async loadMaterias() {
      try {
        const response = await fetch("http://localhost:8000/materias");
        this.materias = await response.json();
      } catch (error) {
        console.error("Error loading materias:", error);
      }
    },

    // Carga las materias relacionadas con el estudiante
    async loadMateriasEstudiantes() {
      try {
        const response = await fetch("http://localhost:8000/materias-estudiantes");
        this.materiasEstudiantes = await response.json();
      } catch (error) {
        console.error("Error loading materias estudiantes:", error);
      }
    },

    // Carga los datos del grafo (nodos y enlaces)
    async loadGrafo() {
      try {
        const response = await fetch("http://localhost:8000/grafo");
        const { nodos, links } = await response.json();
        this.nodos = nodos;
        this.links = links;
      } catch (error) {
        console.error("Error loading grafo:", error);
      }
    },

    // Carga los filtros disponibles desde el backend
    async loadFiltros() {
      try {
        const response = await fetch("http://localhost:8000/filtros");
        const { filters } = await response.json();
        this.filters = filters.reduce((acc, filter) => {
          acc[filter.key] = filter;
          return acc;
        }, {});
      } catch (error) {
        console.error("Error loading filters:", error);
      }
    },

    async applyFilters() {
      try {
        const activeFilters = this.getActiveFilters;
        const response = await fetch("http://localhost:8000/grafo", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ filters: activeFilters }),
        });
        const { nodos, links } = await response.json();
        this.nodos = nodos;
        this.links = links;
      } catch (error) {
        console.error("Error applying filters:", error);
      }
    },

    // Cambia el estado de un filtro
    toggleFilter(key: string) {
      if (this.filters[key]) {
        this.filters[key].applied = !this.filters[key].applied;
      }
    },

    // Actualiza el valor de un filtro de tipo rango o lista
    updateFilterValue(key: string, value: any) {
      if (this.filters[key]) {
        this.filters[key].value = value;
      }
    },
  },
});
