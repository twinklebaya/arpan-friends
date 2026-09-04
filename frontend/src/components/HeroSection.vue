<script setup>
import Button from "./ui/Button.vue";
import SocialShare from "./SocialShare.vue";

function scrollToForm() {
  document.getElementById("contribute")?.scrollIntoView({ behavior: "smooth" });
}
</script>

<template>
  <router-link
    to="/hope"
    class="block bg-urgent px-4 py-2 text-center text-sm font-semibold text-white hover:bg-red-800"
  >
    Global "Rasuwa Hope and Awareness" event &middot; Sun, Sept 6 &middot; 5 PM Pacific &middot;
    <span class="underline">Learn more &rarr;</span>
  </router-link>
  <section class="relative bg-gray-900 text-white">
    <SocialShare />
    <div class="mx-auto max-w-7xl px-4 pt-6 sm:pt-8">
      <p class="text-sm font-semibold uppercase tracking-wide text-red-400">
        Active search: Nepal flash floods
      </p>
      <h1 class="mt-2 text-2xl font-bold leading-tight sm:text-4xl">
        Help us find Arpan, Bhavin and Karan
      </h1>
      <p class="mt-3 max-w-none text-gray-300">
        Arpan Kothari, Karan Bhardwaj, and Bhavinkumar Raval have been missing, along with the
        rest of their Kailash Journeys tour group, since the flash floods near the Nepal-Tibet
        border, Rasuwa district. If you have any information, however small, please share it
        below.
      </p>
      <div class="mt-6 flex flex-wrap items-center gap-4">
        <Button variant="urgent" @click="scrollToForm">Submit Information</Button>
        <p class="text-sm text-gray-300">
          Or call/text
          <a href="tel:+16575221011" class="font-semibold text-white hover:underline">+1 (657) 522-1011</a>
          with any tip
        </p>
      </div>
    </div>
  </section>
</template>
