// GraphStore.ts
import { defineStore } from 'pinia';
import { fetchPlans, fetchCycles } from "@services/apiService";


interface Node {
  id: string;
  name: string;
  year: number | string;
  fx?: number;
  fy?: number;
}

interface Link {
  source: string;
  target: string;
}

interface Plan {
  id: string;
  nombre: string;
}

export const useGraphStore = defineStore('graph', {
  state: () => ({
    plans: [] as Plan[],
    selectedPlan: null as string | null,
    nodes: [] as Node[],
    links: [] as Link[],
  }),

  actions: {
    async fetchPlans() {
      try {
        const plansData = await fetchPlans();
        this.plans = plansData.results;
        if (this.plans.length > 0) {
          this.selectedPlan = this.plans[0].id;
        }
      } catch (error) {
        console.error("Error fetching plans:", error);
        throw error;
      }
    },

    async fetchCycles() {
      if (!this.selectedPlan) return;

      try {
        const data = await fetchCycles(this.selectedPlan);
        this.processData(data.anios);
      } catch (error) {
        console.error("Error fetching plan cycles:", error);
        throw error;
      }
    },

    processData(anios: any) {
      const nodes: Node[] = [];
      const links: Link[] = [];
      const nodeMap = new Map<string, Node>();

      // Procesar nodos
      Object.entries(anios).forEach(([key, materias]) => {
        if (Array.isArray(materias)) {
          (materias as any[]).forEach((materia) => {
            const node: Node = {
              id: materia.codigo.trim(),
              name: materia.nombre.trim(),
              year: key === "0" ? "Sin año" : parseInt(key, 10)
            };
            nodes.push(node);
            nodeMap.set(node.id, node);
          });
        }
      });

      // Procesar enlaces
      Object.entries(anios).forEach(([key, materias]) => {
        if (Array.isArray(materias)) {
          (materias as any[]).forEach((materia) => {
            if (materia.correlativas && Array.isArray(materia.correlativas)) {
              (materia.correlativas as string[]).forEach((correlativa) => {
                const trimmedCorrelativa = correlativa.trim();
                if (nodeMap.has(trimmedCorrelativa)) {
                  links.push({
                    source: trimmedCorrelativa,
                    target: materia.codigo.trim()
                  });
                }
              });
            }
          });
        }
      });

      this.nodes = nodes;
      this.links = links;
    }
  }
});