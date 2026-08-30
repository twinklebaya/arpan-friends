<script setup>
import { onUnmounted } from "vue";

import ContributionForm from "../components/ContributionForm.vue";
import CounterBar from "../components/CounterBar.vue";
import EmergencyContacts from "../components/EmergencyContacts.vue";
import HeroSection from "../components/HeroSection.vue";
import LiveFeeds from "../components/LiveFeeds.vue";
import MapSection from "../components/MapSection.vue";
import RegisterPersonForm from "../components/RegisterPersonForm.vue";
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
    <RegisterPersonForm />
    <ContributionForm />

    <footer class="mx-auto max-w-5xl px-4 py-6 text-center text-xs text-gray-400">
      <router-link to="/admin" class="hover:underline">Admin review queue</router-link>
    </footer>
  </div>
</template>
