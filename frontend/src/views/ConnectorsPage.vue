<template>
  <div class="flex flex-col items-center mx-auto text-center">
    <div v-if="!showLoadData">
      <div v-if="imageLoaded">
        <h1 class="text-4xl font-normal">Create your connector</h1>
        <h1>
          <small class="text-sm mt-2 font-normal text-gray-500"
            >Lets bring data from external source into IRIS database</small
          >
        </h1>
      </div>

      <img
        @load="imageLoaded = true"
        class="max-w-3xl"
        src="../assets/connectors.png"
        alt="Flow Chart"
      />
      <div v-if="imageLoaded">
        <button
          type="button"
          class="inline-flex items-center rounded-md bg-iscblue px-3 py-2 text-sm font-normal text-white shadow-sm"
          @click="showLoadData = true"
        >
          <PlusIcon class="ml-0.5 mr-1.5 h-5 w-5" aria-hidden="true" />
          Connector
        </button>
      </div>
    </div>
    <div v-else>
      <LoadData />
    </div>
  </div>
</template>
<script setup>
import { ref } from "vue";
import { PlusIcon } from "@heroicons/vue/20/solid";
import LoadData from "../components/LoadData.vue";

const showLoadData = ref(false);
const imageLoaded = ref(false);
</script>
