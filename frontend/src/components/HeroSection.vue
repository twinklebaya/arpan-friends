<script setup>
import Button from "./ui/Button.vue";

function scrollToForm() {
  document.getElementById("contribute")?.scrollIntoView({ behavior: "smooth" });
}
</script>

<template>
  <section class="bg-gray-900 text-white">
    <div class="mx-auto max-w-5xl px-4 pt-10 sm:pt-14">
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
        <a href="tel:+16575221011" class="text-sm text-gray-300 hover:text-white">
          or <span class="font-semibold text-white">+1 (657) 522-1011</span>
        </a>
      </div>
    </div>
  </section>
</template>
