<script setup>
import { computed, ref } from "vue";

import { openLightbox } from "../lib/lightbox";
import { useCrisisStore } from "../stores/crisis";

const store = useCrisisStore();

const PHOTO_NAMES = ["Arpan Mithalal Kothari", "Karan Bhardwaj", "Bhavinkumar Rajnikant Raval"];
const photoPeople = computed(() =>
  store.primaryTargets.filter((p) => PHOTO_NAMES.includes(p.name)),
);
const otherPeople = computed(() =>
  store.primaryTargets.filter((p) => !PHOTO_NAMES.includes(p.name)),
);

const GROUP_PHOTOS = [
  { url: "/photos/friends-group.jpg", caption: "Arpan, Bhavin, and Karan together" },
  {
    url: "/photos/kailash-tour-group.jpg",
    caption: "The full Kailash Journeys tour group at Hotel Tibet, Kathmandu",
  },
  {
    url: "/photos/location-timeline-search-area.jpg",
    caption: "Location timeline and likely search area",
  },
];

const scrollEl = ref(null);
function scrollBy(amount) {
  scrollEl.value?.scrollBy({ left: amount, behavior: "smooth" });
}
</script>

<template>
  <section class="bg-gray-900 text-white">
    <div class="mx-auto max-w-7xl px-4 pb-10 pt-6 sm:pb-14">
      <div class="grid grid-cols-1 gap-6 lg:grid-cols-3">
        <!-- Individual photos: larger, takes up 2/3 on desktop -->
        <div class="lg:col-span-2">
          <div class="grid grid-cols-1 gap-4 sm:grid-cols-3">
            <div
              v-for="person in photoPeople"
              :key="person.id"
              class="overflow-hidden rounded-lg bg-gray-800"
            >
              <button
                type="button"
                class="flex aspect-square w-full items-center justify-center bg-gray-700"
                :disabled="!person.photo_url"
                @click="openLightbox(person.photo_url, person.name)"
              >
                <img
                  v-if="person.photo_url"
                  :src="person.photo_url"
                  :alt="person.name"
                  loading="lazy"
                  class="h-full w-full cursor-pointer object-cover"
                />
                <span v-else class="px-2 text-center text-xs text-gray-400">Photo pending</span>
              </button>
              <div class="p-3">
                <p class="truncate text-sm font-semibold text-white">{{ person.name }}</p>
                <p class="text-xs text-gray-400">Age {{ person.age ?? "unknown" }}</p>
                <div v-if="person.photo_urls?.length" class="mt-2 flex gap-1.5">
                  <button
                    v-for="url in person.photo_urls"
                    :key="url"
                    type="button"
                    class="block h-8 w-8 overflow-hidden rounded border border-gray-600"
                    @click="openLightbox(url, `Additional photo of ${person.name}`)"
                  >
                    <img
                      :src="url"
                      :alt="`Additional photo of ${person.name}`"
                      loading="lazy"
                      class="h-full w-full cursor-pointer object-cover"
                    />
                  </button>
                </div>
              </div>
            </div>
          </div>

          <div v-if="otherPeople.length" class="mt-6 border-t border-gray-700 pt-4">
            <p class="text-base font-semibold uppercase tracking-wide text-gray-400">
              Also missing from the same tour group
            </p>
            <ul class="mt-2 grid grid-cols-1 gap-x-6 gap-y-1 text-sm text-gray-300 sm:grid-cols-2">
              <li v-for="person in otherPeople" :key="person.id">
                {{ person.name }}
                <span class="text-gray-500">
                  (age {{ person.age ?? "unknown" }}, {{ person.sex ?? "sex unknown" }},
                  {{ person.nationality ?? "nationality unknown" }})
                </span>
              </li>
            </ul>
          </div>
        </div>

        <!-- Additional (group) photos: smaller, takes up 1/3 on desktop -->
        <div>
          <div class="flex items-center justify-between">
            <h2 class="text-base font-bold text-white">Additional Photos</h2>
            <div class="flex gap-1">
              <button
                type="button"
                class="rounded-md border border-gray-600 px-1.5 py-0.5 text-xs text-gray-300 hover:bg-gray-800"
                @click="scrollBy(-160)"
              >
                ←
              </button>
              <button
                type="button"
                class="rounded-md border border-gray-600 px-1.5 py-0.5 text-xs text-gray-300 hover:bg-gray-800"
                @click="scrollBy(160)"
              >
                →
              </button>
            </div>
          </div>
          <div ref="scrollEl" class="mt-3 flex snap-x gap-3 overflow-x-auto pb-2 lg:flex-col lg:overflow-x-visible">
            <button
              v-for="photo in GROUP_PHOTOS"
              :key="photo.url"
              type="button"
              class="block w-36 shrink-0 snap-start overflow-hidden rounded-lg bg-gray-800 text-left lg:w-full"
              @click="openLightbox(photo.url, photo.caption)"
            >
              <img :src="photo.url" :alt="photo.caption" loading="lazy" class="h-24 w-full cursor-pointer object-cover" />
              <p class="p-2 text-xs font-medium text-gray-300">{{ photo.caption }}</p>
            </button>
          </div>
          <p class="mt-3 text-xs text-gray-400">
            If you recognize any details, person or location from these pictures, or if you have
            any additional information to share, please reach out to us!
          </p>
        </div>
      </div>
    </div>
  </section>
</template>
