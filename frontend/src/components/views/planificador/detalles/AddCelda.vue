<template>
    <v-card>
        <v-card-title class="title-container">
            <span class="title-dialog">Agregar celdas</span>
            <v-icon class="close-button" @click="$emit('close-dialog')" size="small">mdi-close</v-icon>
        </v-card-title>
        <v-card-text>
            <div class="boton-columna">
                <v-btn prepend-icon="mdi mdi-table-column-plus-after" @click="addColumn">
                    <template v-slot:prepend>
                        <v-icon style="color:blue;"></v-icon>
                        <v-icon style="color:blue;">mdi mdi-plus</v-icon>
                    </template>
                </v-btn>
                <v-btn prepend-icon="mdi mdi-table-column-remove" @click="removeColumn">
                    <template v-slot:prepend>
                        <v-icon style="color:red;"></v-icon>
                        <v-icon style="color:red;">mdi mdi-minus</v-icon>

                    </template>
                </v-btn>
            </div>
            <div class="mini-tablero">
                <GridLayout
                    v-if="layoutGenerado"
                    :layout="layout"
                    :col-num="columnas"
                    :row-height="30"
                >
                    <GridItem
                        v-for="item in layout"
                        :key="item.i"
                        :x="item.x"
                        :y="item.y"
                        :w="item.w"
                        :h="item.h"
                        :i="item.i"
                        :is-resizable="item.isNew"
                        :is-draggable="true"
                        :style="{ backgroundColor: item.isNew ? '#f0f0f0' : '#3332' }"
                    >
                        <div class="celda-content">
                            <span v-if="!item.isNew" class="placeholder">{{ item.contenido }}</span>
                            <textarea v-if="item.isNew" v-model="item.contenido" placeholder="Ingrese contenido aquí" />
                            <v-icon v-if="item.isNew" class="close-button" @click="removeCelda(item.i)" size="small">mdi-close</v-icon>
                        </div>
                    </GridItem>
                </GridLayout>
            </div>
            <div class="boton-fila">
                <v-btn prepend-icon="mdi mdi-table-row-plus-after" @click="addRow">
                    <template v-slot:prepend>
                        <v-icon style="color:blue;"></v-icon>
                    </template>
                    Fila
                </v-btn>
            </div>
            <div class="botones-acciones">
                <v-btn prepend-icon="mdi mdi-plus" @click="addCelda">
                    <template v-slot:prepend>
                        <v-icon style="color:blue;"></v-icon>
                    </template>
                    Celda
                </v-btn>
                <v-btn prepend-icon="mdi-check-circle" @click="commitChanges">
                    <template v-slot:prepend>
                        <v-icon color="success"></v-icon>
                    </template>
                    Guardar
                </v-btn>

                <v-btn prepend-icon="mdi mdi-window-close" @click="cancelChanges">
                    <template v-slot:prepend>
                        <v-icon color="error"></v-icon>
                    </template>
                    Cancelar
                </v-btn>
            </div>
        </v-card-text>
    </v-card>
</template>

<script>
  import { GridLayout, GridItem } from 'vue3-grid-layout-next';
  import Swal from 'sweetalert2/dist/sweetalert2';

  export default {
    components: {
      GridLayout,
      GridItem,
    },
    data() {
      return {
        layout: [],
        columnas: 0,
        columnasOriginal: 0, // Agrega esta línea para guardar el estado original
        filas: 0,
        celdas: [],
        layoutGenerado: false,
      };
    },
    created() {
      this.fetchData();
    },

    methods: {
    async fetchData() {
        const planificadorId = this.$route.params.id || "pk";
        const response = await fetch(`http://localhost:8000/estructuras-planificador/${planificadorId}/`);
        if (response.ok) {
            const data = await response.json();
            this.columnas = data.columnas;
            this.columnasOriginal = data.columnas;
            this.filas = data.filas;
            this.celdas = Object.entries(data.tabla).map(([coordenadas, celda]) => ({...celda, coordenadas}));
            this.layout = this.generateLayout(this.celdas);
            this.layoutGenerado = true;
        }},

        generateLayout(celdas) {
            const layout = celdas.map((celda, index) => {
                const [fila, columna] = celda.coordenadas.split(",").map(Number);
                return {
                i: celda.id,
                x: columna - 1,
                y: fila - 1,
                w: celda.w,
                h: celda.h,
                contenido: celda.contenido || '',
                isNew: false
                };
            });
            return layout;
        },
        addColumn() {
            this.columnas++;
            this.layout.forEach(celda => {
            if (celda.x >= this.columnas - 1) {
                celda.w = this.columnas;
            }
            });
        },

        addRow() {
            const maxY = Math.max(...this.layout.map(item => item.y + item.h), 0);
            this.layout.push({
            x: 0,
            y: maxY,
            w: this.columnas,
            h: 1,
            i: null,
            contenido: '',
            isNew: true,
            isResizable: true,
            isDraggable: true,
            });
        },

      addCelda() {
        this.layout.push({
          x: 0,
          y: this.layout.reduce((max, item) => Math.max(max, item.y), 0) + 1,
          w: 1,
          h: 1,
          i: null,
          contenido: '',
          isNew: true,
          isResizable: true,
          isDraggable: true,
        });
      },
      removeCelda(id) {
        this.layout = this.layout.filter(celda => celda.i !== id);
      },
      onLayoutUpdated(newLayout) {
        this.layout = this.layout.filter(celda => !celda.isNew);
      },
      async commitChanges() {
        // Preparar datos para la estructura
        const estructuraData = {
            filas: this.filas,
            columnas: this.columnas,
            tabla: {},
        };

        // Procesar el layout para construir el objeto `tabla`
        this.layout.forEach((celda) => {
            const key = `${celda.y + 1},${celda.x + 1}`;
            estructuraData.tabla[key] = {
            id: celda.i,
            contenido: celda.contenido,
            fila: celda.y + 1,
            columna: celda.x + 1,
            w: celda.w,
            h: celda.h,
            };
        });

        // Preparar datos de nuevas celdas
        const nuevasCeldas = this.layout
            .filter((celda) => celda.isNew)
            .map((celda) => ({
            contenido: celda.contenido,
            fila: celda.y + 1,
            columna: celda.x + 1,
            }));

        try {
            // Enviar datos al backend
            const response = await fetch(`http://localhost:8000/planificador/estructura/actualizar/${this.$route.params.id}/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                filas: estructuraData.filas,
                columnas: estructuraData.columnas,
                tabla: estructuraData.tabla,
                celdas: nuevasCeldas,
            }),
            });

            if (!response.ok) throw new Error('Error al guardar los cambios');
            this.$emit('update-layout');
            this.$emit('close-dialog');
            Swal.fire('Guardado', 'Los cambios han sido guardados correctamente.', 'success');
        } catch (error) {
            Swal.fire('Error', error.message, 'error');
        }
        },
        removeColumn() {
            if (this.columnas > 1) {
                this.columnas--;
                this.layout = this.layout.filter((celda) => celda.x < this.columnas);

                this.layout.forEach((celda) => {
                    if (celda.x >= this.columnas) {
                        celda.w = Math.min(celda.w, this.columnas - celda.x);
                    }
                });
            } else {
                Swal.fire('Error', 'Debe haber al menos una columna.', 'error');
            }
        },
      cancelChanges() {
        this.columnas = this.columnasOriginal;

        this.layout.forEach(celda => {
            if (celda.x < this.columnas) {
            celda.w = 1;
            }
        });

        this.onLayoutUpdated(this.layout);
        }
    }
};
</script>

<style scoped>

.title-container {
  display: flex;
  align-items: center;
  justify-content: space-between; /* Espacia los elementos dentro del contenedor */
}

.close-button {
  margin-right: auto; /* Empuja todo lo demás hacia la derecha */
}

.title-dialog {
  flex-grow: 1;
  text-align: center; /* Centra el texto del título */
}

.boton-columna {
    display: flex;
    justify-content: flex-end; /* Alinea el botón de columna a la derecha */
    padding-right: 10px; /* Espacio para no pegar directamente al borde */
}

.boton-fila {
    left: 0; /* Alinea el bpadding-leftotón de fila a la izquierda */
    margin-bottom: 10px; /* Espacio para no pegar directamente al borde */
}

.mini-tablero {
    flex-direction: column;
    align-items: center;
    margin: 10px;
    margin-bottom: 20px;
    border: 1px solid #ccc;
    padding-bottom: 10px;
    overflow: auto;
}
.grid-item {
    flex: 1 0 auto; /* Flexibilidad para adaptarse pero mantiene el tamaño base */
    width: calc(100% / var(--num-columns)); /* Ancho basado en el número de columnas */
    height: calc(100% / var(--num-columns)); /* Altura igual al ancho para mantener aspecto cuadrado */
    box-sizing: border-box;
    padding: 2px; /* Espacio entre celdas */
}
.celda-content {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100%;
    border: 1px solid #ccc; /* Borde para visualizar celda */
    background-color: #f0f0f0; /* Color de fondo */
}
.celda-content span.text {
  font-size: 12px;
}
textarea {
    width: 90%;
    margin-bottom: 2px;
    height: 30px;
    font-size: 12px;
}
</style>