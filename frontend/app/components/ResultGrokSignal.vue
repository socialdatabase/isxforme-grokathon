<template>
  <div class="groksignal-container">
    <div class="groksignal-layout">
      <!-- Chat Section -->
      <div class="groksignal-chat">
        <!-- Experts Found -->
        <div class="grok-accordion">
          <button class="accordion-header" @click="toggleEntities">
            <span>{{ entitiesCountDisplay }}</span>
            <div v-if="entityAvatars.length > 0" class="entity-avatars">
              <img v-for="(avatar, index) in entityAvatars" :key="index" :src="avatar" alt="Entity" class="entity-avatar" />
            </div>
            <svg class="accordion-arrow" :class="{ open: entitiesOpen }" width="20" height="20" viewBox="0 0 24 24" fill="none">
              <path d="M6 9L12 15L18 9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
          <div v-if="entitiesOpen" class="accordion-content">
            <div v-if="loadingEntities || loadingFilteredEntities" class="entity-loading">
              <div class="spinner-small"></div>
              <span>Loading experts...</span>
            </div>
            <div v-else class="entity-list">
              <div v-for="account in entityAccounts" :key="account.username" class="entity-item">
                <img :src="account.avatar" :alt="account.displayName" />
                <span>{{ account.displayName }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Content Sources -->
        <div class="grok-accordion">
          <button class="accordion-header" @click="toggleSources">
            <span>{{ contentPostsCountDisplay }}</span>
            <svg class="accordion-arrow" :class="{ open: sourcesOpen }" width="20" height="20" viewBox="0 0 24 24" fill="none">
              <path d="M6 9L12 15L18 9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
          <div v-if="sourcesOpen" class="accordion-content">
            <div v-if="loadingPosts || loadingFilteredPosts" class="entity-loading">
              <div class="spinner-small"></div>
              <span>Loading posts...</span>
            </div>
            <div v-else-if="contentPosts.length > 0" class="content-posts-list">
              <div v-for="post in contentPosts" :key="post.id" class="content-post-item">
                <img :src="post.avatar" :alt="post.username" class="content-post-avatar" />
                <div class="content-post-body">
                  <a :href="`https://x.com/${post.username}/status/${post.id}`" target="_blank" class="content-post-link">
                    <span class="content-post-username">@{{ post.username }}</span>
                    <span class="content-post-text">{{ truncateText(post.text, 80) }}</span>
                  </a>
                  <span class="content-post-likes">❤️ {{ formatNumber(post.likes) }}</span>
                </div>
              </div>
            </div>
            <p v-else class="no-posts">No posts found</p>
          </div>
        </div>

        <!-- User Query -->
        <div class="grok-query">
          <span class="grok-query-text">{{ currentQuestion }}</span>
        </div>

        <!-- LLM Response -->
        <div class="grok-response">
          <div v-if="loadingGrokResponse && !displayedResponse" class="response-loading">
            <div class="spinner-small"></div>
            <span>Analyzing expert views...</span>
          </div>
          <template v-else>
          <p v-html="displayedResponse"></p>
          <span v-if="isTyping" class="typing-cursor">|</span>
          </template>
        </div>

        <!-- Follow-up Prompt -->
        <form class="grok-followup" @submit.prevent="handleFollowup">
          <input
            v-model="grokFollowup"
            type="text"
            class="followup-input"
            placeholder="Ask a follow-up question..."
          />
          <button type="submit" class="followup-submit" :disabled="!grokFollowup.trim()">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
              <path d="M5 12H19M19 12L12 5M19 12L12 19" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
        </form>
      </div>

      <!-- Expert Views Sidebar -->
      <div class="expert-views">
        <h3 class="expert-title">Expert Views</h3>
        <p class="expert-subtitle">Filter by perspective</p>
        <div class="expert-categories">
          <div v-if="loadingCategories" class="categories-loading">
            <div class="spinner-small"></div>
            <span>Loading categories...</span>
          </div>
          <template v-else-if="expertCategories.length > 0">
          <button 
            v-for="category in expertCategories" 
            :key="category.name"
            class="expert-category"
            :class="{ active: selectedExpertView === category.name }"
            @click="selectExpertView(category.name)"
          >
            <span class="category-name">{{ category.name }}</span>
            <span class="category-count">{{ category.count }}</span>
          </button>
          </template>
          <p v-else class="no-categories">No expert categories found</p>
        </div>
        
        <!-- Start Debate Button -->
        <button class="start-debate-btn" @click="emit('start-debate')">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
            <path d="M21 15C21 15.5304 20.7893 16.0391 20.4142 16.4142C20.0391 16.7893 19.5304 17 19 17H7L3 21V5C3 4.46957 3.21071 3.96086 3.58579 3.58579C3.96086 3.21071 4.46957 3 5 3H19C19.5304 3 20.0391 3.21071 20.4142 3.58579C20.7893 3.96086 21 4.46957 21 5V15Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          Start Debate
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const config = useRuntimeConfig()

const props = defineProps<{
  isActive: boolean
  keyword?: string
}>()

const emit = defineEmits<{
  (e: 'start-debate'): void
}>()

// Types
interface EntityAccount {
  id: string
  displayName: string
  username: string
  avatar: string
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

interface ContentPost {
  id: string
  text: string
  username: string
  avatar: string
  likes: number
  created_at: string
  photo: string | null
}

interface ApiPost {
  post: {
    id: string
    text: string
    created_at: string
    account_id: string
    retweet_count: number | null
    reply_count: number | null
    like_count: number | null
    impression_count: number | null
    media: any[] | null
  }
  account: {
    id: string
    username: string
    verified: boolean | null
    profile_image_url: string | null
  }
}

const entitiesOpen = ref(false)
const sourcesOpen = ref(false)
const isTyping = ref(false)
const displayedResponse = ref('')
const grokFollowup = ref('')
const selectedExpertView = ref<string | null>(null)
const loadingEntities = ref(true)
const loadingCategories = ref(true)
const loadingPosts = ref(true)
const loadingFilteredPosts = ref(false)
const totalEntitiesCount = ref(0)
const loadingGrokResponse = ref(false)
const grokResponseLoaded = ref(false)

// Conversation history for follow-up questions
interface ConversationMessage {
  role: 'user' | 'assistant'
  content: string
}
const conversationHistory = ref<ConversationMessage[]>([])

// Computed for dynamic question based on topic and selected expert view
const currentQuestion = computed(() => {
  const topic = props.keyword
  if (!topic) return 'Waiting for topic...'
  if (selectedExpertView.value) {
    return `What do ${selectedExpertView.value} think about ${topic}?`
  }
  return `What are the latest expert views on ${topic}?`
})

// Posts for "Content found on" section
const allContentPosts = ref<ContentPost[]>([])
const filteredContentPosts = ref<ContentPost[]>([])

// Use filtered posts when a category is selected, otherwise all posts
const contentPosts = computed(() => 
  selectedExpertView.value ? filteredContentPosts.value : allContentPosts.value
)

// Store all fetched IDs (up to 100) for expert categories
const allEntityIds = ref<string[]>([])

// Fetched accounts data (all entities)
const allEntityAccounts = ref<EntityAccount[]>([])

// Filtered accounts for selected expert category
const filteredEntityAccounts = ref<EntityAccount[]>([])
const filteredEntitiesCount = ref(0)
const loadingFilteredEntities = ref(false)

// Expert categories from API
interface ExpertCategory {
  name: string
  count: number | string
  ids: number[]
}
const expertCategories = ref<ExpertCategory[]>([])

// Use filtered accounts when a category is selected, otherwise all accounts
const displayedEntityAccounts = computed(() => 
  selectedExpertView.value ? filteredEntityAccounts.value : allEntityAccounts.value
)

const displayedEntitiesCount = computed(() => 
  selectedExpertView.value ? filteredEntitiesCount.value : totalEntitiesCount.value
)

// Top 10 avatars for header
const entityAvatars = computed(() => 
  displayedEntityAccounts.value.slice(0, 10).map(acc => acc.avatar)
)

// Top 25 accounts for expanded list
const entityAccounts = computed(() => 
  displayedEntityAccounts.value.slice(0, 25)
)

// Fetch expert categories from API
const fetchExpertCategories = async (ids: string[]) => {
  if (ids.length === 0) return
  
  loadingCategories.value = true
  
  try {
    const idsParams = ids.map((id: string) => `ids=${id}`).join('&')
    const response = await $fetch<{ categories: Record<string, number[]> }>(
      `${config.public.apiBase}/grokathon/fetch-expert-categories/?${idsParams}`
    )
    
    if (response.categories) {
      // Convert the categories object to an array format for the UI
      expertCategories.value = Object.entries(response.categories)
        .map(([name, categoryIds]: [string, number[]]) => ({
          name,
          count: categoryIds.length >= 1000 ? `${Math.floor(categoryIds.length / 1000)}K+` : categoryIds.length,
          ids: categoryIds
        }))
        .sort((a, b) => {
          // Sort by count (descending)
          const countA = typeof a.count === 'string' ? parseInt(a.count) * 1000 : a.count
          const countB = typeof b.count === 'string' ? parseInt(b.count) * 1000 : b.count
          return countB - countA
        })
    }
  } catch (err) {
    console.error('Error fetching expert categories:', err)
  } finally {
    loadingCategories.value = false
  }
}

// Fetch accounts from API
const fetchEntities = async (keyword: string) => {
  loadingEntities.value = true
  allEntityAccounts.value = []
  allEntityIds.value = []
  expertCategories.value = []

  try {
    // Step 1: Fetch IDs for the keyword
    const idsResponse = await $fetch<{ ids: string[] }>(
      `${config.public.apiBase}/grokathon/fetch-ids/?input_query=${encodeURIComponent(keyword)}`
    )

    if (!idsResponse.ids || idsResponse.ids.length === 0) {
      return
    }

    // Store total count for display
    totalEntitiesCount.value = idsResponse.ids.length

    // Store top 100 IDs for expert categories
    allEntityIds.value = idsResponse.ids.slice(0, 100)

    // Take up to 25 IDs for the entity list display
    const idsToFetch = idsResponse.ids.slice(0, 25)

    // Step 2: Fetch account details
    const idsParams = idsToFetch.map((id: string) => `ids=${id}`).join('&')
    const accountsResponse = await $fetch<{ accounts: ApiAccount[] }>(
      `${config.public.apiBase}/grokathon/fetch-accounts/?${idsParams}`
    )

    if (accountsResponse.accounts && accountsResponse.accounts.length > 0) {
      allEntityAccounts.value = accountsResponse.accounts.map((acc: ApiAccount) => ({
        id: acc.id,
        displayName: acc.name,
        username: acc.username,
        avatar: acc.profile_image_url || ''
      }))
    }

    // Step 3: Fetch expert categories with top 100 IDs
    await fetchExpertCategories(allEntityIds.value)
    
    // Step 4: Fetch posts for "Content found on" section
    await fetchContentPosts(allEntityIds.value)
  } catch (err) {
    console.error('Error fetching entities:', err)
  } finally {
    loadingEntities.value = false
  }
}

// Fetch posts for "Content found on" section
const fetchContentPosts = async (ids: string[]) => {
  if (ids.length === 0) return
  
  loadingPosts.value = true
  allContentPosts.value = []
  
  try {
    // Take top 20 accounts to fetch posts from (20 posts per account = up to 400 posts)
    const idsToFetch = ids.slice(0, 20)
    const idsParams = idsToFetch.map((id: string) => `ids=${id}`).join('&')
    
    const response = await $fetch<{ posts: ApiPost[] }>(
      `${config.public.apiBase}/grokathon/fetch-posts/?${idsParams}`
    )
    
    if (response.posts && response.posts.length > 0) {
      // Map to ContentPost format and take top 20 by likes
      allContentPosts.value = response.posts
        .map((item: ApiPost) => {
          // Extract first media photo if available
          let photo: string | null = null
          if (item.post.media && item.post.media.length > 0) {
            const firstMedia = item.post.media[0]
            if (firstMedia.url) {
              photo = firstMedia.url
            } else if (firstMedia.preview_image_url) {
              photo = firstMedia.preview_image_url
            }
          }
          
          return {
            id: item.post.id,
            text: item.post.text,
            username: item.account.username,
            avatar: item.account.profile_image_url || '',
            likes: item.post.like_count || 0,
            created_at: item.post.created_at,
            photo
          }
        })
        .sort((a: ContentPost, b: ContentPost) => b.likes - a.likes)
        .slice(0, 20)
    }
  } catch (err) {
    console.error('Error fetching content posts:', err)
  } finally {
    loadingPosts.value = false
  }
}

// Computed display for entity count
const entitiesCountDisplay = computed(() => {
  if (loadingEntities.value || loadingFilteredEntities.value) return 'Loading experts...'
  const count = displayedEntitiesCount.value
  if (count === 0) return 'No experts found'
  if (count >= 1000) return `${Math.floor(count / 1000)}K+ experts found...`
  return `${count}+ experts found...`
})

// Computed display for content posts count
const contentPostsCountDisplay = computed(() => {
  if (loadingPosts.value || loadingFilteredPosts.value) return 'Loading content...'
  if (contentPosts.value.length === 0) return 'Content found on:'
  return `Content found on: ${contentPosts.value.length} posts`
})

// Helper functions
const truncateText = (text: string, maxLength: number): string => {
  if (text.length <= maxLength) return text
  return text.slice(0, maxLength).trim() + '...'
}

const formatNumber = (num: number): string => {
  if (num >= 1000000) return (num / 1000000).toFixed(1).replace(/\.0$/, '') + 'M'
  if (num >= 1000) return (num / 1000).toFixed(1).replace(/\.0$/, '') + 'K'
  return num.toString()
}

// Stream the initial Grok overview response
const streamGrokOverview = async (ids: string[]) => {
  if (ids.length === 0 || grokResponseLoaded.value || !props.keyword) return
  
  const keyword = props.keyword
  loadingGrokResponse.value = true
  isTyping.value = true
  displayedResponse.value = ''
  
  // Reset conversation history for new topic
  conversationHistory.value = []
  const initialQuestion = `What are the latest expert views on ${keyword}?`
  
  try {
    const idsParams = ids.slice(0, 50).map((id: string) => `ids=${id}`).join('&')
    const url = `${config.public.apiBase}/grokathon/stream-expert-overview/?input_query=${encodeURIComponent(keyword)}&${idsParams}`
    
    const response = await fetch(url)
    
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
      displayedResponse.value += chunk
    }
    
    // Save to conversation history
    conversationHistory.value = [
      { role: 'user', content: initialQuestion },
      { role: 'assistant', content: displayedResponse.value }
    ]
    
    grokResponseLoaded.value = true
  } catch (err) {
    console.error('Error streaming Grok overview:', err)
    displayedResponse.value = 'Failed to load expert views. Please try again.'
  } finally {
    loadingGrokResponse.value = false
    isTyping.value = false
  }
}

// Stream the expert category perspective
const streamExpertPerspective = async (category: string, ids: number[]) => {
  if (ids.length === 0 || !props.keyword) return
  
  const keyword = props.keyword
  isTyping.value = true
  displayedResponse.value = ''
  
  // Reset conversation history for new expert category
  conversationHistory.value = []
  const initialQuestion = `What do ${category} think about ${keyword}?`
  
  try {
    const idsParams = ids.slice(0, 50).map((id: number) => `ids=${id}`).join('&')
    const url = `${config.public.apiBase}/grokathon/stream-expert-perspective/?input_query=${encodeURIComponent(keyword)}&expert_category=${encodeURIComponent(category)}&${idsParams}`
    
    const response = await fetch(url)
    
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
      displayedResponse.value += chunk
    }
    
    // Save to conversation history
    conversationHistory.value = [
      { role: 'user', content: initialQuestion },
      { role: 'assistant', content: displayedResponse.value }
    ]
  } catch (err) {
    console.error('Error streaming expert perspective:', err)
    displayedResponse.value = `Failed to load ${category} perspective. Please try again.`
  } finally {
    isTyping.value = false
  }
}

const toggleEntities = () => {
  entitiesOpen.value = !entitiesOpen.value
}

const toggleSources = () => {
  sourcesOpen.value = !sourcesOpen.value
}

// Fetch accounts for a specific expert category
const fetchCategoryAccounts = async (categoryName: string) => {
  const category = expertCategories.value.find((c: ExpertCategory) => c.name === categoryName)
  if (!category || category.ids.length === 0) return

  loadingFilteredEntities.value = true
  filteredEntityAccounts.value = []
  filteredEntitiesCount.value = category.ids.length

  try {
    // Fetch account details for up to 25 IDs from this category
    const idsToFetch = category.ids.slice(0, 25)
    const idsParams = idsToFetch.map((id: number) => `ids=${id}`).join('&')
    const accountsResponse = await $fetch<{ accounts: ApiAccount[] }>(
      `${config.public.apiBase}/grokathon/fetch-accounts/?${idsParams}`
    )

    if (accountsResponse.accounts && accountsResponse.accounts.length > 0) {
      filteredEntityAccounts.value = accountsResponse.accounts.map((acc: ApiAccount) => ({
        id: acc.id,
        displayName: acc.name,
        username: acc.username,
        avatar: acc.profile_image_url || ''
      }))
    }
  } catch (err) {
    console.error('Error fetching category accounts:', err)
  } finally {
    loadingFilteredEntities.value = false
  }
}

// Fetch posts for a specific expert category
const fetchCategoryPosts = async (categoryName: string) => {
  const category = expertCategories.value.find((c: ExpertCategory) => c.name === categoryName)
  if (!category || category.ids.length === 0) return

  loadingFilteredPosts.value = true
  filteredContentPosts.value = []

  try {
    // Fetch posts for up to 20 IDs from this category
    const idsToFetch = category.ids.slice(0, 20)
    const idsParams = idsToFetch.map((id: number) => `ids=${id}`).join('&')
    
    const response = await $fetch<{ posts: ApiPost[] }>(
      `${config.public.apiBase}/grokathon/fetch-posts/?${idsParams}`
    )

    if (response.posts && response.posts.length > 0) {
      // Map to ContentPost format and take top 20 by likes
      filteredContentPosts.value = response.posts
        .map((item: ApiPost) => {
          let photo: string | null = null
          if (item.post.media && item.post.media.length > 0) {
            const firstMedia = item.post.media[0]
            if (firstMedia.url) {
              photo = firstMedia.url
            } else if (firstMedia.preview_image_url) {
              photo = firstMedia.preview_image_url
            }
          }
          
          return {
            id: item.post.id,
            text: item.post.text,
            username: item.account.username,
            avatar: item.account.profile_image_url || '',
            likes: item.post.like_count || 0,
            created_at: item.post.created_at,
            photo
          }
        })
        .sort((a: ContentPost, b: ContentPost) => b.likes - a.likes)
        .slice(0, 20)
    }
  } catch (err) {
    console.error('Error fetching category posts:', err)
  } finally {
    loadingFilteredPosts.value = false
  }
}

const selectExpertView = async (category: string) => {
  if (selectedExpertView.value === category) {
    // Deselect - go back to showing all entities and posts with the overview response
    selectedExpertView.value = null
    filteredEntityAccounts.value = []
    filteredEntitiesCount.value = 0
    filteredContentPosts.value = []
    
    // Stream the overview response again
    if (allEntityIds.value.length > 0) {
      grokResponseLoaded.value = false // Allow re-fetching
      await streamGrokOverview(allEntityIds.value)
    }
  } else {
    // Select new category
    selectedExpertView.value = category
    displayedResponse.value = ''
    
    // Fetch accounts and posts for this category in parallel
    await Promise.all([
      fetchCategoryAccounts(category),
      fetchCategoryPosts(category)
    ])
    
    // Stream the expert category perspective
    const selectedCategory = expertCategories.value.find((c: ExpertCategory) => c.name === category)
    if (selectedCategory && selectedCategory.ids.length > 0) {
      await streamExpertPerspective(category, selectedCategory.ids)
    }
  }
}

const handleFollowup = async () => {
  const question = grokFollowup.value.trim()
  if (!question || !props.keyword) return
  
  // Get the IDs to use - either from selected category or all entities
  let idsToUse: (string | number)[] = []
  if (selectedExpertView.value) {
    const selectedCategory = expertCategories.value.find((c: ExpertCategory) => c.name === selectedExpertView.value)
    if (selectedCategory) {
      idsToUse = selectedCategory.ids
    }
  } else {
    idsToUse = allEntityIds.value
  }
  
  if (idsToUse.length === 0) return
  
  // Add separator and the user's question to displayed response
  displayedResponse.value += `<div class="followup-separator"></div><div class="followup-question">${question}</div><div class="followup-answer">`
  
  // Add to conversation history
  conversationHistory.value.push({ role: 'user', content: question })
  
  // Clear input and show typing state
    grokFollowup.value = ''
  isTyping.value = true
  
  try {
    const response = await fetch(`${config.public.apiBase}/grokathon/stream-followup/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        followup_question: question,
        conversation_history: conversationHistory.value.slice(0, -1), // Don't include the question we just added
        input_query: props.keyword,
        ids: idsToUse.slice(0, 50),
        expert_category: selectedExpertView.value || null
      })
    })
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    const reader = response.body?.getReader()
    if (!reader) {
      throw new Error('No response body')
    }
    
    const decoder = new TextDecoder()
    let followupResponse = ''
    
    while (true) {
      const { done, value } = await reader.read()
      if (done) break
      
      const chunk = decoder.decode(value, { stream: true })
      followupResponse += chunk
      displayedResponse.value += chunk
    }
    
    // Close the followup answer div
    displayedResponse.value += '</div>'
    
    // Add the completed response to conversation history
    conversationHistory.value.push({ role: 'assistant', content: followupResponse })
  } catch (err) {
    console.error('Error sending follow-up:', err)
    displayedResponse.value += 'Failed to get response. Please try again.</div>'
    // Remove the failed question from history
    conversationHistory.value.pop()
  } finally {
    isTyping.value = false
  }
}

// Track the last fetched keyword to avoid re-fetching the same data
const lastFetchedKeyword = ref<string | null>(null)

// Start streaming Grok response when component becomes active and entities are loaded
watch(() => props.isActive, (active: boolean) => {
  if (active && !selectedExpertView.value && !grokResponseLoaded.value && allEntityIds.value.length > 0) {
    // Stream the Grok overview when becoming active
    streamGrokOverview(allEntityIds.value)
  }
}, { immediate: true })

// Watch for keyword changes - fetch entities even when not active (for pre-loading)
watch(() => props.keyword, async (newKeyword: string | undefined) => {
  // Don't fetch if no keyword
  if (!newKeyword) {
    loadingEntities.value = false
    loadingCategories.value = false
    loadingPosts.value = false
    return
  }
  
  const keyword = newKeyword
  
  // Only fetch if keyword has changed
  if (keyword !== lastFetchedKeyword.value) {
    lastFetchedKeyword.value = keyword
    
    // Clear any selected expert view when keyword changes
    selectedExpertView.value = null
    filteredEntityAccounts.value = []
    filteredEntitiesCount.value = 0
    displayedResponse.value = ''
    grokResponseLoaded.value = false
    
    // Fetch entities for new keyword
    await fetchEntities(keyword)
    
    // If active and entities loaded, stream the Grok response
    if (props.isActive && allEntityIds.value.length > 0) {
      await streamGrokOverview(allEntityIds.value)
    }
  }
}, { immediate: true })
</script>

<style scoped>
.groksignal-container {
  width: 100%;
}

/* GrokSignal */
.groksignal-layout {
  display: grid;
  grid-template-columns: 1fr 300px;
  gap: 1.5rem;
  max-width: 1000px;
  margin: 0 auto;
}

.groksignal-chat {
  min-width: 0;
}

.grok-query {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 1.5rem;
}

.grok-query-text {
  background-color: #16181c;
  border: 1px solid #2f3336;
  border-radius: 20px;
  padding: 0.85rem 1.25rem;
  color: #e7e9ea;
  font-size: 0.95rem;
}

.grok-accordion {
  margin-bottom: 0.75rem;
}

.accordion-header {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  background-color: #16181c;
  border: 1px solid #2f3336;
  border-radius: 12px;
  padding: 0.85rem 1rem;
  color: #71767b;
  font-size: 0.9rem;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.15s ease;
}

.accordion-header:hover {
  background-color: #1d1f23;
}

.entity-avatars {
  display: flex;
  margin-left: auto;
  margin-right: 0.5rem;
}

.entity-avatar {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  border: 2px solid #16181c;
  margin-left: -8px;
  object-fit: cover;
}

.entity-avatar:first-child {
  margin-left: 0;
}

.accordion-arrow {
  flex-shrink: 0;
  transition: transform 0.2s ease;
}

.accordion-arrow.open {
  transform: rotate(180deg);
}

.accordion-content {
  background-color: #16181c;
  border: 1px solid #2f3336;
  border-top: none;
  border-radius: 0 0 12px 12px;
  padding: 1rem;
  margin-top: -0.5rem;
}

.entity-loading {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #71767b;
  font-size: 0.85rem;
}

.spinner-small {
  width: 16px;
  height: 16px;
  border: 2px solid #2f3336;
  border-top-color: #1d9bf0;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.response-loading {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: #71767b;
  font-size: 0.95rem;
  padding: 1rem 0;
}

.entity-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}

.entity-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background-color: #202020;
  border-radius: 50px;
  padding: 0.35rem 0.75rem 0.35rem 0.35rem;
  font-size: 0.85rem;
  color: #e7e9ea;
}

.entity-item img {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  object-fit: cover;
}

.content-posts-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  max-height: 400px;
  overflow-y: auto;
  padding-right: 0.5rem;
}

/* Custom scrollbar styling */
.content-posts-list::-webkit-scrollbar {
  width: 6px;
}

.content-posts-list::-webkit-scrollbar-track {
  background: #16181c;
  border-radius: 3px;
}

.content-posts-list::-webkit-scrollbar-thumb {
  background: #3a3f47;
  border-radius: 3px;
}

.content-posts-list::-webkit-scrollbar-thumb:hover {
  background: #4a5058;
}

.content-post-item {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  padding: 0.5rem;
  border-radius: 8px;
  transition: background-color 0.2s ease;
}

.content-post-item:hover {
  background-color: rgba(255, 255, 255, 0.03);
}

.content-post-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  flex-shrink: 0;
}

.content-post-body {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.content-post-link {
  color: #e7e9ea;
  text-decoration: none;
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
}

.content-post-link:hover {
  color: #1d9bf0;
}

.content-post-username {
  color: #1d9bf0;
  font-size: 0.8rem;
  font-weight: 500;
}

.content-post-text {
  font-size: 0.85rem;
  color: #71767b;
  line-height: 1.4;
}

.content-post-likes {
  font-size: 0.75rem;
  color: #71767b;
}

.no-posts {
  color: #71767b;
  font-size: 0.85rem;
  text-align: center;
  padding: 0.75rem;
}

.grok-response {
  margin-top: 1.5rem;
  color: #e7e9ea;
  font-size: 0.95rem;
  line-height: 1.6;
}

.grok-response :deep(h4) {
  font-size: 1.05rem;
  font-weight: 600;
  margin: 1.5rem 0 0.75rem;
  color: #fff;
}

.grok-response :deep(ul) {
  margin: 0.75rem 0;
  padding-left: 1.25rem;
}

.grok-response :deep(li) {
  margin-bottom: 0.5rem;
}

.grok-response :deep(strong) {
  color: #fff;
  font-weight: 600;
}

.typing-cursor {
  display: inline-block;
  color: #fff;
  animation: blink 0.8s infinite;
}

@keyframes blink {
  0%, 50% { opacity: 1; }
  51%, 100% { opacity: 0; }
}

.grok-followup {
  display: flex;
  align-items: center;
  background-color: #16181c;
  border-radius: 50px;
  border: 1px solid #2f3336;
  margin-top: 2rem;
  transition: border-color 0.2s ease;
}

.grok-followup:focus-within {
  border-color: #fff;
}

.followup-input {
  flex: 1;
  background: transparent;
  border: none;
  outline: none;
  padding: 0.85rem 1.25rem;
  font-size: 0.95rem;
  color: #e7e9ea;
  font-family: inherit;
}

.followup-input::placeholder {
  color: #71767b;
}

.followup-submit {
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

.followup-submit:hover:not(:disabled) {
  opacity: 0.7;
}

.followup-submit:disabled {
  color: #38444d;
  cursor: not-allowed;
}

/* Expert Views Sidebar */
.expert-views {
  background-color: #16181c;
  border-radius: 16px;
  padding: 1rem;
  height: fit-content;
  position: sticky;
  top: 1rem;
}

.expert-title {
  font-size: 1.15rem;
  font-weight: 700;
  color: #e7e9ea;
  margin-bottom: 0.25rem;
}

.expert-subtitle {
  font-size: 0.85rem;
  color: #71767b;
  margin-bottom: 1rem;
}

.expert-categories {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.categories-loading {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #71767b;
  font-size: 0.85rem;
  padding: 0.75rem;
}

.no-categories {
  color: #71767b;
  font-size: 0.85rem;
  text-align: center;
  padding: 0.75rem;
}

.expert-category {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  background: transparent;
  border: 1px solid #2f3336;
  border-radius: 12px;
  padding: 0.75rem;
  color: #e7e9ea;
  font-family: inherit;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.15s ease;
  text-align: left;
}

.expert-category:hover {
  background-color: #1d1f23;
  border-color: #3f4347;
}

.expert-category.active {
  background-color: #1d1f23;
  border-color: #fff;
}

.category-name {
  flex: 1;
  font-weight: 500;
}

.category-count {
  font-size: 0.8rem;
  color: #71767b;
}

/* Start Debate Button */
.start-debate-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  width: 100%;
  margin-top: 1rem;
  padding: 0.85rem 1rem;
  background-color: #fff;
  border: none;
  border-radius: 50px;
  color: #000;
  font-size: 0.95rem;
  font-weight: 600;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.2s ease;
}

.start-debate-btn:hover {
  background-color: #d1d1d1;
}

.grok-response :deep(blockquote) {
  background-color: #16181c;
  border-left: 3px solid #2f3336;
  margin: 1rem 0;
  padding: 0.75rem 1rem;
  border-radius: 0 8px 8px 0;
  font-style: italic;
  color: #a0a0a0;
}

.grok-response :deep(.source-link) {
  display: block;
  margin-top: 0.5rem;
  font-style: normal;
  font-size: 0.85rem;
  color: #1d9bf0;
  text-decoration: none;
}

.grok-response :deep(.source-link:hover) {
  text-decoration: underline;
}

/* Follow-up styling */
.grok-response :deep(.followup-separator) {
  height: 1px;
  background-color: #2f3336;
  margin: 2rem 0;
}

.grok-response :deep(.followup-question) {
  background-color: #16181c;
  border: 1px solid #2f3336;
  border-radius: 20px;
  padding: 0.85rem 1.25rem;
  color: #e7e9ea;
  font-size: 0.95rem;
  max-width: 80%;
  margin-left: auto;
  margin-bottom: 1.5rem;
  float: right;
  clear: both;
}

.grok-response :deep(.followup-answer) {
  clear: both;
}

@media (max-width: 900px) {
  .groksignal-layout {
    grid-template-columns: 1fr;
  }
  
  .expert-views {
    position: static;
  }
}
</style>
