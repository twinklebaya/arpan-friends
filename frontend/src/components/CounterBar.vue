<script setup>
import { useCrisisStore } from "../stores/crisis";

const store = useCrisisStore();
</script>

<template>
  <section class="border-y border-gray-200 bg-white">
    <div class="mx-auto max-w-5xl px-4 py-5">
      <p class="text-center text-xs font-semibold uppercase tracking-wide text-gray-500">
        Names registered on this hub (all nationalities)
      </p>
      <div class="mt-2 grid grid-cols-2 gap-4">
        <div class="text-center">
          <p class="text-3xl font-bold text-urgent">{{ store.stats?.still_missing_count ?? "–" }}</p>
          <p class="text-xs text-gray-500">Still missing</p>
        </div>
        <div class="text-center">
          <p class="text-3xl font-bold text-gray-700">{{ store.stats?.confirmed_deceased_count ?? "–" }}</p>
          <p class="text-xs text-gray-500">Confirmed deceased</p>
        </div>
      </div>

      <p class="mt-5 text-center text-xs font-semibold uppercase tracking-wide text-gray-500">
        Official disaster toll (Nepal + Tibet)
      </p>
      <div class="mt-2 grid grid-cols-2 gap-4 sm:grid-cols-5">
        <div class="text-center">
          <p class="text-xl font-bold text-gray-900">{{ store.stats?.nepal_confirmed_dead ?? "–" }}</p>
          <p class="text-xs text-gray-500">Dead (Nepal)</p>
        </div>
        <div class="text-center">
          <p class="text-xl font-bold text-gray-900">{{ store.stats?.nepal_missing ?? "–" }}</p>
          <p class="text-xs text-gray-500">Missing (Nepal)</p>
        </div>
        <div class="text-center">
          <p class="text-xl font-bold text-gray-900">{{ store.stats?.tibet_confirmed_dead ?? "–" }}</p>
          <p class="text-xs text-gray-500">Dead (Tibet)</p>
        </div>
        <div class="text-center">
          <p class="text-xl font-bold text-gray-900">{{ store.stats?.tibet_missing ?? "–" }}</p>
          <p class="text-xs text-gray-500">Missing (Tibet)</p>
        </div>
        <div class="text-center">
          <p class="text-xl font-bold text-gray-900">{{ store.stats?.total_rescued ?? "–" }}</p>
          <p class="text-xs text-gray-500">Rescued</p>
        </div>
      </div>
    </div>
    <p v-if="store.stats?.note" class="px-4 pb-3 text-center text-xs text-gray-400">
      {{ store.stats.note }}
    </p>
  </section>
</template>
