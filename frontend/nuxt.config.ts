export default defineNuxtConfig({
  devtools: { enabled: true },
  
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

  modules: ['@pinia/nuxt', '@nuxt/ui']
})

