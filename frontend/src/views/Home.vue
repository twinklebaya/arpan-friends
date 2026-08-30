<script setup>
import { onUnmounted } from "vue";

import ContributionForm from "../components/ContributionForm.vue";
import CounterBar from "../components/CounterBar.vue";
import EmergencyContacts from "../components/EmergencyContacts.vue";
import HeroSection from "../components/HeroSection.vue";
import LiveFeeds from "../components/LiveFeeds.vue";
import MapSection from "../components/MapSection.vue";
import StatusTables from "../components/StatusTables.vue";
import { useCrisisStore } from "../stores/crisis";

const store = useCrisisStore();
store.startPolling(30000);
onUnmounted(() => store.stopPolling());
</script>

<template>
  <div>
    <HeroSection />
    <section class="mx-auto max-w-5xl px-4 py-6">
      <div class="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <CounterBar />
        <MapSection />
      </div>
    </section>
    <LiveFeeds />
    <StatusTables />
    <EmergencyContacts />
    <ContributionForm />
  </div>
</template>
