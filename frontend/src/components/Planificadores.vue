<template>
    <v-container>
      <v-row justify="center">
        <v-col cols="12" md="8">
          <v-card v-if="!loading && estructura">
            <v-card-title class="text-h5">
              {{ estructura.nombre }}
            </v-card-title>
            <v-card-subtitle>
              {{ estructura.descripcion }}
            </v-card-subtitle>
            <v-card-text>
              <v-simple-table>
                <template v-slot:default>
                  <thead>
                    <tr>
                      <th v-for="(columna, index) in configuracion.columnas" :key="index" class="text-left">
                        {{ columna }}
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(fila, index) in configuracion.filas" :key="index">
                      <td v-for="(columna, indexCol) in configuracion.columnas" :key="indexCol">
                          {{fila}}
                      </td>
                    </tr>
                  </tbody>
                </template>
              </v-simple-table>
            </v-card-text>
          </v-card>

          <v-alert v-if="error" type="error" dense outlined>
            {{ error }}
          </v-alert>

          <div v-if="loading" class="text-center">
            <v-progress-circular indeterminate color="primary"></v-progress-circular>
            <p>Cargando...</p>
          </div>
        </v-col>
      </v-row>
    </v-container>
  </template>

  <script>
  export default {
    name: 'EstructuraPlanificadorComponent',
    data: () => ({
      estructura: null,
      loading: false,
      error: null,
      configuracion: {
        columnas: [],
        filas: [],
      },
      planificadorId: 1, // ID del planificador. Podrías pasarlo como prop
    }),
    created() {
      this.fetchEstructura();
    },
    methods: {
      async fetchEstructura() {
        this.loading = true;
        this.error = null;

        try {
          // Obtener el planificador
          const planificadorResponse = await fetch(`http://localhost:8000/planificadores/${this.planificadorId}/`);
          if (!planificadorResponse.ok) {
            throw new Error('Error al obtener los datos del planificador.');
          }
          const planificadorData = await planificadorResponse.json();

          // Si el planificador tiene una estructura asociada
          if (planificadorData.estructura) {
              const estructuraId = planificadorData.estructura;
              const estructuraResponse = await fetch(`http://localhost:8000/estructuras/${estructuraId}/`);
              if (!estructuraResponse.ok) {
                throw new Error('Error al obtener la estructura del planificador.');
              }
              const estructuraData = await estructuraResponse.json();
              this.estructura = estructuraData;
              this.configuracion = estructuraData.configuracion;
          } else {
              this.error = 'El planificador no tiene una estructura asociada.';
          }

        } catch (error) {
          this.error = error.message;
          console.error(error);
        } finally {
          this.loading = false;
        }
      },
    },
  };
  </script>