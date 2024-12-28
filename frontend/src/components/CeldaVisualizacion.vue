<template>
  <v-card
    class="celda"
    :style="{ width: anchoColumna + 'px', margin: '10px auto' }"
    @click="seleccionarCelda"
  >
    <v-card-text>
      <div v-if="modoEdicion">
        <v-textarea
          v-model="contenidoLocal"
          auto-grow
          rows="2"
          @blur="guardarCambios"
        ></v-textarea>
      </div>
      <div v-else>
        <div>ID: {{ celda.id }}</div>
        <div>Contenido: {{ celda.contenido }}</div>
        <div v-if="elementosRelacionados && elementosRelacionados.length > 0">
          Elementos Relacionados:
          <ul>
            <li v-for="elemento in elementosRelacionados" :key="elemento.id">
              <strong>{{ elemento.nombre }}</strong>
              <v-textarea
                v-model="elemento.descripcion"
                auto-grow
                rows="2"
                @blur="guardarElemento(elemento)"
              ></v-textarea>
              <p>{{ elemento.content_object }}</p>
            </li>
          </ul>
        </div>
        <div v-else>
          No hay elementos relacionados.
        </div>
      </div>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  props: {
    celda: {
      type: Object,
      required: true,
    },
    anchoColumna: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      modoEdicion: false,
      contenidoLocal: this.celda.contenido,
      elementosRelacionados: [], // Inicializada como array vacío para elementos
    };
  },
  mounted() {
    this.cargarElementosRelacionados();
  },
  methods: {
    seleccionarCelda() {
      this.$emit("celda-seleccionada", this.celda);
      this.modoEdicion = true;
    },
    async guardarCambios() {
      this.modoEdicion = false;
      this.$emit("actualizar-celda", {
        ...this.celda,
        contenido: this.contenidoLocal,
      });
    },
    async guardarElemento(elemento) {
      try {
        const response = await fetch(
          `http://localhost:8000/elementos/${elemento.id}/`,
          {
            method: "PATCH",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ descripcion: elemento.descripcion }),
          }
        );
        if (!response.ok) {
          console.error(
            "Error al actualizar el elemento relacionado:",
            response.status
          );
        }
      } catch (error) {
        console.error("Error al actualizar el elemento relacionado:", error);
      }
    },
    async cargarElementosRelacionados() {
      try {
        const response = await fetch(
          `http://localhost:8000/elementos/?celda_id=${this.celda.id}`
        );
        if (response.ok) {
          const data = await response.json();
          this.elementosRelacionados = data.results || data;
          console.log(
            "Elementos relacionados cargados:",
            this.elementosRelacionados
          );
        } else {
          console.error(
            "Error al cargar los elementos relacionados:",
            response.status
          );
        }
      } catch (error) {
        console.error("Error al cargar los elementos relacionados:", error);
      }
    },
  },
};
</script>

<style scoped>
.celda {
  border: 1px solid #ccc;
  padding: 20px; /* Aumentado para mejorar visibilidad */
  text-align: left; /* Alineación ajustada para leer mejor el contenido */
  font-size: 14px; /* Aumentar el tamaño del texto */
  cursor: pointer;
  background-color: #f9f9f9; /* Fondo suave para diferenciar celdas */
  box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1); /* Agregado para mejor visualización */
}
.v-card {
  margin: 10px auto; /* Evita espacio excesivo debajo de la topbar */
}
</style>
