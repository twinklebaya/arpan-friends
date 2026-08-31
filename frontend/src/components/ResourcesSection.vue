<script setup>
import { RESOURCE_PINS } from "../lib/constants";

const hospitals = RESOURCE_PINS.filter((p) => p.category === "hospital");
const shelters = RESOURCE_PINS.filter((p) => p.category === "shelter");

function mapLink(pin) {
  return `https://www.google.com/maps?q=${pin.lat},${pin.lng}`;
}

// Sourced from the family directly: the Kailash Journeys group's ground
// transport was outsourced to these two operators.
const busProviders = [
  { name: "Arabindra Travels", note: "One of the two buses used for the group's ground transport." },
  {
    name: "Namaste Pasang Lhamu Transport",
    note: "The other bus, plate BA 5 KHA 8789 -- a GPS tracker screenshot shows its last recorded position at Timure/Rasuwagadhi, frozen at almost exactly the time the flood hit (see the target feed for details).",
  },
];

// Named survivors from public reporting who were near the same border
// crossing/area and time as the group -- potential leads, not confirmed
// contacts. Verify independently before reaching out.
const peopleToConnect = [
  {
    name: "Raju Budhathoki",
    context: "Customs agent, Rasuwa Customs Office, Timure. Escaped uphill when the flood hit; witnessed the border area's destruction firsthand.",
    source: "Kathmandu Post / The Federal",
  },
  {
    name: "Prakash Gautam",
    context: "Customs agent, Rasuwa Customs Office, Timure. Also escaped the same location; spent a night in the forest before evacuation.",
    source: "Kathmandu Post / The Federal",
  },
  {
    name: "Anjana Raja and Pattabiraman Venkatesan",
    context: "California/Bay Area couple on the Kailash Mansarovar Yatra, survived the flood in Rasuwa district near the China border. Raja said she intends to complete the pilgrimage.",
    source: "SF Chronicle / CBS News",
  },
];
</script>

<template>
  <section class="mx-auto max-w-7xl px-4 py-6">
    <h2 class="text-lg font-bold text-gray-900">Resources</h2>
    <div class="mt-3 grid grid-cols-1 gap-4 md:grid-cols-2">
      <div class="rounded-xl border border-gray-200 bg-white p-4 shadow-sm">
        <h3 class="text-sm font-semibold text-gray-900">People We Want to Connect With</h3>
        <p class="mt-1 text-xs text-gray-500">
          Named survivors from public reporting near the same area and time. Leads to follow up on,
          not confirmed contacts.
        </p>
        <ul class="mt-2 space-y-2 text-sm">
          <li v-for="p in peopleToConnect" :key="p.name">
            <p class="font-medium text-gray-800">{{ p.name }}</p>
            <p class="text-xs text-gray-500">{{ p.context }}</p>
            <p class="text-xs text-gray-400">Source: {{ p.source }}</p>
          </li>
        </ul>
      </div>

      <div class="rounded-xl border border-gray-200 bg-white p-4 shadow-sm">
        <h3 class="text-sm font-semibold text-gray-900">Hospitals</h3>
        <ul class="mt-2 space-y-2 text-sm">
          <li v-for="h in hospitals" :key="h.label">
            <a
              :href="mapLink(h)"
              target="_blank"
              rel="noopener noreferrer"
              class="font-medium text-blue-600 hover:underline"
            >
              {{ h.label }} ↗
            </a>
            <p class="text-xs text-gray-500">{{ h.note }}</p>
          </li>
        </ul>
      </div>

      <div class="rounded-xl border border-gray-200 bg-white p-4 shadow-sm">
        <h3 class="text-sm font-semibold text-gray-900">Shelters</h3>
        <ul class="mt-2 space-y-2 text-sm">
          <li v-for="s in shelters" :key="s.label">
            <a
              :href="mapLink(s)"
              target="_blank"
              rel="noopener noreferrer"
              class="font-medium text-blue-600 hover:underline"
            >
              {{ s.label }} ↗
            </a>
            <p class="text-xs text-gray-500">{{ s.note }}</p>
          </li>
        </ul>
      </div>

      <div class="rounded-xl border border-gray-200 bg-white p-4 shadow-sm">
        <h3 class="text-sm font-semibold text-gray-900">Bus Providers</h3>
        <ul class="mt-2 space-y-2 text-sm">
          <li v-for="b in busProviders" :key="b.name">
            <p class="font-medium text-gray-800">{{ b.name }}</p>
            <p class="text-xs text-gray-500">{{ b.note }}</p>
          </li>
        </ul>
      </div>
    </div>
  </section>
</template>
