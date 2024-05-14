<template>
  <div>
    <div class="border border-2 rounded-lg border-gray-200 px-2 py-0.5">
      <ol
        class="px-8 py-4 flex items-center w-full space-x-6 text-base font-normal text-center text-gray-700 rtl:space-x-reverse">
        <li :class="{
          'text-iscblue': currentPage == 1,
          'flex items-center': true,
        }">
          <span :class="{
            'bg-iscblue border-iscblue text-white': currentPage == 1,
            'flex items-center justify-center w-6 h-6 me-3 text-xs border border-gray-500 rounded-full shrink-0': true,
          }">1</span>
          Load Data
          <ChevronDoubleRightIcon class="stroke-2 ml-4 h-4 w-4" />
        </li>
        <li :class="{
          'text-iscblue': currentPage == 2,
          'flex items-center': true,
        }">
          <span :class="{
            'bg-iscblue border-iscblue text-white': currentPage == 2,
            'flex items-center justify-center w-6 h-6 me-3 text-xs border border-gray-500 rounded-full shrink-0': true,
          }">2</span>
          Configure
          <ChevronDoubleRightIcon class="stroke-2 ml-4 h-4 w-4" />
        </li>
        <li :class="{
          'text-iscblue': currentPage == 3,
          'flex items-center': true,
        }">
          <span :class="{
            'bg-iscblue border-iscblue text-white': currentPage == 3,
            'flex items-center justify-center w-6 h-6 me-3 text-xs border border-gray-500 rounded-full shrink-0': true,
          }">3</span>
          Insert to IRIS
        </li>
      </ol>
    </div>

    <div class="flex flex-col items-center justify-center w-full mt-6">
      <div id="page1">
        <section>
          <div class="mt-4 mx-auto">
            <div class="mx-auto text-center mb-8">
              <h2 class="mb-4 text-base tracking-tight font-medium text-iscblue">
                Choose Data Source
              </h2>
            </div>
            <div class="grid gap-6 grid-cols-2">
              <article v-for="(option, index) in dataSourceOptions" :key="index" :class="{
                'p-6 rounded-lg border-b-8 shadow-md cursor-pointer hover:border-b-iscblue': true,
                'border-iscblue': option.value === selectedDataSource,
              }" @click="selectDataSource(option.value)">
                <div class="flex items-center justify-left mx-auto">
                  <img class="h-12 w-12 rounded-md mr-6" :src="option.icon" v-if="option.icon" alt="Icon" />
                  <p>{{ option.label }}</p>
                </div>
              </article>
            </div>
          </div>
          <div class="mt-8">
            <div>
              <component :is="selectedDataSourceComponent">
                <template v-if="selectedDataSource.value === 'local'">
                  <LocalFile />
                </template>
                <template v-else-if="selectedDataSource.value === 'aws_s3'">
                  <AWSS3 />
                </template>
                <template v-else-if="selectedDataSource.value === 'airtable'">
                  <Airtable />
                </template>
                <template v-else-if="selectedDataSource.value === 'azure'">
                  <AzureStorage />
                </template>
              </component>
            </div>
          </div>
        </section>
      </div>

      <div id="page2" class="w-1/2 text-left">
        <section class="my-4 grid grid-cols-1 gap-y-4">
          <div class="mx-auto text-center">
            <h2 class="mb-4 text-base tracking-tight font-medium text-iscblue">
              Configure for Embeddings
            </h2>
          </div>
          <div>
            <label for="indexingType" class="text-left block text-sm leading-6 text-gray-900">Indexing Type</label>
            <select id="indexingType" v-model="formData.indexing_type"
              class="mt-1 border border-gray-300 w-full text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500">
              <option v-for="(type, index) in indexingTypes" :value="type.value" :key="index">
                {{ type.label }}
              </option>
            </select>
          </div>
          <div>
            <label for="modelName" class="text-left block text-sm leading-6 text-gray-900">Model Name</label>
            <input type="text" id="modelName" v-model="formData.model_name" placeholder="text-embedding-3-large"
              class="mt-1 focus:ring-indigo-500 text-sm focus:border-indigo-500 block w-full shadow-sm border-gray-300 rounded-md" />
          </div>
          <div>
            <label for="dimension" class="text-left block text-sm leading-6 text-gray-900">Dimension</label>
            <input type="text" id="dimension" v-model="formData.embedding_dimension" placeholder="3072"
              class="mt-1 focus:ring-indigo-500 text-sm focus:border-indigo-500 block w-full shadow-sm border-gray-300 rounded-md" />
          </div>
          <div>
            <label for="irisTableName" class="text-left block text-sm leading-6 text-gray-900">IRIS Table Name</label>
            <input type="text" id="irisTableName" v-model="formData.table_name" placeholder="data_table"
              class="mt-1 focus:ring-indigo-500 text-sm focus:border-indigo-500 block w-full shadow-sm border-gray-300 rounded-md" />
          </div>
          <p class="text-xs text-gray-400">
            Upon clicking next, the data will be vectorized and loaded into IRIS DB
            instance.
          </p>
        </section>
      </div>

      <div id="page3" class="w-full hidden">
        <div>
          <h2 v-if="uploadStatus == 'success'">Successfully Loaded data into IRIS</h2>
          <h2 v-else-if="uploadStatus == 'failed'">
            Loading Failed. Error message - {{ errorNote }}
          </h2>
          <PageLoading v-else />
        </div>
      </div>
    </div>

    <div class="flex justify-between mt-6">
      <div>
        <button id="prevBtn" type="button"
          class="inline-flex items-center rounded-md bg-gray-100 px-3 py-2 text-sm font-normal text-iscblue shadow-sm">
          < Previous </button>
      </div>
      <div>
        <button id="nextBtn" type="button"
          class="inline-flex items-center rounded-md bg-iscblue px-3 py-2 text-sm font-normal text-white shadow-sm">
          Next >
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from "axios";
import eventBus from "../utils/EventBus.js";
import { ref, computed, onMounted, onUnmounted } from "vue";
import LocalFile from "./UploadOptions/LocalFile.vue";
import AWSS3 from "./UploadOptions/AWSS3.vue";
import AzureStorage from "./UploadOptions/AzureStorage.vue";
import Airtable from "./UploadOptions/Airtable.vue";
import { ChevronDoubleRightIcon } from "@heroicons/vue/24/outline";

import folderIcon from "../assets/folder_icon.png";
import awsIcon from "../assets/aws_s3_icon.png";
import azureIcon from "../assets/azure_icon.png";
import airtableIcon from "../assets/airtable_icon.png";

import PageLoading from "./PageLoading.vue";

let uploadStatus = ref(null);
let errorNote = ref(null);

const currentPage = ref(1);
const selectedDataSource = ref(null);

const indexingTypes = [
  {
    value: "openai_embeddings",
    label: "OpenAI Embeddings",
    storageLabel: "openai_apikey",
  },
  { value: "cohere_embeddings", label: "Cohere Embeddings", storageLabel: "cohere_apikey" },
];

function getStorageLabel(value) {
  const type = indexingTypes.find((type) => type.value === value);
  return type ? type.storageLabel : null;
}

// Event Bus
let localFiles = ref([]);
const formData = ref({
  username: "",
  password: "",
  hostname: "",
  port: "",
  namespace: "",
  table_name: "",
  load_type: "",
  indexing_type: indexingTypes[0].value,
  model_name: "",
});

let awsCredentials = ref({});
let airtableCredentials = ref({});
let azureCredentials = ref({});

const filesData = (data) => {
  Array.from(data).map((file) => localFiles.value.push(file));
};

const awsCredentialsData = (data) => {
  awsCredentials = data;
};

const airtableCredentialsData = (data) => {
  airtableCredentials = data;
};

const azureCredentialsData = (data) => {
  azureCredentials = data;
};

const SendDataToService = (page) => {
  if (page === 3) {
    const localData = JSON.parse(localStorage.getItem("instances"));
    const activeInstances = localData.filter((instance) => instance.isActive);
    const activeInstance = activeInstances[0];

    if (selectedDataSource.value === "local") {
      formData.value.username = activeInstance.username;
      formData.value.password = activeInstance.password;
      formData.value.hostname = activeInstance.hostname;
      formData.value.port = activeInstance.port.toString();
      formData.value.namespace = activeInstance.namespace;
      formData.value.load_type = selectedDataSource.value;
      uploadData(formData);
    } else if (selectedDataSource.value === "aws_s3") {
      formData.value.username = activeInstance.username;
      formData.value.password = activeInstance.password;
      formData.value.hostname = activeInstance.hostname;
      formData.value.port = activeInstance.port.toString();
      formData.value.namespace = activeInstance.namespace;
      formData.value.load_type = selectedDataSource.value;
      formData.value.aws_access_key = awsCredentials.awsS3ClientId;
      formData.value.aws_secret = awsCredentials.awsS3ClientSecret;
      formData.value.aws_bucket_name = awsCredentials.awsS3BucketName;
      uploadData(formData);
    } else if (selectedDataSource.value === "airtable") {
      formData.value.username = activeInstance.username;
      formData.value.password = activeInstance.password;
      formData.value.hostname = activeInstance.hostname;
      formData.value.port = activeInstance.port.toString();
      formData.value.namespace = activeInstance.namespace;
      formData.value.load_type = selectedDataSource.value;
      formData.value.airtable_token = airtableCredentials.airtableToken;
      formData.value.table_id = airtableCredentials.tableId;
      formData.value.base_id = airtableCredentials.baseId;
      uploadData(formData);
    }
    else if (selectedDataSource.value === "azure") {
      formData.value.username = activeInstance.username;
      formData.value.password = activeInstance.password;
      formData.value.hostname = activeInstance.hostname;
      formData.value.port = activeInstance.port.toString();
      formData.value.namespace = activeInstance.namespace;
      formData.value.load_type = selectedDataSource.value;
      formData.value.container_name = azureCredentials.azureContainerName;
      formData.value.connection_string = azureCredentials.azureConnectionString;
      uploadData(formData);
    }
  }
};

const uploadData = async (formDataValue) => {
  try {
    const formDataToSend = new FormData();
    Object.entries(formDataValue.value).forEach(([key, value]) => {
      formDataToSend.append(key, value);
    });

    localFiles.value.forEach(function (file) {
      formDataToSend.append("files", file);
    });

    const apiKeyValue = sessionStorage.getItem(
      getStorageLabel(formDataValue.value.indexing_type)
    );

    const response = await axios.post(`api/upload_data`, formDataToSend, {
      headers: {
        "Content-Type": "multipart/form-data",
        "api-key": apiKeyValue,
      },
    });
    uploadStatus.value = "success";
  } catch (error) {
    uploadStatus.value = "failed";
    errorNote.value = error;
    console.error("Error uploading data:", error);
  }
};

onMounted(() => {
  eventBus.$on("files-data", filesData);
  eventBus.$on("aws-credentials", awsCredentialsData);
  eventBus.$on("airtable-credentials", airtableCredentialsData);
  eventBus.$on("azure-credentials", azureCredentialsData);
});

onUnmounted(() => {
  eventBus.$off("files-data", filesData);
  eventBus.$off("aws-credentials", awsCredentialsData);
  eventBus.$off("airtable-credentials", airtableCredentialsData);
  eventBus.$off("azure-credentials", azureCredentialsData);
});

const dataSourceOptions = [
  {
    label: "Local Storage",
    value: "local",
    icon: folderIcon,
  },
  { label: "AWS S3", value: "aws_s3", icon: awsIcon },
  { label: "Airtable", value: "airtable", icon: airtableIcon },
  { label: "Azure Blob Storage", value: "azure", icon: azureIcon },
];

const selectedDataSourceComponent = computed(() => {
  switch (selectedDataSource.value) {
    case "local":
      return LocalFile;
    case "aws_s3":
      return AWSS3;
    case "airtable":
      return Airtable;
    case "azure":
      return AzureStorage;
    default:
      return null;
  }
});

const selectDataSource = (dataSource) => {
  selectedDataSource.value = dataSource;
};

const showPage = (n) => {
  const pages = document.querySelectorAll('[id^="page"]');
  pages.forEach((page, index) => {
    page.classList.add("hidden");
  });
  document.getElementById(`page${n}`).classList.remove("hidden");

  if (n === 1 || n === 3) {
    document.getElementById("prevBtn").classList.add("hidden");
  } else {
    document.getElementById("prevBtn").classList.remove("hidden");
  }

  if (n === pages.length) {
    document.getElementById("nextBtn").classList.add("hidden");
  } else {
    document.getElementById("nextBtn").classList.remove("hidden");
  }

  currentPage.value = n;
};

onMounted(() => {
  showPage(1);
  const prevBtn = document.getElementById("prevBtn");
  const nextBtn = document.getElementById("nextBtn");

  prevBtn.addEventListener("click", () => {
    showPage(currentPage.value - 1);
  });

  nextBtn.addEventListener("click", () => {
    showPage(currentPage.value + 1);
    SendDataToService(currentPage.value);
  });
});
</script>
