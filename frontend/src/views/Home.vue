<script setup>
import { onUnmounted } from "vue";

import ContributionForm from "../components/ContributionForm.vue";
import CounterBar from "../components/CounterBar.vue";
import HeroSection from "../components/HeroSection.vue";
import HopeEventPopup from "../components/HopeEventPopup.vue";
import LiveFeeds from "../components/LiveFeeds.vue";
import MapSection from "../components/MapSection.vue";
import PhotoGallery from "../components/PhotoGallery.vue";
import ResourcesSection from "../components/ResourcesSection.vue";
import StatusTables from "../components/StatusTables.vue";
import { useCrisisStore } from "../stores/crisis";

const store = useCrisisStore();
store.startPolling(30000);
onUnmounted(() => store.stopPolling());
</script>

<template>
  <div>
    <HopeEventPopup />
    <HeroSection />
    <PhotoGallery />
    <section class="mx-auto max-w-7xl px-4 py-6">
      <div class="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <CounterBar />
        <MapSection />
      </div>
    </section>
    <StatusTables />
    <ResourcesSection />
    <LiveFeeds />
    <section class="bg-urgent-light py-8">
      <div class="mx-auto max-w-4xl px-4">
        <ContributionForm />
      </div>
    </section>
  </div>
</template>
