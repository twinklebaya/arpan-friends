<script setup>
import { ref } from "vue";

const GROUP_PHOTOS = [
  { url: "/photos/friends-group.jpg", caption: "Arpan, Bhavin, and Karan together" },
  {
    url: "/photos/kailash-tour-group.jpg",
    caption: "The full Kailash Journeys tour group at Hotel Tibet, Kathmandu",
  },
];

const scrollEl = ref(null);
function scrollBy(amount) {
  scrollEl.value?.scrollBy({ left: amount, behavior: "smooth" });
}
</script>

<template>
  <section class="mx-auto max-w-5xl px-4 py-6">
    <div class="flex items-center justify-between">
      <h2 class="text-lg font-bold text-gray-900">Additional Photos</h2>
      <div class="flex gap-2">
        <button
          type="button"
          class="rounded-md border border-gray-300 px-2 py-1 text-sm text-gray-600 hover:bg-gray-50"
          @click="scrollBy(-280)"
        >
          ←
        </button>
        <button
          type="button"
          class="rounded-md border border-gray-300 px-2 py-1 text-sm text-gray-600 hover:bg-gray-50"
          @click="scrollBy(280)"
        >
          →
        </button>
      </div>
    </div>
    <p class="mt-1 text-sm text-gray-600">
      If you recognize any details, person or location from these pictures, or if you have any
      additional information to share, please reach out to us!
    </p>
    <div
      ref="scrollEl"
      class="mt-3 flex snap-x gap-4 overflow-x-auto pb-2"
    >
      <a
        v-for="photo in GROUP_PHOTOS"
        :key="photo.url"
        :href="photo.url"
        target="_blank"
        rel="noopener noreferrer"
        class="block w-56 shrink-0 snap-start overflow-hidden rounded-lg border border-gray-200 bg-white shadow-sm"
      >
        <img :src="photo.url" :alt="photo.caption" loading="lazy" class="h-40 w-full object-cover" />
        <p class="p-2 text-xs font-medium text-gray-700">{{ photo.caption }}</p>
      </a>
    </div>
  </section>
</template>
