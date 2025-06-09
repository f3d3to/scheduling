<template>
  <v-container class="plan-container">
    <h1 class="text-h4 font-weight-bold text-center mb-2">Creación de Plan de Estudio</h1>
    <p class="text-subtitle-1 text-center mb-6">Siga los pasos para configurar el plan, sus materias y correlatividades.</p>

    <v-stepper v-model="step" :items="stepperItems" alt-labels editable>
      <template v-slot:item.1>
        <v-card title="Paso 1: Datos Generales del Plan" flat>
          <v-card-text>
            <v-form ref="planForm">
              <v-text-field
                v-model="plan.nombre"
                label="Nombre del Plan de Estudio"
                :rules="[rules.required]"
                variant="outlined"
                class="mb-4"
              ></v-text-field>
              <v-text-field
                v-model.number="plan.año_creacion"
                label="Año de Creación"
                type="number"
                :rules="[rules.required, rules.year]"
                variant="outlined"
                class="mb-4"
              ></v-text-field>
              <v-textarea
                v-model="plan.descripcion"
                label="Descripción (Opcional)"
                variant="outlined"
                rows="3"
              ></v-textarea>
            </v-form>
          </v-card-text>
        </v-card>
      </template>

      <template v-slot:item.2>
        <v-card title="Paso 2: Agregar Materias" flat>
          <v-card-text>
            <p v-if="!materias.length" class="text-center text-grey mb-4">Aún no hay materias. ¡Agregue la primera!</p>
            <v-list>
              <v-list-item v-for="(materia, index) in materias" :key="materia.id" class="mb-2">
                <v-text-field
                  v-model="materia.nombre"
                  :label="`Nombre de la Materia ${index + 1}`"
                  :rules="[rules.required]"
                  variant="outlined"
                  density="compact"
                  hide-details="auto"
                >
                  <template v-slot:append>
                    <v-btn icon="mdi-delete" variant="text" color="red" @click="removeMateria(index)"></v-btn>
                  </template>
                </v-text-field>
              </v-list-item>
            </v-list>
            <v-btn color="primary" @click="addMateria" block class="mt-4">
              <v-icon left>mdi-plus</v-icon>
              Agregar Materia
            </v-btn>
          </v-card-text>
        </v-card>
      </template>

      <template v-slot:item.3>
        <v-card title="Paso 3: Detalles y Vista Previa" flat>
          <v-card-text>
            <h3 class="text-h6 mb-4">Complete los datos de cada materia</h3>
             <v-expansion-panels variant="inset" class="mb-6">
              <v-expansion-panel v-for="(materia, idx) in materias" :key="materia.id">
                <v-expansion-panel-title>
                  {{ materia.nombre || `Materia #${idx+1}` }} <span class="text-grey ms-2">({{ materia.codigo || 'Sin código' }})</span>
                </v-expansion-panel-title>
                <v-expansion-panel-text>
                  <v-form>
                    <v-row>
                      <v-col cols="12" sm="6">
                        <v-text-field v-model="materia.codigo" label="Código (único)" :rules="[rules.required]" variant="outlined" density="compact" />
                      </v-col>
                      <v-col cols="12" sm="6">
                        <v-autocomplete
                          v-model="materia.correlativas"
                          :items="availableCorrelativas(materia.id)"
                          item-title="nombre"
                          item-value="codigo"
                          label="Correlativas"
                          multiple
                          chips
                          closable-chips
                          variant="outlined"
                          density="compact"
                        />
                      </v-col>
                      <v-col cols="6" md="3">
                        <v-text-field v-model.number="materia.anio" label="Año" type="number" :rules="[rules.required]" variant="outlined" density="compact" />
                      </v-col>
                      <v-col cols="6" md="3">
                        <v-text-field v-model.number="materia.cuatrimestre" label="Cuatrimestre" type="number" :rules="[rules.required]" variant="outlined" density="compact" />
                      </v-col>
                      <v-col cols="6" md="3">
                        <v-text-field v-model.number="materia.creditos" label="Créditos" type="number" :rules="[rules.required]" variant="outlined" density="compact" />
                      </v-col>
                      <v-col cols="6" md="3">
                        <v-text-field v-model.number="materia.ch_semanal" label="Horas semanales" type="number" :rules="[rules.required]" variant="outlined" density="compact" />
                      </v-col>
                      <v-col cols="12" md="3">
                        <v-select v-model="materia.ciclo" :items="ciclosOptions" label="Ciclo" :rules="[rules.required]" variant="outlined" density="compact" />
                      </v-col>
                      <v-col cols="12" md="3">
                        <v-select v-model="materia.condicion" :items="condicionOptions" label="Condición" :rules="[rules.required]" variant="outlined" density="compact" />
                      </v-col>
                      <v-col cols="12" md="3">
                        <v-select
                          v-model="materia.formato_didactico"
                          :items="formatoOptions"
                          label="Formato didáctico (opcional)"
                          variant="outlined"
                          density="compact"
                        />
                      </v-col>
                      <v-col cols="6" md="3">
                        <v-text-field v-model.number="materia.ch_cuatrimestral" label="Horas cuatrimestrales (opcional)" type="number" variant="outlined" density="compact" />
                      </v-col>
                      <v-col cols="6" md="3">
                        <v-text-field v-model.number="materia.ch_presencial" label="Horas presenciales (opcional)" type="number" variant="outlined" density="compact" />
                      </v-col>
                      <v-col cols="6" md="3">
                        <v-text-field v-model.number="materia.ch_distancia" label="Horas a distancia (opcional)" type="number" variant="outlined" density="compact" />
                      </v-col>
                      <v-col cols="6" md="3">
                        <v-text-field v-model.number="materia.ch_total" label="Horas totales (opcional)" type="number" variant="outlined" density="compact" />
                      </v-col>
                      <v-col cols="12">
                        <v-textarea v-model="materia.descripcion" label="Descripción (opcional)" rows="2" variant="outlined" density="compact" />
                      </v-col>
                    </v-row>
                  </v-form>
                </v-expansion-panel-text>
              </v-expansion-panel>
            </v-expansion-panels>

            <h3 class="text-h6 mt-6 mb-2">Previsualización de Correlatividades</h3>
            <v-card variant="outlined">
                <div ref="graphContainer" style="min-height: 400px; width: 100%;"></div>
            </v-card>
          </v-card-text>
        </v-card>
      </template>

      <template v-slot:actions>
        <div class="d-flex justify-space-between w-100 pa-4">
          <v-btn :disabled="step === 1" @click="step--">Anterior</v-btn>
          <v-btn v-if="step < 3" color="primary" @click="nextStep">Siguiente</v-btn>
          <v-btn v-if="step === 3" color="success" @click="confirmarGuardado">Guardar Plan de Estudio</v-btn>
        </div>
        <div class="d-flex flex-column align-center mt-4">
          <v-btn color="error" variant="outlined" @click="descartarBorrador" class="mb-2">Descartar borrador</v-btn>
          <v-menu v-if="borradores.length" open-on-hover>
            <template v-slot:activator="{ props }">
              <v-btn v-bind="props" color="secondary" variant="outlined">Cargar borrador</v-btn>
            </template>
            <v-list>
              <v-list-item v-for="b in borradores" :key="b.id" @click="cargarBorrador(b.id)">
                <v-list-item-title>{{ b.data.plan?.nombre || 'Borrador sin nombre' }}</v-list-item-title>
                <v-list-item-subtitle>Último paso: {{ b.data.step }}</v-list-item-subtitle>
              </v-list-item>
            </v-list>
          </v-menu>
        </div>
      </template>
    </v-stepper>
  </v-container>
</template>

<script setup>
import { ref, reactive, watch, onMounted } from 'vue';
import * as d3 from 'd3';
import Swal from 'sweetalert2';
import { useGraphStore } from '@/store/GraphStore';
import { saveDraft, loadDraft, listDrafts, removeDraft } from '@/utils/draftUtils';

// --- ESTADO REACTIVO ---
const step = ref(1);
const planForm = ref(null);
const stepperItems = ['Datos del Plan', 'Agregar Materias', 'Vista Previa'];
const graphContainer = ref(null);

const plan = reactive({
  nombre: '',
  año_creacion: new Date().getFullYear(),
  descripcion: ''
});

const materias = reactive([]);
let nextMateriaId = 0;

const draftId = ref('crearPlanDraft'); // Puede ser dinámico si se desea múltiples borradores
const borradores = ref([]);

// Opciones para selects
const ciclosOptions = ['Básico', 'General', 'Avanzado', 'Optativo'];
const condicionOptions = ['carrera', 'electiva'];
const formatoOptions = ['Presencial', 'Virtual', 'Mixto'];

// --- REGLAS DE VALIDACIÓN ---
const rules = {
  required: value => !!value || 'Este campo es requerido.',
  year: value => (value >= 1900 && value <= 2100) || 'Ingrese un año válido.'
};

// --- LÓGICA DE NAVEGACIÓN ---
const nextStep = async () => {
  if (step.value === 1) {
    const { valid } = await planForm.value.validate();
    if (!valid) return;
  }
  if (step.value === 2) {
    if (materias.length === 0) {
      Swal.fire('Atención', 'Debe agregar al menos una materia.', 'warning');
      return;
    }
    const allNamesFilled = materias.every(m => m.nombre);
    if (!allNamesFilled) {
       Swal.fire('Atención', 'Todas las materias deben tener un nombre.', 'warning');
      return;
    }
  }
  if (step.value < 3) step.value++;
};

// --- LÓGICA DE MATERIAS ---
const addMateria = () => {
  materias.push({
    id: nextMateriaId++,
    nombre: '',
    codigo: '',
    anio: null,
    cuatrimestre: null,
    creditos: null,
    ch_semanal: null,
    ciclo: '',
    condicion: '',
    formato_didactico: '', // valor inicial vacío
    ch_cuatrimestral: null,
    ch_presencial: null,
    ch_distancia: null,
    ch_total: null,
    descripcion: '',
    correlativas: []
  });
};

const removeMateria = (index) => {
  materias.splice(index, 1);
};

const availableCorrelativas = (materiaId) => {
  return materias.filter(m => m.id !== materiaId && m.codigo);
};

// --- LÓGICA DEL GRAFO D3 (CON FLECHAS) ---
const drawGraph = () => {
  const container = graphContainer.value;
  if (!container || materias.length === 0) return;

  d3.select(container).selectAll('*').remove();

  const validMaterias = materias.filter(m => m.anio && m.codigo);
  if (validMaterias.length === 0) return;

  const width = container.clientWidth;
  const height = 500;
  const margin = { top: 60, right: 40, bottom: 20, left: 40 };
  const nodeRadius = 15;

  const svg = d3.select(container).append("svg")
      .attr("width", width)
      .attr("height", height)
      .attr("viewBox", [0, 0, width, height]);

  // --- INICIO: Definición de la Flecha ---
  // Se crea una sección <defs> para definir elementos reutilizables.
  svg.append('defs').append('marker')
    .attr('id', 'arrowhead') // ID para referenciarla luego
    .attr('viewBox', '-0 -5 10 10') // Sistema de coordenadas del marcador
    .attr('refX', 10) // Posición de la punta de la flecha
    .attr('refY', 0)
    .attr('orient', 'auto') // Rota automáticamente con la línea
    .attr('markerWidth', 6) // Ancho de la flecha
    .attr('markerHeight', 6)
    .append('svg:path')
    .attr('d', 'M0,-5L10,0L0,5') // Forma del triángulo de la flecha
    .attr('fill', '#999');
  // --- FIN: Definición de la Flecha ---

  // 1. Agrupar materias por año
  const materiasPorAnio = d3.group(validMaterias, d => d.anio);
  const anios = Array.from(materiasPorAnio.keys()).sort((a, b) => a - b);
  const colorScale = d3.scaleOrdinal(d3.schemeCategory10).domain(anios);

  // 2. Calcular posiciones
  const nodePositions = new Map();
  const columnWidth = (width - margin.left - margin.right) / (anios.length || 1);

  anios.forEach((anio, i) => {
    const materiasDelAnio = materiasPorAnio.get(anio);
    const columnX = margin.left + i * columnWidth + columnWidth / 2;

    svg.append("rect")
      .attr("x", margin.left + i * columnWidth)
      .attr("y", margin.top - 20)
      .attr("width", columnWidth)
      .attr("height", height - margin.top - margin.bottom + 20)
      .attr("fill", "#f8f9fa")
      .attr("stroke", "#e9ecef")
      .attr("rx", 5);

    svg.append("text")
      .attr("x", columnX)
      .attr("y", margin.top - 30)
      .attr("text-anchor", "middle")
      .attr("font-weight", "bold")
      .attr("font-size", "14px")
      .text(`Año ${anio}`);

    materiasDelAnio.forEach((materia, j) => {
      const ySpacing = (height - margin.top - margin.bottom) / (materiasDelAnio.length + 1);
      const nodeY = margin.top + (j + 1) * ySpacing;
      nodePositions.set(materia.codigo, { x: columnX, y: nodeY, ...materia });
    });
  });

  const nodes = Array.from(nodePositions.values());

  // 3. Preparar enlaces (curvos)
  const links = [];
  validMaterias.forEach(m => {
    m.correlativas.forEach(corrCodigo => {
      if (nodePositions.has(m.codigo) && nodePositions.has(corrCodigo)) {
        let sourceNode = nodePositions.get(corrCodigo);
        let targetNode = nodePositions.get(m.codigo);

        // --- INICIO: Ajuste de coordenadas para que la flecha termine en el borde del círculo ---
        const dx = targetNode.x - sourceNode.x;
        const dy = targetNode.y - sourceNode.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        const ratio = (distance - nodeRadius) / distance; // Reducir la longitud por el radio del nodo

        const adjustedTarget = {
          x: sourceNode.x + dx * ratio,
          y: sourceNode.y + dy * ratio
        };
        // --- FIN: Ajuste de coordenadas ---

        links.push({
          source: sourceNode,
          target: adjustedTarget // Usar el punto de destino ajustado
        });
      }
    });
  });

  const linkGenerator = d3.linkHorizontal()
    .x(d => d.x)
    .y(d => d.y);

  svg.append("g")
      .attr("fill", "none")
      .attr("stroke", "#999")
      .attr("stroke-opacity", 0.6)
    .selectAll("path")
    .data(links)
    .join("path")
      .attr("d", d => linkGenerator({source: d.source, target: d.target}))
      .attr("stroke-width", 1.5)
      .attr('marker-end', 'url(#arrowhead)'); // <-- SE APLICA LA FLECHA A CADA LÍNEA

  // 4. Dibujar nodos
  const nodeGroup = svg.append("g")
    .selectAll("g")
    .data(nodes)
    .join("g")
      .attr("transform", d => `translate(${d.x},${d.y})`);

  nodeGroup.append("circle")
    .attr("r", nodeRadius)
    .attr("fill", d => colorScale(d.anio))
    .attr("stroke", "#fff")
    .attr("stroke-width", 2);

  // 5. Dibujar etiquetas
  nodeGroup.append("text")
    .text(d => d.nombre)
    .attr("text-anchor", "middle")
    .attr("y", 28)
    .attr("font-size", "11px")
    .attr("fill", "#333");

  nodeGroup.append("title")
    .text(d => `${d.nombre} (Código: ${d.codigo})`);
};


// --- WATCHERS ---
watch(materias, () => {
  if (step.value === 3) {
    drawGraph();
  }
}, { deep: true });

watch(step, (newStep) => {
  if (newStep === 3) {
    setTimeout(drawGraph, 100);
  }
});

// Guardar borrador automáticamente al cambiar plan, materias o step
watch([plan, materias, step], () => {
  saveDraft(draftId.value, {
    plan: JSON.parse(JSON.stringify(plan)),
    materias: JSON.parse(JSON.stringify(materias)),
    step: step.value
  });
}, { deep: true });

// Cargar borrador al montar
onMounted(() => {
  const draft = loadDraft(draftId.value);
  if (draft) {
    Object.assign(plan, draft.plan);
    materias.splice(0, materias.length, ...draft.materias);
    step.value = draft.step || 1;
  }
  // Listar borradores existentes
  borradores.value = listDrafts();
});

// Función para descartar el borrador actual
const descartarBorrador = () => {
  removeDraft(draftId.value);
  Object.assign(plan, { nombre: '', año_creacion: new Date().getFullYear(), descripcion: '' });
  materias.splice(0, materias.length);
  step.value = 1;
  borradores.value = listDrafts();
};

// Función para cargar un borrador seleccionado
const cargarBorrador = (id) => {
  const draft = loadDraft(id);
  if (draft) {
    Object.assign(plan, draft.plan);
    materias.splice(0, materias.length, ...draft.materias);
    step.value = draft.step || 1;
    draftId.value = id;
  }
};

// --- LÓGICA DE GUARDADO FINAL (sin cambios) ---
const graphStore = useGraphStore();

const confirmarGuardado = async () => {
  const allMateriasValid = materias.every(m =>
    m.nombre && m.codigo && m.anio && m.cuatrimestre && m.creditos && m.ch_semanal && m.ciclo && m.condicion
  );
  if (!allMateriasValid) {
    Swal.fire('Datos Incompletos', 'Por favor, complete todos los campos de todas las materias.', 'error');
    return;
  }
  const payload = {
    nombre: plan.nombre,
    año_creacion: plan.año_creacion,
    descripcion: plan.descripcion,
    materias: materias.map(m => ({
      nombre: m.nombre,
      codigo: m.codigo,
      anio: m.anio,
      cuatrimestre: m.cuatrimestre,
      creditos: m.creditos,
      ch_semanal: m.ch_semanal,
      ciclo: m.ciclo,
      condicion: m.condicion,
      formato_didactico: m.formato_didactico,
      ch_cuatrimestral: m.ch_cuatrimestral,
      ch_presencial: m.ch_presencial,
      ch_distancia: m.ch_distancia,
      ch_total: m.ch_total,
      descripcion: m.descripcion,
      correlativas: m.correlativas
    }))
  };

  try {
    await graphStore.createPlanConMaterias(payload);
    Swal.fire({
      title: '¡Éxito!',
      text: 'El plan de estudio se ha guardado correctamente.',
      icon: 'success',
      timer: 2000,
      showConfirmButton: false
    });
  } catch (error) {
    let errorMsg = 'Ocurrió un problema al guardar el plan.';
    // Si el backend devuelve detalles, mostrarlos
    if (error?.response?.data) {
      if (typeof error.response.data === 'string') {
        errorMsg = error.response.data;
      } else if (typeof error.response.data === 'object') {
        // Mostrar errores de validación de DRF
        errorMsg = Object.entries(error.response.data)
          .map(([campo, mensajes]) => `<b>${campo}:</b> ${Array.isArray(mensajes) ? mensajes.join(', ') : mensajes}`)
          .join('<br>');
      }
    } else if (error?.message) {
      errorMsg = error.message;
    }
    Swal.fire({
      title: 'Error',
      html: errorMsg,
      icon: 'error',
      width: 600
    });
    console.error("Error al guardar:", error);
  }
};
</script>

<style scoped>
.plan-container {
  padding: 2rem;
  max-width: 960px;
  margin: auto;
}
.w-100 {
  width: 100%;
}
</style>