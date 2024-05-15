<template>
  <div>
    <div class="grid grid-cols-4 gap-4 mb-6">
      <!-- Table Name Select -->
      <div>
        <label for="indexingType" class="text-left block text-sm leading-6 text-gray-900">Table Name</label>
        <select id="indexingType" v-model="selectedTable"
          class="mt-1 border border-gray-300 w-full text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500">
          <option v-for="table in tables" :key="table">
            {{ table.replace("data_", "") }}
          </option>
        </select>
      </div>
      <!-- Indexing Type Select -->
      <div>
        <label for="indexingType" class="text-left block text-sm leading-6 text-gray-900">Indexing Type</label>
        <select id="indexingType" v-model="selectedIndexingType"
          class="mt-1 border border-gray-300 w-full text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500">
          <option v-for="(type, index) in indexingTypes" :value="type.value" :key="index">
            {{ type.label }}
          </option>
        </select>
      </div>
      <!-- Model Name Input -->
      <div>
        <label for="modelName" class="text-left block text-sm font-normal leading-6 text-gray-900">Model Name</label>
        <input type="text" id="modelName" placeholder="text-embedding-3-large" v-model="modelName"
          class="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md" />
      </div>
      <!-- Embedding Dimension Input -->
      <div>
        <label for="embeddingDimension" class="text-left block text-sm font-normal leading-6 text-gray-900">Embedding
          Dimension</label>
        <input type="text" id="embeddingDimension" placeholder="3072" v-model="embeddingDimension"
          class="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md" />
      </div>
    </div>

    <!-- Query Form -->
    <form @submit.prevent="submitQuery" class="mx-auto">
      <label for="default-search" class="mb-2 text-sm font-medium text-gray-900 sr-only dark:text-white">Search</label>
      <div class="relative">
        <div class="absolute inset-y-0 start-0 flex items-center ps-3 pointer-events-none">
          <svg class="w-4 h-4 text-gray-500 dark:text-gray-400" aria-hidden="true" xmlns="http://www.w3.org/2000/svg"
            fill="none" viewBox="0 0 20 20">
            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="m19 19-4-4m0-7A7 7 0 1 1 1 8a7 7 0 0 1 14 0Z" />
          </svg>
        </div>
        <input type="search" v-model="query" id="default-search"
          class="block w-full p-4 ps-10 text-sm text-gray-900 border border-gray-300 rounded-lg bg-white focus:ring-blue-500 focus:border-blue-500" />
        <button type="submit"
          class="text-white absolute end-2.5 bottom-2.5 bg-iscblue hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-4 py-2">
          Search
        </button>
      </div>
    </form>
    <!-- Result Box -->
    <div v-if="result && !isLoading" class="mt-4 pt-4 rounded-lg">
      <h2 class="text-left text-sm font-medium text-gray-400 pb-4">RESPONSE</h2>
      <p class="text-wrap text-gray-900 text-2xl">
        <span>{{ result }}</span>
      </p>
    </div>
    <div v-if="isLoading">
      <PageLoading />
    </div>
  </div>
</template>

<script>
import axios from "axios";
import PageLoading from "./PageLoading.vue";

export default {
  data() {
    return {
      tables: [],
      selectedTable: null,
      selectedIndexingType: "",
      searchTerm: "",
      indexingTypes: [
        {
          value: "openai_embeddings",
          label: "OpenAI Embeddings",
          storageLabel: "openai_apikey",
        },
        {
          value: "cohere_embeddings",
          label: "Cohere Embeddings",
          storageLabel: "cohere_apikey",
        },
      ],
      modelName: "",
      embeddingDimension: "",
      query: "",
      result: null,
      isLoading: false
    };
  },
  components: {
    PageLoading
  },
  mounted() {
    this.fetchTables();
  },
  methods: {
    getStorageLabel(value) {
      const type = this.indexingTypes.find((type) => type.value === value);
      return type ? type.storageLabel : null;
    },
    fetchTables() {
      const localData = JSON.parse(localStorage.getItem("instances"));
      const activeInstances = localData.filter((instance) => instance.isActive);
      const activeInstance = activeInstances[0];

      if (activeInstance) {
        const { username, password, hostname, port, namespace } = activeInstance;

        axios
          .get("api/tables", {
            params: {
              username,
              password,
              hostname,
              port: port.toString(),
              namespace,
            },
          })
          .then((response) => {
            this.tables = response.data.tables;
            this.selectedTable =
              this.tables.length > 0 ? this.tables[0].replace("data_", "") : null;
          })
          .catch((error) => {
            console.error("Error fetching tables:", error);
            alert(error.response.data.error)
          });
      }
    },
    submitQuery() {
      this.isLoading = true
      const localData = JSON.parse(localStorage.getItem("instances"));
      const activeInstances = localData.filter((instance) => instance.isActive);
      const activeInstance = activeInstances[0];

      const apiKeyValue = sessionStorage.getItem(
        this.getStorageLabel(this.selectedIndexingType)
      );

      if (activeInstance) {
        const { username, password, hostname, port, namespace } = activeInstance;
        axios
          .post("api/query_engine", {
            username,
            password,
            hostname,
            port: port.toString(),
            namespace,
            table_name: this.selectedTable,
            indexing_type: this.selectedIndexingType,
            model_name: this.modelName,
            embedding_dimension: this.embeddingDimension,
            query: this.query,
          }, {
            headers: {
              'api-key': apiKeyValue
            }
          })
          .then((response) => {
            this.result = response.data.result;
          })
          .catch((error) => {
            console.error("Error submitting query:", error);
            alert(error.response.data.error)
          })
          .finally(() => {
            this.isLoading = false;
          });
      }
    },
  },
};
</script>
