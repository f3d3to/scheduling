<template>
<div class="form-group">
    <label :for="field.name">{{ field.verbose_name }}</label>
    <input type="number" :id="field.name" v-model.number="value" step="0.01" :required="field.required" class="form-control" />
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
    type: Number,
    default: 0,
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