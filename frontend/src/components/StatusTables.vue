<script setup>
import { useCrisisStore } from "../stores/crisis";

const store = useCrisisStore();
</script>

<template>
  <section class="mx-auto max-w-5xl space-y-8 px-4 py-8">
    <p class="text-sm text-gray-500">
      A shared registry for families and friends of anyone affected by the Nepal-Tibet floods, of
      any nationality. Anyone can add a loved one below — every entry is admin-reviewed before it
      appears here.
    </p>
    <div>
      <h2 class="text-lg font-bold text-gray-900">Still Missing</h2>
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
            <tr v-for="p in store.stillMissing" :key="p.id">
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

    <div>
      <h2 class="text-lg font-bold text-gray-900">Confirmed Deceased</h2>
      <div class="mt-3 overflow-x-auto rounded-lg border border-gray-200">
        <table class="min-w-full divide-y divide-gray-200 text-sm">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-3 py-2 text-left font-semibold text-gray-700">Name</th>
              <th class="px-3 py-2 text-left font-semibold text-gray-700">Age</th>
              <th class="px-3 py-2 text-left font-semibold text-gray-700">Location Found</th>
              <th class="px-3 py-2 text-left font-semibold text-gray-700">Distinct Physical Markers</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100 bg-white">
            <tr v-for="p in store.confirmedDeceased" :key="p.id">
              <td class="px-3 py-2 font-medium text-gray-900">{{ p.name }}</td>
              <td class="px-3 py-2 text-gray-600">{{ p.age ?? "—" }}</td>
              <td class="px-3 py-2 text-gray-600">{{ p.found_location ?? "—" }}</td>
              <td class="px-3 py-2 text-gray-600">{{ p.physical_markers }}</td>
            </tr>
            <tr v-if="!store.confirmedDeceased.length">
              <td colspan="4" class="px-3 py-4 text-center text-gray-400">No records.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </section>
</template>
