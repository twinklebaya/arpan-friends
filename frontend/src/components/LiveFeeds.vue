<script setup>
import { useCrisisStore } from "../stores/crisis";
import FeedColumn from "./FeedColumn.vue";

const store = useCrisisStore();
</script>

<template>
  <section class="mx-auto max-w-7xl px-4 py-6">
    <h2 class="text-lg font-bold uppercase tracking-wide text-gray-900">Live Updates</h2>
    <div class="mt-4 grid grid-cols-1 gap-6 md:grid-cols-2">
      <div class="rounded-xl border border-gray-200 bg-white p-4 shadow-sm sm:p-5">
        <FeedColumn
          title="General Crisis Updates"
          :items="store.generalFeed"
          empty-text="No general updates yet."
        />
      </div>
      <div class="rounded-xl border border-gray-200 bg-white p-4 shadow-sm sm:p-5">
        <FeedColumn
          title="Important Updates"
          :items="store.targetFeed"
          empty-text="No group-specific updates yet."
        />
      </div>
    </div>
  </section>
</template>
