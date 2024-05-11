<template>
  <div class="w-2/3 justify-center items-center mx-auto">
    <form class="my-4 grid grid-cols-1 gap-y-4">
      <div>
        <label class="text-left block text-sm leading-6 text-gray-900"
          >Client ID</label
        >
        <input
          type="password"
          v-model="awsS3ClientId"
          autocomplete="off"
          placeholder="AWS S3 client ID"
          class="mt-1 focus:ring-indigo-500 text-sm focus:border-indigo-500 block w-full shadow-sm border-gray-300 rounded-md"
        />
      </div>
      <div>
        <label class="text-left block text-sm leading-6 text-gray-900"
          >Client Secret</label
        >
        <input
          type="password"
          v-model="awsS3ClientSecret"
          autocomplete="off"
          placeholder="AWS S3 client secret"
          class="mt-1 focus:ring-indigo-500 text-sm focus:border-indigo-500 block w-full shadow-sm border-gray-300 rounded-md"
        />
      </div>
      <div>
        <label class="text-left block text-sm leading-6 text-gray-900"
          >Bucket Name</label
        >
        <input
          type="text"
          v-model="awsS3BucketName"
          placeholder="Include folder path too"
          class="mt-1 focus:ring-indigo-500 text-sm focus:border-indigo-500 block w-full shadow-sm border-gray-300 rounded-md"
        />
      </div>
    </form>
  </div>
</template>

<script>
import eventBus from "../../utils/EventBus.js";

export default {
  data() {
    return {
      awsS3ClientId: "",
      awsS3ClientSecret: "",
      awsS3BucketName: "",
    };
  },
  watch: {
    awsS3ClientId(newValue, oldValue) {
      this.sendDataToParent();
    },
    awsS3ClientSecret(newValue, oldValue) {
      this.sendDataToParent();
    },
    awsS3BucketName(newValue, oldValue) {
      this.sendDataToParent();
    },
  },
  methods: {
    sendDataToParent() {
      eventBus.$emit("aws-credentials", {
        awsS3ClientId: this.awsS3ClientId,
        awsS3ClientSecret: this.awsS3ClientSecret,
        awsS3BucketName: this.awsS3BucketName,
      });
    },
  },
};
</script>
