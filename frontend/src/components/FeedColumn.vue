<script setup>
import { onBeforeUnmount, onMounted, ref } from "vue";

import Badge from "./ui/Badge.vue";
import Card from "./ui/Card.vue";

defineProps({
  title: { type: String, required: true },
  items: { type: Array, default: () => [] },
  emptyText: { type: String, default: "No updates yet." },
});

function sourceTone(sourceType) {
  if (sourceType === "official" || sourceType === "family") return "success";
  if (sourceType === "social_media") return "warning";
  return "neutral";
}

function sourceLabel(sourceType) {
  return (
    {
      official: "Official source",
      news_media: "News media",
      family: "Family account",
      social_media: "Social media — unverified",
      other: "Other source",
      tip: "Public tip",
    }[sourceType] || "Source"
  );
}

function formatTime(iso) {
  return new Date(iso).toLocaleString(undefined, {
    month: "short",
    day: "numeric",
    hour: "numeric",
    minute: "2-digit",
  });
}

// Slow auto-scroll that pauses on any manual interaction (hover, touch,
// wheel, drag-scroll) and resumes a couple of seconds after it stops.
const scrollEl = ref(null);
let rafId = null;
let paused = false;
let resumeTimer = null;

function tick() {
  const el = scrollEl.value;
  if (el && !paused) {
    const atBottom = el.scrollTop + el.clientHeight >= el.scrollHeight - 1;
    el.scrollTop = atBottom ? 0 : el.scrollTop + 0.4;
  }
  rafId = requestAnimationFrame(tick);
}

function pauseThenResume() {
  paused = true;
  clearTimeout(resumeTimer);
  resumeTimer = setTimeout(() => {
    paused = false;
  }, 2500);
}

onMounted(() => {
  rafId = requestAnimationFrame(tick);
  const el = scrollEl.value;
  if (el) {
    ["wheel", "touchstart", "mouseenter", "pointerdown"].forEach((evt) =>
      el.addEventListener(evt, pauseThenResume, { passive: true }),
    );
  }
});

onBeforeUnmount(() => {
  cancelAnimationFrame(rafId);
  clearTimeout(resumeTimer);
});
</script>

<template>
  <div>
    <h3 class="mb-3 text-base font-bold text-gray-900">{{ title }}</h3>
    <div ref="scrollEl" class="max-h-[28rem] space-y-3 overflow-y-auto pr-1">
      <Card v-for="item in items" :key="item.id" class="p-4">
        <div class="flex items-start justify-between gap-2">
          <p class="text-sm font-semibold text-gray-900">{{ item.title }}</p>
          <Badge :tone="sourceTone(item.origin === 'tip' ? 'tip' : item.source_type)">
            {{ item.origin === "tip" ? "Public tip" : sourceLabel(item.source_type) }}
          </Badge>
        </div>
        <p class="mt-1 text-sm text-gray-600">{{ item.body }}</p>
        <div class="mt-2 flex items-center justify-between text-xs text-gray-400">
          <span>{{ item.source_name }}</span>
          <span>{{ formatTime(item.published_at) }}</span>
        </div>
        <a
          v-if="item.source_url"
          :href="item.source_url"
          target="_blank"
          rel="noopener noreferrer"
          class="mt-1 inline-block text-xs font-medium text-blue-600 hover:underline"
        >
          View source
        </a>
      </Card>
      <p v-if="!items.length" class="text-sm text-gray-400">{{ emptyText }}</p>
    </div>
  </div>
</template>
