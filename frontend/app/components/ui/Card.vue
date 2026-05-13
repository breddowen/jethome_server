<!-- ./frontend/app/components/ui/Card.vue -->
<script setup>
defineProps({
  title: String,
  subtitle: String,
})
</script>

<template>
  <div class="bg-white rounded-lg shadow-md overflow-hidden">
    <div v-if="title || subtitle" class="px-6 py-4 border-b border-gray-200">
      <h3 v-if="title" class="text-lg font-semibold text-gray-900">{{ title }}</h3>
      <p v-if="subtitle" class="text-sm text-gray-600 mt-1">{{ subtitle }}</p>
    </div>
    <div class="px-6 py-4">
      <slot />
    </div>
  </div>
</template>