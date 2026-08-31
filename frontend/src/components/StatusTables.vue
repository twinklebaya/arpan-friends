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
  <section id="still-missing" class="mx-auto max-w-5xl scroll-mt-4 px-4 py-6">
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
    <div class="mt-3 grid grid-cols-1 gap-4 md:grid-cols-2">
      <div
        v-for="p in store.stillMissing"
        :key="p.id"
        class="rounded-xl border border-gray-200 bg-white p-4 shadow-sm"
      >
        <div class="flex items-baseline justify-between gap-2">
          <p class="font-semibold text-gray-900">{{ p.name }}</p>
          <p class="shrink-0 text-sm text-gray-500">Age {{ p.age ?? "—" }}</p>
        </div>
        <div class="mt-2 space-y-2 text-sm">
          <div>
            <p class="text-xs font-medium uppercase tracking-wide text-gray-400">
              Last Seen Location
            </p>
            <p class="text-gray-700">{{ p.last_seen_location || "—" }}</p>
          </div>
          <div>
            <p class="text-xs font-medium uppercase tracking-wide text-gray-400">
              Distinct Physical Markers
            </p>
            <p class="text-gray-700">{{ p.physical_markers || "—" }}</p>
          </div>
        </div>
      </div>
      <p v-if="!store.stillMissing.length" class="text-sm text-gray-400">No records yet.</p>
    </div>
  </section>
</template>
