export default defineNuxtConfig({
  devtools: { enabled: false },

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
        { property: 'og:title', content: 'Is X for me? - Check if your interests are active on X!' },
        { property: 'og:description', content: 'Check if your interests are active on X.' },
        { property: 'og:image', content: '/img/og-image.png' },  
        { property: 'og:image:width', content: '1200' },
        { property: 'og:image:height', content: '630' },
        { property: 'og:image:alt', content: 'Is X for me?' },
        { property: 'og:image:type', content: 'image/png' },
        { property: 'og:site_name', content: 'Is X for me?' },
        { name: 'twitter:image', content: '/img/og-image.png' }, 
        { name: 'twitter:card', content: 'summary_large_image' }

      ]
    }
  },

  css: ['~/assets/css/main.css'],

  modules: ['@pinia/nuxt', '@nuxt/ui',]
})