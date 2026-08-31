<script setup>
import { computed } from "vue";

import { useCrisisStore } from "../stores/crisis";
import Button from "./ui/Button.vue";

const store = useCrisisStore();

// Only these three get a photo card -- the rest of the primary-target
// roster is listed as text underneath instead.
const PHOTO_NAMES = ["Arpan Mithalal Kothari", "Karan Bhardwaj", "Bhavinkumar Rajnikant Raval"];

const photoPeople = computed(() =>
  store.primaryTargets.filter((p) => PHOTO_NAMES.includes(p.name)),
);
const otherPeople = computed(() =>
  store.primaryTargets.filter((p) => !PHOTO_NAMES.includes(p.name)),
);

function scrollToForm() {
  document.getElementById("contribute")?.scrollIntoView({ behavior: "smooth" });
}
</script>

<template>
  <section class="bg-gray-900 text-white">
    <div class="mx-auto max-w-5xl px-4 py-10 sm:py-14">
      <p class="text-sm font-semibold uppercase tracking-wide text-red-400">
        Active search: Nepal flash floods
      </p>
      <h1 class="mt-2 text-2xl font-bold leading-tight sm:text-4xl">
        Help us find Arpan, Bhavin and Karan
      </h1>
      <p class="mt-3 max-w-3xl text-gray-300">
        Arpan Kothari, Karan Bhardwaj, and Bhavinkumar Raval have been missing, along with the
        rest of their Kailash Journeys tour group, since the flash floods near the Nepal-Tibet
        border, Rasuwa district. If you have any information, however small, please share it
        below.
      </p>
      <div class="mt-6 flex flex-wrap items-center gap-4">
        <Button variant="urgent" @click="scrollToForm">Submit Information</Button>
        <a href="tel:+14087808343" class="text-sm text-gray-300 hover:text-white">
          Or call/text <span class="font-semibold text-white">+1 (408) 780-8343</span> with any tip
        </a>
      </div>

      <div class="mt-8 grid grid-cols-2 gap-4 sm:grid-cols-3">
        <div
          v-for="person in photoPeople"
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
            <div v-if="person.photo_urls?.length" class="mt-2 flex gap-1.5">
              <a
                v-for="url in person.photo_urls"
                :key="url"
                :href="url"
                target="_blank"
                rel="noopener noreferrer"
                class="block h-8 w-8 overflow-hidden rounded border border-gray-600"
              >
                <img :src="url" :alt="`Additional photo of ${person.name}`" loading="lazy" class="h-full w-full object-cover" />
              </a>
            </div>
          </div>
        </div>
      </div>

      <div v-if="otherPeople.length" class="mt-6 border-t border-gray-700 pt-4">
        <p class="text-xs font-semibold uppercase tracking-wide text-gray-400">
          Also missing from the same tour group
        </p>
        <ul class="mt-2 space-y-1 text-sm text-gray-300">
          <li v-for="person in otherPeople" :key="person.id">
            {{ person.name }} <span class="text-gray-500">(age {{ person.age ?? "unknown" }})</span>
          </li>
        </ul>
      </div>
    </div>
  </section>
</template>
