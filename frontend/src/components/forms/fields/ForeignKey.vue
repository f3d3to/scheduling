<template>
<form @submit.prevent="handleSubmit">
    <component
    v-for="field in fields"
    :key="field.name"
    :is="getComponent(field.type)"
    :field="field"
    v-model="formData[field.name]"
    />
    <button type="submit" class="btn btn-primary">Guardar</button>
</form>
</template>

<script>
import { defineComponent, ref, onMounted } from 'vue';
import TextField from './fields/TextField.vue';
import DateField from './fields/DateField.vue';
import BooleanField from './fields/BooleanField.vue';
import ForeignKeyField from './fields/ForeignKeyField.vue';
import DateTimeField from './fields/DateTimeField.vue';
import DecimalField from './fields/DecimalField.vue';
import BigAutoField from './fields/BigAutoField.vue';

export default defineComponent({
components: {
    TextField,
    DateField,
    BooleanField,
    ForeignKeyField,
    DateTimeField,
    DecimalField,
    BigAutoField,
},
props: {
    modelName: {
    type: String,
    required: true,
    },
},
setup(props) {
    const fields = ref([]);
    const formData = ref({});
    const fieldComponents = {
    CharField: 'TextField',
    TextField: 'TextField',
    DateField: 'DateField',
    BooleanField: 'BooleanField',
    ForeignKey: 'ForeignKeyField',
    DateTimeField: 'DateTimeField',
    DecimalField: 'DecimalField',
    BigAutoField: 'BigAutoField',
    // Mapea el resto de tipos de campos a sus componentes
    };

    const getComponent = (fieldType) => {
    return fieldComponents[fieldType] || 'TextField'; // Por defecto usa TextField
    };

    const fetchData = async () => {
    try {
        const response = await fetch('http://localhost:8000/estructura-modelos/');
        const models = await response.json();
        const modelData = models.find((model) => model.model_name === props.modelName);
        if (modelData) {
        fields.value = modelData.fields;
        modelData.fields.forEach((field) => {
            formData.value[field.name] = null;
        });
        }
    } catch (error) {
        console.error('Error fetching data:', error);
    }
    };

    const handleSubmit = () => {
    console.log('Form data:', formData.value);
    fetch('/tu-endpoint-de-guardado/', {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData.value)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
    };

    onMounted(fetchData);

    return { fields, formData, getComponent, handleSubmit };
},
});
</script>
