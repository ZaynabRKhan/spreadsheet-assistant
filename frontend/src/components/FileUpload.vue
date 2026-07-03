<script setup>
function submitFile(event) {
  const files = event.target.files
  const formData = new FormData()
  for (let file of files) {
    formData.append('files', file)
  }
  fetch("http://localhost:8000/upload", {
  method: "POST",
  body: formData
})
  .then((res) => res.json())
  .then((data) => {
    alert("Files Uploaded successfully")
  })
  .catch((e) => {
    console.log("Error: "+e)
  })
}
</script>

<template>
  <div class="p-4 bg-white rounded-lg shadow-md w-[80vw] max-w-md mx-auto">
    <h2 class="font-bold text-blue-900 mb-4"> Upload CSV/ Excel Files</h2>
    <label class="block width-full cursor-pointer">
      <input type="file" @change="submitFile" class="block width-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full
      file:border-0 file:text-sm file:font-semibold file:bg-blue-500 file:text-white hover:file:bg-blue-600" multiple accept=".csv,.xlsx,.xls">
    </label>
  </div>
</template>