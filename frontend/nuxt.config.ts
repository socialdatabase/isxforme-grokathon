export default defineNuxtConfig({
  devtools: { enabled: true },

  vite: {
    server: {
      watch: {
        usePolling: true,
        interval: 500,  // Optional: Adjust poll frequency in ms (default is 1000; lower = more responsive but higher CPU)
      },
    },
  },
  
  ssr: false, // SPA mode for simplicity with API backend
  
  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || 'http://localhost:8000/api'
    }
  },

  app: {
    head: {
      title: 'Grokathon',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        { name: 'description', content: 'Django REST + Nuxt boilerplate with JWT authentication' }
      ]
    }
  },

  css: ['~/assets/css/main.css'],

  modules: ['@pinia/nuxt', '@nuxt/ui',]
})

