<template>
  <div class="categories-container">
    <!-- Breadcrumb navigation -->
    <div class="breadcrumb" v-if="breadcrumbs.length > 0">
      <button class="breadcrumb-item" @click="goToLevel(0)">
        All Categories
      </button>
      <template v-for="(crumb, idx) in breadcrumbs" :key="crumb.id">
        <span class="breadcrumb-separator">›</span>
        <button 
          class="breadcrumb-item"
          :class="{ active: idx === breadcrumbs.length - 1 }"
          @click="goToLevel(Number(idx) + 1)"
        >
          {{ crumb.name }}
        </button>
      </template>
    </div>
    
    <p class="results-subtitle" v-else>
      Explore categories
    </p>
    
    <div v-if="loading" class="loading-state">
      <div class="loading-spinner"></div>
      <span>Loading categories...</span>
    </div>
    
    <div v-else-if="categories.length === 0" class="empty-state">
      <p>No subcategories found</p>
      <button class="back-btn" @click="goBack" v-if="breadcrumbs.length > 0">
        ← Go back
      </button>
    </div>
    
    <div v-else class="category-grid">
      <button
        v-for="category in categories"
        :key="category.id"
        class="category-btn"
        @click="selectCategory(category)"
      >
        {{ category.name }}
      </button>
    </div>

    <!-- Authority Index for selected category -->
    <div v-if="currentCategory" class="authority-section">
      <!-- Authority header with title and country selector -->
      <div class="authority-header">
        <h3 class="authority-title">
          Top <span v-if="!loadingAuthority && authorityAccounts.length > 0">{{ authorityAccounts.length }}</span> authorities in <span class="topic-highlight">{{ currentCategory }}{{ selectedCountry !== 'USA' ? ` in ${getCountryName(selectedCountry)}` : '' }}</span>
        </h3>
        <div class="country-selector">
          <label for="country-select" class="country-label">Region:</label>
          <select id="country-select" v-model="selectedCountry" @change="onCountryChange" class="country-dropdown">
            <option v-for="country in countries" :key="country.code" :value="country.code">
              {{ country.flag }} {{ country.name }}
            </option>
          </select>
        </div>
      </div>

      <div v-if="loadingAuthority" class="loading-authority">
        <div class="loading-spinner"></div>
        <span>Loading...</span>
      </div>

      <template v-else-if="authorityAccounts.length > 0">
        
        <div class="authority-grid">
          <div 
            v-for="(account, index) in authorityAccounts" 
            :key="account.username" 
            class="authority-card"
            @click="emit('select-account', account)"
          >
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
              
              <div class="rank-badge" :class="getRankClass(index)">
                <span class="rank-number">#{{ Number(index) + 1 }}</span>
              </div>
            </div>
          </div>
        </div>
      </template>

      <div v-else-if="!loadingAuthority" class="empty-authority">
        <p>No authorities found for this category{{ selectedCountry !== 'USA' ? ` in ${getCountryName(selectedCountry)}` : '' }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const config = useRuntimeConfig()

// Types
interface Classifier {
  name: string
  parent_id: number | null
  group: string | null
  level: number
}

type ClassifiersData = Record<string, Classifier>

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

// Emits
const emit = defineEmits<{
  (e: 'select-account', account: AuthorityAccount): void
}>()

// Countries
const countries = [
  { code: 'USA', name: 'United States', flag: '🇺🇸' },
  { code: 'UK', name: 'United Kingdom', flag: '🇬🇧' },
  { code: 'Netherlands', name: 'Netherlands', flag: '🇳🇱' },
  { code: 'Japan', name: 'Japan', flag: '🇯🇵' },
]

// State
const classifiers = ref<ClassifiersData>({})
const categories = ref<{ id: string; name: string }[]>([])
const loading = ref(true)
const breadcrumbs = ref<{ id: string; name: string }[]>([])
const loadingAuthority = ref(false)
const authorityAccounts = ref<AuthorityAccount[]>([])
const currentCategory = ref('')
const selectedCountry = ref('USA')

// Categories to exclude from display
const excludedPrefixes = ['ALIAS FOR', 'No Path', 'Pro Sentiment', 'Retriever Test', 'Fossil Hunter']

const isValidCategory = (name: string): boolean => {
  return !excludedPrefixes.some(prefix => name.startsWith(prefix))
}

// Format follower count
const formatFollowers = (count: number): string => {
  if (count >= 1000000) return (count / 1000000).toFixed(1).replace(/\.0$/, '') + 'M'
  if (count >= 1000) return (count / 1000).toFixed(1).replace(/\.0$/, '') + 'K'
  return count.toString()
}

// Get rank class for styling
const getRankClass = (index: number) => {
  if (index === 0) return 'rank-gold'
  if (index === 1) return 'rank-silver'
  if (index === 2) return 'rank-bronze'
  return 'rank-default'
}

// Get country name from code
const getCountryName = (code: string): string => {
  const country = countries.find(c => c.code === code)
  return country?.name || code
}

// Handle country change
const onCountryChange = () => {
  if (currentCategory.value) {
    fetchAuthorityAccounts(currentCategory.value)
  }
}

// Fetch authority accounts for a category
const fetchAuthorityAccounts = async (categoryName: string) => {
  loadingAuthority.value = true
  currentCategory.value = categoryName
  authorityAccounts.value = []

  // Build query with country if not USA
  const query = selectedCountry.value === 'USA' 
    ? categoryName 
    : `${categoryName} in ${getCountryName(selectedCountry.value)}`

  try {
    // Step 1: Fetch IDs for the category
    const idsResponse = await $fetch<{ ids: string[] }>(
      `${config.public.apiBase}/grokathon/fetch-ids/?input_query=${encodeURIComponent(query)}`
    )

    if (!idsResponse.ids || idsResponse.ids.length === 0) {
      return // No results found
    }

    // Take up to 20 IDs for the category view
    const idsToFetch = idsResponse.ids.slice(0, 20)

    // Step 2: Fetch account details
    const idsParams = idsToFetch.map((id: string) => `ids=${id}`).join('&')
    const accountsResponse = await $fetch<{ accounts: ApiAccount[] }>(
      `${config.public.apiBase}/grokathon/fetch-accounts/?${idsParams}`
    )

    if (accountsResponse.accounts && accountsResponse.accounts.length > 0) {
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
    console.error('Error fetching authority accounts:', err)
  } finally {
    loadingAuthority.value = false
  }
}

const loadClassifiers = async () => {
  loading.value = true
  try {
    const response = await fetch('/classifiersroot.json')
    classifiers.value = await response.json()
    showRootCategories()
  } catch (error) {
    console.error('Failed to load classifiers:', error)
    categories.value = []
  } finally {
    loading.value = false
  }
}

const showRootCategories = () => {
  // Get level 1 categories
  const entries = Object.entries(classifiers.value) as [string, Classifier][]
  const level1 = entries
    .filter(([_, v]) => v.level === 1 && isValidCategory(v.name))
    .map(([id, v]) => ({ id, name: v.name }))
    .sort((a, b) => a.name.localeCompare(b.name))
  categories.value = level1
  // Clear authority accounts when going to root
  authorityAccounts.value = []
  currentCategory.value = ''
}

const getChildren = (parentId: string): { id: string; name: string }[] => {
  const parentIdNum = parseInt(parentId)
  const entries = Object.entries(classifiers.value) as [string, Classifier][]
  return entries
    .filter(([_, v]) => v.parent_id === parentIdNum && isValidCategory(v.name))
    .map(([id, v]) => ({ id, name: v.name }))
    .sort((a, b) => a.name.localeCompare(b.name))
}

const selectCategory = (category: { id: string; name: string }) => {
  const children = getChildren(category.id)
  if (children.length > 0) {
    breadcrumbs.value.push(category)
    categories.value = children
  }
  // Always fetch authority accounts when clicking a category
  fetchAuthorityAccounts(category.name)
}

const goToLevel = (level: number) => {
  if (level === 0) {
    // Go back to root
    breadcrumbs.value = []
    showRootCategories()
  } else {
    // Go to specific level
    breadcrumbs.value = breadcrumbs.value.slice(0, level)
    const parent = breadcrumbs.value[breadcrumbs.value.length - 1]
    categories.value = getChildren(parent.id)
    // Fetch authority for the level we navigated to
    fetchAuthorityAccounts(parent.name)
  }
}

const goBack = () => {
  if (breadcrumbs.value.length > 0) {
    goToLevel(breadcrumbs.value.length - 1)
  }
}

onMounted(() => {
  loadClassifiers()
})
</script>

<style scoped>
.categories-container {
  width: 100%;
}

.breadcrumb {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.25rem;
  margin-bottom: 1.5rem;
  padding: 0.75rem 1rem;
  background: #16181c;
  border-radius: 8px;
}

.breadcrumb-item {
  background: none;
  border: none;
  color: #1d9bf0;
  font-size: 0.9rem;
  font-family: inherit;
  cursor: pointer;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  transition: background 0.15s ease;
}

.breadcrumb-item:hover {
  background: rgba(29, 155, 240, 0.1);
}

.breadcrumb-item.active {
  color: #e7e9ea;
  cursor: default;
}

.breadcrumb-item.active:hover {
  background: none;
}

.breadcrumb-separator {
  color: #71767b;
  font-size: 0.9rem;
}

.results-subtitle {
  font-size: 1rem;
  color: #71767b;
  text-align: center;
  margin-bottom: 1.5rem;
}

.loading-state,
.loading-authority {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  padding: 2rem;
  color: #71767b;
}

.loading-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid #2f3336;
  border-top-color: #1d9bf0;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  padding: 2rem;
  color: #71767b;
}

.back-btn {
  background: none;
  border: 1px solid #2f3336;
  border-radius: 8px;
  padding: 0.5rem 1rem;
  color: #1d9bf0;
  font-size: 0.9rem;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.15s ease;
}

.back-btn:hover {
  background: #16181c;
  border-color: #1d9bf0;
}

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

/* Authority Section */
.authority-section {
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid #2f3336;
}

.authority-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 1.25rem;
  flex-wrap: wrap;
}

.authority-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #e7e9ea;
  margin: 0;
}

.country-selector {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.country-label {
  color: #71767b;
  font-size: 0.85rem;
}

.country-dropdown {
  background-color: #16181c;
  border: 1px solid #2f3336;
  border-radius: 8px;
  padding: 0.4rem 0.75rem;
  color: #e7e9ea;
  font-size: 0.85rem;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.15s ease;
}

.country-dropdown:hover {
  border-color: #3f4347;
}

.country-dropdown:focus {
  outline: none;
  border-color: #1d9bf0;
}

.country-dropdown option {
  background-color: #16181c;
  color: #e7e9ea;
  padding: 0.5rem;
}

.empty-authority {
  padding: 2rem;
  text-align: center;
  color: #71767b;
}

.topic-highlight {
  color: #1d9bf0;
}

.authority-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

.authority-card {
  background-color: #16181c;
  border: 1px solid #2f3336;
  border-radius: 12px;
  padding: 1rem;
  transition: all 0.15s ease;
  cursor: pointer;
}

.authority-card:hover {
  border-color: #3f4347;
  background-color: #1d1f23;
}

.account-row {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.account-avatar {
  width: 44px;
  height: 44px;
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
}

.account-name {
  font-weight: 700;
  color: #e7e9ea;
  font-size: 0.9rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 150px;
}

.verified-badge {
  flex-shrink: 0;
}

.account-handle {
  color: #71767b;
  font-size: 0.8rem;
  margin-bottom: 0.1rem;
}

.account-followers {
  color: #71767b;
  font-size: 0.75rem;
}

.rank-badge {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  flex-shrink: 0;
  background-color: #2f3336;
}

.rank-number {
  font-size: 0.75rem;
  font-weight: 700;
  color: #e7e9ea;
}

.rank-badge.rank-gold {
  background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
}

.rank-badge.rank-gold .rank-number {
  color: #000;
}

.rank-badge.rank-silver {
  background: linear-gradient(135deg, #C0C0C0 0%, #A8A8A8 100%);
}

.rank-badge.rank-silver .rank-number {
  color: #000;
}

.rank-badge.rank-bronze {
  background: linear-gradient(135deg, #CD7F32 0%, #B87333 100%);
}

.rank-badge.rank-bronze .rank-number {
  color: #000;
}

/* Responsive */
@media (max-width: 900px) {
  .category-grid {
    grid-template-columns: repeat(3, 1fr);
  }
  
  .authority-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 600px) {
  .breadcrumb {
    padding: 0.5rem 0.75rem;
  }
  
  .breadcrumb-item {
    font-size: 0.85rem;
  }
  
  .category-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .category-btn {
    padding: 0.85rem 1rem;
    font-size: 0.9rem;
  }
  
  .authority-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }
  
  .authority-title {
    font-size: 1rem;
  }
  
  .account-avatar {
    width: 36px;
    height: 36px;
  }
  
  .account-name {
    font-size: 0.85rem;
    max-width: 120px;
  }
}
</style>
