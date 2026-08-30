<script setup>
import { useCrisisStore } from "../stores/crisis";
import Button from "./ui/Button.vue";

const store = useCrisisStore();

function scrollToForm() {
  document.getElementById("contribute")?.scrollIntoView({ behavior: "smooth" });
}
</script>

<template>
  <section class="bg-gray-900 text-white">
    <div class="mx-auto max-w-5xl px-4 py-10 sm:py-14">
      <p class="text-sm font-semibold uppercase tracking-wide text-red-400">
        Active search — Nepal flash floods
      </p>
      <h1 class="mt-2 text-2xl font-bold leading-tight sm:text-4xl">
        Help us find the Kailash Journeys tour group
      </h1>
      <p class="mt-3 max-w-3xl text-gray-300">
        Members of the Kailash Journeys tour group have been missing since the flash floods near
        the Nepal-Tibet border, Rasuwa district. If you have any information — however small —
        please share it below.
      </p>
      <p class="mt-2 max-w-3xl text-sm text-gray-400">
        This hub is also open to families and friends of anyone affected by the Nepal-Tibet
        floods, of any nationality — see the registry and tables further down the page.
      </p>

      <div class="mt-6">
        <Button variant="urgent" @click="scrollToForm">Submit Information</Button>
      </div>

      <div class="mt-8 grid grid-cols-2 gap-4 sm:grid-cols-3">
        <div
          v-for="person in store.primaryTargets"
          :key="person.id"
          class="overflow-hidden rounded-lg bg-gray-800"
        >
          <div class="flex aspect-square items-center justify-center bg-gray-700">
            <img
              v-if="person.photo_url"
              :src="person.photo_url"
              :alt="person.name"
              loading="lazy"
              class="h-full w-full object-cover"
            />
            <span v-else class="px-2 text-center text-xs text-gray-400">Photo pending</span>
          </div>
          <div class="p-3">
            <p class="truncate text-sm font-semibold">{{ person.name }}</p>
            <p class="text-xs text-gray-400">Age {{ person.age ?? "unknown" }}</p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
