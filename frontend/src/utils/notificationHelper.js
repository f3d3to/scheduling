// src/utils/notificationHelper.js
import { onUnmounted } from 'vue';
import { push, updateConfig } from 'notivue';

export function sendNotificationWithCustomConfig(notificationConfig, newConfig, onNotificationSent) {
  const previousConfig = updateConfig();

  updateConfig(newConfig);
  push.info(notificationConfig);

  onUnmounted(() => {
    updateConfig(previousConfig);
  });

  if (onNotificationSent) {
    onNotificationSent();
  }
}
