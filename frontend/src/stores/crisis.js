import { defineStore } from "pinia";

import { api } from "../lib/api";

// State shape here is intentionally flat and driven entirely by fetch
// actions, so swapping the polling in startPolling() for a real-time
// subscription (Supabase channel, WebSocket, SSE) later only means
// replacing the interval with a subscription callback that calls the same
// setters -- components never need to change.
export const useCrisisStore = defineStore("crisis", {
  state: () => ({
    persons: [],
    stats: null,
    generalFeed: [],
    targetFeed: [],
    loading: false,
    error: null,
    _pollHandle: null,
  }),

  getters: {
    stillMissing: (state) => {
      const missing = state.persons.filter((p) => p.status === "missing");
      const featured = ["Arpan Mithalal Kothari", "Bhavinkumar Rajnikant Raval", "Karan Bhardwaj"];
      const rank = (p) => {
        const i = featured.indexOf(p.name);
        return i === -1 ? featured.length : i;
      };
      return [...missing].sort((a, b) => rank(a) - rank(b));
    },
    confirmedDeceased: (state) => state.persons.filter((p) => p.status === "deceased"),
    primaryTargets: (state) =>
      state.persons.filter((p) => p.is_primary_target && p.status === "missing"),
  },

  actions: {
    async fetchAll() {
      this.loading = true;
      this.error = null;
      try {
        const [persons, stats, generalFeed, targetFeed] = await Promise.all([
          api.getPersons(),
          api.getStats(),
          api.getGeneralFeed(),
          api.getTargetFeed(),
        ]);
        this.persons = persons;
        this.stats = stats;
        this.generalFeed = generalFeed;
        this.targetFeed = targetFeed;
      } catch (err) {
        this.error = err.message;
      } finally {
        this.loading = false;
      }
    },

    startPolling(intervalMs = 30000) {
      this.fetchAll();
      this.stopPolling();
      this._pollHandle = setInterval(() => this.fetchAll(), intervalMs);
    },

    stopPolling() {
      if (this._pollHandle) {
        clearInterval(this._pollHandle);
        this._pollHandle = null;
      }
    },
  },
});
