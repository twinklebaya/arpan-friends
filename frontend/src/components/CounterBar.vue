<script setup>
import { useCrisisStore } from "../stores/crisis";
import Card from "./ui/Card.vue";

const store = useCrisisStore();
</script>

<template>
  <Card class="h-full p-5 sm:p-6">
      <p class="text-center text-xs font-semibold uppercase tracking-wide text-gray-500">
        Official toll — all nationalities, Nepal + Tibet
      </p>
      <div class="mt-3 grid grid-cols-2 gap-4">
        <div class="rounded-lg bg-urgent-light p-4 text-center">
          <p class="text-3xl font-bold text-urgent sm:text-4xl">
            {{ store.stats?.still_missing_count?.toLocaleString() ?? "–" }}
          </p>
          <p class="mt-1 text-xs font-medium text-gray-600">Still missing</p>
        </div>
        <div class="rounded-lg bg-gray-100 p-4 text-center">
          <p class="text-3xl font-bold text-gray-800 sm:text-4xl">
            {{ store.stats?.confirmed_deceased_count?.toLocaleString() ?? "–" }}
          </p>
          <p class="mt-1 text-xs font-medium text-gray-600">Confirmed deceased</p>
        </div>
      </div>

      <div class="mt-4 grid grid-cols-3 gap-3 border-t border-gray-100 pt-4 sm:grid-cols-5">
        <div class="rounded-md border border-gray-100 p-2 text-center">
          <p class="text-lg font-bold text-gray-900">{{ store.stats?.nepal_confirmed_dead ?? "–" }}</p>
          <p class="text-xs text-gray-500">Dead (Nepal)</p>
        </div>
        <div class="rounded-md border border-gray-100 p-2 text-center">
          <p class="text-lg font-bold text-gray-900">{{ store.stats?.nepal_missing ?? "–" }}</p>
          <p class="text-xs text-gray-500">Missing (Nepal)</p>
        </div>
        <div class="rounded-md border border-gray-100 p-2 text-center">
          <p class="text-lg font-bold text-gray-900">{{ store.stats?.tibet_confirmed_dead ?? "–" }}</p>
          <p class="text-xs text-gray-500">Dead (Tibet)</p>
        </div>
        <div class="rounded-md border border-gray-100 p-2 text-center">
          <p class="text-lg font-bold text-gray-900">{{ store.stats?.tibet_missing ?? "–" }}</p>
          <p class="text-xs text-gray-500">Missing (Tibet)</p>
        </div>
        <div class="rounded-md border border-gray-100 p-2 text-center">
          <p class="text-lg font-bold text-gray-900">{{ store.stats?.total_rescued ?? "–" }}</p>
          <p class="text-xs text-gray-500">Rescued</p>
        </div>
      </div>

      <p class="mt-4 text-center text-xs text-gray-400">
        <strong>{{ store.stats?.hub_registered_missing_count ?? 0 }}</strong> missing and
        <strong>{{ store.stats?.hub_registered_deceased_count ?? 0 }}</strong> deceased named
        individuals are registered on this hub specifically (see tables below) — a small subset
        of the official toll above.
      </p>
      <p v-if="store.stats?.note" class="mt-2 text-center text-xs text-gray-400">
        {{ store.stats.note }}
      </p>
  </Card>
</template>
