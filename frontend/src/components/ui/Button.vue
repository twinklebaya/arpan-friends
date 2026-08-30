<script setup>
defineProps({
  variant: { type: String, default: "primary" }, // primary | outline | urgent
  type: { type: String, default: "button" },
  disabled: { type: Boolean, default: false },
});
</script>

<template>
  <button
    :type="type"
    :disabled="disabled"
    class="inline-flex items-center justify-center rounded-md px-4 py-2 text-sm font-semibold transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
    :class="{
      'bg-gray-900 text-white hover:bg-gray-700 focus-visible:ring-gray-900': variant === 'primary',
      'border border-gray-300 bg-white text-gray-900 hover:bg-gray-50 focus-visible:ring-gray-400':
        variant === 'outline',
      'bg-urgent text-white hover:bg-red-800 focus-visible:ring-urgent': variant === 'urgent',
    }"
  >
    <slot />
  </button>
</template>
