<script setup>
import { Analytics } from "@vercel/analytics/vue";

import PhotoLightbox from "./components/PhotoLightbox.vue";
</script>

<template>
  <router-view />
  <PhotoLightbox />
  <Analytics />
</template>
