<script setup>
import { ref } from "vue";

import { useCrisisStore } from "../stores/crisis";

const store = useCrisisStore();

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
  </section>
</template>
