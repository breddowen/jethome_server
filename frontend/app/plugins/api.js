// ./frontend/app/plugins/api.js
export default defineNuxtPlugin(() => {
  const config = useRuntimeConfig()

  const api = async (endpoint, options = {}) => {
    const url = `${config.public.apiBase}/${endpoint}`
    
    try {
      const response = await $fetch(url, {
        ...options,
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
      })
      return response
    } catch (error) {
      console.error('API Error:', error)
      throw error
    }
  }

  return {
    provide: {
      api,
    },
  }
})