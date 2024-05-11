<template>
  <div
    @click="redirectToSettings"
    class="flex items-center space-x-2 mr-4 hover:cursor-pointer"
  >
    <span
      v-if="activeInstanceRef"
      class="h-2 w-2 rounded-full bg-green-500"
      title="Online"
    ></span>
    <span v-if="activeInstanceRef" class="text-sm text-gray-600">{{
      activeInstanceRef.name
    }}</span>
    <span v-else class="text-sm text-gray-600">No active instance</span>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue";
import { useRouter } from "vue-router";
import eventBus from "../utils/EventBus.js";

const router = useRouter();
const instances = ref([]);
const activeInstanceRef = ref(null);

onMounted(() => {
  loadInstancesFromLocalStorage(); // Call the function when component is mounted
  eventBus.$on("instance-updated", handleInstanceUpdate);
});

onUnmounted(() => {
  eventBus.$off("instance-updated", handleInstanceUpdate);
});

const handleInstanceUpdate = () => {
  loadInstancesFromLocalStorage();
};

const loadInstancesFromLocalStorage = () => {
  const storedInstances = localStorage.getItem("instances");
  if (storedInstances) {
    instances.value = JSON.parse(storedInstances);
    updateActiveInstance();
  }
};

const updateActiveInstance = () => {
  activeInstanceRef.value = instances.value.find(
    (instance) => instance.isActive
  );
};

const redirectToSettings = () => {
  router.push("/settings");
};
</script>
