<script setup>
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import iconRetinaUrl from "leaflet/dist/images/marker-icon-2x.png";
import iconUrl from "leaflet/dist/images/marker-icon.png";
import shadowUrl from "leaflet/dist/images/marker-shadow.png";
import { onMounted, ref } from "vue";

import { LAST_KNOWN_LOCATION, MAP_DEFAULT_ZOOM, RESOURCE_PINS } from "../lib/constants";

const mapContainer = ref(null);

// Vite bundles Leaflet's default marker images under a hashed path that the
// library's own CSS doesn't know about -- this is the standard fix.
L.Icon.Default.mergeOptions({ iconRetinaUrl, iconUrl, shadowUrl });

function pinIcon(emoji, bg) {
  return L.divIcon({
    html: `<div style="background:${bg};width:26px;height:26px;border-radius:50%;display:flex;align-items:center;justify-content:center;border:2px solid white;box-shadow:0 1px 3px rgba(0,0,0,.4);font-size:14px;">${emoji}</div>`,
    className: "",
    iconSize: [26, 26],
    iconAnchor: [13, 13],
  });
}

const ICONS = {
  hospital: pinIcon("🏥", "#dc2626"),
  shelter: pinIcon("⛺", "#2563eb"),
};

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
      // Leaflet's default popup width (up to 300px) doesn't fit a narrow
      // mobile map -- without a tighter cap it overflows this card and
      // gets clipped unreadable by the rounded-corner wrapper below.
      { maxWidth: 200 },
    )
    .openPopup();

  for (const pin of RESOURCE_PINS) {
    L.marker([pin.lat, pin.lng], { icon: ICONS[pin.category] })
      .addTo(map)
      .bindPopup(
        `<strong>${pin.label}</strong><br/><span style="color:#6b7280">${pin.note}</span>`,
        { maxWidth: 200 },
      );
  }
});
</script>

<template>
  <div class="h-full rounded-xl border border-gray-200 bg-white p-5 shadow-sm sm:p-6">
    <p class="text-center text-xs font-semibold uppercase tracking-wide text-gray-500">
      Last Known Location &amp; Nearby Resources
    </p>
    <p class="mt-1 text-sm text-gray-500">{{ LAST_KNOWN_LOCATION.note }}</p>
    <div class="mt-3 overflow-hidden rounded-lg border border-gray-200">
      <div ref="mapContainer" class="leaflet-map"></div>
    </div>
    <div class="mt-2 flex flex-wrap gap-x-4 gap-y-1 text-xs text-gray-500">
      <span>📍 Last known location</span>
      <span>🏥 Hospital</span>
      <span>⛺ Shelter</span>
    </div>
    <p class="mt-1 text-xs text-gray-500">
      Coordinates: {{ LAST_KNOWN_LOCATION.lat.toFixed(4) }}, {{ LAST_KNOWN_LOCATION.lng.toFixed(4) }}
    </p>
  </div>
</template>
