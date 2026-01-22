<template>
  <div class="audience-insights-container">
    <header class="page-header">
      <h1 class="page-title">Audience Insights</h1>
      <p class="page-subtitle">Explore curated audience segments on X</p>
    </header>

    <div class="audiences-grid">
      <NuxtLink to="/AudienceInsights/alexi" class="audience-card">
        <div class="audience-icon chicago-mayor">
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M3 21L12 2L21 21H3Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </div>
        <div class="audience-info">
          <h3 class="audience-name">Chicago Mayor Race</h3>
          <p class="audience-desc">Track Alexi Giannoulias vs other candidates</p>
          <span class="audience-size">Campaign Tracker</span>
        </div>
        <svg class="chevron" width="20" height="20" viewBox="0 0 24 24" fill="none">
          <path d="M9 18L15 12L9 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </NuxtLink>

      <NuxtLink to="/AudienceInsights/RustEngineers" class="audience-card">
        <div class="audience-icon">
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M2 17L12 22L22 17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M2 12L12 17L22 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </div>
        <div class="audience-info">
          <h3 class="audience-name">Rust Engineers</h3>
          <p class="audience-desc">Rust Engineers active on X</p>
          <span class="audience-size">241,000 users</span>
        </div>
        <svg class="chevron" width="20" height="20" viewBox="0 0 24 24" fill="none">
          <path d="M9 18L15 12L9 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </NuxtLink>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  layout: false
})
</script>

<style scoped>
.audience-insights-container {
  min-height: 100vh;
  background-color: #000;
  padding: 3rem 1.5rem;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.page-header {
  text-align: center;
  margin-bottom: 3rem;
}

.page-title {
  font-size: clamp(2rem, 5vw, 3rem);
  font-weight: 700;
  color: #fff;
  margin-bottom: 0.75rem;
  letter-spacing: -0.03em;
}

.page-subtitle {
  font-size: 1.05rem;
  color: #71767b;
}

.audiences-grid {
  max-width: 800px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.audience-card {
  display: flex;
  align-items: center;
  gap: 1.25rem;
  background-color: #16181c;
  border: 1px solid #2f3336;
  border-radius: 16px;
  padding: 1.5rem;
  text-decoration: none;
  transition: all 0.2s ease;
}

.audience-card:hover {
  border-color: #3f4347;
  background-color: #1d1f23;
  transform: translateY(-2px);
}

.audience-icon {
  width: 56px;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #B7410E 0%, #E25822 100%);
  border-radius: 12px;
  color: #fff;
  flex-shrink: 0;
}

.audience-icon.chicago-mayor {
  background: linear-gradient(135deg, #1d4ed8 0%, #3b82f6 100%);
}

.audience-info {
  flex: 1;
  min-width: 0;
}

.audience-name {
  font-size: 1.25rem;
  font-weight: 700;
  color: #e7e9ea;
  margin-bottom: 0.25rem;
}

.audience-desc {
  font-size: 0.95rem;
  color: #71767b;
  margin-bottom: 0.5rem;
}

.audience-size {
  display: inline-block;
  background-color: #2f3336;
  color: #1d9bf0;
  font-size: 0.8rem;
  font-weight: 600;
  padding: 0.35rem 0.75rem;
  border-radius: 50px;
}

.chevron {
  color: #71767b;
  flex-shrink: 0;
  transition: transform 0.2s ease;
}

.audience-card:hover .chevron {
  transform: translateX(4px);
  color: #e7e9ea;
}

@media (max-width: 600px) {
  .audience-insights-container {
    padding: 2rem 1rem;
  }
  
  .audience-card {
    padding: 1.25rem;
  }
  
  .audience-icon {
    width: 48px;
    height: 48px;
  }
  
  .audience-name {
    font-size: 1.1rem;
  }
}
</style>
