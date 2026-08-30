import { createRouter, createWebHistory } from "vue-router";

import AdminReview from "./views/AdminReview.vue";
import Home from "./views/Home.vue";

export default createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", name: "home", component: Home },
    { path: "/admin", name: "admin", component: AdminReview },
  ],
  scrollBehavior(to) {
    if (to.hash) {
      // Retries internally for a short window, since the target section
      // (e.g. #confirmed-deceased) may not exist yet on first paint while
      // Home.vue's data is still loading.
      return { el: to.hash, behavior: "smooth" };
    }
    return { top: 0 };
  },
});
