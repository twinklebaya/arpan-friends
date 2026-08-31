<script setup>
import { closeLightbox, lightboxState } from "../lib/lightbox";
</script>

<template>
  <div
    v-if="lightboxState.url"
    class="fixed inset-0 z-50 flex items-center justify-center bg-black/85 p-4"
    @click="closeLightbox"
  >
    <button
      type="button"
      class="absolute right-4 top-4 text-3xl leading-none text-white hover:text-gray-300"
      aria-label="Close"
      @click="closeLightbox"
    >
      &times;
    </button>
    <img
      :src="lightboxState.url"
      :alt="lightboxState.alt"
      class="max-h-[90vh] max-w-[90vw] rounded-lg object-contain"
      @click.stop
    />
  </div>
</template>
