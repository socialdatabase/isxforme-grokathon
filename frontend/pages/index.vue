<template>
  <div class="home">
    <h1>Welcome to Grokathon</h1>
    <p>Test/Prep repo for the xai hackathon</p>
    
    <div class="api-test">
      <button @click="testApiConnection" class="btn-test" :disabled="testing">
        {{ testing ? 'Testing...' : 'Test API Connection' }}
      </button>
      
      <div v-if="apiStatus" class="api-status" :class="apiStatus.success ? 'success' : 'error'">
        <span class="status-icon">{{ apiStatus.success ? '✓' : '✗' }}</span>
        <span>{{ apiStatus.message }}</span>
      </div>
    </div>
    
    <div class="features">
      <h2>Example Designs:</h2>
      <ul>
        <li><NuxtLink to="/example-designs/result?tab=overview">Overview</NuxtLink></li>
        <li><NuxtLink to="/example-designs/result?tab=timeline">Timeline</NuxtLink></li>
        <li><NuxtLink to="/example-designs/result?tab=groksignal">GrokSignal</NuxtLink></li>
        <li><NuxtLink to="/example-designs/result?tab=index">Authority Index</NuxtLink></li>
        <li><NuxtLink to="/example-designs/result?tab=account&user=LewisHamilton">Account Details</NuxtLink></li>
      </ul>
    </div>
    
    <div class="cta">
      <NuxtLink to="/example-designs" class="btn">Grokathon Example Designs</NuxtLink>
    </div>
  </div>
</template>

<script setup lang="ts">
const config = useRuntimeConfig()

const testing = ref(false)
const apiStatus = ref<{success: boolean, message: string} | null>(null)

const testApiConnection = async () => {
  testing.value = true
  apiStatus.value = null
  
  try {
    const response: any = await $fetch(`${config.public.apiBase}/auth/health/`)
    apiStatus.value = {
      success: true,
      message: response.message || 'API connection successful!'
    }
  } catch (error) {
    apiStatus.value = {
      success: false,
      message: 'Failed to connect to API. Make sure the backend is running.'
    }
  } finally {
    testing.value = false
  }
}

definePageMeta({
  layout: false
})
</script>

<style scoped>
.home {
  text-align: center;
  padding: 3rem 1rem;
}

h1 {
  font-size: 2.5em;
  margin-bottom: 1rem;
  color: #2c3e50;
}

p {
  font-size: 1.2em;
  color: #666;
  margin-bottom: 2rem;
}

.api-test {
  margin: 2rem auto;
  max-width: 600px;
}

.btn-test {
  padding: 0.75rem 1.5rem;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 1em;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-test:hover:not(:disabled) {
  background-color: #2980b9;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

.btn-test:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.api-status {
  margin-top: 1rem;
  padding: 1rem;
  border-radius: 5px;
  font-weight: 500;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.api-status.success {
  background-color: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.api-status.error {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

.status-icon {
  font-size: 1.2em;
  font-weight: bold;
}

.features {
  background-color: white;
  padding: 2rem;
  border-radius: 8px;
  margin: 2rem auto;
  max-width: 600px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.features h2 {
  color: #2c3e50;
  margin-bottom: 1.5rem;
}

.features ul {
  list-style: none;
  padding: 0;
  text-align: left;
}

.features li {
  font-size: 1.1em;
  margin: 0.8rem 0;
  padding-left: 1.5rem;
}

.features li a {
  color: #3498db;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s;
}

.features li a:hover {
  color: #2980b9;
  text-decoration: underline;
}

.cta {
  margin-top: 3rem;
}

.btn {
  display: inline-block;
  padding: 1rem 2rem;
  background-color: #42b983;
  color: white;
  border-radius: 5px;
  font-size: 1.1em;
  font-weight: 500;
  transition: background-color 0.3s;
}

.btn:hover {
  background-color: #35a372;
}
</style>

