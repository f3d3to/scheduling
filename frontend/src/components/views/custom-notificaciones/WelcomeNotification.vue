<script setup lang="ts">
import { computed, ref, watchEffect, defineProps } from 'vue';
import { useNotivue, type NotivueItem } from 'notivue';

interface WelcomeNotificationProps {
  icon?: string;
  title: string;
  subtitle?: string;
  duration?: number;
  color?: string;
}

const props = defineProps<{
  item: NotivueItem<WelcomeNotificationProps>
}>();

const icon = ref(props.item.props.icon || 'mdi-information-outline');
const title = ref(props.item.props.title);
const subtitle = ref(props.item.props.subtitle);
const color = computed(() => props.item.props.color || 'default');

const closeNotification = () => {
  props.item.clear();
};

watchEffect(() => {
  icon.value = props.item.props.icon || 'mdi-information-outline';
  title.value = props.item.props.title;
  subtitle.value = props.item.props.subtitle;
});

</script>

<template>
  <div class="welcome-notification" :class="`color-${color}`">
    <div v-if="icon" class="icon" >
      <i :class="icon"></i>
    </div>
    <div class="content">
      <h3 class="title">{{ title }}</h3>
      <p v-if="subtitle" class="subtitle">{{ subtitle }}</p>
    </div>
    <button class="close-button" :class="`color-${color}`" @click="closeNotification">
      <i class="mdi mdi-close"></i>
    </button>
  </div>
</template>

<style scoped>
.welcome-notification {
  display: flex;
  align-items: center;
  background-color: #f8f8f8; /* Default background color */
  border: 1px solid #e0e0e0; /* Default border color */
  border-radius: 5px;
  padding: 15px;
  width: 450px; /* Increased width */
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

/* Dynamic color configurations */
.color-default { /* Default color setup */
  background-color: #f8f8f8;
  color: #3a475b;
}
.color-blue { /* Blue theme */
  background-color: #127bae;
  color: #FFF;
}
.color-green { /* Green theme */
  background-color: #178570;
  color: #FFF;
}
.color-red { /* Red theme */
  background-color: #c94430;
  color: #FFF;
}
.color-yellow { /* Yellow theme */
  background-color: #ffe556;
  color: #4f5358;
}
.color-grey { /* Grey theme */
  background-color: #9E9E9E;
  color: #FFF;
}

.icon {
  margin-right: 15px;
  font-size: 50px;
}

.content {
  flex-grow: 1;
  overflow: hidden; /* Added to handle text overflow */
}

.title {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  white-space: nowrap; /* Added to keep title in one line */
  overflow: hidden; /* Added to handle text overflow */
  text-overflow: ellipsis; /* Added to handle text overflow */
}

.subtitle {
  margin: 5px 0 0;
  font-size: 14px;
}

.close-button {
  background: none;
  border: none;
  padding: 0;
  cursor: pointer;
  font-size: 30px;
  margin-left: 10px;
}

.close-button:hover {
  color: #333;
}
</style>
