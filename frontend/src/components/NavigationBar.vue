<template>
  <header class="absolute inset-x-0 top-0 z-50">
    <nav
      class="flex items-center justify-between px-8 bg-white fixed w-full z-20 top-0 start-0 border-b border-gray-200 dark:border-gray-600"
      aria-label="Global"
    >
      <div class="flex py-3 lg:flex-1">
        <a href="/" class="-m-1.5 p-1.5">
          <span class="sr-only">IRIS AI Studio</span>
          <div style="display: inline-flex; align-items: center">
            <img class="h-12 w-auto" src="../assets/logo.png" alt="" />
            <span
              class="tracking-wider underline underline-offset-4 decoration-dotted decoration-4 decoration-iscgreen font-medium text-lg text-iscblue"
              >IRIS AI Studio</span
            >
          </div>
        </a>
      </div>
      <div class="lg:flex lg:gap-x-12">
        <a
          href="/connectors"
          :class="{ 'text-iscblue font-medium': isActive('/connectors') }"
          class="text-base leading-6 text-gray-700"
          >Connectors</a
        >
        <a
          href="/playground"
          :class="{ 'text-iscblue font-medium': isActive('/playground') }"
          class="text-base leading-6 text-gray-700"
          >Playground</a
        >
        <a
          href="/settings"
          :class="{ 'text-iscblue font-medium': isActive('/settings') }"
          class="text-base leading-6 text-gray-700"
          >Settings</a
        >
      </div>
      <div class="flex flex-1 justify-end">
        <ActiveInstance />
        <a
          href="https://github.com/ikram-shah"
          target="_blank"
          rel="noopener noreferrer"
          class="flex items-center ml-3 hover:bg-transparent hover:text-iscblue"
        >
          <img
            class="h-6 w-6"
            src="../assets/github_logo.png"
            alt="GitHub Icon"
          />
        </a>
      </div>
    </nav>
  </header>
</template>

<script setup>
import ActiveInstance from "./ActiveInstance.vue";
import { useRoute } from "vue-router";

const route = useRoute();

const isActive = (path) => {
  return route.path === path;
};
</script>
