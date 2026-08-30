import { createRouter, createWebHistory } from "vue-router";

import AdminReview from "./views/AdminReview.vue";
import Home from "./views/Home.vue";

export default createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", name: "home", component: Home },
    { path: "/admin", name: "admin", component: AdminReview },
  ],
});
