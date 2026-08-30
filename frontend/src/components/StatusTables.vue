<script setup>
import { ref } from "vue";

import { useCrisisStore } from "../stores/crisis";

const store = useCrisisStore();

const expandedId = ref(null);
function toggle(id) {
  expandedId.value = expandedId.value === id ? null : id;
}

const copiedId = ref(null);
async function copyLink(anchorId) {
  const url = `${window.location.origin}${window.location.pathname}#${anchorId}`;
  try {
    await navigator.clipboard.writeText(url);
    copiedId.value = anchorId;
    setTimeout(() => {
      if (copiedId.value === anchorId) copiedId.value = null;
    }, 2000);
  } catch {
    // clipboard API unavailable -- silently ignore, the anchor link still works if shared manually
  }
}
</script>

<template>
  <section class="mx-auto max-w-5xl space-y-6 px-4 py-6">
    <p class="text-sm text-gray-500">
      A shared registry for families and friends of anyone affected by the Nepal-Tibet floods, of
      any nationality. Anyone can add a loved one below — every entry is admin-reviewed before it
      appears here.
    </p>
    <div
      id="still-missing"
      class="scroll-mt-4 rounded-xl border border-gray-200 bg-white p-4 shadow-sm sm:p-5"
    >
      <div class="flex items-center justify-between gap-2">
        <h2 class="text-lg font-bold text-gray-900">Still Missing</h2>
        <button
          type="button"
          class="text-xs font-medium text-blue-600 hover:underline"
          @click="copyLink('still-missing')"
        >
          {{ copiedId === "still-missing" ? "Link copied!" : "Share this list" }}
        </button>
      </div>
      <div class="mt-3 overflow-x-auto rounded-lg border border-gray-200">
        <table class="min-w-full divide-y divide-gray-200 text-sm">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-3 py-2 text-left font-semibold text-gray-700">Name</th>
              <th class="px-3 py-2 text-left font-semibold text-gray-700">Age</th>
              <th class="px-3 py-2 text-left font-semibold text-gray-700">Last Seen Location</th>
              <th class="px-3 py-2 text-left font-semibold text-gray-700">Distinct Physical Markers</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100 bg-white">
            <tr v-for="p in store.stillMissing" :key="p.id" class="hover:bg-gray-50">
              <td class="px-3 py-2 font-medium text-gray-900">{{ p.name }}</td>
              <td class="px-3 py-2 text-gray-600">{{ p.age ?? "—" }}</td>
              <td class="px-3 py-2 text-gray-600">{{ p.last_seen_location }}</td>
              <td class="px-3 py-2 text-gray-600">{{ p.physical_markers }}</td>
            </tr>
            <tr v-if="!store.stillMissing.length">
              <td colspan="4" class="px-3 py-4 text-center text-gray-400">No records yet.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div
      id="confirmed-deceased"
      class="scroll-mt-4 rounded-xl border border-gray-200 bg-white p-4 shadow-sm sm:p-5"
    >
      <div class="flex items-center justify-between gap-2">
        <h2 class="text-lg font-bold text-gray-900">Confirmed Deceased</h2>
        <button
          type="button"
          class="text-xs font-medium text-blue-600 hover:underline"
          @click="copyLink('confirmed-deceased')"
        >
          {{ copiedId === "confirmed-deceased" ? "Link copied!" : "Share this list" }}
        </button>
      </div>
      <p class="mt-1 text-xs text-gray-500">Click a name to see distinct physical markers.</p>
      <div class="mt-3 divide-y divide-gray-100 rounded-lg border border-gray-200">
        <div v-for="p in store.confirmedDeceased" :key="p.id">
          <button
            type="button"
            class="flex w-full items-center justify-between gap-3 px-3 py-2 text-left text-sm hover:bg-gray-50"
            :aria-expanded="expandedId === p.id"
            @click="toggle(p.id)"
          >
            <span class="min-w-0 flex-1 truncate">
              <span class="font-medium text-gray-900">{{ p.name }}</span>
              <span class="text-gray-500"> · Age {{ p.age ?? "—" }}</span>
              <span class="text-gray-500"> · Found at: {{ p.found_location ?? "—" }}</span>
            </span>
            <span class="shrink-0 text-gray-400">{{ expandedId === p.id ? "▲" : "▼" }}</span>
          </button>
          <div v-if="expandedId === p.id" class="bg-gray-50 px-3 py-2 text-sm text-gray-600">
            <span class="font-medium text-gray-700">Distinct physical markers: </span>
            {{ p.physical_markers || "None on record." }}
          </div>
        </div>
        <p v-if="!store.confirmedDeceased.length" class="px-3 py-4 text-center text-sm text-gray-400">
          No records.
        </p>
      </div>
    </div>
  </section>
</template>
