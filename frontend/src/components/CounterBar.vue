<script setup>
import { useCrisisStore } from "../stores/crisis";

const store = useCrisisStore();
</script>

<template>
  <section class="border-y border-gray-200 bg-white">
    <div class="mx-auto grid max-w-5xl grid-cols-2 gap-4 px-4 py-5 sm:grid-cols-4">
      <div class="text-center">
        <p class="text-2xl font-bold text-urgent">{{ store.stats?.still_missing_count ?? "–" }}</p>
        <p class="text-xs text-gray-500">Still missing</p>
      </div>
      <div class="text-center">
        <p class="text-2xl font-bold text-gray-700">{{ store.stats?.confirmed_deceased_count ?? "–" }}</p>
        <p class="text-xs text-gray-500">Confirmed deceased</p>
      </div>
      <div class="text-center">
        <p class="text-2xl font-bold text-gray-900">{{ store.stats?.official_rescued_count ?? "–" }}</p>
        <p class="text-xs text-gray-500">Officially rescued</p>
      </div>
      <div class="text-center">
        <p class="text-2xl font-bold text-gray-900">{{ store.stats?.total_group_members ?? "–" }}</p>
        <p class="text-xs text-gray-500">Total group members</p>
      </div>
    </div>
    <p v-if="store.stats?.note" class="px-4 pb-3 text-center text-xs text-gray-400">
      {{ store.stats.note }}
    </p>
  </section>
</template>
