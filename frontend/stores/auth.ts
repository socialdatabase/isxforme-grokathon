import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    accessToken: null as string | null,
    refreshToken: null as string | null,
    user: null as any
  }),

  getters: {
    isAuthenticated: (state) => !!state.accessToken
  },

  actions: {
    setTokens(access: string, refresh: string) {
      this.accessToken = access
      this.refreshToken = refresh
      
      if (process.client) {
        localStorage.setItem('access_token', access)
        localStorage.setItem('refresh_token', refresh)
      }
    },

    async login(username: string, password: string) {
      const config = useRuntimeConfig()
      
      try {
        const data: any = await $fetch(`${config.public.apiBase}/auth/login/`, {
          method: 'POST',
          body: { username_or_email: username, password }
        })

        this.setTokens(data.access, data.refresh)
        await this.fetchUser()
        return { success: true }
      } catch (error: any) {
        return { 
          success: false, 
          error: error.data?.detail || 'Login failed' 
        }
      }
    },

    async register(userData: any) {
      const config = useRuntimeConfig()
      
      try {
        await $fetch(`${config.public.apiBase}/auth/register/`, {
          method: 'POST',
          body: userData
        })
        return { success: true }
      } catch (error: any) {
        const errors = error.data || {}
        const errorMessage = Object.values(errors).flat().join(' ')
        return { 
          success: false, 
          error: errorMessage || 'Registration failed' 
        }
      }
    },

    async fetchUser() {
      const { apiFetch } = useApi()
      
      try {
        const data: any = await apiFetch('/auth/user/')
        this.user = data
      } catch (error) {
        console.error('Failed to fetch user:', error)
      }
    },

    async refreshAccessToken() {
      const config = useRuntimeConfig()
      
      if (!this.refreshToken) {
        throw new Error('No refresh token available')
      }

      try {
        const data: any = await $fetch(`${config.public.apiBase}/auth/token/refresh/`, {
          method: 'POST',
          body: { refresh: this.refreshToken }
        })

        this.accessToken = data.access
        
        if (process.client) {
          localStorage.setItem('access_token', data.access)
        }
      } catch (error) {
        this.logout()
        throw error
      }
    },

    logout() {
      this.accessToken = null
      this.refreshToken = null
      this.user = null
      
      if (process.client) {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
      }
    },

    initFromStorage() {
      if (process.client) {
        this.accessToken = localStorage.getItem('access_token')
        this.refreshToken = localStorage.getItem('refresh_token')
        
        if (this.accessToken) {
          this.fetchUser()
        }
      }
    }
  }
})

