<script setup>
import { onMounted, ref } from "vue";

const visible = ref(false);

onMounted(() => {
  setTimeout(() => {
    visible.value = true;
  }, 1500);
});

function dismiss() {
  visible.value = false;
}
</script>

<template>
  <Transition
    enter-active-class="transition ease-out duration-300"
    enter-from-class="opacity-0 translate-y-4"
    enter-to-class="opacity-100 translate-y-0"
    leave-active-class="transition ease-in duration-150"
    leave-from-class="opacity-100"
    leave-to-class="opacity-0"
  >
    <div
      v-if="visible"
      class="fixed bottom-4 right-4 z-[1000] w-[calc(100%-2rem)] max-w-sm rounded-lg border border-gray-200 bg-white p-4 shadow-xl sm:right-6 sm:bottom-6"
    >
      <button
        type="button"
        aria-label="Dismiss"
        class="absolute right-2 top-2 text-gray-400 hover:text-gray-600"
        @click="dismiss"
      >
        &times;
      </button>
      <p class="pr-4 text-sm font-bold text-gray-900">Global Event: Rasuwa Hope and Awareness</p>
      <ul class="mt-1 space-y-0.5 text-xs text-gray-600">
        <li>Sun, Sept 6 &middot; 5:00 PM Pacific (USA)</li>
        <li>Sun, Sept 6 &middot; 8:00 PM Eastern (Canada)</li>
        <li>Mon, Sept 7 &middot; 8:00 AM Malaysia (MYT)</li>
        <li>Mon, Sept 7 &middot; 10:00 AM Australia Eastern (AEST)</li>
      </ul>
      <p class="mt-2 text-sm text-gray-600">
        Virtual and in person from the SF Bay Area. Hear from families who found their way back.
      </p>
      <div class="mt-3 flex items-center gap-4">
        <router-link
          to="/hope"
          class="rounded-md bg-urgent px-3 py-1.5 text-sm font-semibold text-white hover:bg-red-800"
          @click="dismiss"
        >
          Learn more
        </router-link>
        <button type="button" class="text-sm text-gray-500 hover:underline" @click="dismiss">
          Dismiss
        </button>
      </div>
    </div>
  </Transition>
</template>
