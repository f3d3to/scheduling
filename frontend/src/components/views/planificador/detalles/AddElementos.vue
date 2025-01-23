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
import { usePlanificadorStore } from '@store/PlanificadorStore';

export default {
  props: {
    planificadorId: {
      type: [Number, String],
      required: true,
    },
    celdaId: {
      type: [Number, String],
      required: true,
    },
  },
  setup() {
    const planificadorStore = usePlanificadorStore();
    return { planificadorStore };
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
        const response = await this.planificadorStore.fetchModels();
        this.models = response;
        this.modelsLoaded = true;
      } catch (error) {
        console.error("Error en fetchModels:", error);
        Swal.fire({
          icon: 'error',
          title: 'Error',
          text: 'No se pudieron cargar los modelos.'
        });
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
          const valid = await this.$refs.createForm.validate();
          if (!valid.valid) return;

          const response = await this.planificadorStore.createInstance({
            model: this.selectedModel,
            datos: this.newInstance,
          });
          await this.fetchModels();
          this.onModelChange();
          this.selectedInstance = response.id;
        } else {
          await this.asociarElemento(this.selectedInstance);
        }
        this.closeDialog();
      } catch (error) {
        console.error("Error en submit:", error);
        Swal.fire({
          icon: 'error',
          title: 'Error',
          text: error.message || 'Ocurrió un error inesperado.'
        });
      }
    },
    async asociarElemento(instanciaId) {
      try {
        const response = await this.planificadorStore.asociarElemento(
          this.planificadorId,
          this.celdaId,
          instanciaId,
          this.selectedModel
        );
        push.success({
          title: 'Agregado!',
          message: 'El elemento ha sido agregado correctamente.'

        })
        this.$emit('elemento-asociado', response.id);
      } catch (error) {
        console.error("Error al asociar elemento:", error);
        Swal.fire({
          icon: 'error',
          title: 'Error',
          text: error.message || 'Error al asociar el elemento.'
        });
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