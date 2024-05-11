import { createRouter, createWebHistory } from "vue-router";
import HomePage from "../views/HomePage.vue";
import ConnectorsPage from "../views/ConnectorsPage.vue";
import PlaygroundPage from "../views/PlaygroundPage.vue";
import SettingsPage from "../views/SettingsPage.vue";

const routes = [
  { path: "/", component: HomePage },
  { path: "/connectors", component: ConnectorsPage },
  {
    path: "/playground",
    component: PlaygroundPage,
  },
  { path: "/settings", component: SettingsPage },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
