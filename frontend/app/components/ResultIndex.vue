<template>
  <div class="index-container">
    <!-- Results View -->
    <div v-if="showResults || loading" class="results-container">
      <!-- Results Header -->
      <div class="results-header">
        <h2 class="results-title">Authority Index</h2>
        <p class="results-subtitle">
          <template v-if="loading">
            Loading authorities in <span class="topic-highlight">{{ currentTopic }}</span>...
          </template>
          <template v-else>
            Top {{ authorityAccounts.length }} authorities in <span class="topic-highlight">{{ currentTopic }}</span>
          </template>
        </p>
      </div>

      <!-- Loading Spinner -->
      <div v-if="loading" class="loading-container">
        <div class="spinner"></div>
        <p class="loading-message">Fetching authority rankings...</p>
      </div>

      <!-- Authority Index Grid -->
      <div v-else class="authority-grid">
        <div 
          v-for="(account, index) in authorityAccounts" 
          :key="account.username" 
          class="authority-card"
          @click="emit('select-account', account)"
        >
          <!-- Account Info Row -->
          <div class="account-row">
            <div class="account-avatar">
              <img :src="account.avatar" :alt="account.displayName" />
            </div>
            <div class="account-details">
              <div class="account-name-row">
                <span class="account-name">{{ account.displayName }}</span>
                <svg v-if="account.verified" class="verified-badge" width="16" height="16" viewBox="0 0 24 24" fill="#1d9bf0">
                  <path d="M22.5 12.5c0-1.58-.875-2.95-2.148-3.6.154-.435.238-.905.238-1.4 0-2.21-1.71-3.998-3.818-3.998-.47 0-.92.084-1.336.25C14.818 2.415 13.51 1.5 12 1.5s-2.816.917-3.437 2.25c-.415-.165-.866-.25-1.336-.25-2.11 0-3.818 1.79-3.818 4 0 .494.083.964.237 1.4-1.272.65-2.147 2.018-2.147 3.6 0 1.495.782 2.798 1.942 3.486-.02.17-.032.34-.032.514 0 2.21 1.708 4 3.818 4 .47 0 .92-.086 1.335-.25.62 1.334 1.926 2.25 3.437 2.25 1.512 0 2.818-.916 3.437-2.25.415.163.865.248 1.336.248 2.11 0 3.818-1.79 3.818-4 0-.174-.012-.344-.033-.513 1.158-.687 1.943-1.99 1.943-3.484zm-6.616-3.334l-4.334 6.5c-.145.217-.382.334-.625.334-.143 0-.288-.04-.416-.126l-.115-.094-2.415-2.415c-.293-.293-.293-.768 0-1.06s.768-.294 1.06 0l1.77 1.767 3.825-5.74c.23-.345.696-.436 1.04-.207.346.23.44.696.21 1.04z"/>
                </svg>
              </div>
              <div class="account-handle">@{{ account.username }}</div>
              <div class="account-followers">{{ account.followers }} followers</div>
            </div>
            
            <!-- Rank Badge -->
            <div class="rank-badge" :class="getRankClass(index)">
              <span class="rank-number">#{{ Number(index) + 1 }}</span>
              <span class="rank-in">in</span>
              <span class="rank-topic">{{ currentTopic }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Category Buttons (below results) -->
      <div class="category-section">
        <h3 class="category-section-title">Explore Other Categories</h3>
        <div class="category-grid">
          <button
            v-for="category in categories"
            :key="category"
            class="category-btn"
            :class="{ selected: selectedCategory === category }"
            @click="selectCategory(category)"
          >
            {{ category }}
          </button>
        </div>
      </div>
    </div>

    <!-- Browse Categories (when no results) -->
    <template v-else>
      <!-- Category Title -->
      <div class="category-header">
        <h2 class="category-title">Browse by Category</h2>
        <p class="category-subtitle">Select a topic to explore the Authority Index</p>
      </div>

      <!-- Category Grid -->
      <div class="category-grid">
        <button
          v-for="category in categories"
          :key="category"
          class="category-btn"
          :class="{ selected: selectedCategory === category }"
          @click="selectCategory(category)"
        >
          {{ category }}
        </button>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
const config = useRuntimeConfig()

const props = defineProps<{
  keyword: string
}>()

const emit = defineEmits<{
  (e: 'select-account', account: AuthorityAccount): void
}>()

// Types
interface AuthorityAccount {
  id: string
  displayName: string
  username: string
  avatar: string
  followers: string
  following: string
  verified: boolean
  description: string
}

interface ApiAccount {
  id: string
  username: string
  name: string
  description: string
  profile_image_url: string
  verified: boolean
  public_metrics: {
    followers_count: number
    following_count: number
    tweet_count: number
  }
}

const selectedCategory = ref<string | null>(null)
const showResults = ref(false)
const currentTopic = ref('F1')
const loading = ref(false)

const categories = [
  'Aerospace',
  'Agriculture',
  'Animals',
  'Automotive',
  'Business',
  'Companies',
  'Culture',
  'Education',
  'Energy',
  'Entertainment',
  'Environment & Sustainability',
  'Financial',
  'Food/Beverages',
  'Healthcare',
  'Home & Garden',
  'IT/Tech',
  'Lifestage',
  'Lifestyle',
  'Locations',
  'Media',
  'Non Profit',
  'Politics',
  'Recreational Activities',
  'Religion',
  'Science',
  'Service',
  'Sports',
  'Adult / 18+',
]

// Reactive accounts data
const authorityAccounts = ref<AuthorityAccount[]>([])

// Fallback F1 Authority accounts (no longer used but kept for reference)
const fallbackF1Accounts: AuthorityAccount[] = []

// Format follower count
const formatFollowers = (count: number): string => {
  if (count >= 1000000) return (count / 1000000).toFixed(1).replace(/\.0$/, '') + 'M'
  if (count >= 1000) return (count / 1000).toFixed(1).replace(/\.0$/, '') + 'K'
  return count.toString()
}

// Fetch accounts from API
const fetchAccounts = async (keyword: string) => {
  loading.value = true
  authorityAccounts.value = [] // Reset while loading
  showResults.value = true

  try {
    // Step 1: Fetch IDs for the keyword (backend returns strings)
    const idsResponse = await $fetch<{ ids: string[] }>(
      `${config.public.apiBase}/grokathon/fetch-ids/?input_query=${encodeURIComponent(keyword)}`
    )

    if (!idsResponse.ids || idsResponse.ids.length === 0) {
      return // No results found
    }

    // Take up to 100 IDs (full index)
    const idsToFetch = idsResponse.ids.slice(0, 100)

    // Step 2: Fetch account details
    const idsParams = idsToFetch.map((id: string) => `ids=${id}`).join('&')
    const accountsResponse = await $fetch<{ accounts: ApiAccount[] }>(
      `${config.public.apiBase}/grokathon/fetch-accounts/?${idsParams}`
    )

    if (accountsResponse.accounts && accountsResponse.accounts.length > 0) {
      // Map API response to authority account format
      // The order from the API determines the ranking
      authorityAccounts.value = accountsResponse.accounts.map((acc: ApiAccount) => ({
        id: acc.id,
        displayName: acc.name,
        username: acc.username,
        avatar: acc.profile_image_url || '',
        followers: formatFollowers(acc.public_metrics?.followers_count || 0),
        following: formatFollowers(acc.public_metrics?.following_count || 0),
        verified: acc.verified || false,
        description: acc.description || ''
      }))
    }
  } catch (err) {
    console.error('Error fetching accounts:', err)
    // Keep empty on error
  } finally {
    loading.value = false
  }
}

const selectCategory = async (category: string) => {
  selectedCategory.value = category
  currentTopic.value = category
  await fetchAccounts(category)
}

// Watch for keyword changes from parent
watch(() => props.keyword, (newKeyword: string) => {
  if (newKeyword) {
    currentTopic.value = newKeyword
    fetchAccounts(newKeyword)
  }
}, { immediate: true })

const getRankClass = (index: number) => {
  if (index === 0) return 'rank-gold'
  return 'rank-silver'
}
</script>

<style scoped>
.index-container {
  max-width: 1200px;
  margin: 0 auto;
}

/* Prompt Bar */
.prompt-bar-container {
  margin-bottom: 2.5rem;
}

.prompt-bar {
  display: flex;
  align-items: center;
  background-color: #16181c;
  border-radius: 50px;
  border: 1px solid #2f3336;
  transition: border-color 0.2s ease;
}

.prompt-bar:focus-within {
  border-color: #fff;
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
  color: #e7e9ea;
  font-family: inherit;
}

.prompt-input::placeholder {
  color: #71767b;
}

.prompt-clear {
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: none;
  padding: 0.5rem;
  color: #71767b;
  cursor: pointer;
  transition: color 0.15s ease;
}

.prompt-clear:hover {
  color: #e7e9ea;
}

.prompt-submit {
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: none;
  padding: 0.75rem 1rem;
  color: #fff;
  cursor: pointer;
  transition: opacity 0.15s ease;
}

.prompt-submit:hover:not(:disabled) {
  opacity: 0.7;
}

.prompt-submit:disabled {
  color: #38444d;
  cursor: not-allowed;
}

/* Results Header */
.results-header {
  text-align: center;
  margin-bottom: 2rem;
}

.results-title {
  font-size: 1.75rem;
  font-weight: 700;
  color: #e7e9ea;
  margin-bottom: 0.5rem;
}

.results-subtitle {
  font-size: 1rem;
  color: #71767b;
}

.topic-highlight {
  color: #1d9bf0;
  font-weight: 600;
}

/* Loading State */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
}

.spinner {
  width: 48px;
  height: 48px;
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
  margin-top: 1.25rem;
  color: #71767b;
  font-size: 0.95rem;
}

/* Authority Grid */
.authority-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

.authority-card {
  background-color: #16181c;
  border: 1px solid #2f3336;
  border-radius: 16px;
  padding: 1rem 1.25rem;
  transition: all 0.15s ease;
  cursor: pointer;
}

.authority-card:hover {
  border-color: #3f4347;
  background-color: #1d1f23;
}

/* Account Row */
.account-row {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

/* Rank Badge */
.rank-badge {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  background-color: #2f3336;
  border-radius: 50px;
  padding: 0.5rem 0.85rem;
  margin-left: auto;
  flex-shrink: 0;
}

.rank-number {
  font-size: 0.85rem;
  font-weight: 700;
  color: #e7e9ea;
}

.rank-in {
  font-size: 0.7rem;
  color: #71767b;
  font-weight: 400;
}

.rank-topic {
  font-size: 0.85rem;
  font-weight: 600;
  color: #1d9bf0;
}

.rank-badge.rank-gold {
  background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
}

.rank-badge.rank-gold .rank-number,
.rank-badge.rank-gold .rank-in,
.rank-badge.rank-gold .rank-topic {
  color: #000;
}

.rank-badge.rank-silver {
  background: linear-gradient(135deg, #C0C0C0 0%, #A8A8A8 100%);
}

.rank-badge.rank-silver .rank-number,
.rank-badge.rank-silver .rank-in,
.rank-badge.rank-silver .rank-topic {
  color: #000;
}

/* Account Avatar */
.account-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  overflow: hidden;
  flex-shrink: 0;
}

.account-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.account-details {
  flex: 1;
  min-width: 0;
}

.account-name-row {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  margin-bottom: 0.1rem;
  max-width: 100%;
  overflow: hidden;
}

.account-name {
  font-weight: 700;
  color: #e7e9ea;
  font-size: 0.95rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 180px;
}

.verified-badge {
  flex-shrink: 0;
}

.account-handle {
  color: #71767b;
  font-size: 0.85rem;
  margin-bottom: 0.1rem;
}

.account-followers {
  color: #71767b;
  font-size: 0.8rem;
}

/* Category Section (below results) */
.category-section {
  margin-top: 3rem;
  padding-top: 2rem;
  border-top: 1px solid #2f3336;
}

.category-section-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #71767b;
  margin-bottom: 1.25rem;
  text-align: center;
}

/* Category Header */
.category-header {
  text-align: center;
  margin-bottom: 2rem;
}

.category-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #e7e9ea;
  margin-bottom: 0.5rem;
}

.category-subtitle {
  font-size: 0.95rem;
  color: #71767b;
}

/* Category Grid */
.category-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
}

.category-btn {
  background-color: transparent;
  border: 1px solid #2f3336;
  border-radius: 12px;
  padding: 1rem 1.25rem;
  color: #e7e9ea;
  font-size: 0.95rem;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.15s ease;
  text-align: center;
}

.category-btn:hover {
  background-color: #16181c;
  border-color: #3f4347;
}

.category-btn.selected {
  background-color: #16181c;
  border-color: #fff;
}

/* Responsive */
@media (max-width: 900px) {
  .authority-grid {
    grid-template-columns: 1fr;
  }
  
  .category-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 600px) {
  .category-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .category-btn {
    padding: 0.85rem 1rem;
    font-size: 0.9rem;
  }
  
  .account-avatar {
    width: 40px;
    height: 40px;
  }
  
  .account-name {
    font-size: 0.9rem;
  }
  
  .rank-badge {
    padding: 0.4rem 0.7rem;
  }
  
  .rank-number,
  .rank-topic {
    font-size: 0.75rem;
  }
  
  .rank-in {
    font-size: 0.6rem;
  }
}
</style>
