<template>
  <div class="w-full">
    <img class="mb-8" src="../assets/pipeline.png" alt="Flow Chart" />
    <div class="w-4/5 justify-center items-center mx-auto" id="accordion-collapse" data-accordion="collapse">
      <div v-for="(item, index) in accordionItems" :key="index" class="accordion">
        <h2 :id="'accordion-collapse-heading-' + index">
          <button type="button"
            class="flex items-center justify-between w-full p-5 font-medium rtl:text-right text-gray-500 border border-gray-100 focus:ring-4 focus:ring-gray-200 dark:focus:ring-gray-800 dark:border-gray-700 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 gap-3"
            @click="toggleAccordion(index)" :aria-expanded="item.isOpen ? 'true' : 'false'"
            :aria-controls="'accordion-collapse-body-' + index">
            <span>{{ item.question }}</span>
            <svg data-accordion-icon class="w-3 h-3 rotate-180 shrink-0" aria-hidden="true"
              xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 10 6">
              <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M9 5 5 1 1 5" />
            </svg>
          </button>
        </h2>
        <div :id="'accordion-collapse-body-' + index" class="accordion-content" :class="{ 'hidden': !item.isOpen }"
          :aria-labelledby="'accordion-collapse-heading-' + index">
          <div class="p-5 border border-gray-100 dark:border-gray-700 dark:bg-gray-900">
            <p class="mb-2 text-gray-500 dark:text-gray-400">{{ item.answer }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      accordionItems: [
        {
          question: "What is IRIS AI Studio?",
          answer: "An open source application that lets you explore the capabilities of vector embeddings in InterSystems IRIS DB. It has two major modules, Connectors let load data from files as vector embeddings into IRIS DB & Playground let users explore different retrieval channels on the vector embeddings reside in IRIS DB.",
          isOpen: true
        },
        {
          question: "How do I use this application?",
          answer: "Firstly go to settings and add the IRIS DB credentials and API keys. Secondly on connectors page, you can either load the sample data or your own data from preferred source. Finally, you could go to playground and retrive the information through various channels.",
          isOpen: false
        },
        {
          question: "Where could I see the embeddings?",
          answer: "You may connect to your IRIS DB through DBeaver client or SQL editor and query the table where the data was loaded to. Please note, you have to append 'data_' prefix to the table name and the tables created through this platform would be on 'SQLUser' schema.",
          isOpen: false
        },
        {
          question: "What is 'missing required parameters' error?",
          answer: "The OpenAI / Cohere API Keys are saved only to browser's session storage which makes it prone to get deleted when the session ends (browser tab getting closed). Mostly this will be the reason for this error, otherwise check the other input parameters asked in the page.",
          isOpen: false
        },
        {
          question: "What kind of files I could embed as vectors in IRIS DB?",
          answer: "Plain text files (.txt) and CSV are two formats that are tested to work seamlessly.",
          isOpen: false
        },
        {
          question: "How could I use this in my organization?",
          answer: "The goal of this application is to let existing or new IRIS DB users to explore the vector capabilities it offer. If you are planning to try out with your own sensitive information, then it's suggested you host the application on your preferred cloud provider for data security reasons.",
          isOpen: false
        },
        {
          question: "How can I raise any issues/bugs in the application?",
          answer: "You may click on the Github icon on the right top corner of the application, go to the issues section and add the issue/bug that you've faced with steps to replicate.",
          isOpen: false
        }
      ]
    };
  },
  methods: {
    toggleAccordion(index) {
      this.accordionItems.forEach((item, i) => {
        if (i === index) {
          item.isOpen = !item.isOpen;
        } else {
          item.isOpen = false;
        }
      });
    }
  }
};
</script>

<style>
/* Add your custom styles for accordion here */
</style>
