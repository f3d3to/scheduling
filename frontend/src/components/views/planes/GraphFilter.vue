<!-- GraphFilter.vue -->
<template>
  <v-card
    ref="draggableElement"
    class="pa-4 mb-4 draggable-card"
    :style="{ transform: `translate(${x}px, ${y}px)` }"
  >
  <v-select
      :model-value="selectedPlan"
      :items="plans"
      item-title="nombre"
      item-value="id"
      label="Seleccionar Plan"
      @update:modelValue="handlePlanChange"
      outlined
      dense
      class="mb-4"
    ></v-select>
  <v-row dense>
    <!-- Filtros básicos -->
    <v-col cols="12" sm="6" md="4" lg="2">
        <v-text-field
        v-model="anio"
        label="Año"
        type="number"
        outlined
        dense
        clearable
        placeholder="Ej: 3"
        ></v-text-field>
    </v-col>

    <v-col cols="12" sm="6" md="4" lg="2">
      <v-select
        v-model="ciclo"
        :items="cicloOptions"
        label="Ciclo"
        outlined
        dense
        clearable
        item-title="title"
        item-value="value"
      ></v-select>
    </v-col>

    <v-col cols="12" sm="6" md="4" lg="2">
        <v-text-field
        v-model="creditos"
        label="Créditos"
        type="number"
        outlined
        dense
        clearable
        ></v-text-field>
    </v-col>

    <v-col cols="12" sm="6" md="4" lg="3">
      <v-text-field
        v-model="nombreIcontains"
        label="Nombre contiene"
        outlined
        dense
        clearable
      ></v-text-field>
    </v-col>

    <v-col cols="12" sm="6" md="4" lg="3">
        <v-text-field
        v-model="formatoDidactico"
        label="Formato didáctico"
        outlined
        dense
        clearable
        ></v-text-field>
    </v-col>

    <!-- Selectores -->
    <v-col cols="12" sm="6" md="4" lg="3">
        <v-select
        v-model="estado"
        :items="estadoOptions"
        label="Estado"
        outlined
        dense
        clearable
        item-title="title"
        item-value="value"
        ></v-select>
    </v-col>

    <v-col cols="12" sm="6" md="4" lg="3">
        <v-select
        v-model="condicion"
        :items="condicionOptions"
        label="Condición"
        outlined
        dense
        clearable
        item-title="title"
        item-value="value"
        ></v-select>
    </v-col>

    <!-- Filtros especiales -->
    <v-col cols="12" sm="6" md="4" lg="3">
        <v-text-field
        v-model="materia"
        label="Código"
        outlined
        dense
        clearable
        ></v-text-field>
    </v-col>

    <v-col cols="12" sm="6" md="4" lg="3">
      <v-text-field
        v-model="correlativasIn"
        label="Correlativas (Códigos separados por coma)"
        outlined
        dense
        clearable
      ></v-text-field>
    </v-col>

    <v-col cols="12" sm="6" md="4" lg="3">
      <v-switch
        v-model="mostrarPromocionadas"
        label="Resaltar promocionadas"
        @change="applyFilter"
      ></v-switch>
    </v-col>
    <v-col cols="12" sm="6" md="4" lg="3">
      <v-switch
        v-model="mostrarDisponibles"
        label="Resaltar disponibles"
        @change="applyFilter"
        color="purple"
      ></v-switch>
    </v-col>
    <!-- Botón de acción -->
    <v-btn
        color="primary"
        @click="applyFilter"
        class="mt-2"
        >
        Aplicar Filtros
        </v-btn>
    </v-row>
</v-card>
</template>

<script>
import { ref, onMounted } from 'vue';
import interact from 'interactjs';

export default {
  name: "GraphFilter",
  props: {
    plans: {
      type: Array,
      required: true,
    },
    selectedPlan: {
      type: [String, Number],
      required: true,
    },
  },
  emits: ["update:selectedPlan", "filter-changed"],
  setup(props, { emit }) {
    const draggableElement = ref(null);
    const x = ref(0);
    const y = ref(window.innerHeight - 450);

    onMounted(() => {
      interact(draggableElement.value.$el)
        .draggable({
          modifiers: [
            interact.modifiers.restrictRect({
              restriction: 'parent',
              endOnly: true,
            }),
          ],
          listeners: {
            start(event) {
              event.target.style.transition = 'none';
            },
            move(event) {
              x.value += event.dx;
              y.value += event.dy;
            },
            end(event) {
              event.target.style.transition = 'transform 0.3s ease';
            },
          },
        });
    });

    const handlePlanChange = (newPlan) => {
        emit("update:selectedPlan", newPlan);
    };

    return {
      draggableElement,
      x,
      y,
      handlePlanChange,
    };
  },
  data() {
    return {
      anio: "",
      ciclo: "",
      creditos: "",
      nombreIcontains: "",
      formatoDidactico: "",
      estado: "",
      condicion: "",
      materia: "",
      correlativasIn: "",
      mostrarPromocionadas: false,
      mostrarDisponibles: false,
      estadoOptions: [
        { title: 'Pendiente', value: 'pendiente' },
        { title: 'Cursando', value: 'cursando' },
        { title: 'Aprobada', value: 'aprobada' },
        { title: 'Desaprobada', value: 'desaprobada' },
        { title: 'Promocionada', value: 'promocionada' },
      ],
      condicionOptions: [
        { title: 'Ninguno', value: '' },
        { title: 'Obligatoria', value: 'carrera' },
        { title: 'Electiva', value: 'electiva' },
      ],
      cicloOptions: [
        { title: 'Básico', value: 'Básico' },
        { title: 'General', value: 'General' },
        { title: 'Avanzado', value: 'Avanzado' },
      ],
    };
  },
  methods: {
    applyFilter() {
      const filters = {
        anio: this.anio,
        estado: this.estado,
        'nombre__icontains': this.nombreIcontains,
        ciclo: this.ciclo,
        creditos: this.creditos,
        'formato_didactico': this.formatoDidactico,
        condicion: this.condicion,
        materia: this.materia,
        'correlativas__in': this.correlativasIn,
        promocionadas: this.mostrarPromocionadas ? "promocionadas" : "",
        disponibles: this.mostrarDisponibles ? "disponibles" : "",
      };

      Object.keys(filters).forEach((key) => {
        if (filters[key] === "" || filters[key] === null) delete filters[key];
      });

      this.$emit("filter-changed", filters);
    },
  },
};
</script>

<style scoped>
.draggable-card {
  position: absolute;
  z-index: 1000;
  cursor: move;
  user-select: none;
  transition: transform 0.3s ease;
}
</style>