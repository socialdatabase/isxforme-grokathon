<template>
  <div class="groksignal-container">
    <div class="groksignal-layout">
      <!-- Chat Section -->
      <div class="groksignal-chat">
        <!-- Entities Found -->
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
              <span>Loading...</span>
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
            <span>Content found on:</span>
            <svg class="accordion-arrow" :class="{ open: sourcesOpen }" width="20" height="20" viewBox="0 0 24 24" fill="none">
              <path d="M6 9L12 15L18 9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
          <div v-if="sourcesOpen" class="accordion-content">
            <div class="source-list">
              <a href="#" class="source-item">x.com/F1</a>
              <a href="#" class="source-item">x.com/LewisHamilton</a>
              <a href="#" class="source-item">x.com/ScuderiaFerrari</a>
              <a href="#" class="source-item">x.com/McLarenF1</a>
              <a href="#" class="source-item">x.com/redbullracing</a>
              <a href="#" class="source-item">formula1.com</a>
              <a href="#" class="source-item">motorsport.com</a>
            </div>
          </div>
        </div>

        <!-- User Query -->
        <div class="grok-query">
          <span class="grok-query-text">{{ selectedExpertView ? `What do ${selectedExpertView} think about F1?` : "What's the latest news in F1?" }}</span>
        </div>

        <!-- LLM Response -->
        <div class="grok-response">
          <p v-html="displayedResponse"></p>
          <span v-if="isTyping" class="typing-cursor">|</span>
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

const entitiesOpen = ref(false)
const sourcesOpen = ref(false)
const isTyping = ref(true)
const displayedResponse = ref('')
const typingIndex = ref(0)
const grokFollowup = ref('')
const selectedExpertView = ref<string | null>(null)
const loadingEntities = ref(true)
const loadingCategories = ref(true)
const totalEntitiesCount = ref(0)

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
  } catch (err) {
    console.error('Error fetching entities:', err)
  } finally {
    loadingEntities.value = false
  }
}

// Computed display for entity count
const entitiesCountDisplay = computed(() => {
  if (loadingEntities.value || loadingFilteredEntities.value) return 'Loading entities...'
  const count = displayedEntitiesCount.value
  if (count === 0) return 'No entities found'
  if (count >= 1000) return `${Math.floor(count / 1000)}K+ entities found...`
  return `${count}+ entities found...`
})

const grokFullResponse = `Here's the latest buzz in Formula 1 as we head into the <strong>2026 season</strong>—it's shaping up to be one of the most dramatic yet!

<h4>2026 Car Launches & Testing</h4>
The <strong>2026 season</strong> is just around the corner, and teams are already teasing their new machines. <strong>Audi</strong> made headlines by becoming the first team to run its <strong>2026 F1 car</strong> in a shakedown at Barcelona, giving fans a sneak peek at the radical new regulations. Meanwhile, <strong>Ferrari</strong> has revealed its 2026 challenger will be called the <strong>SF-26</strong>, and <strong>Cadillac</strong> (entering F1 with Andretti) has unveiled a special test livery to hide its design secrets.

<h4>Driver Market Drama</h4>
<ul>
<li><strong>Alpine</strong> has parted ways with reserve driver <strong>Jack Doohan</strong> ahead of 2026, ending months of speculation after he lost his race seat.</li>
<li><strong>Yuki Tsunoda's future</strong> is still uncertain—Honda has confirmed he hasn't signed a <strong>2026 Red Bull contract</strong> yet, with Ford's involvement complicating things.</li>
<li><strong>Isack Hadjar</strong>, Red Bull's 2026 signing, is already making waves—he's taking on a <strong>rally-raid challenge in a Ford Raptor</strong> to prepare for his F1 debut!</li>
</ul>

<h4>Engine & Regulation Updates</h4>
The FIA is holding emergency meetings with engine manufacturers to discuss a potential loophole in the 2026 power unit rules—<strong>Mercedes</strong> and <strong>Red Bull</strong> are reportedly under scrutiny.

<strong>Honda</strong> has given a first glimpse of its 2026 F1 engine, which will power Aston Martin's new superteam with <strong>Adrian Newey</strong> at the helm.

<strong>Ford</strong> has clarified its F1 timeline, insisting its partnership with Red Bull isn't just about Max Verstappen—though his future remains a hot topic.

<h4>Team & Tech Developments</h4>
<strong>McLaren</strong> has admitted mistakes in 2025 made them a "better team", with Zak Brown confident they'll carry momentum into 2026.

<strong>Aston Martin</strong> is banking on Newey's genius, Honda power, and a new wind tunnel to challenge for the title—but some analysts question if they're truly ready.

<strong>Williams</strong> isn't treating 2026 as a make-or-break year, preferring to focus on long-term progress rather than short-term results.

<h4>Fun & Off-Track News</h4>
<strong>Lewis Hamilton</strong> is switching up his training, trading his Ducati for a KTM dirt bike—apparently, mud-slinging is the new way to stay sharp!

<strong>Brad Pitt</strong> praised Hamilton's role in the upcoming F1 movie, calling him the "consultant Hollywood needed."

<strong>Lando Norris</strong> posted his first vlog since winning the 2025 title, thanking fans with an emotional message.

<h4>What's Next?</h4>
Pre-season testing kicks off in Barcelona (Feb 25-27), with all eyes on Audi, Ferrari, and Mercedes to see who's leading the pack.

Car launches are happening thick and fast—expect Red Bull, McLaren, and Mercedes to reveal their 2026 challengers soon.

The 2026 season is already shaping up to be a game-changer—new cars, new engines, and a completely reshuffled driver market. Who's your pick for the title? 🏆🚀`

const expertResponses: Record<string, string> = {
  'F1 Drivers': `From the drivers' perspective, 2026 is generating a mix of excitement and uncertainty.

<h4>Driver Reactions</h4>
<strong>Lewis Hamilton</strong> shared his thoughts on the new regulations:
<blockquote>"The 2026 cars will be a completely different beast. The focus on sustainable fuels and the new aero philosophy will challenge everything we know."
<a href="https://x.com/LewisHamilton" class="source-link">@LewisHamilton</a></blockquote>

<strong>Max Verstappen</strong> has been more cautious:
<blockquote>"I'm not worried about the changes, but it's hard to predict where everyone will be. Red Bull has a lot of work to do with the new engine partnership."
<a href="https://x.com/Max33Verstappen" class="source-link">@Max33Verstappen</a></blockquote>

<strong>Charles Leclerc</strong> is optimistic about Ferrari's chances:
<blockquote>"The SF-26 name gives me goosebumps. 2026 is our year to fight for the championship."
<a href="https://x.com/Charles_Leclerc" class="source-link">@Charles_Leclerc</a></blockquote>`,

  'Team Principals': `Team principals are taking different approaches to the 2026 regulations.

<h4>Team Leadership Views</h4>
<strong>Toto Wolff</strong> (Mercedes) sees opportunity:
<blockquote>"The regulation reset is exactly what we needed. Our 2026 power unit development has been our focus for two years."</blockquote>

<strong>Christian Horner</strong> (Red Bull) acknowledges challenges:
<blockquote>"Switching from Honda to Ford is a massive undertaking. But we've built a team capable of adapting quickly."</blockquote>

<strong>Fred Vasseur</strong> (Ferrari) is confident:
<blockquote>"The SF-26 will be the culmination of years of preparation. We have the right people in place."</blockquote>`,

  'Journalists': `F1 journalists are analyzing every detail of the 2026 shakeup.

<h4>Media Analysis</h4>
<strong>Will Buxton</strong> offers perspective:
<blockquote>"The 2026 regulations represent the biggest change in F1 since the turbo-hybrid era. Teams that adapt fastest will dominate."
<a href="https://x.com/wbuxtonofficial" class="source-link">@wbuxtonofficial</a></blockquote>

Key storylines journalists are following:
<ul>
<li>Audi's first full F1 entry and their Barcelona shakedown</li>
<li>The engine manufacturer battles between Mercedes, Ferrari, Honda, and newcomers</li>
<li>Driver market chaos with several top seats still uncertain</li>
<li>Andretti/Cadillac's entry changing the competitive landscape</li>
</ul>`,

  'Engineers': `Engineers are deep into the technical challenges of 2026.

<h4>Technical Perspectives</h4>
The new regulations bring fundamental changes:
<ul>
<li><strong>Active Aero:</strong> Engineers are developing complex movable aerodynamic systems</li>
<li><strong>Sustainable Fuels:</strong> 100% sustainable fuel requires complete powertrain redesigns</li>
<li><strong>Simplified Front Wings:</strong> Less downforce dependency, more mechanical grip focus</li>
<li><strong>Battery Technology:</strong> Increased energy recovery systems demand new solutions</li>
</ul>

Teams are hiring aggressively, with Aston Martin's new wind tunnel and Adrian Newey signing seen as major coups.`,

  'Analysts': `Data analysts are crunching numbers on 2026 predictions.

<h4>Statistical Predictions</h4>
Based on historical regulation changes:
<ul>
<li><strong>Mercedes</strong> - 35% chance of winning constructors' (strong PU development)</li>
<li><strong>Ferrari</strong> - 28% chance (best prepared chassis team)</li>
<li><strong>Red Bull</strong> - 22% chance (new engine partnership risk)</li>
<li><strong>McLaren</strong> - 10% chance (momentum from 2025)</li>
<li><strong>Others</strong> - 5% combined</li>
</ul>

Key metrics to watch: Pre-season testing pace, reliability data, and early race performance.`,

  'Fans': `The F1 fanbase is buzzing with excitement and speculation!

<h4>Fan Sentiment</h4>
Trending topics across F1 communities:
<ul>
<li>🔥 <strong>#SF26</strong> - Ferrari's car name reveal has fans hyped</li>
<li>🏆 <strong>Hamilton to Ferrari</strong> - Dream move finally happening</li>
<li>🆕 <strong>Audi F1</strong> - New team excitement is massive</li>
<li>❓ <strong>Verstappen's future</strong> - Will he stay at Red Bull?</li>
</ul>

<blockquote>"2026 is going to be the most competitive season in years. Can't wait!" - Popular sentiment across X
</blockquote>

Fan polls show Ferrari as the most anticipated team reveal for 2026.`,
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

const selectExpertView = async (category: string) => {
  if (selectedExpertView.value === category) {
    // Deselect - go back to showing all entities
    selectedExpertView.value = null
    filteredEntityAccounts.value = []
    filteredEntitiesCount.value = 0
    displayedResponse.value = ''
    typingIndex.value = 0
    isTyping.value = true
    setTimeout(typeResponse, 300)
  } else {
    // Select new category
    selectedExpertView.value = category
    displayedResponse.value = ''
    typingIndex.value = 0
    isTyping.value = true
    
    // Fetch accounts for this category
    await fetchCategoryAccounts(category)
    
    setTimeout(() => typeExpertResponse(category), 300)
  }
}

const typeExpertResponse = (category: string) => {
  const response = expertResponses[category] || ''
  if (typingIndex.value < response.length) {
    const chunkSize = 5
    displayedResponse.value = response.slice(0, typingIndex.value + chunkSize)
    typingIndex.value += chunkSize
    setTimeout(() => typeExpertResponse(category), 8)
  } else {
    isTyping.value = false
  }
}

const handleFollowup = () => {
  if (grokFollowup.value.trim()) {
    console.log('Follow-up question:', grokFollowup.value)
    grokFollowup.value = ''
  }
}

const typeResponse = () => {
  if (typingIndex.value < grokFullResponse.length) {
    const chunkSize = 3
    displayedResponse.value = grokFullResponse.slice(0, typingIndex.value + chunkSize)
    typingIndex.value += chunkSize
    setTimeout(typeResponse, 10)
  } else {
    isTyping.value = false
  }
}

// Track the last fetched keyword to avoid re-fetching the same data
const lastFetchedKeyword = ref<string | null>(null)

// Start typing animation when component becomes active
watch(() => props.isActive, (active: boolean) => {
  if (active && !selectedExpertView.value) {
    // Only start typing animation when becoming active (not already showing expert response)
    displayedResponse.value = ''
    typingIndex.value = 0
    isTyping.value = true
    setTimeout(typeResponse, 500)
  }
}, { immediate: true })

// Watch for keyword changes - fetch entities even when not active (for pre-loading)
watch(() => props.keyword, (newKeyword: string | undefined) => {
  const keyword = newKeyword || 'F1'
  
  // Only fetch if keyword has changed
  if (keyword !== lastFetchedKeyword.value) {
    lastFetchedKeyword.value = keyword
    
    // Clear any selected expert view when keyword changes
    selectedExpertView.value = null
    filteredEntityAccounts.value = []
    filteredEntitiesCount.value = 0
    
    // Fetch entities for new keyword
    fetchEntities(keyword)
    
    // If active, also restart typing animation
    if (props.isActive) {
      displayedResponse.value = ''
      typingIndex.value = 0
      isTyping.value = true
      setTimeout(typeResponse, 500)
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

.source-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.source-item {
  color: #1d9bf0;
  font-size: 0.85rem;
  text-decoration: none;
}

.source-item:hover {
  text-decoration: underline;
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

@media (max-width: 900px) {
  .groksignal-layout {
    grid-template-columns: 1fr;
  }
  
  .expert-views {
    position: static;
  }
}
</style>
