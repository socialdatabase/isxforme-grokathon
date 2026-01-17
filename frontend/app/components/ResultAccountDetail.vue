<template>
  <div class="account-detail-container">
    <!-- Prompt Bar -->
    <div class="prompt-bar-container">
      <form class="prompt-bar" @submit.prevent="handleHandleSubmit">
        <svg class="search-icon" width="20" height="20" viewBox="0 0 24 24" fill="none">
          <path d="M21 21L16.65 16.65M19 11C19 15.4183 15.4183 19 11 19C6.58172 19 3 15.4183 3 11C3 6.58172 6.58172 3 11 3C15.4183 3 19 6.58172 19 11Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <input
          v-model="handleInput"
          type="text"
          class="prompt-input"
          placeholder="@username"
          @keydown.enter="handleHandleSubmit"
        />
        <button type="button" class="prompt-clear" @click="emit('back')">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
            <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
      </form>
    </div>

    <!-- Account Header with Bio -->
    <div class="account-header">
      <div class="account-avatar">
        <img :src="upgradeImg(account.avatar)" :alt="account.displayName" />
      </div>
      <div class="account-info">
        <div class="account-name-row">
          <h1 class="account-name">{{ account.displayName }}</h1>
          <svg v-if="account.verified" class="verified-badge" width="22" height="22" viewBox="0 0 24 24" fill="#1d9bf0">
            <path d="M22.5 12.5c0-1.58-.875-2.95-2.148-3.6.154-.435.238-.905.238-1.4 0-2.21-1.71-3.998-3.818-3.998-.47 0-.92.084-1.336.25C14.818 2.415 13.51 1.5 12 1.5s-2.816.917-3.437 2.25c-.415-.165-.866-.25-1.336-.25-2.11 0-3.818 1.79-3.818 4 0 .494.083.964.237 1.4-1.272.65-2.147 2.018-2.147 3.6 0 1.495.782 2.798 1.942 3.486-.02.17-.032.34-.032.514 0 2.21 1.708 4 3.818 4 .47 0 .92-.086 1.335-.25.62 1.334 1.926 2.25 3.437 2.25 1.512 0 2.818-.916 3.437-2.25.415.163.865.248 1.336.248 2.11 0 3.818-1.79 3.818-4 0-.174-.012-.344-.033-.513 1.158-.687 1.943-1.99 1.943-3.484zm-6.616-3.334l-4.334 6.5c-.145.217-.382.334-.625.334-.143 0-.288-.04-.416-.126l-.115-.094-2.415-2.415c-.293-.293-.293-.768 0-1.06s.768-.294 1.06 0l1.77 1.767 3.825-5.74c.23-.345.696-.436 1.04-.207.346.23.44.696.21 1.04z"/>
          </svg>
        </div>
        <div class="account-handle">@{{ account.username }}</div>
        <div class="account-stats">
          <span class="stat"><strong>{{ account.followers }}</strong> followers</span>
          <span class="stat"><strong>{{ account.following }}</strong> following</span>
        </div>
        <p v-if="account.description" class="account-bio">{{ account.description }}</p>
      </div>
    </div>

    <!-- Authority Rankings Section -->
    <section class="detail-section">
      <div class="section-header">
        <svg class="section-icon" width="20" height="20" viewBox="0 0 24 24" fill="none">
          <path d="M12 15C15.866 15 19 11.866 19 8V2H5V8C5 11.866 8.13401 15 12 15Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M5 2H19" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M12 15V19" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M8 22H16" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M8 19H16" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <h2 class="section-title">Authority Rankings</h2>
      </div>
      
      <!-- Loading State -->
      <div v-if="loading" class="loading-container">
        <div class="spinner"></div>
        <p class="loading-message">Loading rankings...</p>
      </div>
      
      <!-- Error State -->
      <div v-else-if="error" class="error-message">
        {{ error }}
      </div>
      
      <!-- Rankings Grid -->
      <div v-else-if="rankings.length > 0" class="rankings-grid">
        <div 
          v-for="ranking in rankings" 
          :key="ranking.category" 
          class="ranking-card"
          :class="getRankClass(ranking.rank)"
        >
          <span class="ranking-number">#{{ ranking.rank }}</span>
          <span class="ranking-label">in</span>
          <span class="ranking-category">{{ ranking.category }}</span>
        </div>
      </div>
      
      <!-- No Rankings -->
      <div v-else class="no-data-message">
        No rankings data available for this account.
      </div>
    </section>

    <!-- AI Post Summary Section -->
    <section class="detail-section">
      <div class="section-header">
        <svg class="section-icon" width="20" height="20" viewBox="0 0 24 24" fill="none">
          <path d="M14 2H6C5.46957 2 4.96086 2.21071 4.58579 2.58579C4.21071 2.96086 4 3.46957 4 4V20C4 20.5304 4.21071 21.0391 4.58579 21.4142C4.96086 21.7893 5.46957 22 6 22H18C18.5304 22 19.0391 21.7893 19.4142 21.4142C19.7893 21.0391 20 20.5304 20 20V8L14 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M14 2V8H20" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M16 13H8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M16 17H8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <h2 class="section-title">AI Summary</h2>
      </div>
      
      <!-- Loading State -->
      <div v-if="loadingAiSummary && !aiSummary" class="loading-container">
        <div class="spinner"></div>
        <p class="loading-message">Generating AI summary...</p>
      </div>
      
      <!-- AI Summary Content -->
      <p v-else class="ai-summary">
        {{ aiSummary }}<span v-if="loadingAiSummary" class="typing-cursor">|</span>
      </p>
    </section>

    <!-- Interests Section -->
    <section class="detail-section">
      <div class="section-header">
        <svg class="section-icon" width="20" height="20" viewBox="0 0 24 24" fill="none">
          <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <h2 class="section-title">Interests</h2>
      </div>
      
      <!-- Loading State -->
      <div v-if="loading" class="loading-container">
        <div class="spinner"></div>
        <p class="loading-message">Loading interests...</p>
      </div>
      
      <!-- Error State -->
      <div v-else-if="error" class="error-message">
        {{ error }}
      </div>
      
      <!-- Interests Grid -->
      <div v-else-if="interests.length > 0" class="interests-grid">
        <span v-for="interest in interests" :key="interest" class="interest-tag">
          {{ interest }}
        </span>
      </div>
      
      <!-- No Interests -->
      <div v-else class="no-data-message">
        No interests data available for this account.
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
const config = useRuntimeConfig()

interface AccountInput {
  id: string
  displayName: string
  username: string
  avatar: string
  followers: string
  following: string
  verified: boolean
  description: string
}

interface Ranking {
  category: string
  rank: number
}

const props = defineProps<{
  account: AccountInput
}>()

const emit = defineEmits<{
  (e: 'back'): void
  (e: 'changeHandle', handle: string): void
}>()

const upgradeImg = (url: string) => {
  return url.replace('_normal', '_400x400');
}

// State for handle input
const handleInput = ref(`@${props.account.username}`)

// State for fetched data
const interests = ref<string[]>([])
const rankings = ref<Ranking[]>([])
const loading = ref(true)
const error = ref<string | null>(null)

// State for AI summary
const aiSummary = ref('')
const loadingAiSummary = ref(false)

// Handle form submission for changing handle
const handleHandleSubmit = () => {
  const newHandle = handleInput.value.trim()
  if (newHandle && newHandle !== `@${props.account.username}`) {
    // Ensure it starts with @
    const cleanHandle = newHandle.startsWith('@') ? newHandle : `@${newHandle}`
    emit('changeHandle', cleanHandle)
  }
}

// Fetch interests and rankings from API using handle
const fetchAccountData = async () => {
  loading.value = true
  error.value = null
  
  try {
    const response = await $fetch<{ topics: string[], ranks: string[] }>(
      `${config.public.apiBase}/grokathon/fetch-topics-ranks-handle/?handle=@${props.account.username}`
    )
    
    if (response.topics) {
      interests.value = response.topics
    }
    
    if (response.ranks) {
      // Parse ranks from strings like "#1 - Robotics" into { rank: 1, category: "Robotics" }
      rankings.value = response.ranks.map((rankStr: string) => {
        // Handle formats like "#1 - Robotics" or "1 - Robotics"
        const match = rankStr.match(/^#?(\d+)\s*-\s*(.+)$/)
        if (match && match[1] && match[2]) {
          return {
            rank: parseInt(match[1], 10),
            category: match[2].trim()
          }
        }
        return null
      }).filter((r: Ranking | null): r is Ranking => r !== null)
    }
  } catch (err) {
    console.error('Error fetching account data:', err)
    error.value = 'Failed to load data'
  } finally {
    loading.value = false
  }
}

// Stream AI summary from the API
const streamAiSummary = async () => {
  loadingAiSummary.value = true
  aiSummary.value = ''
  
  try {
    const response = await fetch(
      `${config.public.apiBase}/grokathon/generate-ai-bio-handle/?handle=@${props.account.username}`
    )
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    const reader = response.body?.getReader()
    if (!reader) {
      throw new Error('No response body')
    }
    
    const decoder = new TextDecoder()
    
    while (true) {
      const { done, value } = await reader.read()
      if (done) break
      
      const chunk = decoder.decode(value, { stream: true })
      aiSummary.value += chunk
    }
  } catch (err) {
    console.error('Error streaming AI summary:', err)
    aiSummary.value = 'Failed to generate AI summary.'
  } finally {
    loadingAiSummary.value = false
  }
}

// Get CSS class based on rank
const getRankClass = (rank: number) => {
  if (rank <= 3) return 'rank-gold'
  if (rank <= 25) return 'rank-silver'
  if (rank <= 100) return 'rank-bronze'
  return 'rank-default'
}

// Fetch data when component mounts
onMounted(() => {
  fetchAccountData()
  streamAiSummary()
})

// Re-fetch if account changes
watch(() => props.account.username, (newUsername: string) => {
  handleInput.value = `@${newUsername}`
  fetchAccountData()
  streamAiSummary()
})
</script>

<style scoped>
.account-detail-container {
  max-width: 800px;
  margin: 0 auto;
}

/* Prompt Bar */
.prompt-bar-container {
  margin-bottom: 2rem;
}

.prompt-bar {
  display: flex;
  align-items: center;
  background-color: #16181c;
  border-radius: 50px;
  border: 1px solid #2f3336;
}

.search-icon {
  margin-left: 1.25rem;
  color: #71767b;
  flex-shrink: 0;
}

.prompt-input {
  flex: 1;
  background: transparent;
  border: none;
  outline: none;
  padding: 0.85rem 1rem;
  font-size: 0.95rem;
  color: #1d9bf0;
  font-family: inherit;
  font-weight: 600;
}

.prompt-clear {
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: none;
  padding: 0.75rem 1rem;
  color: #71767b;
  cursor: pointer;
  transition: color 0.15s ease;
}

.prompt-clear:hover {
  color: #e7e9ea;
}

/* Account Header */
.account-header {
  display: flex;
  gap: 1.5rem;
  padding: 1.5rem;
  background-color: #16181c;
  border: 1px solid #2f3336;
  border-radius: 16px;
  margin-bottom: 1.5rem;
}

.account-avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  overflow: hidden;
  flex-shrink: 0;
}

.account-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.account-info {
  flex: 1;
}

.account-name-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.25rem;
}

.account-name {
  font-size: 1.5rem;
  font-weight: 700;
  color: #e7e9ea;
  margin: 0;
}

.verified-badge {
  flex-shrink: 0;
}

.account-handle {
  color: #71767b;
  font-size: 1rem;
  margin-bottom: 0.75rem;
}

.account-stats {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 1rem;
}

.stat {
  color: #71767b;
  font-size: 0.95rem;
}

.stat strong {
  color: #e7e9ea;
  font-weight: 700;
}

.account-bio {
  color: #a0a0a0;
  font-size: 0.9rem;
  line-height: 1.5;
  margin: 0;
}

/* Sections */
.detail-section {
  background-color: #16181c;
  border: 1px solid #2f3336;
  border-radius: 16px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.section-icon {
  color: #71767b;
}

.section-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: #e7e9ea;
  margin: 0;
}

/* Loading State */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem 1rem;
}

.spinner {
  width: 32px;
  height: 32px;
  border: 3px solid #2f3336;
  border-top-color: #1d9bf0;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.loading-message {
  margin-top: 1rem;
  color: #71767b;
  font-size: 0.9rem;
}

/* Error and No Data */
.error-message,
.no-data-message {
  color: #71767b;
  font-size: 0.9rem;
  text-align: center;
  padding: 1rem;
}

/* Rankings Grid */
.rankings-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: 0.75rem;
}

.ranking-card {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  background-color: #2f3336;
  border-radius: 8px;
  padding: 0.65rem 0.9rem;
  transition: background-color 0.15s ease;
}

.ranking-card:hover {
  background-color: #3a3d41;
}

.ranking-number {
  font-size: 0.95rem;
  font-weight: 700;
  color: #e7e9ea;
}

.ranking-label {
  font-size: 0.85rem;
  color: #71767b;
}

.ranking-category {
  font-size: 0.9rem;
  font-weight: 500;
  color: #e7e9ea;
}

/* Top 3 - Gold background */
.ranking-card.rank-gold {
  background-color: #a08520;
}

.ranking-card.rank-gold:hover {
  background-color: #b8992a;
}

.ranking-card.rank-gold .ranking-number,
.ranking-card.rank-gold .ranking-label,
.ranking-card.rank-gold .ranking-category {
  color: #fff;
}

/* Top 25 */
.ranking-card.rank-silver {
  background-color: #404550;
}

.ranking-card.rank-silver:hover {
  background-color: #4a5060;
}

/* Top 100 */
.ranking-card.rank-bronze {
  background-color: #353840;
}

.ranking-card.rank-bronze:hover {
  background-color: #3f434c;
}

/* AI Summary */
.ai-summary {
  color: #e7e9ea;
  font-size: 0.95rem;
  line-height: 1.6;
  margin: 0;
  min-height: 60px;
}

.typing-cursor {
  display: inline-block;
  color: #1d9bf0;
  animation: blink 0.8s infinite;
  margin-left: 2px;
}

@keyframes blink {
  0%, 50% { opacity: 1; }
  51%, 100% { opacity: 0; }
}

/* Interests Grid */
.interests-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}

.interest-tag {
  background-color: #2f3336;
  color: #e7e9ea;
  padding: 0.5rem 1rem;
  border-radius: 50px;
  font-size: 0.9rem;
  transition: all 0.15s ease;
}

.interest-tag:hover {
  background-color: #3f4347;
}

/* Responsive */
@media (max-width: 600px) {
  .account-header {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }
  
  .account-stats {
    justify-content: center;
  }
  
  .rankings-grid {
    grid-template-columns: 1fr;
  }
}
</style>
