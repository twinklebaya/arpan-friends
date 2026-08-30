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
    <EmergencyContacts />
    <HeroSection />
    <CounterBar />
    <MapSection />
    <LiveFeeds />
    <StatusTables />
    <ContributionForm />
  </div>
</template>
