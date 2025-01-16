<template>
  <v-dialog v-model="dialog" max-width="600px">
    <v-card>
      <v-card-title class="title-container">
        <span class="title-dialog text-h6">Añadir Elemento</span>
        <v-icon @click="closeDialog" class="close-button" size="small">
          mdi-close
        </v-icon>
      </v-card-title>
      <v-card-text>
        <div class="d-flex align-center">
          <v-select
            v-model="selectedModel"
            :items="models"
            item-title="nombre"
            item-value="model"
            label="Selecciona el tipo de elemento"
            @update:modelValue="onModelChange"
            class="flex-grow-1"
          ></v-select>
          <v-checkbox
            v-model="createInstance"
            label="Crear elemento"
            @change="toggleCreateForm"
            class="ml-4"
          ></v-checkbox>
        </div>
        <v-select
          v-if="selectedModel && !createInstance"
          v-model="selectedInstance"
          :items="instances"
          item-title="nombre"
          item-value="id"
          label="Selecciona tu elemento"
          :key="selectedModel"
        ></v-select>

        <div v-if="createFormVisible">
          <v-form ref="createForm" v-model="valid">
            <v-text-field
              v-for="campo in selectedModelData.campos"
              :key="campo"
              v-model="newInstance[campo]"
              :label="campo"
              :rules="[v => !!v || 'Campo requerido']"
            ></v-text-field>
          </v-form>
        </div>
      </v-card-text>
      <v-card-actions>
        <v-btn color="primary" @click="submit" :disabled="!isSaveEnabled">
          Guardar
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import Swal from 'sweetalert2';
export default {
  props: {
    planificadorId: {
      type: [Number, String], // Podría ser String si tu ID es un UUID
      required: true,
    },
    celdaId: {
      type: [Number, String],
      required: true,
    },
  },
  data() {
    return {
      models: [],
      selectedModel: null,
      selectedInstance: null,
      dialog: false,
      modelsLoaded: false,
      instances: [],
      createInstance: false,
      createFormVisible: false,
      newInstance: {},
      valid: false,
    };
  },
  computed: {
    selectedModelData() {
      return this.models.find(
        (model) => model.model === this.selectedModel
      );
    },
    isSaveEnabled() {
      return this.createFormVisible
        ? this.valid
        : this.selectedInstance !== null;
    },
  },
  methods: {
    openDialog() {
      this.dialog = true;
      if (!this.modelsLoaded) {
        this.fetchModels();
      }
    },
    closeDialog() {
      this.dialog = false;
      this.resetState();
    },
    resetState() {
      this.selectedModel = null;
      this.selectedInstance = null;
      this.instances = [];
      this.createInstance = false;
      this.createFormVisible = false;
      this.newInstance = {};
    },
    async fetchModels() {
      try {
        const response = await fetch("http://localhost:8000/models/");
        if (!response.ok) throw new Error("Error al obtener modelos");
        this.models = await response.json();
        this.modelsLoaded = true;
      } catch (error) {
        console.error("Error en fetchModels:", error);
        this.modelsLoaded = false;
      }
    },
    onModelChange() {
        this.selectedInstance = null;
        this.createInstance = false;
        this.createFormVisible = false;
        if (this.selectedModel) {
          this.instances = this.selectedModelData
            ? this.selectedModelData.instancias
            : [];
        } else {
          this.instances = [];
        }
      },
    toggleCreateForm() {
      this.createFormVisible = this.createInstance;
      if (this.createFormVisible) {
        this.newInstance = {};
        if (
          this.selectedModelData &&
          this.selectedModelData.campos
        ) {
          this.selectedModelData.campos.forEach((campo) => {
            this.newInstance[campo] = "";
          });
        }
      }
    },
    async submit() {
      try {
        if (this.createFormVisible) {
          const response = await fetch(
            "http://localhost:8000/models/",
            {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify({
                modelo: this.selectedModel,
                datos: this.newInstance,
              }),
            }
          );
          if (!response.ok)
            throw new Error("Error al crear la instancia");
          const data = await response.json();
          await this.fetchModels();
          this.onModelChange();
          this.selectedInstance = data.id;
        } else {
          await this.asociarElemento(this.selectedInstance);
          console.log(
            "Asociando instancia existente:",
            this.selectedInstance
          );
        }
        this.closeDialog();
      } catch (error) {
        console.error("Error en submit:", error);
      }
    },
    async asociarElemento(instanciaId) {
      const planificadorId = this.planificadorId;
      const celdaId = this.celdaId;
      try {
        const response = await fetch(
          `http://localhost:8000/celdas/${planificadorId}/${celdaId}/elementos/`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ instancia_id: instanciaId , model:this.selectedModel}),
          }
        );

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.error || "Error al asociar el elemento");
        }

        const data = await response.json();
        Swal.fire({
                title: "Agregado!",
                text: "El elemento ha sido agregado con éxito.",
                icon: "success",
                confirmButtonColor: "#54a832",
              });

        this.$emit('elemento-asociado', data.id); // Emitir evento para actualizar la celda
      } catch (error) {
        console.error("Error al asociar elemento:", error);
        console.log(error.message);
      }
    },
  },
};
</script>

<style scoped>
.title-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.close-button {
  margin-right: auto;
}
.title-dialog {
  flex-grow: 1;
  text-align: center;
}
</style>