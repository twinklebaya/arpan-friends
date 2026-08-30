<script setup>
// All numbers below verified against official/government-linked sources as
// of Aug 2026. Sources:
// - DFAT hotline: Senator Penny Wong, official statement (X/Twitter)
//   https://x.com/SenatorWong/status/2092865278984192011
// - Australian Embassy Kathmandu phone + email: confirmed via the family's
//   own missing-person flyer for Arpan Kothari (matches the embassy site's
//   phone number independently fetched earlier)
// - India MEA control room: corroborated across multiple Indian outlets
//   (Free Press Journal, Telangana Today, The Tribune, Oneindia, The Federal)
// - Nepal national hotlines: Nepal Home Ministry (disaster hotline moved
//   from 1149 to 1234 in July 2026)
// - Nepal Tourist Police + Nepal Tourism Board hotline: family flyer
//
// "Family tip line" is the one placeholder left -- only you can fill in a
// real direct-to-family contact.
const contactGroups = [
  {
    country: "Australia",
    contacts: [
      {
        label: "DFAT 24hr Consular Emergency Centre",
        phone: "1300 555 135 (within Australia) / +61 2 6261 3305 (overseas)",
      },
      {
        label: "Australian Embassy, Kathmandu",
        phone: "+977 1 437 1678",
        note: "Email: kathmandu.embassy@dfat.gov.au",
      },
    ],
  },
  {
    country: "India",
    contacts: [
      {
        label: "MEA 24x7 Control Room (New Delhi)",
        phone: "+91 11 2308 8718 / +91 11 2308 8719",
        note: "WhatsApp: +91 99682 91988 · Email: situationroom@mea.gov.in",
      },
      {
        label: "Indian Embassy, Kathmandu (also on WhatsApp)",
        phone: "+977 985 131 6807 / +977 970 910 7500 / +977 981 032 6117",
      },
    ],
  },
  {
    country: "Nepal",
    contacts: [
      { label: "National Disaster Hotline", phone: "1234" },
      { label: "Nepal Tourist Police (24/7)", phone: "+977 985 128 9445", note: "Also on WhatsApp" },
      { label: "Nepal Tourism Board — Tourist Assistance (24/7)", phone: "1234 / 1144" },
      { label: "Nepal Police", phone: "100" },
      { label: "Ambulance", phone: "102" },
      { label: "General mobile emergency", phone: "112" },
    ],
  },
  {
    country: "This site",
    contacts: [{ label: "Family tip line (direct, call or text)", phone: "+1 (408) 780-8343" }],
  },
];
</script>

<template>
  <section class="bg-urgent-light">
    <div class="mx-auto max-w-5xl px-4 py-5">
      <p class="text-xs font-semibold uppercase tracking-wide text-urgent">Emergency contacts</p>
      <p class="mt-0.5 text-xs text-gray-500 sm:hidden">Scroll for all countries ↓</p>
      <div
        class="mt-3 grid max-h-72 grid-cols-1 gap-3 overflow-y-auto text-sm sm:max-h-none sm:grid-cols-2 sm:overflow-visible lg:grid-cols-4"
      >
        <div
          v-for="group in contactGroups"
          :key="group.country"
          class="rounded-lg border border-red-100 bg-white p-4 shadow-sm"
        >
          <p class="mb-2 text-xs font-semibold uppercase tracking-wide text-gray-500">
            {{ group.country }}
          </p>
          <div v-for="c in group.contacts" :key="c.label" class="mb-3 last:mb-0">
            <p class="font-medium text-gray-900">{{ c.label }}</p>
            <p class="text-gray-600">{{ c.phone }}</p>
            <p v-if="c.note" class="text-xs text-gray-500">{{ c.note }}</p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
