<!-- ./frontend/app/components/ui/StatCard.vue -->
<script setup>
defineProps({
  title: String,
  value: [String, Number],
  icon: String,
  color: {
    type: String,
    default: 'blue'
  }
})
</script>

<template>
  <div class="bg-white rounded-lg shadow-md p-6">
    <div class="flex items-center justify-between">
      <div>
        <p class="text-sm text-gray-600">{{ title }}</p>
        <p class="text-2xl font-bold text-gray-900 mt-1">{{ value }}</p>
      </div>
      <div
        :class="[
          'p-3 rounded-full',
          color === 'blue' && 'bg-blue-100',
          color === 'green' && 'bg-green-100',
          color === 'orange' && 'bg-orange-100',
        ]"
      >
        <Icon
          :name="icon"
          :class="[
            'w-6 h-6',
            color === 'blue' && 'text-blue-600',
            color === 'green' && 'text-green-600',
            color === 'orange' && 'text-orange-600',
          ]"
        />
      </div>
    </div>
  </div>
</template>