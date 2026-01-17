<template>
  <UApp>
    <NuxtLayout>
      <NuxtPage />
    </NuxtLayout>
  </UApp>
</template>

<script setup lang="ts">
useSeoMeta({
  title: 'Is X for me? ', 
  description: 'Check if your interests are active on X.',
  ogTitle: 'Is X for me? - Check if your interests are active on X!',
  ogDescription: 'Check if your interests are active on X.',
  ogImage: {
    url: 'https://www.isxforme.com/img/og-image.png',
    width: 1200,
    height: 630,
    alt: 'Is X for me?',
    type: 'image/png',
  },
  ogImageAlt: 'Is X for me?',
  ogImageHeight: 630,
  ogImageWidth: 1200,
  ogSiteName: 'Is X for me?',
  twitterImage: 'https://www.isxforme.com/img/og-image.png',
  twitterCard: 'summary_large_image',
})
</script>
