<template>
  <v-container class="plan-container">
    <h1 class="title text-h2">Modo Creación</h1>
    <h4 class="title text-h3">Plan de Estudio</h4>

    <!-- Stepper -->
    <v-stepper>
      <template v-slot:default="{ prev, next }">
        <!-- Stepper Header -->
        <v-stepper-header>
          <v-stepper-item
            :complete="step > 1"
            editable
            title="Datos del Plan"
            value="1"
          ></v-stepper-item>
          <v-divider></v-divider>
          <v-stepper-item
            :complete="step > 2"
            editable
            title="Agregar Materias"
            value="2"
          ></v-stepper-item>
          <v-divider></v-divider>
          <v-stepper-item
            editable
            title="Vista Previa"
            value="3"
          ></v-stepper-item>
        </v-stepper-header>

        <!-- Stepper Window -->
        <v-stepper-window>
          <!-- Paso 1: Datos del plan de estudio -->
          <v-stepper-window-item value="1">
            <v-card flat class="card">
              <v-card-text>
                <v-form ref="planForm" @submit.prevent="nextStep">
                  <v-text-field
                    v-model="plan.nombre"
                    label="Nombre del Plan de Estudio"
                    :rules="[v => !!v || 'Este campo es requerido']"
                    required
                    outlined
                    dense
                    class="input-field"
                  ></v-text-field>
                  <v-text-field
                    v-model="plan.año_creacion"
                    label="Año de Creación"
                    type="number"
                    :rules="[v => !!v || 'Este campo es requerido']"
                    required
                    outlined
                    dense
                    class="input-field"
                  ></v-text-field>
                  <v-textarea
                    v-model="plan.descripcion"
                    label="Descripción"
                    rows="3"
                    optional
                    outlined
                    dense
                    class="input-field"
                  ></v-textarea>
                </v-form>
              </v-card-text>
            </v-card>
          </v-stepper-window-item>
        <!-- Paso 2: Agregar materias -->
        <v-stepper-window-item value="2">
          <v-card flat class="card">
            <v-card-text>
              <v-list>
                <v-list-item v-for="(materia, index) in materias" :key="index" class="list-item">
                  <div class="d-flex align-center">
                    <v-text-field
                      v-model="materias[index]"
                      label="Nombre de la Materia"
                      :rules="[v => !!v || 'Este campo es requerido']"
                      required
                      outlined
                      dense
                      class="flex-grow-1 mr-2"
                    ></v-text-field>
                    <v-btn icon @click="removeMateria(index)">
                      <v-icon>mdi-delete</v-icon>
                    </v-btn>
                  </div>
                </v-list-item>
              </v-list>
              <v-btn color="primary" @click="addMateria" class="mt-4">Agregar Materia</v-btn>
            </v-card-text>
          </v-card>
        </v-stepper-window-item>
          <!-- Paso 3: Vista Previa -->
          <v-stepper-window-item value="3">
            <h2 class="subtitle">Vista Previa del Plan de Estudio</h2>
            <p><strong>Nombre:</strong> {{ plan.nombre }}</p>
            <p><strong>Año de Creación:</strong> {{ plan.año_creacion }}</p>
            <p><strong>Descripción:</strong> {{ plan.descripcion }}</p>
            <h3>Materias</h3>
            <v-expansion-panels>
              <v-expansion-panel v-for="(materia, index) in materiasCompletas" :key="index">
                <v-expansion-panel-title>{{ materia.nombre }}</v-expansion-panel-title>
                <v-expansion-panel-text>
                  <v-form ref="materiaForm" @submit.prevent="guardarMateria(materia)">
                    <v-text-field
                      v-model="materia.codigo"
                      label="Código"
                      :rules="[v => !!v || 'Este campo es requerido']"
                      required
                      outlined
                      dense
                      class="input-field"
                    ></v-text-field>
                    <v-text-field
                      v-model="materia.anio"
                      label="Año"
                      type="number"
                      :rules="[v => !!v || 'Este campo es requerido']"
                      required
                      outlined
                      dense
                      class="input-field"
                    ></v-text-field>
                    <v-text-field
                      v-model="materia.cuatrimestre"
                      label="Cuatrimestre"
                      type="number"
                      :rules="[v => !!v || 'Este campo es requerido']"
                      required
                      outlined
                      dense
                      class="input-field"
                    ></v-text-field>
                    <v-text-field
                      v-model="materia.creditos"
                      label="Créditos"
                      type="number"
                      :rules="[v => !!v || 'Este campo es requerido']"
                      required
                      outlined
                      dense
                      class="input-field"
                    ></v-text-field>
                    <v-text-field
                      v-model="materia.ch_semanal"
                      label="Horas Semanales"
                      type="number"
                      :rules="[v => !!v || 'Este campo es requerido']"
                      required
                      outlined
                      dense
                      class="input-field"
                    ></v-text-field>
                    <v-text-field
                      v-model="materia.ch_cuatrimestral"
                      label="Horas Cuatrimestrales"
                      type="number"
                      :rules="[v => !!v || 'Este campo es requerido']"
                      required
                      outlined
                      dense
                      class="input-field"
                    ></v-text-field>
                    <v-text-field
                      v-model="materia.ch_total"
                      label="Horas Totales"
                      type="number"
                      :rules="[v => !!v || 'Este campo es requerido']"
                      required
                      outlined
                      dense
                      class="input-field"
                    ></v-text-field>
                    <v-textarea
                      v-model="materia.descripcion"
                      label="Descripción"
                      rows="3"
                      optional
                      outlined
                      dense
                      class="input-field"
                    ></v-textarea>
                    <v-text-field
                      v-model="materia.correlativas"
                      label="Correlativas (separadas por comas)"
                      hint="Ejemplo: Materia1, Materia2"
                      optional
                      outlined
                      dense
                      class="input-field"
                    ></v-text-field>
                  </v-form>
                </v-expansion-panel-text>
              </v-expansion-panel>
            </v-expansion-panels>
            <div id="graph-preview" class="mt-4">
              <h3>Previsualización de Correlatividades</h3>
              <div ref="graphContainer"></div>
            </div>
            <v-btn color="primary" class="mt-4 save-btn" @click="confirmarGuardado">Guardar Plan de Estudio</v-btn>
          </v-stepper-window-item>
        </v-stepper-window>

        <!-- Stepper Actions -->
        <v-stepper-actions
          @click:prev="prev"
          @click:next="next"
          next-text="Siguiente"
          color="success"
          prev-text="Anterior"
          :disable-next="isNextButtonDisabled"
        >
        </v-stepper-actions>
      </template>
    </v-stepper>
  </v-container>
</template>

<script>
  import Swal from "sweetalert2";
  import { useGraphStore } from "@store/GraphStore";
  import * as d3 from "d3";
  import {
    createChart,
    highlightConnections,
    resetHighlight,
  } from "@/utils/graphUtils";

  export default {
    data() {
      return {
        step: 1,
        plan: {
          nombre: "",
          año_creacion: null,
          descripcion: "",
        },
        materias: [], // Nombres de las materias ingresadas
        materiasCompletas: [], // Materias con detalles completos
        isStep1Valid: false,
      };
    },
    computed: {
      isNextButtonDisabled() {
        if (this.step === 1) {
          return !this.isStep1Valid;
        }
        if (this.step === 2) {
          return this.materias.length === 0; // Debe haber al menos una materia
        }
        return false;
      },
    },
    watch: {
      "plan.nombre": function () {
        this.validateStep1();
      },
      "plan.año_creacion": function () {
        this.validateStep1();
      },
      materiasCompletas: {
        deep: true,
        handler() {
          this.updateGraph();
        },
      },
    },
    methods: {
      validateStep1() {
        const isValid = this.$refs.planForm?.validate().valid;
        this.isStep1Valid = isValid;
      },
      async nextStep() {
        if (this.step === 1) {
          const isValid = await this.$refs.planForm.validate();
          if (!isValid.valid) {
            return;
          }
          this.step++;
        }
        if (this.step === 2) {
          if (this.materias.length === 0) {
            return;
          }
          // Convertir los nombres de las materias en objetos completos
          this.materiasCompletas = this.materias.map((nombre) => ({
            nombre,
            codigo: "",
            anio: null,
            cuatrimestre: null,
            creditos: null,
            ch_semanal: null,
            ch_cuatrimestral: null,
            ch_total: null,
            descripcion: "",
            correlativas: "",
          }));
          this.step++;
        }
        if (this.step === 3) {
          this.drawGraph();
        }
      },
      prevStep() {
        if (this.step > 1) {
          this.step--;
        }
      },
      addMateria() {
        this.materias.push(""); // Agregar un nuevo campo para el nombre de la materia
      },
      removeMateria(index) {
        this.materias.splice(index, 1); // Eliminar el nombre de la materia
      },
      drawGraph() {
        // Validar correlativas
        if (!this.validateCorrelativas()) {
          return;
        }

        // Crear nodos
        const nodes = this.materiasCompletas.map((materia) => ({
          id: materia.codigo.trim(),
          name: materia.nombre.trim(),
          year: materia.anio || "Sin año",
          color: "#69b3a2",
          customColor: "#4CAF50",
        }));

        // Crear enlaces
        const links = [];
        const nodeMap = new Map(nodes.map((node) => [node.id, node]));

        this.materiasCompletas.forEach((materia) => {
          if (materia.correlativas) {
            materia.correlativas.split(",").forEach((correlativa) => {
              const targetCodigo = correlativa.trim();
              if (nodeMap.has(targetCodigo)) {
                links.push({
                  source: materia.codigo.trim(),
                  target: targetCodigo,
                  color: "#FFD700",
                });
              } else {
                console.warn(`Correlativa no encontrada: ${targetCodigo}`);
              }
            });
          }
        });

        // Dibujar el gráfico
        createChart(this.$refs.graphContainer, nodes, links, [], highlightConnections, resetHighlight);
      },
      validateCorrelativas() {
        const allCodigos = this.materiasCompletas.map((m) => m.codigo.trim());
        const invalidCorrelativas = [];

        this.materiasCompletas.forEach((materia) => {
          if (materia.correlativas) {
            materia.correlativas.split(",").forEach((correlativa) => {
              const trimmedCorrelativa = correlativa.trim();
              if (!allCodigos.includes(trimmedCorrelativa)) {
                invalidCorrelativas.push({
                  materia: materia.nombre,
                  correlativa: correlativa.trim(),
                });
              }
            });
          }
        });

        return true;
      },

      updateGraph() {
        this.drawGraph();
      },
      async confirmarGuardado() {
        // Validar que todos los campos de las materias estén completos
        const isValid = this.materiasCompletas.every(
          (materia) =>
            materia.nombre &&
            materia.codigo &&
            materia.anio !== null &&
            materia.cuatrimestre !== null &&
            materia.creditos !== null &&
            materia.ch_semanal !== null &&
            materia.ch_cuatrimestral !== null &&
            materia.ch_total !== null
        );

        if (!isValid) {
          return;
        }

        try {
          const graphStore = useGraphStore();
          const requestData = {
            nombre: this.plan.nombre,
            año_creacion: this.plan.año_creacion,
            descripcion: this.plan.descripcion,
            materias: this.materiasCompletas.map((materia) => ({
              codigo: materia.codigo,
              nombre: materia.nombre,
              anio: materia.anio,
              cuatrimestre: materia.cuatrimestre,
              creditos: materia.creditos,
              ch_semanal: materia.ch_semanal,
              ch_cuatrimestral: materia.ch_cuatrimestral,
              ch_total: materia.ch_total,
              descripcion: materia.descripcion,
              correlativas: materia.correlativas.split(",").map((c) => c.trim()),
            })),
          };

          // Llamar al endpoint unificado
          await graphStore.createPlanConMaterias(requestData);

          Swal.fire("Éxito", "El plan y las materias han sido creados correctamente.", "success");
        } catch (error) {
          console.error("Error al crear el plan o las materias:", error);
          Swal.fire("Error", "Ocurrió un error al crear el plan o las materias.", "error");
        }
      },
    },
  };
  </script>

<style scoped>
.plan-container {
  padding: 2rem;
  max-width: 800px;
  margin: auto;
}

.title {
  text-align: center;
  margin-bottom: 2rem;
  font-weight: bold;
  color: #333;
}

.subtitle {
  margin-top: 1rem;
  font-size: 1.5rem;
  font-weight: bold;
  color: #555;
}

.card {
  padding: 1.5rem;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.input-field {
  margin-bottom: 1rem;
}

.list-item {
  padding: 0.5rem 0;
  border-bottom: 1px solid #eee;
}

.delete-btn {
  color: #ff5252;
}

.add-btn {
  margin-top: 1rem;
  width: 100%;
}

.save-btn {
  background-color: #4caf50;
  color: white;
  width: 100%;
  margin-top: 1rem;
}
</style>