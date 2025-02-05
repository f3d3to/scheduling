<template>
  <v-dialog v-model="dialogVisible" max-width="600px" persistent>
    <v-card>
      <v-card-title>Agregar evento</v-card-title>
      <v-card-text>
        <v-form @submit.prevent="crearEvento">
          <!-- Sección de Categoría y Elemento -->
          <div class="mb-4">
            <v-select
              v-model="categoriaSeleccionada"
              :items="categorias"
              item-value="categoria"
              item-title="nombre"
              label="Categoría"
              @update:modelValue="cargarElementos"
              :rules="[v => !!v || 'La categoría es requerida']"
              required
            ></v-select>
            <v-select
              v-if="elementos.length"
              v-model="elementoSeleccionado"
              :items="elementos"
              item-value="id"
              item-title="nombre"
              label="Elemento relacionado"
              :rules="[v => !!v || 'El elemento es requerido']"
              required
            ></v-select>
          </div>
          <!-- Información básica del evento -->
          <div class="mb-4">
            <v-text-field
              v-model="titulo"
              label="Título del evento"
              :rules="[v => !!v || 'El título es requerido']"
              required
            ></v-text-field>
            <v-textarea
              v-model="descripcion"
              label="Descripción detallada"
              rows="2"
            ></v-textarea>
          </div>
          <!-- Configuración de tiempo -->
          <div class="mb-4">
            <div class="d-flex gap-4">
              <v-text-field
                v-model="inicio"
                type="datetime-local"
                label="Inicio"
                :rules="[v => !!v || 'La fecha de inicio es requerida']"
                required
              ></v-text-field>
              <v-text-field
                v-model="fin"
                type="datetime-local"
                label="Fin"
                :rules="tipoEsExamen ? [v => !!v || 'La fecha de fin es requerida'] : []"
                :required="tipoEsExamen"
              ></v-text-field>
            </div>
            <v-checkbox
              v-model="todoElDia"
              label="Dura todo el día"
              :disabled="tipoEsRecordatorio"
            ></v-checkbox>
          </div>
          <!-- Selectores de tipo y recurrencia -->
          <div class="mb-4">
            <v-select
              v-model="tipoSeleccionado"
              :items="tipos"
              item-value="id"
              item-title="nombre"
              label="Tipo"
              :rules="[v => !!v || 'El tipo es requerido']"
              required
            ></v-select>
            <v-select
              v-model="recurrenciaSeleccionada"
              :items="recurrencias"
              item-value="id"
              item-title="frecuencia"
              label="Se repite cada"
              clearable
            ></v-select>
          </div>
          <!-- Nuevos campos para FullCalendar -->
          <div class="mb-4">
            <v-select
              v-model="display"
              :items="['block', 'list-item', 'background', 'none']"
              label="Modo de visualización"
              hint="Controla cómo se muestra el evento."
            ></v-select>
            <v-checkbox
              v-model="editable"
              label="¿El evento es editable?"
              hint="Indica si el evento puede ser modificado."
            ></v-checkbox>
            <v-checkbox
              v-model="startEditable"
              label="¿La fecha/hora de inicio es editable?"
              hint="Indica si se puede modificar la fecha/hora de inicio."
            ></v-checkbox>
            <v-checkbox
              v-model="durationEditable"
              label="¿La duración es editable?"
              hint="Indica si se puede modificar la duración del evento."
            ></v-checkbox>
            <v-checkbox
              v-model="resourceEditable"
              label="¿El evento puede moverse entre recursos?"
              hint="Indica si el evento puede asignarse a diferentes recursos."
            ></v-checkbox>
            <v-text-field
              v-model="exdate"
              label="Fechas excluidas de la recurrencia"
              hint="Fechas específicas excluidas de la recurrencia (ISO string)."
            ></v-text-field>
            <v-text-field
              v-model="classNames"
              label="Clases CSS adicionales"
              hint="Clases CSS personalizadas para estilizar el evento."
            ></v-text-field>
          </div>
          <!-- Selectores de color con etiquetas mejoradas -->
          <div class="mb-4">
            <div class="color-picker-group">
              <label class="text-caption">Color principal</label>
              <v-color-picker
                v-model="color"
                mode="hexa"
                hide-inputs
                show-swatches
              ></v-color-picker>
            </div>
            <div class="color-picker-group">
              <label class="text-caption">Color de fondo</label>
              <v-color-picker
                v-model="backgroundColor"
                mode="hexa"
                hide-inputs
                show-swatches
              ></v-color-picker>
            </div>
            <div class="color-picker-group">
              <label class="text-caption">Color de borde</label>
              <v-color-picker
                v-model="borderColor"
                mode="hexa"
                hide-inputs
                show-swatches
              ></v-color-picker>
            </div>
            <div class="color-picker-group">
              <label class="text-caption">Color de texto</label>
              <v-color-picker
                v-model="textColor"
                mode="hexa"
                hide-inputs
                show-swatches
              ></v-color-picker>
            </div>
          </div>
          <!-- URL y acciones -->
          <v-text-field
            v-model="url"
            label="Enlace relacionado"
            type="url"
          ></v-text-field>
          <div class="d-flex justify-space-between mt-4">
            <v-btn
              type="submit"
              color="primary"
              :disabled="!formularioValido"
              :loading="cargando"
            >
              Guardar Evento
            </v-btn>
            <v-btn @click="cerrar" color="secondary">Cancelar</v-btn>
          </div>
        </v-form>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
import { defineComponent, ref, computed, onMounted } from "vue";
import { useEventoAcademicoStore } from "@store/eventoAcademicoStore";

interface Categoria {
  categoria: string;
  nombre: string;
}

interface Elemento {
  id: number;
  nombre: string;
}

interface Tipo {
  id: number;
  nombre: string;
}

interface Recurrencia {
  id: number;
  frecuencia: string;
}

export default defineComponent({
  emits: ["cerrar", "eventoCreado"],
  setup(_, { emit }) {
    const store = useEventoAcademicoStore();
    const dialogVisible = ref(true);
    const cargando = ref(false);

    // Estado reactivo
    const categoriaSeleccionada = ref("");
    const elementoSeleccionado = ref("");
    const titulo = ref("");
    const descripcion = ref("");
    const inicio = ref("");
    const fin = ref("");
    const todoElDia = ref(false);
    const color = ref("#FFFFFF");
    const backgroundColor = ref("#FFFFFF");
    const borderColor = ref("#000000");
    const textColor = ref("#000000");
    const url = ref("");
    const tipoSeleccionado = ref<number | null>(null);
    const recurrenciaSeleccionada = ref<number | null>(null);
    const elementos = ref<Elemento[]>([]);
    const categorias = ref<Categoria[]>([]);
    const tipos = ref<Tipo[]>([]);
    const recurrencias = ref<Recurrencia[]>([]);

    // Nuevos campos para FullCalendar
    const display = ref("block");
    const editable = ref(true);
    const startEditable = ref(true);
    const durationEditable = ref(true);
    const resourceEditable = ref(false);
    const exdate = ref("");
    const classNames = ref("");

    // Cargar datos iniciales
    onMounted(async () => {
      cargando.value = true;
      try {
        await Promise.all([
          store.fetchCategorias(),
          store.fetchTiposEvento(),
          store.fetchRecurrencias(),
        ]);
        categorias.value = store.categorias;
        tipos.value = store.tipos;
        recurrencias.value = store.recurrencias;
      } catch (error) {
        console.error("Error cargando datos iniciales:", error);
      } finally {
        cargando.value = false;
      }
    });

    // Computadas
    const tipoEsExamen = computed(() => tipoSeleccionado.value?.nombre === "examen");
    const tipoEsRecordatorio = computed(() => tipoSeleccionado.value?.nombre === "recordatorio");

    const formularioValido = computed(() => {
      return (
        !!categoriaSeleccionada.value &&
        !!elementoSeleccionado.value &&
        !!titulo.value &&
        !!inicio.value &&
        (!tipoEsExamen.value || !!fin.value)
      );
    });

    // Métodos
    const cargarElementos = async () => {
      if (!categoriaSeleccionada.value) return;
      try {
        await store.fetchElementos(categoriaSeleccionada.value);
        elementos.value = store.elementos;
        elementoSeleccionado.value = "";
      } catch (error) {
        console.error("Error cargando elementos:", error);
      }
    };

    const crearEvento = async () => {
      cargando.value = true;
      try {
        if (!tipoSeleccionado.value) {
          throw new Error("El tipo de evento es obligatorio.");
        }

        await store.crearEvento({
          content_type: categoriaSeleccionada.value,
          object_id: elementoSeleccionado.value,
          titulo: titulo.value,
          descripcion: descripcion.value,
          inicio: inicio.value,
          fin: fin.value || null,
          todo_el_dia: todoElDia.value,
          color: color.value,
          background_color: backgroundColor.value,
          border_color: borderColor.value,
          text_color: textColor.value,
          url: url.value || null,
          tipo: tipoSeleccionado.value, // Enviar solo el ID del tipo
          recurrencia: recurrenciaSeleccionada.value || null, // Enviar solo el ID de la recurrencia
          display: display.value,
          editable: editable.value,
          start_editable: startEditable.value,
          duration_editable: durationEditable.value,
          resource_editable: resourceEditable.value,
          exdate: exdate.value || null,
          class_names: classNames.value || null,
        });
        emit("eventoCreado");
        cerrar();
      } catch (error) {
        console.error("Error creando evento:", error);
      } finally {
        cargando.value = false;
      }
    };

    const cerrar = () => {
      // Resetear estado al cerrar
      categoriaSeleccionada.value = "";
      elementoSeleccionado.value = "";
      titulo.value = "";
      descripcion.value = "";
      inicio.value = "";
      fin.value = "";
      todoElDia.value = false;
      color.value = "#FFFFFF";
      backgroundColor.value = "#FFFFFF";
      borderColor.value = "#000000";
      textColor.value = "#000000";
      url.value = "";
      tipoSeleccionado.value = null;
      recurrenciaSeleccionada.value = null;
      elementos.value = [];
      display.value = "block";
      editable.value = true;
      startEditable.value = true;
      durationEditable.value = true;
      resourceEditable.value = false;
      exdate.value = "";
      classNames.value = "";
      emit("cerrar");
    };

    return {
      dialogVisible,
      cargando,
      categoriaSeleccionada,
      elementoSeleccionado,
      titulo,
      descripcion,
      inicio,
      fin,
      todoElDia,
      color,
      backgroundColor,
      borderColor,
      textColor,
      url,
      tipoSeleccionado,
      recurrenciaSeleccionada,
      elementos,
      categorias,
      tipos,
      recurrencias,
      display,
      editable,
      startEditable,
      durationEditable,
      resourceEditable,
      exdate,
      classNames,
      tipoEsExamen,
      tipoEsRecordatorio,
      formularioValido,
      cargarElementos,
      crearEvento,
      cerrar,
    };
  },
});
</script>

<style scoped>
.color-picker-group {
  margin: 1rem 0;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 0.5rem;
}
.color-picker-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: rgba(0, 0, 0, 0.6);
}
.gap-4 {
  gap: 1rem;
}
</style>