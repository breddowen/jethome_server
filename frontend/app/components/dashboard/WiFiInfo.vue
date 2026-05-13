<!-- ./frontend/app/components/dashboard/WiFiInfo.vue -->
<script setup>
import { ref } from 'vue'

const props = defineProps({
  ssid: String,
  password: String,
  clients: Number,
  ipAddress: String,
})

const showPassword = ref(false)
const copied = ref(false)

const copyPassword = async () => {
  if (props.password) {
    await navigator.clipboard.writeText(props.password)
    copied.value = true
    setTimeout(() => {
      copied.value = false
    }, 2000)
  }
}
</script>

<template>
  <UiCard title="WiFi Hotspot" subtitle="Информация о точке доступа">
    <div class="space-y-4">
      <div class="flex items-center justify-between py-3 border-b border-gray-100">
        <div>
          <p class="text-sm text-gray-600">Название сети (SSID)</p>
          <p class="text-lg font-semibold text-gray-900 mt-1">{{ ssid }}</p>
        </div>
        <Icon name="mdi:wifi" class="w-8 h-8 text-blue-600" />
      </div>

      <div class="flex items-center justify-between py-3 border-b border-gray-100">
        <div class="flex-1">
          <p class="text-sm text-gray-600">Пароль</p>
          <div class="flex items-center mt-1 space-x-2">
            <p class="text-lg font-mono text-gray-900">
              {{ showPassword ? password : '••••••••' }}
            </p>
            <button
              @click="showPassword = !showPassword"
              class="text-gray-400 hover:text-gray-600"
            >
              <Icon
                :name="showPassword ? 'mdi:eye-off' : 'mdi:eye'"
                class="w-5 h-5"
              />
            </button>
            <button
              @click="copyPassword"
              class="text-gray-400 hover:text-gray-600"
            >
              <Icon
                :name="copied ? 'mdi:check' : 'mdi:content-copy'"
                class="w-5 h-5"
              />
            </button>
          </div>
        </div>
      </div>

      <div class="flex items-center justify-between py-3 border-b border-gray-100">
        <div>
          <p class="text-sm text-gray-600">IP адрес роутера</p>
          <p class="text-lg font-mono text-gray-900 mt-1">{{ ipAddress }}</p>
        </div>
      </div>

      <div class="flex items-center justify-between py-3">
        <div>
          <p class="text-sm text-gray-600">Подключено устройств</p>
          <p class="text-2xl font-bold text-gray-900 mt-1">{{ clients }}</p>
        </div>
        <Icon name="mdi:devices" class="w-8 h-8 text-green-600" />
      </div>
    </div>
  </UiCard>
</template>