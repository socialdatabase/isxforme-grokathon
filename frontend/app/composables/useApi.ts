export const useApi = () => {
  const config = useRuntimeConfig()
  const authStore = useAuthStore()

  const apiFetch = async (endpoint: string, options: any = {}) => {
    const token = authStore.accessToken

    const headers: any = {
      'Content-Type': 'application/json',
      ...options.headers
    }

    if (token) {
      headers.Authorization = `Bearer ${token}`
    }

    try {
      const response = await $fetch(`${config.public.apiBase}${endpoint}`, {
        ...options,
        headers
      })
      return response
    } catch (error: any) {
      // Handle 401 - try to refresh token
      if (error.statusCode === 401 && authStore.refreshToken) {
        try {
          await authStore.refreshAccessToken()
          // Retry original request with new token
          headers.Authorization = `Bearer ${authStore.accessToken}`
          return await $fetch(`${config.public.apiBase}${endpoint}`, {
            ...options,
            headers
          })
        } catch (refreshError) {
          authStore.logout()
          navigateTo('/login')
          throw refreshError
        }
      }
      throw error
    }
  }

  return {
    apiFetch
  }
}

