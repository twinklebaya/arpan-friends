<script setup>
// PLACEHOLDER contacts -- replace every number below with a verified,
// real hotline before this goes live. Do not publish invented numbers.
const contacts = [
  { label: "Australian Department of Foreign Affairs (DFAT) 24hr Consular Emergency", phone: "PLACEHOLDER: +61 …" },
  { label: "Nepalese Rasuwa District Authority / Police", phone: "PLACEHOLDER: +977 …" },
  { label: "Family tip line (direct)", phone: "PLACEHOLDER: +__ …" },
];
</script>

<template>
  <section class="bg-urgent-light">
    <div class="mx-auto max-w-5xl px-4 py-4">
      <p class="text-xs font-semibold uppercase tracking-wide text-urgent">Emergency contacts</p>
      <div class="mt-2 grid grid-cols-1 gap-2 text-sm sm:grid-cols-3">
        <div v-for="c in contacts" :key="c.label">
          <p class="font-medium text-gray-900">{{ c.label }}</p>
          <p class="text-gray-600">{{ c.phone }}</p>
        </div>
      </div>
    </div>
  </section>
</template>
