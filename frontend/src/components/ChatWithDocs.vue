<template>
  <div>
    <div class="grid grid-cols-3">
      <div class="border border-gray-200 rounded-lg m-4">
        <div class="grid grid-rows-4 gap-4 m-4 py-4">
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
            <label for="modelName" class="text-left block text-sm font-normal leading-6 text-gray-900">Model
              Name</label>
            <input type="text" id="modelName" placeholder="text-embedding-3-large" v-model="model_name"
              class="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md" />
          </div>
          <!-- Embedding Dimension Input -->
          <div>
            <label for="embeddingDimension"
              class="text-left block text-sm font-normal leading-6 text-gray-900">Embedding Dimension</label>
            <input type="text" id="embeddingDimension" placeholder="3072" v-model="embedding_dimension"
              class="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md" />
          </div>
          <!-- Start Button -->
          <div class="mt-2">
            <button type="button"
              class="inline-flex items-center rounded-md bg-iscblue px-3 py-2 text-sm font-normal text-white shadow-sm"
              @click="makeChatActive()">
              Start
            </button>
          </div>
        </div>
      </div>
      <div v-if="this.activeInstance && isChatActive" class="m-4 col-span-2">
        <deep-chat style="
            border-radius: 0.5rem;
            border-width: 1px;
            border-style: solid;
            border-color: #f3f4f6;
            width: calc(40vw);
            height: calc(80vh - 70px);
            margin: 2rem;
            padding-top: 10px;
            font-family: Poppins, Inter, system-ui;
          " :textInput="{
            styles: {
              container: {
                width: '100%',
                margin: '0',
                border: 'unset',
                borderTop: '1px solid #e5e7eb',
                borderRadius: '0px',
                boxShadow: 'unset',
              },
              text: {
                fontSize: '1.05em',
                paddingTop: '11px',
                paddingBottom: '13px',
                paddingLeft: '12px',
                paddingRight: '2.4em',
              },
            },
            placeholder: {
              text: 'Type a message...',
              style: { color: '#bcbcbc' },
            },
          }" :submitButtonStyles="{
            submit: {
              container: {
                default: {
                  transform: 'scale(1.21)',
                  marginBottom: '-3px',
                  marginRight: '0.4em',
                },
              },
            },
          }" :messageStyles="{
            default: {
              shared: {
                bubble: {
                  padding: '0.5rem 1rem',
                },
              },
              user: {
                bubble: {
                  backgroundColor: '#363990',
                  textColor: 'ffffff',
                },
              },
            },
            loading: { bubble: { padding: '0.6em 0.75em 0.6em 1.3em' } },
          }" :initialMessages="initialMessages" :request="inputRequest"></deep-chat>
      </div>
    </div>
  </div>
</template>

<script>
import "deep-chat";
import axios from "axios";

export default {
  name: "App",
  data() {
    return {
      activeInstance: null,
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
      model_name: "",
      embedding_dimension: "",
      inputRequestData: {},
      isChatActive: false,
      initialMessages: [],
    };
  },
  mounted() {
    this.fetchTables();
  },
  watch: {
    selectedTable: {
      handler: "generateInputRequest",
      immediate: true,
    },
    selectedIndexingType: {
      handler: "generateInputRequest",
      immediate: true,
    },
    model_name: {
      handler: "generateInputRequest",
      immediate: true,
    },
    embedding_dimension: {
      handler: "generateInputRequest",
      immediate: true,
    },
  },
  computed: {
    inputRequest() {
      return {
        url: "/api/chat_engine",
        method: "POST",
        additionalBodyProps: {
          username: this.activeInstance.username,
          password: this.activeInstance.password,
          hostname: this.activeInstance.hostname,
          port: String(this.activeInstance.port),
          namespace: this.activeInstance.namespace,
          table_name: this.selectedTable,
          indexing_type: this.selectedIndexingType,
          model_name: this.model_name,
          embedding_dimension: this.embedding_dimension,
        },
        headers: {
          'api-key': sessionStorage.getItem(
            this.getStorageLabel(this.selectedIndexingType))
        },
      };
    },
  },
  methods: {
    getStorageLabel(value) {
      const type = this.indexingTypes.find((type) => type.value === value);
      return type ? type.storageLabel : null;
    },
    makeChatActive() {
      if (
        this.selectedTable &&
        this.selectedIndexingType &&
        this.model_name &&
        this.embedding_dimension
      ) {
        this.isChatActive = true;
      }
    },
    fetchTables() {
      const localData = JSON.parse(localStorage.getItem("instances"));
      const activeInstances = localData.filter((instance) => instance.isActive);
      this.activeInstance = activeInstances[0];

      if (this.activeInstance) {
        const { username, password, hostname, port, namespace } = this.activeInstance;

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
  },
};
</script>
