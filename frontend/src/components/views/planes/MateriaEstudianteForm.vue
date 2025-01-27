<template>
  <v-form @submit.prevent="submitForm" ref="formRef">
    <v-card>
      <v-card-title>
        Crear Nueva Materia Estudiante
        <v-icon @click="resetForm">mdi-arrow-u-left-top</v-icon>
        <v-icon @click="closeForm">mdi-close</v-icon>
      </v-card-title>
      <v-card-text>
        <!-- Nota Final -->
        <v-text-field
          v-model="form.nota_final"
          label="Nota Final"
          type="number"
          step="0.01"
          :rules="[validateNota]"
        ></v-text-field>

        <!-- Final Obligatorio -->
        <v-checkbox
          v-model="form.final_obligatorio"
          label="Final Obligatorio"
        ></v-checkbox>

        <!-- Cátedra -->
        <v-text-field
          v-model="form.catedra"
          label="Cátedra"
        ></v-text-field>

        <!-- Comentarios -->
        <v-textarea
          v-model="form.comentarios"
          label="Comentarios"
        ></v-textarea>

        <!-- Intentos -->
        <v-text-field
          v-model="form.intentos"
          label="Intentos"
          type="number"
          :rules="[validateIntentos]"
        ></v-text-field>

        <!-- Comentarios del Docente -->
        <v-textarea
          v-model="form.comentarios_docente"
          label="Comentarios del Docente"
        ></v-textarea>

        <!-- Estado -->
        <v-select
          v-model="form.estado"
          :items="estados"
          label="Estado"
          :rules="[required]"
          required
        ></v-select>

        <!-- Fecha de Inscripción -->
        <v-text-field
          v-model="form.fecha_inscripcion"
          label="Fecha de Inscripción"
          type="date"
        ></v-text-field>

        <!-- Método de Aprobación -->
        <v-select
          v-model="form.metodo_aprobacion"
          :items="metodosAprobacion"
          label="Método de Aprobación"
        ></v-select>

        <!-- Créditos Asignados -->
        <v-text-field
          v-model="form.creditos_asignados"
          label="Créditos Asignados"
          type="number"
        ></v-text-field>

        <!-- Dificultad -->
        <v-text-field
          v-model="form.dificultad"
          label="Dificultad"
          type="number"
          :rules="[validateDificultad]"
        ></v-text-field>

        <!-- Disponible -->
        <v-checkbox
          v-model="form.disponible"
          label="Disponible"
        ></v-checkbox>
      </v-card-text>
      <v-card-actions>
        <v-btn type="submit" color="primary">
          Crear
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-form>
</template>

<script>
import { defineComponent, ref } from 'vue';
import { useGraphStore } from '@/store/GraphStore'; // Asegúrate de importar tu store

export default defineComponent({
  name: 'MateriaEstudianteForm',
  props: {
    materia: {
      type: Object,
      required: true, // La materia es obligatoria
    },
  },
  emits: ['close', 'created'], // Eventos para cerrar y notificar creación
  setup(props, { emit }) {
    const form = ref({
      estudiante: null, //
      materia: props.materia.metadata.id, // La materia se toma de la prop
      nota_final: null,
      final_obligatorio: true,
      catedra: '',
      comentarios: '',
      intentos: 0,
      comentarios_docente: '',
      estado: 'pendiente',
      fecha_inscripcion: null,
      metodo_aprobacion: null,
      creditos_asignados: null,
      dificultad: null,
      disponible: false,
    });
    const graphStore = useGraphStore();
    const estados = ref(['pendiente', 'cursando', 'aprobada', 'desaprobada', 'promocionada']);
    const metodosAprobacion = ref(['final', 'promocion', 'equivalencia']);
    const formRef = ref(null);

    // Reglas de validación
    const required = (value) => !!value || 'Este campo es obligatorio.';
    const validateNota = (value) => {
      if (value === null || value === '') return true;
      const nota = parseFloat(value);
      return (nota >= 0 && nota <= 10) || 'La nota debe estar entre 0 y 10.';
    };
    const validateIntentos = (value) => {
      const intentos = parseInt(value, 10);
      return intentos >= 0 || 'Los intentos no pueden ser negativos.';
    };
    const validateDificultad = (value) => {
      if (value === null || value === '') return true;
      const dificultad = parseInt(value, 10);
      return (dificultad >= 1 && dificultad <= 5) || 'La dificultad debe estar entre 1 y 5.';
    };

    const submitForm = async () => {
      const isValid = await formRef.value.validate();
      if (!isValid.valid) return;

      try {
        const response = await graphStore.createMateriaEstudiante(form.value);
        if (!response.status === 201) throw new Error('Error al crear');
        emit('created');
        emit('materia-estudiante-created', response.data);
        resetForm();
        emit('close');
      } catch (error) {
        console.error('Error:', error);
      }
    };


    // Resetear formulario (optimizado)
    const resetForm = () => {
      Object.assign(form.value, {
        estudiante: null, //
        materia: props.materia.id,
        nota_final: null,
        final_obligatorio: true,
        catedra: '',
        comentarios: '',
        intentos: 0,
        comentarios_docente: '',
        estado: 'pendiente',
        fecha_inscripcion: null,
        metodo_aprobacion: null,
        creditos_asignados: null,
        dificultad: null,
        disponible: false,
      });
    };

    // Cerrar formulario
    const closeForm = () => {
      emit('close');
    };

    return {
      form,
      estados,
      metodosAprobacion,
      formRef,
      required,
      validateNota,
      validateIntentos,
      validateDificultad,
      submitForm,
      resetForm,
      closeForm,
    };
  },
});
</script>

<style scoped>
/* Estilo principal del formulario alineado al sidebar */
.v-card {
  background: #1e1e2f;
  color: white;
}

/* Título del card */
.v-card-title {
  background: linear-gradient(90deg, #2c2c3e, #1e1e2f);
  color: white;
  padding: 1rem;
  font-size: 1.2rem;
  font-weight: 500;
  border-bottom: 1px solid #535bf2;
}

/* Contenido del formulario */
.v-card-text {
  padding: 1.5rem;
  background: #1e1e2f;
}

/* Campos del formulario */
.v-text-field :deep(.v-input__control),
.v-select :deep(.v-input__control),
.v-textarea :deep(.v-input__control) {
  background-color: rgba(255, 255, 255, 0.05);
  border-radius: 4px;
  margin-bottom: 1rem;
}

/* Labels y texto */
:deep(.v-label) {
  color: #a0a0c0 !important;
  font-size: 0.9rem;
}

/* Inputs y textareas */
:deep(.v-input__slot) {
  background: transparent !important;
}

:deep(.v-input input),
:deep(.v-input textarea) {
  color: white !important;
  caret-color: #535bf2;
}

/* Select items */
:deep(.v-select__selection) {
  color: white !important;
}

/* Checkboxes */
:deep(.v-icon) {
  color: #535bf2 !important;
}

/* Botones de acciones */
.v-card-actions {
  background: #2c2c3e;
  padding: 1rem;
  border-top: 1px solid #535bf2;
}

.v-btn {
  background-color: #535bf2 !important;
  color: white !important;
  text-transform: uppercase;
  font-weight: 500;
  letter-spacing: 0.05em;
}

/* Iconos */
.v-icon {
  color: #a0a0c0;
  cursor: pointer;
  transition: color 0.3s;
  margin: 0 0.5rem;
}

.v-icon:hover {
  color: #535bf2;
}

/* Mensajes de validación */
:deep(.v-messages__message) {
  color: #ff5252 !important;
  font-size: 0.8rem;
}

/* Efectos de focus */
:deep(.v-input--is-focused .v-label) {
  color: #535bf2 !important;
}

:deep(.v-input--is-focused .v-input__slot) {
  box-shadow: 0 0 0 2px rgba(83, 91, 242, 0.3) !important;
}
</style>