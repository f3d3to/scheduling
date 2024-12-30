<template>
    <div class="tarea-visualizacion">
      <h4>{{ elemento.nombre }}</h4>
      <p>{{ elemento.descripcion }}</p>
      <p>Fecha límite: {{ elemento.fecha_limite }}</p>
      <div>
        <label>
          <input
            type="checkbox"
            v-model="realizada"
            @change="toggleRealizada"
          />
          Completada
        </label>
      </div>
    </div>
</template>

<script>
  export default {
    props: {
      elemento: {
        type: Object,
        required: true,
      },
    },
    data() {
      return {
        realizada: !!this.elemento.esta_realizada,
      };
    },
    methods: {
      async toggleRealizada() {
        try {
          const response = await fetch(
            `http://localhost:8000/tareas/${this.elemento.id}/`,
            {
              method: "PATCH",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify({ esta_realizada: this.realizada }),
            }
          );
          if (!response.ok) {
            throw new Error("No se pudo actualizar la tarea");
          }
        } catch (error) {
          console.error("Error al actualizar tarea:", error);
        }
      },
    },
  };
  </script>

  <style scoped>
  .tarea-visualizacion {
    background-color: #fefefe;
    border-left: 4px solid #ff0000; /* Rojo para tareas */
    padding: 10px;
    margin-bottom: 5px;
    border-radius: 4px;
  }
  </style>
