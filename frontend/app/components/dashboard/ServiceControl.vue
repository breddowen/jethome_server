<!-- ./frontend/app/components/dashboard/ServiceControl.vue -->
<script setup>
const props = defineProps({
  title: String,
  description: String,
  icon: String,
  enabled: Boolean,
  loading: Boolean,
  status: String,
})

const emit = defineEmits(['toggle'])

const statusColor = computed(() => {
  if (props.status === 'enabled') return 'text-green-600'
  if (props.status === 'disabled') return 'text-gray-600'
  return 'text-yellow-600'
})

const statusText = computed(() => {
  if (props.status === 'enabled') return 'Активен'
  if (props.status === 'disabled') return 'Выключен'
  return 'Неизвестно'
})
</script>

<template>
  <UiCard>
    <div class="flex items-center justify-between">
      <div class="flex items-start space-x-4">
        <div class="p-3 bg-blue-100 rounded-lg">
          <Icon :name="icon" class="w-6 h-6 text-blue-600" />
        </div>
        <div>
          <h4 class="text-lg font-semibold text-gray-900">{{ title }}</h4>
          <p class="text-sm text-gray-600 mt-1">{{ description }}</p>
          <p class="text-sm mt-2" :class="statusColor">
            Статус: {{ statusText }}
          </p>
        </div>
      </div>
      <div class="flex items-center space-x-3">
        <Icon
          v-if="loading"
          name="svg-spinners:ring-resize"
          class="w-5 h-5 text-blue-600"
        />
        <UiToggle
          :model-value="enabled"
          :disabled="loading"
          :label="title"
          @update:model-value="emit('toggle', $event)"
        />
      </div>
    </div>
  </UiCard>
</template>