<template>
  <div class="w-2/3 justify-center items-center mx-auto">
    <form class="my-4 grid grid-cols-1 gap-y-4">
      <div>
        <label class="text-left block text-sm leading-6 text-gray-900">Airtable Token</label>
        <input type="password" v-model="airtableToken" autocomplete="off" placeholder="API Key"
          class="mt-1 focus:ring-indigo-500 text-sm focus:border-indigo-500 block w-full shadow-sm border-gray-300 rounded-md" />
      </div>
      <div>
        <label class="text-left block text-sm leading-6 text-gray-900">Base ID</label>
        <input type="text" v-model="baseId" autocomplete="off" placeholder="app..."
          class="mt-1 focus:ring-indigo-500 text-sm focus:border-indigo-500 block w-full shadow-sm border-gray-300 rounded-md" />
      </div>
      <div>
        <label class="text-left block text-sm leading-6 text-gray-900">Table ID</label>
        <input type="text" v-model="tableId" autocomplete="off" placeholder="tbl..."
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
      airtableToken: "",
      tableId: "",
      baseId: "",
    };
  },
  watch: {
    airtableToken(newValue, oldValue) {
      this.sendDataToParent();
    },
    tableId(newValue, oldValue) {
      this.sendDataToParent();
    },
    baseId(newValue, oldValue) {
      this.sendDataToParent();
    },
  },
  methods: {
    sendDataToParent() {
      eventBus.$emit("airtable-credentials", {
        airtableToken: this.airtableToken,
        tableId: this.tableId,
        baseId: this.baseId
      });
    },
  },
};
</script>
