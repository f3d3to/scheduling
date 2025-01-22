// src/utils/notificationHelper.js
import { onUnmounted } from 'vue';
import { push, updateConfig } from 'notivue';

export function sendNotificationWithCustomConfig(notificationConfig, newConfig, onNotificationSent) {
  const previousConfig = updateConfig();
  push.destroyAll();
  updateConfig({
    position: 'top-center',
  });
  push.info(notificationConfig);
  updateConfig(previousConfig);


  if (onNotificationSent) {
    onNotificationSent();
  }
}
