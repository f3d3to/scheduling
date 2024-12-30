<template>
  <div>
    <div v-if="!modeloAsociadoId">
      <div v-if="modeloAsociado === 'actividad'">
        <h3>Datos de Actividad</h3>
        <FormKit type="group" :name="`${modeloAsociado}_data`" #default="{ value }">
          <template v-for="(campo, index) in obtenerCampos(modeloAsociado)" :key="index">
            <FormKit
              v-if="campo.type !== 'ForeignKey'"
              :type="obtenerTipoInput(campo.type, campo.name)"
              :name="campo.name"
              :label="campo.verbose_name"
              :validation="campo.required ? 'required' : ''"
              v-model="value[campo.name]"
            />
            <div v-else>
              <h4>{{ campo.verbose_name }}</h4>
              <FormKit type="group" :name="campo.name" #default="{ value: nestedValue }">
                <div v-for="(nestedCampo, nestedIndex) in obtenerCamposRelacionados(campo.name)" :key="nestedIndex">
                  <FormKit
                    :type="obtenerTipoInput(nestedCampo.type, nestedCampo.name)"
                    :name="nestedCampo.name"
                    :label="nestedCampo.verbose_name"
                    :validation="nestedCampo.required ? 'required' : ''"
                    v-model="nestedValue[nestedCampo.name]"
                  />
                </div>
              </FormKit>
            </div>
          </template>
        </FormKit>
      </div>
      <div v-if="modeloAsociado === 'tarea'">
        <h3>Datos de Tarea</h3>
        <FormKit type="group" :name="`${modeloAsociado}_data`" #default="{ value }">
          <template v-for="(campo, index) in obtenerCampos(modeloAsociado)" :key="index">
            <FormKit
              v-if="campo.type !== 'ForeignKey'"
              :type="obtenerTipoInput(campo.type, campo.name)"
              :name="campo.name"
              :label="campo.verbose_name"
              :validation="campo.required ? 'required' : ''"
              v-model="value[campo.name]"
            />
            <div v-else>
              <h4>{{ campo.verbose_name }}</h4>
              <FormKit type="group" :name="campo.name" #default="{ value: nestedValue }">
                <div v-for="(nestedCampo, nestedIndex) in obtenerCamposRelacionados(campo.name)" :key="nestedIndex">
                  <FormKit
                    :type="obtenerTipoInput(nestedCampo.type, nestedCampo.name)"
                    :name="nestedCampo.name"
                    :label="nestedCampo.verbose_name"
                    :validation="nestedCampo.required ? 'required' : ''"
                    v-model="nestedValue[nestedCampo.name]"
                  />
                </div>
              </FormKit>
            </div>
          </template>
        </FormKit>
      </div>
      <div v-if="modeloAsociado === 'objetivo'">
        <h3>Datos de Objetivo</h3>
        <FormKit type="group" :name="`${modeloAsociado}_data`" #default="{ value }">
          <template v-for="(campo, index) in obtenerCampos(modeloAsociado)" :key="index">
            <FormKit
              v-if="campo.type !== 'ForeignKey'"
              :type="obtenerTipoInput(campo.type, campo.name)"
              :name="campo.name"
              :label="campo.verbose_name"
              :validation="campo.required ? 'required' : ''"
              v-model="value[campo.name]"
            />
            <div v-else>
              <h4>{{ campo.verbose_name }}</h4>
              <FormKit type="group" :name="campo.name" #default="{ value: nestedValue }">
                <div v-for="(nestedCampo, nestedIndex) in obtenerCamposRelacionados(campo.name)" :key="nestedIndex">
                  <FormKit
                    :type="obtenerTipoInput(nestedCampo.type, nestedCampo.name)"
                    :name="nestedCampo.name"
                    :label="nestedCampo.verbose_name"
                    :validation="nestedCampo.required ? 'required' : ''"
                    v-model="nestedValue[nestedCampo.name]"
                  />
                </div>
              </FormKit>
            </div>
          </template>
        </FormKit>
      </div>
      <div v-if="modeloAsociado === 'registro_progreso'">
        <h3>Datos de Registro Progreso</h3>
        <FormKit type="group" :name="`${modeloAsociado}_data`" #default="{ value }">
          <template v-for="(campo, index) in obtenerCampos(modeloAsociado)" :key="index">
            <FormKit
              v-if="campo.type !== 'ForeignKey'"
              :type="obtenerTipoInput(campo.type, campo.name)"
              :name="campo.name"
              :label="campo.verbose_name"
              :validation="campo.required ? 'required' : ''"
              v-model="value[campo.name]"
            />
            <div v-else>
              <h4>{{ campo.verbose_name }}</h4>
              <FormKit type="group" :name="campo.name" #default="{ value: nestedValue }">
                <div v-for="(nestedCampo, nestedIndex) in obtenerCamposRelacionados(campo.name)" :key="nestedIndex">
                  <FormKit
                    :type="obtenerTipoInput(nestedCampo.type, nestedCampo.name)"
                    :name="nestedCampo.name"
                    :label="nestedCampo.verbose_name"
                    :validation="nestedCampo.required ? 'required' : ''"
                    v-model="nestedValue[nestedCampo.name]"
                  />
                </div>
              </FormKit>
            </div>
          </template>
        </FormKit>
      </div>
      <div v-if="modeloAsociado === 'comentario'">
        <h3>Datos de Comentario</h3>
        <FormKit type="group" :name="`${modeloAsociado}_data`" #default="{ value }">
          <template v-for="(campo, index) in obtenerCampos(modeloAsociado)" :key="index">
            <FormKit
              v-if="campo.type !== 'ForeignKey'"
              :type="obtenerTipoInput(campo.type, campo.name)"
              :name="campo.name"
              :label="campo.verbose_name"
              :validation="campo.required ? 'required' : ''"
              v-model="value[campo.name]"
            />
            <div v-else>
              <h4>{{ campo.verbose_name }}</h4>
              <FormKit type="group" :name="campo.name" #default="{ value: nestedValue }">
                <div v-for="(nestedCampo, nestedIndex) in obtenerCamposRelacionados(campo.name)" :key="nestedIndex">
                  <FormKit
                    :type="obtenerTipoInput(nestedCampo.type, nestedCampo.name)"
                    :name="nestedCampo.name"
                    :label="nestedCampo.verbose_name"
                    :validation="nestedCampo.required ? 'required' : ''"
                    v-model="nestedValue[nestedCampo.name]"
                  />
                </div>
              </FormKit>
            </div>
          </template>
        </FormKit>
      </div>
      <div v-if="modeloAsociado === 'etiqueta'">
        <h3>Datos de Etiqueta</h3>
        <FormKit type="group" :name="`${modeloAsociado}_data`" #default="{ value }">
          <template v-for="(campo, index) in obtenerCampos(modeloAsociado)" :key="index">
            <FormKit
              v-if="campo.type !== 'ForeignKey'"
              :type="obtenerTipoInput(campo.type, campo.name)"
              :name="campo.name"
              :label="campo.verbose_name"
              :validation="campo.required ? 'required' : ''"
              v-model="value[campo.name]"
            />
            <div v-else>
              <h4>{{ campo.verbose_name }}</h4>
              <FormKit type="group" :name="campo.name" #default="{ value: nestedValue }">
                <div v-for="(nestedCampo, nestedIndex) in obtenerCamposRelacionados(campo.name)" :key="nestedIndex">
                  <FormKit
                    :type="obtenerTipoInput(nestedCampo.type, nestedCampo.name)"
                    :name="nestedCampo.name"
                    :label="nestedCampo.verbose_name"
                    :validation="nestedCampo.required ? 'required' : ''"
                    v-model="nestedValue[nestedCampo.name]"
                  />
                </div>
              </FormKit>
            </div>
          </template>
        </FormKit>
      </div>
      <div v-if="modeloAsociado === 'evento'">
        <h3>Datos de Evento</h3>
        <FormKit type="group" :name="`${modeloAsociado}_data`" #default="{ value }">
          <template v-for="(campo, index) in obtenerCampos(modeloAsociado)" :key="index">
            <FormKit
              v-if="campo.type !== 'ForeignKey'"
              :type="obtenerTipoInput(campo.type, campo.name)"
              :name="campo.name"
              :label="campo.verbose_name"
              :validation="campo.required ? 'required' : ''"
              v-model="value[campo.name]"
            />
            <div v-else>
              <h4>{{ campo.verbose_name }}</h4>
              <FormKit type="group" :name="campo.name" #default="{ value: nestedValue }">
                <div v-for="(nestedCampo, nestedIndex) in obtenerCamposRelacionados(campo.name)" :key="nestedIndex">
                  <FormKit
                    :type="obtenerTipoInput(nestedCampo.type, nestedCampo.name)"
                    :name="nestedCampo.name"
                    :label="nestedCampo.verbose_name"
                    :validation="nestedCampo.required ? 'required' : ''"
                    v-model="nestedValue[nestedCampo.name]"
                  />
                </div>
              </FormKit>
            </div>
          </template>
        </FormKit>
      </div>
      <div v-if="modeloAsociado === 'recurrente'">
        <h3>Datos de Recurrente</h3>
        <FormKit type="group" :name="`${modeloAsociado}_data`" #default="{ value }">
          <template v-for="(campo, index) in obtenerCampos(modeloAsociado)" :key="index">
            <FormKit
              v-if="campo.type !== 'ForeignKey'"
              :type="obtenerTipoInput(campo.type, campo.name)"
              :name="campo.name"
              :label="campo.verbose_name"
              :validation="campo.required ? 'required' : ''"
              v-model="value[campo.name]"
            />
            <div v-else>
              <h4>{{ campo.verbose_name }}</h4>
              <FormKit type="group" :name="campo.name" #default="{ value: nestedValue }">
                <div v-for="(nestedCampo, nestedIndex) in obtenerCamposRelacionados(campo.name)" :key="nestedIndex">
                  <FormKit
                    :type="obtenerTipoInput(nestedCampo.type, nestedCampo.name)"
                    :name="nestedCampo.name"
                    :label="nestedCampo.verbose_name"
                    :validation="nestedCampo.required ? 'required' : ''"
                    v-model="nestedValue[nestedCampo.name]"
                  />
                </div>
              </FormKit>
            </div>
          </template>
        </FormKit>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    modeloAsociado: {
      type: String,
      required: true,
    },
    estructuraModelos: {
      type: Array,
      required: true,
    },
    urlsModelos: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      modeloAsociadoId: null,
      modeloData: {},
    };
  },
  methods: {
    obtenerCampos(modelo) {
      const modeloEstructura = this.estructuraModelos.find(
        (m) => m.model_name === modelo
      );
      return modeloEstructura ? modeloEstructura.fields : [];
    },
    obtenerCamposRelacionados(modeloRelacionado) {
      const modeloEstructura = this.estructuraModelos.find(
        (m) => m.model_name === modeloRelacionado
      );
      return modeloEstructura ? modeloEstructura.fields : [];
    },
    obtenerTipoInput(tipo, nombre) {
      switch (tipo) {
        case "CharField":
          return nombre === 'color' ? "color" : "text";
        case "TextField":
        case "EmailField":
        case "URLField":
          return "text";
        case "BooleanField":
          return "checkbox";
        case "DateField":
          return "date";
        case "DateTimeField":
          return "datetime-local";
        case "IntegerField":
        case "DecimalField":
          return "number";
        case "ForeignKey":
          return "group";
        default:
          return "text";
      }
    },
  },
  watch: {
    modeloData: {
      handler(newVal) {
        this.$emit("update:modelo_data", newVal);
      },
      deep: true,
    },
    modeloAsociadoId: {
      handler(newVal) {
        this.$emit("update:modelo_asociado_id", newVal);
      },
    },
  },
};
</script>