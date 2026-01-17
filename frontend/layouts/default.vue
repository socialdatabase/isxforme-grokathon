<template>
  <div id="app">
    <nav class="navbar">
      <div class="nav-container">
        <NuxtLink to="/" class="logo">Grokathon</NuxtLink>
        <div class="nav-links">
          <NuxtLink to="/">Home</NuxtLink>
          <NuxtLink to="/example-designs">Example Designs</NuxtLink>
        </div>
      </div>
    </nav>
    <main>
      <slot />
    </main>
  </div>
</template>

<script setup lang="ts">
</script>

<style scoped>
.navbar {
  background-color: #2c3e50;
  padding: 1rem 0;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  font-size: 1.5rem;
  font-weight: bold;
  color: #42b983;
  text-decoration: none;
}

.nav-links {
  display: flex;
  gap: 1.5rem;
  align-items: center;
}

.nav-links a {
  color: white;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s;
}

.nav-links a:hover,
.nav-links a.router-link-active {
  color: #42b983;
}

main {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}
</style>

