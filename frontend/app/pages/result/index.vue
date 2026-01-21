<template>
  <div class="container-isxforme">
    <!-- Full-page Shooting Stars Overlay -->
    <transition name="fade">
      <div v-if="showStars" class="stars-overlay" @click="skipStars">
        <div class="shooting-stars-fullpage">
          <div class="star star-1"></div>
          <div class="star star-2"></div>
          <div class="star star-3"></div>
          <div class="star star-4"></div>
          <div class="star star-5"></div>
          <div class="star star-6"></div>
          <div class="star star-7"></div>
          <div class="star star-8"></div>
        </div>
      </div>
    </transition>

    <!-- Hero Section / Toggle -->
    <header class="hero" :class="{ collapsed: showTabs }" @click="collapseHero">
      <transition name="fade" mode="out-in">
        <div v-if="!showTabs" key="hero" class="hero-content">
          <h1 class="hero-title">𝕏 is definitely for you!</h1>
          <p class="hero-subtitle">We found an amazing community that matches your interests</p>
        </div>
        <div v-else key="tabs" class="search-bar-container" :class="searchBarWidthClass">
          <div class="search-bar-row">
            <form class="search-bar" @submit.prevent="handleSearch">
              <svg class="search-icon" width="20" height="20" viewBox="0 0 24 24" fill="none">
                <path d="M21 21L16.65 16.65M19 11C19 15.4183 15.4183 19 11 19C6.58172 19 3 15.4183 3 11C3 6.58172 6.58172 3 11 3C15.4183 3 19 6.58172 19 11Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              <input
                v-model="searchInput"
                type="text"
                class="search-input"
                placeholder="Search for a topic or @handle..."
              />
              <button type="submit" class="search-submit" :disabled="!searchInput.trim()">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
                  <path d="M5 12H19M19 12L12 5M19 12L12 19" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </button>
            </form>
          
            <!-- Podcast Mode Button (Timeline only) -->
            <button 
              v-if="activeTab === 'timeline'"
              class="podcast-btn"
              :class="{ active: podcastMode, loading: podcastLoading }"
              :disabled="podcastLoading"
              @click="podcastMode = !podcastMode"
            >
              <div v-if="podcastLoading" class="podcast-spinner"></div>
              <template v-else>
                <span class="podcast-label hidden sm:flex">{{ podcastMode ? 'Pause' : 'Podcast' }}</span>
                <div class="sound-waves" :class="{ playing: podcastMode }">
                  <span class="wave"></span>
                  <span class="wave"></span>
                  <span class="wave"></span>
                  <span class="wave"></span>
                </div>
              </template>
            </button>
          </div>
          <BaseTabs v-model="activeTabUi" />
        </div>
      </transition>
    </header>

    <!-- Overview Tab Content (use v-show for preloading) -->
    <div v-show="activeTab === 'overview'" class="tab-content">
      <ResultOverview @switch-to-timeline="switchToTimeline" />
    </div>

    <!-- Timeline Tab Content (use v-show for preloading) -->
    <div v-show="activeTab === 'timeline'" class="tab-content">
      <ResultTimeline 
        ref="timelineRef"
        :keyword 
        :podcast-mode="podcastMode"
        @open-newspaper="openNewspaper"
        @podcast-state-change="(playing: boolean, loading: boolean) => { podcastMode = playing; podcastLoading = loading }"
      />
    </div>

    <!-- Index Tab Content (use v-show for preloading) -->
    <div v-show="activeTab === 'index'" class="tab-content">
      <ResultIndex
        :keyword
        @select-account="handleAccountSelect"
      />
    </div>

    <!-- Account Detail View -->
    <div v-if="activeTab === 'account' && selectedAccount" class="tab-content">
      <ResultAccountDetail
        :account="selectedAccount"
        @back="backToIndex"
        @change-handle="handleChangeHandle"
      />
    </div>

    <!-- GrokSignal Tab Content (use v-show for preloading) -->
    <div v-show="activeTab === 'groksignal'" class="tab-content">
      <ResultGrokSignal :is-active="activeTab === 'groksignal'" :keyword="searchKeyword" @start-debate="switchToDebate" />
    </div>

    <!-- Expert Debate Tab Content -->
    <div v-if="activeTab === 'debate'" class="tab-content">
      <ResultExpertDebate :is-active="activeTab === 'debate'" :keyword="searchKeyword" />
    </div>

    <!-- The Grok Times Overlay -->
    <div v-show="showNewspaper" class="newspaper-overlay" @click.self="closeNewspaper">
      <button class="newspaper-close" @click="closeNewspaper">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
          <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </button>
      <div class="newspaper-content">
        <TheGrokTimes :keyword="searchKeyword" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import ResultAccountDetail from '~/components/ResultAccountDetail.vue'
import ResultExpertDebate from '~/components/ResultExpertDebate.vue'
import ResultGrokSignal from '~/components/ResultGrokSignal.vue'
import ResultOverview from '~/components/ResultOverview.vue'
import ResultTimeline from '~/components/ResultTimeline.vue'
import useData from '~/composables/useData'
import useDataStore from '~/stores/useDataStore'

const config = useRuntimeConfig()
const route = useRoute()
const { fetchIds } = useData()
// Account type (must match ExampleIndex)
interface SelectedAccountData {
  id: string
  displayName: string
  username: string
  avatar: string
  followers: string
  following: string
  verified: boolean
  description: string
}

const showTabs = ref(false)
const showStars = ref(true)
const activeTabUi = ref<'overview' | 'timeline' | 'groksignal' | 'index'>('overview')
const activeTab = ref<'overview' | 'timeline' | 'groksignal' | 'index' | 'account' | 'debate'>('overview')
const selectedAccount = ref<SelectedAccountData | null>(null)
// const searchKeyword = ref('') // Start empty, will be set from query
const searchInput = ref('') // Input field value
const podcastMode = ref(false)
const podcastLoading = ref(false)
const showNewspaper = ref(false)

const { keyword } = storeToRefs(useDataStore())

watch(activeTabUi, () => {
  activeTab.value = activeTabUi.value;
})

// Apply query params and reset state for fresh search
const applyQueryParams = () => {
  const tab = route.query.tab as string
  const user = route.query.user as string
  const q = route.query.q as string
  
  // Set search keyword from query
  if (q) {
    keyword.value = q
    searchInput.value = q
  } else {
    // Default to F1 if no query
    keyword.value = 'F1'
    searchInput.value = ''
  }
  
  // Reset to overview for fresh search unless specific tab requested
  if (tab) {
    const validTabs = ['overview', 'timeline', 'groksignal', 'index', 'account', 'debate']
    if (validTabs.includes(tab)) {
      activeTab.value = tab as typeof activeTab.value
      showTabs.value = true
    }
  } else {
    activeTab.value = 'overview'
  }
  
  // Note: Direct URL navigation to account detail is not supported
  // Users must navigate through the index to view account details
  if (tab !== 'account') {
    selectedAccount.value = null
  }
}

const collapseHero = () => {
  showTabs.value = true
}

const skipStars = () => {
  showStars.value = false
  showTabs.value = true
}

const switchToTimeline = () => {
  showTabs.value = true
  activeTab.value = 'timeline'
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const switchToDebate = () => {
  showTabs.value = true
  activeTab.value = 'debate'
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const openNewspaper = () => {
  showNewspaper.value = true
  document.body.style.overflow = 'hidden'
}

const closeNewspaper = () => {
  showNewspaper.value = false
  document.body.style.overflow = ''
}

// Handle unified search
const handleSearch = async () => {
  if (searchInput.value.trim()) {
    keyword.value = searchInput.value.trim()

    await fetchIds();
    await fet
    


    // Stay on current tab, but if on account/debate view, go back to a main tab
    if (activeTab.value === 'account') {
      activeTab.value = 'index'
    } else if (activeTab.value === 'debate') {
      activeTab.value = 'groksignal'
    }
    // Otherwise stay on current tab (overview, timeline, groksignal, index)
    selectedAccount.value = null
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
}

const handleAccountSelect = (account: SelectedAccountData) => {
  selectedAccount.value = account
  activeTab.value = 'account'
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const backToIndex = () => {
  activeTab.value = 'index'
  selectedAccount.value = null
}

const handleChangeHandle = async (newHandle: string) => {
  try {
    const response = await $fetch<{ account: any }>(
      `${config.public.apiBase}/grokathon/fetch-account-handle/?handle=${encodeURIComponent(newHandle)}`
    )
    
    if (response.account) {
      const acc = response.account
      selectedAccount.value = {
        id: acc.id,
        displayName: acc.name || acc.username,
        username: acc.username,
        avatar: acc.profile_image_url || '',
        followers: formatFollowers(acc.public_metrics?.followers_count || 0),
        following: formatFollowers(acc.public_metrics?.following_count || 0),
        verified: acc.verified || false,
        description: acc.description || ''
      }
    }
  } catch (err) {
    console.error('Error fetching account by handle:', err)
  }
}

// Format followers count
const formatFollowers = (count: number): string => {
  if (count >= 1000000) {
    return (count / 1000000).toFixed(1) + 'M'
  } else if (count >= 1000) {
    return (count / 1000).toFixed(1) + 'K'
  }
  return count.toString()
}

// Compute search bar width class based on active tab
const searchBarWidthClass = computed(() => {
  switch (activeTab.value) {
    case 'overview':
    case 'account':
      return 'width-800'
    case 'timeline':
    case 'groksignal':
    case 'debate':
      return 'width-1000'
    case 'index':
      return 'width-1200'
    default:
      return 'width-800'
  }
})

// Watch for route query changes (handles navigation from index.vue)
watch(() => route.query.q, (newQ: string | (string | null)[] | null | undefined) => {
  if (newQ && typeof newQ === 'string') {
    keyword.value = newQ
    searchInput.value = newQ
    // Go to overview only on initial navigation (when coming from index page)
    // This happens when first arriving at the result page
    if (!showTabs.value) {
      activeTab.value = 'overview'
    }
    selectedAccount.value = null
    showTabs.value = true
  }
})

onMounted(() => {
  applyQueryParams()
  
  if (!route.query.tab) {
    // Show shooting stars for 2 seconds, then show message
    setTimeout(() => {
      showStars.value = false
    }, 2000)
    
    // Collapse after 5 seconds total (2s stars + 3s message)
    setTimeout(() => {
      showTabs.value = true
    }, 5000)
  } else {
    // Skip stars if coming from a specific tab
    showStars.value = false
  }
})

definePageMeta({
  layout: false
})
</script>

<style scoped>
.container-isxforme {
  /* width: full; */
  min-height: 100vh;
  background-color: #000;
  padding: 3rem 1.5rem;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* Hero */
.hero {
  text-align: center;
  margin-bottom: 2.5rem;
  cursor: pointer;
  transition: all 0.4s ease;
}

.hero.collapsed {
  cursor: default;
}

.hero-content {
  padding: 1rem 0;
}

/* Full-page Shooting Stars Overlay */
.stars-overlay {
  position: fixed;
  inset: 0;
  background: #000;
  z-index: 9999;
  cursor: pointer;
  overflow: hidden;
}

.shooting-stars-fullpage {
  position: absolute;
  inset: 0;
}

.star {
  position: absolute;
  width: 4px;
  height: 4px;
  background: #fff;
  border-radius: 50%;
  box-shadow: 0 0 8px 3px rgba(255, 255, 255, 0.7);
  opacity: 0;
  animation: shooting 1.2s ease-out forwards;
}

.star::after {
  content: '';
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 120px;
  height: 2px;
  background: linear-gradient(to left, rgba(255, 255, 255, 0.9), transparent);
  right: 4px;
}

.star-1 {
  top: 15%;
  left: 5%;
  animation-delay: 0s;
}

.star-2 {
  top: 35%;
  left: 25%;
  animation-delay: 0.15s;
}

.star-3 {
  top: 10%;
  left: 50%;
  animation-delay: 0.3s;
}

.star-4 {
  top: 55%;
  left: 15%;
  animation-delay: 0.25s;
}

.star-5 {
  top: 25%;
  left: 70%;
  animation-delay: 0.4s;
}

.star-6 {
  top: 65%;
  left: 40%;
  animation-delay: 0.5s;
}

.star-7 {
  top: 45%;
  left: 60%;
  animation-delay: 0.35s;
}

.star-8 {
  top: 75%;
  left: 75%;
  animation-delay: 0.55s;
}

@keyframes shooting {
  0% {
    opacity: 1;
    transform: translateX(0) translateY(0);
  }
  70% {
    opacity: 1;
  }
  100% {
    opacity: 0;
    transform: translateX(300px) translateY(150px);
  }
}

.hero-title {
  font-size: clamp(2rem, 5vw, 3rem);
  font-weight: 700;
  color: #fff;
  margin-bottom: 0.75rem;
  letter-spacing: -0.03em;
}

.hero-subtitle {
  font-size: 1.05rem;
  color: #71767b;
}

/* Tabs */
.tabs-container {
  display: flex;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.5rem;
  background-color: #16181c;
  border-radius: 50px;
  width: fit-content;
  margin: 0 auto;
}

.tab {
  flex: 1;
  padding: 0.75rem 2rem;
  background: transparent;
  border: none;
  border-radius: 50px;
  color: #71767b;
  font-size: 0.95rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  font-family: inherit;
  text-align: center;
}

.tab.groksignal {
  margin-left: -1rem;
}

.tab:hover {
  color: #e7e9ea;
}

.tab.active {
  background-color: #fff;
  color: #000;
}

/* Unified Search Bar */
.search-bar-container {
  margin: 0 auto 2rem;
  max-width: 1000px;
  transition: max-width 0.3s ease;
}



.search-bar-container.width-800 {
  max-width: 800px;
}

.search-bar-container.width-1000 {
  max-width: 1000px;
}

.search-bar-container.width-1200 {
  max-width: 1200px;
}

.search-bar-row {
  display: flex;
  gap: 0.75rem;
  margin-bottom: 20px;
  align-items: stretch;
}

.search-bar {
  flex: 1;
  display: flex;
  align-items: center;
  background-color: #16181c;
  border-radius: 28px;
  border: 1px solid #2f3336;
  padding: 0.25rem 0.5rem;
  transition: border-color 0.2s ease;
}

.search-bar:focus-within {
  border-color: #1d9bf0;
}

.search-icon {
  color: #71767b;
  margin-left: 0.75rem;
  flex-shrink: 0;
}

.search-input {
  flex: 1;
  background: transparent;
  border: none;
  outline: none;
  padding: 0.85rem 0.75rem;
  font-size: 1rem;
  color: #e7e9ea;
  font-family: inherit;
}

.search-input::placeholder {
  color: #71767b;
}

.search-submit {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  background-color: #fff;
  border: none;
  border-radius: 50%;
  color: #000;
  cursor: pointer;
  transition: background-color 0.2s ease;
  flex-shrink: 0;
}

.search-submit:hover:not(:disabled) {
  background-color: #d1d1d1;
}

.search-submit:disabled {
  background-color: #3f4347;
  color: #71767b;
  cursor: not-allowed;
}

/* Podcast Mode Button */
.podcast-btn {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  background-color: #16181c;
  border: 1px solid #2f3336;
  border-radius: 28px;
  padding: 0 1.25rem;
  color: #71767b;
  font-size: 0.95rem;
  font-weight: 500;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
}

.podcast-btn:hover {
  border-color: #1d9bf0;
  color: #e7e9ea;
}

.podcast-btn.active {
  background-color: #fff;
  border-color: #fff;
  color: #000;
}

.podcast-btn.loading {
  opacity: 0.7;
  cursor: wait;
}

.podcast-btn:disabled {
  cursor: wait;
}

.podcast-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: #1d9bf0;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.podcast-label {
  min-width: 60px;
}

/* Sound Waves Animation */
.sound-waves {
  display: flex;
  align-items: center;
  gap: 3px;
  height: 20px;
}

.sound-waves .wave {
  width: 3px;
  height: 8px;
  background-color: currentColor;
  border-radius: 2px;
  opacity: 0.4;
}

.sound-waves.playing .wave {
  opacity: 1;
  animation: soundWave 0.8s ease-in-out infinite;
}

.sound-waves.playing .wave:nth-child(1) {
  animation-delay: 0s;
}

.sound-waves.playing .wave:nth-child(2) {
  animation-delay: 0.1s;
}

.sound-waves.playing .wave:nth-child(3) {
  animation-delay: 0.2s;
}

.sound-waves.playing .wave:nth-child(4) {
  animation-delay: 0.3s;
}

@keyframes soundWave {
  0%, 100% {
    height: 8px;
  }
  50% {
    height: 18px;
  }
}

/* Transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.fade-enter-from {
  opacity: 0;
  transform: translateY(-10px);
}

.fade-leave-to {
  opacity: 0;
  transform: translateY(10px);
}

/* Tab Content */
.tab-content {
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

/* Newspaper Overlay */
.newspaper-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.9);
  z-index: 1000;
  overflow-y: auto;
  animation: fadeIn 0.3s ease;
}

.newspaper-close {
  position: fixed;
  top: 1rem;
  right: 1rem;
  z-index: 1001;
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.8);
  border: 1px solid #333;
  border-radius: 50%;
  color: #fff;
  cursor: pointer;
  transition: all 0.2s ease;
}

.newspaper-close:hover {
  background: rgba(50, 50, 50, 0.9);
  transform: scale(1.1);
}

.newspaper-content {
  min-height: 100vh;
}

/* Responsive */
@media (max-width: 600px) {
  .container-isxforme {
    padding: 2rem 1rem;
  }
  
  .newspaper-close {
    top: 0.5rem;
    right: 0.5rem;
  }
}
</style>
