<!-- ./frontend/app/components/ui/Button.vue -->
<script setup>
defineProps({
  variant: {
    type: String,
    default: 'primary',
    validator: (value) => ['primary', 'secondary', 'danger'].includes(value)
  },
  disabled: Boolean,
  loading: Boolean,
})
</script>

<template>
  <button
    :class="[
      'px-4 py-2 rounded-lg font-medium transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed',
      variant === 'primary' && 'bg-blue-600 text-white hover:bg-blue-700',
      variant === 'secondary' && 'bg-gray-200 text-gray-900 hover:bg-gray-300',
      variant === 'danger' && 'bg-red-600 text-white hover:bg-red-700',
    ]"
    :disabled="disabled || loading"
  >
    <Icon v-if="loading" name="svg-spinners:ring-resize" class="inline-block mr-2" />
    <slot />
  </button>
</template>