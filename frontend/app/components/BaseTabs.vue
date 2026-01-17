<script lang="ts" setup>
  import type { TabsItem } from '@nuxt/ui';

  const active = defineModel<string>({ required: true });

  const items = computed<TabsItem[]>(() => [
  {
    label: 'Overview',
    value: 'overview',
  },
  {
    label: 'Timeline',
    value: 'timeline',
  },
  {
    label: 'GrokSignal',
    value: 'groksignal',
  },
  {
    label: 'Index',
    value: 'index',
  }
]);
</script>

<template>
  <div class="">
    <UTabs size="xl" :items v-model="active" />
  </div>
</template>
