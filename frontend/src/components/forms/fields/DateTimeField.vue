<template>
<div class="form-group">
    <label :for="field.name">{{ field.verbose_name }}</label>
    <input type="datetime-local" :id="field.name" v-model="value" :required="field.required" class="form-control" />
</div>
</template>

<script>
import { defineComponent, ref, watchEffect } from 'vue';

export default defineComponent({
props: {
    field: {
    type: Object,
    required: true,
    },
    modelValue: {
    type: String,
    default: '',
    },
},
emits: ['update:modelValue'],
setup(props, { emit }) {
    const value = ref(props.modelValue);

    watchEffect(() => {
    emit('update:modelValue', value.value);
    });

    return { value };
},
});
</script>