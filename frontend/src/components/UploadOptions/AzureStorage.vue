<template>
  <div class="w-2/3 justify-center items-center mx-auto">
    <form class="my-4 grid grid-cols-1 gap-y-4">
      <div>
        <label class="text-left block text-sm leading-6 text-gray-900">Container Name</label>
        <input type="text" v-model="azureContainerName" autocomplete="off" placeholder="Blob Storage Container Name"
          class="mt-1 focus:ring-indigo-500 text-sm focus:border-indigo-500 block w-full shadow-sm border-gray-300 rounded-md" />
      </div>
      <div>
        <label class="text-left block text-sm leading-6 text-gray-900">Connection String</label>
        <input type="password" v-model="azureConnectionString" autocomplete="off"
          placeholder="Blob Storage Connection String"
          class="mt-1 focus:ring-indigo-500 text-sm focus:border-indigo-500 block w-full shadow-sm border-gray-300 rounded-md" />
      </div>
    </form>
  </div>
</template>

<script>
import eventBus from "../../utils/EventBus.js";

export default {
  data() {
    return {
      azureContainerName: "",
      azureConnectionString: "",
    };
  },
  watch: {
    azureContainerName(newValue, oldValue) {
      this.sendDataToParent();
    },
    azureConnectionString(newValue, oldValue) {
      this.sendDataToParent();
    },
  },
  methods: {
    sendDataToParent() {
      eventBus.$emit("azure-credentials", {
        azureContainerName: this.azureContainerName,
        azureConnectionString: this.azureConnectionString
      });
    },
  },
};
</script>
