import { defineStore } from "pinia";
import { fetchPlans } from "@services/apiService"; // si sigues usando tu fetchPlans antiguo
import { api } from "@/services/apiServiceAuth";    // tu instancia de fetch o axios-like (ver comentario)

export interface MateriaEstudiante {
  estudiante: {
    id: string;
    username: string;
  };
  materia: {
    id: string;
    nombre: string;
    codigo: string;
  };
  nota_final: number | null;
  final_obligatorio: boolean;
  catedra: string | null;
  comentarios: string | null;
  intentos: number;
  comentarios_docente: string | null;
  estado: 'pendiente' | 'cursando' | 'aprobada' | 'desaprobada' | 'promocionada';
  fecha_inscripcion: string | null;
  metodo_aprobacion: 'final' | 'promocion' | 'equivalencia' | null;
  creditos_asignados: number | null;
  fecha_actualizacion: string;
  dificultad: number | null;
}

interface MateriaMetadata {
  id : number | null;
  plan_de_estudio: {
    id: number;
    nombre: string;
  };
  codigo: string;
  anio: number | null;
  ciclo: string | null;
  cuatrimestre: number | null;
  condicion: string | null;
  nombre: string;
  formato_didactico: string | null;
  ch_semanal: number | null;
  ch_cuatrimestral: number | null;
  creditos: number | null;
  ch_presencial: number | null;
  ch_distancia: number | null;
  ch_total: number | null;
  descripcion: string | null;
  correlativas: string[];
}

interface Node {
  id: string;
  name: string;
  anio: number | string;
  fx?: number;
  fy?: number;
  materiaEstudiante?: MateriaEstudiante | null;
  metadata?: MateriaMetadata | null;
  color?: string;
  customColor?: string; // Color personalizado
}

interface Link {
  source: string;
  target: string;
  color?: string;
}

interface Plan {
  id: string;
  nombre: string;
}

interface CarreraStatus {
  creditos: {
    obtenidos: number;
    total: number;
    porcentaje: number;
  };
  ciclos: Array<{
    nombre: string;
    creditos_obtenidos: number;
    total_creditos: number;
    porcentaje: number;
  }>;
  promedio: {
    valor: number;
    materias_cursadas: number;
  };
  plan_actual: any; // Usa una interfaz específica si tienes el serializer
  ultima_actualizacion: string;
  selectedCycle?: string | null;
}

export const useGraphStore = defineStore("graph", {
  state: () => ({
    plans: [] as Plan[],
    selectedPlan: null as string | null,
    nodes: [] as Node[],
    links: [] as Link[],
    carreraStatus: null as CarreraStatus | null,
    selectedCycle: null as string | null
  }),

  actions: {
    async fetchPlans() {
      try {
        const plansData = await fetchPlans();
        this.plans = plansData.results;
        if (this.plans.length > 0) {
          this.selectedPlan = this.plans[0].id;
          console.log("PLAN SELECCIONADO:", this.selectedPlan);
        }
      } catch (error) {
        console.error("Error fetching plans:", error);
        throw error;
      }
    },

    async fetchCycles(filters?: any) {
      if (!this.selectedPlan) return;

      try {
        // 1) Construimos la query string
        let queryString = "";
        if (filters && Object.keys(filters).length > 0) {
          const params = new URLSearchParams();
          for (const [key, value] of Object.entries(filters)) {
            if (value !== "") {
              // Evitamos parámetros vacíos
              params.append(key, String(value));
            }
          }
          queryString = params.toString(); // p.ej. "anio=3&estado=aprobada"
        }
        // console.log("QUERY STRING: ", queryString);
        // 2) Concatenar la query string si no está vacía
        let url = `grafos/filtrado/${this.selectedPlan}/`;
        if (queryString) {
          url += `?${queryString}`;
        }

        // 3) Petición
        const response = await api.get(url);
        const { nodos, enlaces } = response.data;

        // Mapeo correlativas - (igual)
        const correlativasMap = new Map<string, string[]>();
        enlaces.forEach((enlace: any) => {
          const target = enlace.target.trim();
          if (!correlativasMap.has(target)) {
            correlativasMap.set(target, []);
          }
          correlativasMap.get(target)?.push(enlace.source.trim());
        });

        // Agrupar nodos por año para 'processData'
        const anios: { [key: string]: any[] } = {};
        nodos.forEach((nodo: any) => {
          const year = nodo.anio?.toString() || "0";
          if (!anios[year]) anios[year] = [];

          anios[year].push({
            codigo: nodo.metadata.codigo.trim(),
            nombre: nodo.metadata.nombre.trim(),
            correlativas: correlativasMap.get(nodo.metadata.codigo.trim()) || [],
            materiaEstudiante: nodo.materia_estudiante,
            metadata: nodo.metadata,
            color: nodo.color,
          });
        });

        this.processData(anios, filters?.mostrarAprobadas || false);
      } catch (error) {
        console.error("Error fetching filtered graph:", error);
        throw error;
      }
    },

    processData(anios: any, mostrarAprobadas: boolean = false) {
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
              year: key === "0" ? "Sin año" : parseInt(key, 10),
              materiaEstudiante: materia.materiaEstudiante,
              metadata: materia.metadata,
              color: materia.color,
              disponible: materia.disponible,
            };
            nodes.push(node);
            nodeMap.set(node.id, node);
          });
        }
      });

      // Procesar enlaces desde correlativas
      Object.entries(anios).forEach(([key, materias]) => {
        if (Array.isArray(materias)) {
          (materias as any[]).forEach((materia) => {
            if (materia.correlativas && Array.isArray(materia.correlativas)) {
              (materia.correlativas as string[]).forEach((correlativa) => {
                const trimmedCorrelativa = correlativa.trim();
                if (nodeMap.has(trimmedCorrelativa)) {
                  const link: Link = {
                    source: trimmedCorrelativa,
                    target: materia.codigo.trim(),
                    color: materia.color,
                  };

                  links.push(link);
                }
              });
            }
          });
        }
      });

      this.nodes = nodes;
      this.links = links;
    },
    async updateMateriaEstudiante(materiaEstudiante: any) {
      try {
        // Usar PATCH en lugar de PUT
        const response = await api.patch(`materias/estudiantes/${materiaEstudiante.id}/`, materiaEstudiante);

        // Actualizar el estado local si es necesario
        const index = this.nodes.findIndex(node => node.materiaEstudiante?.id === materiaEstudiante.id);
        if (index !== -1) {
          this.nodes[index].materiaEstudiante = response.data;
        }
      } catch (error) {
        console.error("Error updating MateriaEstudiante:", error);
        throw error;
      }
    },
    async createMateriaEstudiante(materiaEstudiante: MateriaEstudiante) {
      try {
        // Realizar la solicitud POST con los datos de la materia
        const response = await api.post('materias/estudiantes/', materiaEstudiante);

        // Procesar la respuesta del backend
        const nuevaMateriaBackend = response.data;

        // Mapear el objeto devuelto por el backend a la estructura esperada
        const nuevaMateria: MateriaEstudiante = {
          id: nuevaMateriaBackend.id,
          nota_final: nuevaMateriaBackend.nota_final,
          final_obligatorio: nuevaMateriaBackend.final_obligatorio,
          catedra: nuevaMateriaBackend.catedra,
          comentarios: nuevaMateriaBackend.comentarios,
          intentos: nuevaMateriaBackend.intentos,
          comentarios_docente: nuevaMateriaBackend.comentarios_docente,
          estado: nuevaMateriaBackend.estado,
          fecha_inscripcion: nuevaMateriaBackend.fecha_inscripcion,
          metodo_aprobacion: nuevaMateriaBackend.metodo_aprobacion,
          creditos_asignados: nuevaMateriaBackend.creditos_asignados,
          fecha_actualizacion: nuevaMateriaBackend.fecha_actualizacion,
          dificultad: nuevaMateriaBackend.dificultad,
          estudiante: {
            id: nuevaMateriaBackend.estudiante.toString(), // Convertir a string si es necesario
            username: "", // Aquí deberías obtener el username si lo necesitas
          },
          materia: {
            id: nuevaMateriaBackend.materia.toString(), // Convertir a string si es necesario
            nombre: "", // Aquí deberías obtener el nombre de la materia si lo necesitas
            codigo: "", // Aquí deberías obtener el código de la materia si lo necesitas
          },
        };

        // Buscar el nodo correspondiente en la store
        const nodeIndex = this.nodes.findIndex(node => node.id === nuevaMateria.materia.id);
        if (nodeIndex !== -1) {
          // Si el nodo existe, actualizar su materiaEstudiante
          this.nodes[nodeIndex].materiaEstudiante = nuevaMateria;
        } else {
          // Si el nodo no existe, agregarlo (esto depende de tu lógica)
          this.nodes.push({
            id: nuevaMateria.materia.id,
            name: nuevaMateria.materia.nombre,
            anio: nuevaMateria.materia.anio || "Sin año",
            materiaEstudiante: nuevaMateria,
            metadata: null, // Aquí deberías agregar el metadata si lo tienes
          });
        }

        return response; // Retornar la materia creada si es necesario
      } catch (error) {
        console.error("Error creando materiaEstudiante:", error);
        throw error;
      }
    },
    async updateCarreraStatusOnSelection(node: Node) {
      console.log('Ciclo seleccionado:', node.metadata?.ciclo);
      if (node.metadata?.ciclo) {
        this.selectedCycle = node.metadata.ciclo;
        await this.fetchEstadoCarrera(this.selectedPlan);
      }
    },
    async fetchEstadoCarrera(carreraId: any) {
      try {
        const response = await api.get(`carrera/${carreraId}/estado/`);
        console.log("Respuesta de carrera status:", response.data);
        return response.data;
      } catch (error) {
        console.error("Error fetching carrera status:", error);
        throw error;
      }
    },
  },
});