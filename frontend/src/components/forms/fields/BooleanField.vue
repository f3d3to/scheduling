<template>
<div class="form-check">
    <input type="checkbox" :id="field.name" v-model="value" :required="field.required" class="form-check-input" />
    <label :for="field.name" class="form-check-label">{{ field.verbose_name }}</label>
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
    type: Boolean,
    default: false,
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