<template>
    <div>
      <label :for="field.name">{{ field.verbose_name }}</label>
      <input type="text" :id="field.name" v-model="value" :required="field.required">
    </div>
</template>

<script>
export default {
props: ['field', 'value'],
emits: ['update:value'],
}
</script>