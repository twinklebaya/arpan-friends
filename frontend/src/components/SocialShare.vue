<script setup>
import { ref } from "vue";

const SHARE_URL = "https://findingarpan.vercel.app/";
const SHARE_TEXT = "Help us find Arpan, Bhavin and Karan, missing since the Nepal-Tibet flash floods.";

const copied = ref(false);

function shareWhatsapp() {
  window.open(
    `https://wa.me/?text=${encodeURIComponent(`${SHARE_TEXT} ${SHARE_URL}`)}`,
    "_blank",
    "noopener,noreferrer",
  );
}

function shareX() {
  window.open(
    `https://twitter.com/intent/tweet?text=${encodeURIComponent(SHARE_TEXT)}&url=${encodeURIComponent(SHARE_URL)}`,
    "_blank",
    "noopener,noreferrer",
  );
}

// Instagram has no public web share-intent URL for posting to feed/story/DM
// from an arbitrary site (unlike X/WhatsApp) -- copy the link+message so it
// can be pasted into a bio, story, or DM instead of pretending a direct
// share flow exists.
async function shareInstagram() {
  try {
    await navigator.clipboard.writeText(`${SHARE_TEXT} ${SHARE_URL}`);
    copied.value = true;
    setTimeout(() => (copied.value = false), 2500);
  } catch {
    // clipboard API unavailable -- nothing to fall back to here
  }
}
</script>

<template>
  <div class="absolute right-4 top-4 flex items-center gap-2 sm:right-6 sm:top-6">
    <button
      type="button"
      title="Share on WhatsApp"
      aria-label="Share on WhatsApp"
      class="flex h-8 w-8 items-center justify-center rounded-full bg-gray-800 text-xs font-bold text-white hover:bg-gray-700"
      @click="shareWhatsapp"
    >
      WA
    </button>
    <button
      type="button"
      title="Share on X"
      aria-label="Share on X"
      class="flex h-8 w-8 items-center justify-center rounded-full bg-gray-800 text-xs font-bold text-white hover:bg-gray-700"
      @click="shareX"
    >
      X
    </button>
    <button
      type="button"
      title="Copy link to share on Instagram"
      aria-label="Copy link to share on Instagram"
      class="flex h-8 w-8 items-center justify-center rounded-full bg-gray-800 text-xs font-bold text-white hover:bg-gray-700"
      @click="shareInstagram"
    >
      IG
    </button>
    <span v-if="copied" class="text-xs font-medium text-gray-300">Link copied!</span>
  </div>
</template>
