// ./frontend/app/stores/settings.js
export const useSettingsStore = defineStore('settings', () => {
  const { $api } = useNuxtApp()
  
  const settings = ref(null)
  const wifiInfo = ref(null)
  const logs = ref([])
  const loading = ref(false)
  
  const vpnEnabled = computed(() => settings.value?.vpn_enabled ?? false)
  const adblockEnabled = computed(() => settings.value?.adblock_enabled ?? false)
  const wifiClients = computed(() => settings.value?.wifi_clients_count ?? 0)
  
  async function fetchSettings() {
    loading.value = true
    try {
      settings.value = await $api('api/v1/settings/')
    } catch (error) {
      console.error('Failed to fetch settings:', error)
    } finally {
      loading.value = false
    }
  }
  
  async function toggleVPN(enabled) {
    loading.value = true
    try {
      const response = await $api('api/v1/settings/vpn/toggle', {
        method: 'POST',
        body: { enabled }
      })
      await fetchSettings()
      return response
    } catch (error) {
      console.error('Failed to toggle VPN:', error)
      throw error
    } finally {
      loading.value = false
    }
  }
  
  async function toggleAdblock(enabled) {
    loading.value = true
    try {
      const response = await $api('api/v1/settings/adblock/toggle', {
        method: 'POST',
        body: { enabled }
      })
      await fetchSettings()
      return response
    } catch (error) {
      console.error('Failed to toggle Adblock:', error)
      throw error
    } finally {
      loading.value = false
    }
  }
  
  async function fetchWifiInfo() {
    try {
      wifiInfo.value = await $api('api/v1/settings/wifi')
    } catch (error) {
      console.error('Failed to fetch WiFi info:', error)
    }
  }
  
  async function fetchLogs(limit = 50) {
    try {
      logs.value = await $api(`api/v1/settings/logs?limit=${limit}`)
    } catch (error) {
      console.error('Failed to fetch logs:', error)
    }
  }
  
  return {
    settings,
    wifiInfo,
    logs,
    loading,
    vpnEnabled,
    adblockEnabled,
    wifiClients,
    fetchSettings,
    toggleVPN,
    toggleAdblock,
    fetchWifiInfo,
    fetchLogs,
  }
})