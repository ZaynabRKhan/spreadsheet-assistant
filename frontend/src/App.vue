<script setup>
import FileUpload from "./components/FileUpload.vue"
import ChatBox from "./components/ChatBox.vue"
</script>

<template>
  <section class="h-screen bg-linear-to-r from-cyan-500 to-blue-500 flex items-center justify-center px-4">
    <div class="bg-blue-300 shadow-2xl rounded-3xl w-full max-w-5xl h-[90vh] flex flex-col p-8 gap-4 overflow-hidden">
      <h1 class="text-3xl font-bold text-blue-900 text-center flex-shrink-0">Your Personal Business Assistant</h1>
      <div class="flex-shrink-0">
        <FileUpload />
      </div>
      <div class="flex-1 min-h-0 overflow-hidden">
        <ChatBox />
      </div>
    </div>
  </section>
</template>