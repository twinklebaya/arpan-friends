<script setup>
defineProps({
  tone: { type: String, default: "neutral" }, // neutral | urgent | success | warning
});
</script>

<template>
  <span
    class="inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium"
    :class="{
      'bg-gray-100 text-gray-800': tone === 'neutral',
      'bg-red-100 text-red-800': tone === 'urgent',
      'bg-green-100 text-green-800': tone === 'success',
      'bg-amber-100 text-amber-800': tone === 'warning',
    }"
  >
    <slot />
  </span>
</template>
