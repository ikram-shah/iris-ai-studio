<template>
  <div>
    <aside class="fixed top-16 left-0 z-40 w-64 h-screen" aria-label="Sidebar">
      <div class="h-full px-2 py-8 bg-white border-r border-gray-200">
        <div class="mx-2 mt-2 mb-4">
          <span
            class="bg-iscgreen text-white text-xs font-medium me-2 px-2.5 py-0.5 rounded"
            >TEXT</span
          >
        </div>
        <ul>
          <li
            class="hover:cursor-pointer hover:bg-transparent hover:text-iscblue"
            @click="activePage = 'semantic-search'"
          >
            <div class="flex items-center p-3" v-if="activePage !== 'semantic-search'">
              <MagnifyingGlassIcon class="ml-0.5 h-6 w-6" />
              <span class="ms-3 font-normal">Semantic Search</span>
            </div>
            <div class="flex items-center p-3" v-else>
              <MagnifyingGlassIcon class="stroke-2 ml-0.5 h-6 w-6" />
              <span class="ms-3 text-iscblue text-base font-medium">Semantic Search</span>
            </div>
          </li>
          <hr class="my-2 border-gray-100" />
          <li
            class="hover:cursor-pointer hover:bg-transparent hover:text-iscblue"
            @click="activePage = 'chat-with-docs'"
          >
            <div class="flex items-center p-3" v-if="activePage !== 'chat-with-docs'">
              <ChatBubbleOvalLeftEllipsisIcon class="ml-0.5 h-6 w-6" />
              <span class="ms-3 font-normal">Chat with Docs</span>
            </div>
            <div class="flex items-center p-3" v-else>
              <ChatBubbleOvalLeftEllipsisIcon class="stroke-2 ml-0.5 h-6 w-6" />
              <span class="ms-3 text-iscblue text-base font-medium">Chat with Docs</span>
            </div>
          </li>
          <hr class="my-2 border-gray-100" />
          <li
            class="hover:cursor-pointer hover:bg-transparent hover:text-iscblue"
            @click="activePage = 'text-content-recommender'"
          >
            <div
              class="flex items-center p-3"
              v-if="activePage !== 'text-content-recommender'"
            >
              <RectangleStackIcon class="ml-0.5 h-6 w-6" />
              <span class="ms-3 font-normal">Recommender</span>
            </div>
            <div class="flex items-center p-3" v-else>
              <RectangleStackIcon class="stroke-2 ml-0.5 h-6 w-6" />
              <span class="ms-3 text-iscblue text-base font-medium">Recommender</span>
            </div>
          </li>
          <hr class="my-2 border-gray-100" />
          <li
            class="hover:cursor-pointer hover:bg-transparent hover:text-iscblue"
            @click="activePage = 'text-similarity'"
          >
            <div class="flex items-center p-3" v-if="activePage !== 'text-similarity'">
              <RectangleGroupIcon class="ml-0.5 h-6 w-6" />
              <span class="ms-3 font-normal">Similarity</span>
            </div>
            <div class="flex items-center p-3" v-else>
              <RectangleGroupIcon class="stroke-2 ml-0.5 h-6 w-6" />
              <span class="ms-3 text-iscblue text-base font-medium">Similarity</span>
            </div>
          </li>
        </ul>
        <div class="mx-2 mt-6 mb-4">
          <span
            class="bg-iscgreen text-white text-xs font-medium me-2 px-2.5 py-0.5 rounded dark:bg-gray-700 dark:text-gray-300"
            >IMAGE</span
          >
        </div>
        <ul>
          <li
            class="hover:cursor-pointer hover:bg-transparent hover:text-iscblue"
            @click="activePage = 'image-content-recommender'"
          >
            <div
              class="flex items-center p-3"
              v-if="activePage !== 'image-content-recommender'"
            >
              <RectangleStackIcon class="ml-0.5 h-6 w-6" />
              <span class="ms-3 font-normal">Recommender</span>
            </div>
            <div class="flex items-center p-3" v-else>
              <RectangleStackIcon class="stroke-2 ml-0.5 h-6 w-6" />
              <span class="ms-3 text-iscblue text-base font-medium">Recommender</span>
            </div>
          </li>
          <hr class="my-2 border-gray-100" />
          <li
            class="hover:cursor-pointer hover:bg-transparent hover:text-iscblue"
            @click="activePage = 'image-similarity'"
          >
            <div class="flex items-center p-3" v-if="activePage !== 'image-similarity'">
              <RectangleGroupIcon class="ml-0.5 h-6 w-6" />
              <span class="ms-3 font-normal">Similarity</span>
            </div>
            <div class="flex items-center p-3" v-else>
              <RectangleGroupIcon class="stroke-2 ml-0.5 h-6 w-6" />
              <span class="ms-3 text-iscblue text-base font-medium">Similarity</span>
            </div>
          </li>
          <hr class="my-2 border-gray-100" />
        </ul>
      </div>
    </aside>
    <div class="mx-auto items-center justify-center ml-48">
      <SemanticSearch v-if="activePage == 'semantic-search'" />
      <ChatWithDocs v-if="activePage == 'chat-with-docs'" />
      <TextContentRecommender v-if="activePage == 'text-content-recommender'" />
      <ImageContentRecommender v-if="activePage == 'image-content-recommender'" />
      <TextSimilarity v-if="activePage == 'text-similarity'" />
      <ImageSimilarity v-if="activePage == 'image-similarity'" />
    </div>
  </div>
</template>

<script setup>
import { RectangleGroupIcon } from "@heroicons/vue/24/outline";
import { MagnifyingGlassIcon } from "@heroicons/vue/24/outline";
import { ChatBubbleOvalLeftEllipsisIcon } from "@heroicons/vue/24/outline";
import { RectangleStackIcon } from "@heroicons/vue/24/outline";
import { PhotoIcon } from "@heroicons/vue/24/outline";

import SemanticSearch from "../components/SemanticSearch.vue";
import ChatWithDocs from "../components/ChatWithDocs.vue";
import TextContentRecommender from "../components/TextContentRecommender.vue";
import ImageContentRecommender from "../components/ImageContentRecommender.vue";
import TextSimilarity from "../components/TextSimilarity.vue";
import ImageSimilarity from "../components/ImageSimilarity.vue";

import { ref } from "vue";

const activePage = ref("semantic-search");
</script>
