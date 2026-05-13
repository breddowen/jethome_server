<!-- ./frontend/app/components/dashboard/LogsTable.vue -->
<script setup>
defineProps({
  logs: {
    type: Array,
    default: () => []
  }
})

const serviceIcon = (type) => {
  if (type === 'vpn') return 'mdi:shield-lock'
  if (type === 'adblock') return 'mdi:shield-check'
  return 'mdi:information'
}

const actionColor = (action) => {
  if (action === 'enabled') return 'text-green-600 bg-green-100'
  if (action === 'disabled') return 'text-gray-600 bg-gray-100'
  if (action === 'error') return 'text-red-600 bg-red-100'
  return 'text-blue-600 bg-blue-100'
}

const formatDate = (date) => {
  return new Date(date).toLocaleString('ru-RU')
}
</script>

<template>
  <UiCard title="Логи событий" subtitle="Последние 50 записей">
    <div class="overflow-x-auto">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">
              Сервис
            </th>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">
              Действие
            </th>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">
              Сообщение
            </th>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">
              Время
            </th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="log in logs" :key="log.uid" class="hover:bg-gray-50">
            <td class="px-4 py-3 whitespace-nowrap">
              <div class="flex items-center">
                <Icon :name="serviceIcon(log.service_type)" class="w-5 h-5 mr-2 text-gray-600" />
                <span class="text-sm font-medium text-gray-900">
                  {{ log.service_type === 'vpn' ? 'VPN' : 'AdBlock' }}
                </span>
              </div>
            </td>
            <td class="px-4 py-3 whitespace-nowrap">
              <span
                :class="[
                  'px-2 py-1 text-xs font-medium rounded-full',
                  actionColor(log.action)
                ]"
              >
                {{ log.action }}
              </span>
            </td>
            <td class="px-4 py-3">
              <span class="text-sm text-gray-600">{{ log.message || '-' }}</span>
            </td>
            <td class="px-4 py-3 whitespace-nowrap text-sm text-gray-500">
              {{ formatDate(log.created_at) }}
            </td>
          </tr>
          <tr v-if="logs.length === 0">
            <td colspan="4" class="px-4 py-8 text-center text-gray-500">
              Нет записей в логах
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </UiCard>
</template>