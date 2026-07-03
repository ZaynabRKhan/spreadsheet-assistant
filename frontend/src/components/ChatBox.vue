<script setup>
import {ref, nextTick} from "vue"
const userInput = ref("")
const messages = ref([])
const chatContainer = ref(null)
async function sendMessage() {
  const message = userInput.value
  messages.value.push({"role": "User", "text": message})
  const typingPlaceholder = { role: "Agent", text: "__typing__" }
  messages.value.push(typingPlaceholder)
  await nextTick()
  scrolltoBottom()
  const res = await fetch("http://localhost:8000/chat", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ question: userInput.value })
  })
  const agentMessage = await res.json()
  const index = messages.value.indexOf(typingPlaceholder)
  if (index !== -1) {
    messages.value[index] = { "role": "Agent", "text": agentMessage.response }
  }
  await nextTick()
  scrolltoBottom()
  userInput.value = ""
}
function scrolltoBottom() {
  const el = chatContainer.value
  if (el) el.scrollTop = el.scrollHeight
}
</script>

<template>
  <div class="h-full flex flex-col p-4 bg-white rounded-lg shadow-lg"> 
    <h2 class="text-xl font-bold text-blue-900">Chat with your Data</h2>
    <!-- <div class="flex flex-col flex-1 bg-blue-200 rounded-lg shadow-inner overflow-hidden"> -->
      <div ref="chatContainer" class="flex flex-col flex-1 overflow-y-auto space-y-2 px-2 py-2 bg-blue-200 m-2 rounded-lg shadow-indigo-lg min-h-0">
        <div v-for="(msg, index) in messages" :key="index" :class="msg.role === 'User'? 'self-end bg-blue-100 text-blue-900' : 'self-start bg-gray-100 text-gray-900'" class="max-w-[70%] p-2 rounded-lg text-sm shadow-sm">
          <b class="block mb-1 text-xs text-gray-500">{{ msg.role }}:</b>
          <div v-if="msg.text === '__typing__'" class="flex space-x-1 p-1">
              <span class="w-2 h-2 bg-gray-500 rounded-full animate-bounce"></span>
              <span class="w-2 h-2 bg-gray-500 rounded-full animate-bounce [animation-delay:0.15s]"></span>
              <span class="w-2 h-2 bg-gray-500 rounded-full animate-bounce [animation-delay:0.3s]"></span>
            </div>
          <div v-else>
            {{ msg.text }}
          </div>
        </div>
      </div> 
      <!-- </div> -->
      <form @submit.prevent="sendMessage" class="mt-2 px-2">
        <input v-model="userInput" type="text" class="w-full border border-blue-500 px-3 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400" placeholder="Ask a question...">
      </form>
    </div>
</template>

