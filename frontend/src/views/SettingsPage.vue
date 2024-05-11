<template>
  <div class="w-2/3 justify-center items-center mx-auto">
    <form>
      <div class="m-auto">
        <h2 class="text-left text-2xl font-normal leading-7 text-gray-900">Settings</h2>
        <p class="text-left mt-2 text-sm leading-6 text-gray-500">
          Though we save the critial information only into the browser, suggesting to
          delete the keys after use.
        </p>

        <form @submit.prevent="addInstance">
          <div class="border-b pb-6 border-gray-100">
            <h2 class="mt-6 text-left font-medium leading-7 text-gray-900">
              Add new IRIS instance
            </h2>
            <div class="mt-4">
              <div class="mb-4 flex flex-wrap">
                <div class="w-1/3 pr-2">
                  <label
                    for="name"
                    class="text-left block text-sm font-normal leading-6 text-gray-900"
                    >Name</label
                  >
                  <input
                    type="text"
                    v-model="newInstance.name"
                    placeholder="UPMC Demo Instance"
                    class="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                  />
                </div>
                <div class="w-1/3 pr-2">
                  <label
                    for="username"
                    class="text-left block text-sm font-normal leading-6 text-gray-900"
                    >Username</label
                  >
                  <input
                    type="text"
                    v-model="newInstance.username"
                    placeholder="demo_user"
                    class="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                  />
                </div>
                <div class="w-1/3">
                  <label
                    for="password"
                    class="text-left block text-sm font-normal leading-6 text-gray-900"
                    >Password</label
                  >
                  <input
                    type="password"
                    v-model="newInstance.password"
                    placeholder="..."
                    autocomplete="off"
                    class="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                  />
                </div>
              </div>
              <div class="mb-6 flex flex-wrap">
                <div class="w-2/3 pr-2">
                  <label
                    for="hostname"
                    class="text-left block text-sm font-normal leading-6 text-gray-900"
                    >Hostname</label
                  >
                  <input
                    type="text"
                    v-model="newInstance.hostname"
                    placeholder="..."
                    class="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                  />
                </div>
                <div class="w-1/6 pr-2">
                  <label
                    for="namespace"
                    class="text-left block text-sm font-normal leading-6 text-gray-900"
                    >Namespace</label
                  >
                  <input
                    type="text"
                    v-model="newInstance.namespace"
                    placeholder="USER"
                    class="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                  />
                </div>
                <div class="w-1/6">
                  <label
                    for="port"
                    class="text-left block text-sm font-normal leading-6 text-gray-900"
                    >Port</label
                  >
                  <input
                    type="number"
                    v-model.number="newInstance.port"
                    placeholder="1972"
                    class="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                  />
                </div>
              </div>
              <div class="flex justify-start">
                <button
                  type="submit"
                  class="inline-flex items-center rounded-md bg-iscblue px-3 py-2 text-sm font-normal text-white shadow-sm"
                >
                  <PlusIcon class="ml-0.5 mr-1.5 h-5 w-5" aria-hidden="true" />
                  Add
                </button>
              </div>
            </div>
          </div>
        </form>

        <div class="border-b pb-4 border-gray-100">
          <h2 class="mt-6 text-left font-medium leading-7 text-gray-900">
            Manage IRIS instances
          </h2>
          <ul v-if="instances.length > 0">
            <li
              v-for="(instance, index) in instances"
              :key="index"
              class="flex justify-between items-center py-4"
            >
              <div class="flex items-center">
                <input
                  type="radio"
                  name="instance"
                  class="mr-4"
                  :value="index"
                  v-model="selectedInstanceIndex"
                  @change="toggleInstanceActive(index)"
                />
                <div>
                  <p class="text-gray-800 font-normal">
                    {{ instance.name }}
                    <span class="font-normal text-sm text-gray-400 ml-2">{{
                      getInstanceUrl(instance)
                    }}</span>
                  </p>
                </div>
              </div>
              <button
                type="button"
                @click="removeInstance(index)"
                class="bg-white focus:bg-red"
              >
                <TrashIcon class="-ml-0.5 mr-1.5 h-5 w-5" aria-hidden="true" />
              </button>
            </li>
          </ul>
          <p v-else class="font-normal text-sm text-gray-400 mt-3">
            No instances available.
          </p>
        </div>

        <div>
          <div>
            <h2 class="mt-6 text-left font-medium leading-7 text-gray-900">API Keys</h2>
            <p class="text-left mt-1 text-sm leading-6 text-gray-500">
              We save the API keys to your browser's session storage. You have to re-enter
              the keys for every session
            </p>
            <div class="my-4 grid grid-cols-1 gap-x-6 gap-y-4 sm:grid-cols-6">
              <div class="sm:col-span-4">
                <label
                  for="username"
                  class="text-left block text-sm font-normal leading-6 text-gray-900"
                  >OpenAI API Key</label
                >
                <input
                  type="password"
                  autocomplete="off"
                  v-model="openai_apikey"
                  placeholder="sk-..."
                  class="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                />
                <div class="mt-2"></div>
              </div>
              <div class="sm:col-span-4">
                <label
                  for="username"
                  class="text-left block text-sm font-normal leading-6 text-gray-900"
                  >Cohere API Key</label
                >
                <input
                  type="password"
                  autocomplete="off"
                  v-model="cohere_apikey"
                  placeholder="..."
                  class="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from "vue";
import eventBus from "../utils/EventBus.js";
import { PlusIcon, TrashIcon } from "@heroicons/vue/20/solid";

const openai_apikey = ref("");
const cohere_apikey = ref("");

// Reactive variable for new instance
const newInstance = ref({
  name: "",
  username: "",
  password: "",
  hostname: "",
  namespace: "",
  port: "",
  isActive: false,
});

// Reactive variable for instances
const instances = ref([]);

// Reactive variable for selected instance index
const selectedInstanceIndex = ref(null);

// Load instances from local storage on component mount
const loadInstancesFromLocalStorage = () => {
  const storedInstances = localStorage.getItem("instances");
  if (storedInstances) {
    instances.value = JSON.parse(storedInstances);
  }

  // Fetch the latest isActive state from local storage
  const storedSelectedIndex = localStorage.getItem("selectedInstanceIndex");
  if (storedSelectedIndex) {
    selectedInstanceIndex.value = parseInt(storedSelectedIndex);
  }
};
loadInstancesFromLocalStorage();

// Save instances to local storage whenever instances change
watch(
  instances,
  () => {
    localStorage.setItem("instances", JSON.stringify(instances.value));
    eventBus.$emit("instance-updated", true);
  },
  { deep: true }
);

// Watch for changes in selected instance index and update local storage
watch(selectedInstanceIndex, (newValue) => {
  localStorage.setItem("selectedInstanceIndex", newValue.toString());
});

// Function to add a new instance
const addInstance = () => {
  const isFirstInstance = instances.value.length === 0;
  const newInstanceData = { ...newInstance.value, isActive: isFirstInstance };
  instances.value.push(newInstanceData);

  // If it's the first instance, set selectedInstanceIndex to 0
  if (isFirstInstance) {
    selectedInstanceIndex.value = 0;
  }

  newInstance.value = {
    name: "",
    username: "",
    password: "",
    hostname: "",
    namespace: "",
    port: "",
    isActive: false,
  };
};

// Function to remove an instance
const removeInstance = (index) => {
  instances.value.splice(index, 1);
};

// Function to toggle isActive for selected instance
const toggleInstanceActive = (index) => {
  instances.value.forEach((instance, i) => {
    instance.isActive = i === index;
  });
};

// Function to get the instance URL
const getInstanceUrl = (instance) => {
  const { username, password, hostname, port, namespace } = instance;
  return `iris://${username}:${"*".repeat(
    password.length
  )}@${hostname}:${port}/${namespace}`;
};

watch(openai_apikey, (newValue) => {
  sessionStorage.setItem("openai_apikey", newValue);
});

watch(cohere_apikey, (newValue) => {
  sessionStorage.setItem("cohere_apikey", newValue);
});

onMounted(() => {
  const storedOpenaiApiKey = sessionStorage.getItem("openai_apikey");
  if (storedOpenaiApiKey) {
    openai_apikey.value = storedOpenaiApiKey;
  }

  const storedCohereApiKey = sessionStorage.getItem("cohere_apikey");
  if (storedCohereApiKey) {
    cohere_apikey.value = storedCohereApiKey;
  }
});
</script>
