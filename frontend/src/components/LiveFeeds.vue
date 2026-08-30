<script setup>
import { useCrisisStore } from "../stores/crisis";
import FeedColumn from "./FeedColumn.vue";

const store = useCrisisStore();
</script>

<template>
  <section class="mx-auto max-w-5xl px-4 py-8">
    <h2 class="text-lg font-bold text-gray-900">Live Updates</h2>
    <p class="mt-1 text-sm text-gray-500">
      Updates are reviewed by an admin before publishing and refresh automatically.
    </p>
    <div class="mt-4 grid grid-cols-1 gap-6 md:grid-cols-2">
      <FeedColumn
        title="General Crisis Updates"
        :items="store.generalFeed"
        empty-text="No general updates yet."
      />
      <FeedColumn
        title="Kailash Journeys Group Updates"
        :items="store.targetFeed"
        empty-text="No group-specific updates yet."
      />
    </div>
  </section>
</template>
