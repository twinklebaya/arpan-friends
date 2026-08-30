<script setup>
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import iconRetinaUrl from "leaflet/dist/images/marker-icon-2x.png";
import iconUrl from "leaflet/dist/images/marker-icon.png";
import shadowUrl from "leaflet/dist/images/marker-shadow.png";
import { onMounted, ref } from "vue";

import { LAST_KNOWN_LOCATION, MAP_DEFAULT_ZOOM } from "../lib/constants";

const mapContainer = ref(null);

// Vite bundles Leaflet's default marker images under a hashed path that the
// library's own CSS doesn't know about -- this is the standard fix.
L.Icon.Default.mergeOptions({ iconRetinaUrl, iconUrl, shadowUrl });

onMounted(() => {
  const map = L.map(mapContainer.value, {
    center: [LAST_KNOWN_LOCATION.lat, LAST_KNOWN_LOCATION.lng],
    zoom: MAP_DEFAULT_ZOOM,
    scrollWheelZoom: false,
  });

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "&copy; OpenStreetMap contributors",
    maxZoom: 18,
  }).addTo(map);

  L.marker([LAST_KNOWN_LOCATION.lat, LAST_KNOWN_LOCATION.lng])
    .addTo(map)
    .bindPopup(
      `<strong>Last known location</strong><br/>${LAST_KNOWN_LOCATION.label}<br/>` +
        `${LAST_KNOWN_LOCATION.lat.toFixed(4)}, ${LAST_KNOWN_LOCATION.lng.toFixed(4)}<br/>` +
        `<span style="color:#b91c1c">${LAST_KNOWN_LOCATION.note}</span>`,
    )
    .openPopup();
});
</script>

<template>
  <section class="mx-auto max-w-5xl px-4 py-6">
    <div class="rounded-xl border border-gray-200 bg-white p-5 shadow-sm sm:p-6">
      <h2 class="text-lg font-bold text-gray-900">Last Known Location</h2>
      <p class="mt-1 text-sm text-gray-500">{{ LAST_KNOWN_LOCATION.note }}</p>
      <div class="mt-3 overflow-hidden rounded-lg border border-gray-200">
        <div ref="mapContainer" class="leaflet-map"></div>
      </div>
      <p class="mt-2 text-xs text-gray-500">
        Coordinates: {{ LAST_KNOWN_LOCATION.lat.toFixed(4) }}, {{ LAST_KNOWN_LOCATION.lng.toFixed(4) }}
      </p>
    </div>
  </section>
</template>
