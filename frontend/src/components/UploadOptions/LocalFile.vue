<template>
  <div>
    <div class="flex items-center justify-center w-full">
      <label for="dropzone-file"
        class="flex flex-col items-center justify-center w-full h-64 border-2 border-gray-300 border-dashed rounded-lg cursor-pointer bg-gray-50">
        <div class="flex flex-col items-center justify-center pt-5 pb-6">
          <svg class="w-8 h-8 mb-4 text-gray-500" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none"
            viewBox="0 0 20 16">
            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M13 13h3a3 3 0 0 0 0-6h-.025A5.56 5.56 0 0 0 16 6.5 5.5 5.5 0 0 0 5.207 5.021C5.137 5.017 5.071 5 5 5a4 4 0 0 0 0 8h2.167M10 15V6m0 0L8 8m2-2 2 2" />
          </svg>
          <p class="mb-2 text-sm text-gray-500">
            <span class="font-normal">Click to upload</span> or drag and drop
          </p>
          <p class="text-xs text-gray-500" v-if="allowedFileTypes.length">{{ allowedFileTypes.join(', ') }} (max {{
            maxFileLimit }} files)</p>
        </div>
        <input ref="fileInput" id="dropzone-file" type="file" class="hidden" @change="handleFileUpload" multiple
          accept=".txt,.csv" />
      </label>
    </div>
    <div v-if="uploadedFiles.length > 0" class="mt-4">
      <div v-for="file in uploadedFiles" :key="file.id" class="mb-2 flex items-center justify-between">
        <div>{{ file.name }} ({{ file.size }} KB)</div>
        <button @click="deleteFile(file.id)" class="text-red-500 hover:text-red-700 focus:outline-none">
          <svg class="w-4 h-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from "vue";
import eventBus from "../../utils/EventBus.js";

export default {
  data() {
    return {
      uploadedFiles: [],
      fileInput: null,
      allowedFileTypes: [".txt", ".csv"],
      maxFileLimit: 10
    };
  },
  methods: {
    deleteFile(id) {
      this.uploadedFiles = this.uploadedFiles.filter((file) => file.id !== id);
    },
    handleFileUpload(event) {
      const files = event.target.files;

      // Check if the number of uploaded files exceeds the maximum limit
      if (files.length > this.maxFileLimit) {
        alert("Exceeded maximum file limit (10)");
        return;
      }

      // Check if each file is of an allowed file type
      const invalidFiles = Array.from(files).filter(file => {
        const extension = file.name.split(".").pop();
        return !this.allowedFileTypes.includes("." + extension.toLowerCase());
      });

      if (invalidFiles.length > 0) {
        alert("Invalid file types. Allowed file types are: " + this.allowedFileTypes.join(", "));
        return;
      }

      this.uploadedFiles = Array.from(files).map((file) => ({
        id: file.lastModified,
        name: file.name,
        size: (file.size / 1024).toFixed(2),
      }));
      eventBus.$emit("files-data", event.target.files);
    },

  },
};
</script>
