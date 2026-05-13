<!-- ./frontend/app/pages/index.vue -->
<script setup>
const settingsStore = useSettingsStore()

const refreshing = ref(false)

const refresh = async () => {
  refreshing.value = true
  await Promise.all([
    settingsStore.fetchSettings(),
    settingsStore.fetchWifiInfo(),
    settingsStore.fetchLogs()
  ])
  refreshing.value = false
}

onMounted(() => {
  refresh()
})

// Auto-refresh каждые 10 секунд
const intervalId = ref(null)
onMounted(() => {
  intervalId.value = setInterval(() => {
    settingsStore.fetchSettings()
    settingsStore.fetchWifiInfo()
  }, 10000)
})

onUnmounted(() => {
  if (intervalId.value) {
    clearInterval(intervalId.value)
  }
})

const handleVPNToggle = async (enabled) => {
  try {
    await settingsStore.toggleVPN(enabled)
  } catch (error) {
    alert('Ошибка при переключении VPN: ' + error.message)
  }
}

const handleAdblockToggle = async (enabled) => {
  try {
    await settingsStore.toggleAdblock(enabled)
  } catch (error) {
    alert('Ошибка при переключении AdBlock: ' + error.message)
  }
}
</script>

<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Header -->
      <div class="mb-8">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-3xl font-bold text-gray-900">JetHub VPN Manager</h1>
            <p class="text-gray-600 mt-1">Управление VPN роутером и блокировщиком рекламы</p>
          </div>
          <UiButton
            @click="refresh"
            :loading="refreshing"
            variant="secondary"
          >
            <Icon name="mdi:refresh" class="w-5 h-5 mr-2" />
            Обновить
          </UiButton>
        </div>
      </div>

      <!-- Stats -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <UiStatCard
          title="Подключено устройств"
          :value="settingsStore.wifiClients"
          icon="mdi:devices"
          color="blue"
        />
        <UiStatCard
          title="VPN трафик"
          :value="`${settingsStore.settings?.vpn_traffic_mb.toFixed(2) || 0} MB`"
          icon="mdi:cloud-upload"
          color="green"
        />
        <UiStatCard
          title="Всего трафик"
          :value="`${settingsStore.settings?.total_traffic_mb.toFixed(2) || 0} MB`"
          icon="mdi:chart-line"
          color="orange"
        />
      </div>

      <!-- Service Controls -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <DashboardServiceControl
          title="VPN"
          description="Проксирование всего трафика через Xray (VLESS + Reality)"
          icon="mdi:shield-lock"
          :enabled="settingsStore.vpnEnabled"
          :status="settingsStore.settings?.vpn_status"
          :loading="settingsStore.loading"
          @toggle="handleVPNToggle"
        />
        <DashboardServiceControl
          title="Блокировщик рекламы"
          description="Блокировка рекламы и трекеров на уровне DNS"
          icon="mdi:shield-check"
          :enabled="settingsStore.adblockEnabled"
          :status="settingsStore.settings?.adblock_status"
          :loading="settingsStore.loading"
          @toggle="handleAdblockToggle"
        />
      </div>

      <!-- WiFi Info -->
      <div class="mb-8">
        <DashboardWiFiInfo
          v-if="settingsStore.wifiInfo"
          :ssid="settingsStore.wifiInfo.ssid"
          :password="settingsStore.wifiInfo.password"
          :clients="settingsStore.wifiClients"
          :ip-address="settingsStore.wifiInfo.ip_address"
        />
      </div>

      <!-- Logs -->
      <div>
        <DashboardLogsTable :logs="settingsStore.logs" />
      </div>
    </div>
  </div>
</template>