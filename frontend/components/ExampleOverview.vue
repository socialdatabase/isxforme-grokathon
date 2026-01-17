<template>
  <div class="overview-container">
    <!-- Loading State -->
    <div v-if="loading" class="loading-container">
      <div class="spinner"></div>
      <p class="loading-text">Discovering your community...</p>
    </div>

    <template v-else>
      <!-- Stats Card -->
      <section class="stats-card">
        <div class="stats-number" :class="{ 'loading': sizeLoading }">{{ communitySize }}</div>
        <div class="stats-label">people interested in <span class="keyword-highlight">{{ keyword }}</span> on X</div>
      </section>

      <!-- Accounts to Follow -->
      <section v-if="accounts.length > 0" class="card">
        <h2 class="section-title">
          <span class="title-bar"></span>
          Accounts to follow
        </h2>
        <div class="accounts-grid">
        <div class="accounts-list">
          <div v-for="account in accountsLeft" :key="account.handle" class="account-item">
            <div class="account-avatar">
              <img :src="account.avatar" :alt="account.name" />
            </div>
            <div class="account-info">
              <div class="account-name">
                {{ account.name }}
                <svg v-if="account.verified" class="verified-badge" width="16" height="16" viewBox="0 0 24 24" fill="#1d9bf0">
                  <path d="M22.5 12.5c0-1.58-.875-2.95-2.148-3.6.154-.435.238-.905.238-1.4 0-2.21-1.71-3.998-3.818-3.998-.47 0-.92.084-1.336.25C14.818 2.415 13.51 1.5 12 1.5s-2.816.917-3.437 2.25c-.415-.165-.866-.25-1.336-.25-2.11 0-3.818 1.79-3.818 4 0 .494.083.964.237 1.4-1.272.65-2.147 2.018-2.147 3.6 0 1.495.782 2.798 1.942 3.486-.02.17-.032.34-.032.514 0 2.21 1.708 4 3.818 4 .47 0 .92-.086 1.335-.25.62 1.334 1.926 2.25 3.437 2.25 1.512 0 2.818-.916 3.437-2.25.415.163.865.248 1.336.248 2.11 0 3.818-1.79 3.818-4 0-.174-.012-.344-.033-.513 1.158-.687 1.943-1.99 1.943-3.484zm-6.616-3.334l-4.334 6.5c-.145.217-.382.334-.625.334-.143 0-.288-.04-.416-.126l-.115-.094-2.415-2.415c-.293-.293-.293-.768 0-1.06s.768-.294 1.06 0l1.77 1.767 3.825-5.74c.23-.345.696-.436 1.04-.207.346.23.44.696.21 1.04z"/>
                </svg>
              </div>
              <div class="account-handle">@{{ account.handle }} <span class="separator">|</span> <span class="account-followers">{{ account.followers }}</span></div>
            </div>
          </div>
        </div>
        <div class="accounts-list">
          <div v-for="account in accountsRight" :key="account.handle" class="account-item">
            <div class="account-avatar">
              <img :src="account.avatar" :alt="account.name" />
            </div>
            <div class="account-info">
              <div class="account-name">
                {{ account.name }}
                <svg v-if="account.verified" class="verified-badge" width="16" height="16" viewBox="0 0 24 24" fill="#1d9bf0">
                  <path d="M22.5 12.5c0-1.58-.875-2.95-2.148-3.6.154-.435.238-.905.238-1.4 0-2.21-1.71-3.998-3.818-3.998-.47 0-.92.084-1.336.25C14.818 2.415 13.51 1.5 12 1.5s-2.816.917-3.437 2.25c-.415-.165-.866-.25-1.336-.25-2.11 0-3.818 1.79-3.818 4 0 .494.083.964.237 1.4-1.272.65-2.147 2.018-2.147 3.6 0 1.495.782 2.798 1.942 3.486-.02.17-.032.34-.032.514 0 2.21 1.708 4 3.818 4 .47 0 .92-.086 1.335-.25.62 1.334 1.926 2.25 3.437 2.25 1.512 0 2.818-.916 3.437-2.25.415.163.865.248 1.336.248 2.11 0 3.818-1.79 3.818-4 0-.174-.012-.344-.033-.513 1.158-.687 1.943-1.99 1.943-3.484zm-6.616-3.334l-4.334 6.5c-.145.217-.382.334-.625.334-.143 0-.288-.04-.416-.126l-.115-.094-2.415-2.415c-.293-.293-.293-.768 0-1.06s.768-.294 1.06 0l1.77 1.767 3.825-5.74c.23-.345.696-.436 1.04-.207.346.23.44.696.21 1.04z"/>
                </svg>
              </div>
              <div class="account-handle">@{{ account.handle }} <span class="separator">|</span> <span class="account-followers">{{ account.followers }}</span></div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Visual Highlights -->
    <section v-if="images.length > 0" class="card">
      <h2 class="section-title">
        <span class="title-bar"></span>
        Visual highlights from X
        <span v-if="imagesLoading" class="loading-indicator">Loading...</span>
      </h2>
      <div class="image-grid">
        <div 
          v-for="(img, idx) in images" 
          :key="idx" 
          class="grid-item" 
          :class="[img.size, { 'image-error': img.error }]"
        >
          <img 
            :src="img.url" 
            :alt="`Highlight ${Number(idx) + 1}`"
            @error="handleImageError(idx)"
          />
        </div>
      </div>
    </section>

    <!-- Join Conversation CTA -->
    <section class="cta-section">
      <p class="cta-text">Ready to join the conversation?</p>
      <button class="cta-button" @click="emit('switch-to-timeline')">
        Create an account with this interest
      </button>
    </section>

    <!-- Conversations -->
    <section v-if="tweets.length > 0" class="card">
      <h2 class="section-title">
        <span class="title-bar"></span>
        Join the conversation happening now
      </h2>
      <div class="tweets-list">
        <div v-for="(tweet, idx) in tweets" :key="idx" class="tweet-card">
          <p class="tweet-text">{{ tweet.text }}</p>
          <div class="tweet-stats">
            <span class="stat">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
              </svg>
              {{ tweet.likes }}
            </span>
            <span class="stat">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/>
              </svg>
              {{ tweet.comments }}
            </span>
            <span class="stat">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M17 1l4 4-4 4"/><path d="M3 11V9a4 4 0 0 1 4-4h14"/><path d="M7 23l-4-4 4-4"/><path d="M21 13v2a4 4 0 0 1-4 4H3"/>
              </svg>
              {{ tweet.retweets }}
            </span>
            <span class="stat">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/>
              </svg>
              {{ tweet.views }}
            </span>
          </div>
        </div>
      </div>
    </section>

    <!-- Final CTA -->
    <section class="final-cta">
      <a href="https://x.com" target="_blank" class="join-button">Join X</a>
    </section>
    </template>
  </div>
</template>

<script setup lang="ts">
const config = useRuntimeConfig()

const props = defineProps<{
  keyword: string
}>()

const emit = defineEmits<{
  (e: 'switch-to-timeline'): void
}>()

// Loading and error states
const loading = ref(false)
const sizeLoading = ref(false)
const error = ref<string | null>(null)

// Community size
const communitySize = ref<string>('--')

// Types
interface AccountDisplay {
  name: string
  handle: string
  followers: string
  verified: boolean
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
    media: Array<{ url?: string; preview_image_url?: string; type?: string }> | null
  }
  account: {
    id: string
    username: string
    verified: boolean | null
    profile_image_url: string | null
  }
}

interface ImageDisplay {
  url: string
  size: 'normal' | 'wide' | 'tall' | 'large'
  error?: boolean
}

// Accounts data
const accounts = ref<AccountDisplay[]>([])

// Images data
const images = ref<ImageDisplay[]>([])
const imagesLoading = ref(false)

// Tweets/conversations data
interface TweetDisplay {
  text: string
  likes: string
  comments: string
  retweets: string
  views: string
}
const tweets = ref<TweetDisplay[]>([])

// Fallback F1 accounts (used when API fails or for F1 keyword)
const fallbackF1Accounts = [
  { name: 'Formula 1', handle: 'F1', followers: '11.7M', verified: true, avatar: 'https://www.gtplanet.net/wp-content/uploads/2017/11/F1-2018-Logo.jpg' },
  { name: 'Lewis Hamilton', handle: 'LewisHamilton', followers: '8.3M', verified: true, avatar: 'https://pbs.twimg.com/profile_images/1874472051517296640/anm3Q000_400x400.jpg' },
  { name: 'Max Verstappen', handle: 'Max33Verstappen', followers: '4.1M', verified: true, avatar: 'https://pbs.twimg.com/profile_images/1759865143410765824/5B64vpgr_400x400.jpg' },
  { name: 'McLaren', handle: 'McLarenF1', followers: '4.4M', verified: true, avatar: 'https://pbs.twimg.com/profile_images/2009686309229441024/YAoyori-_400x400.jpg' },
  { name: 'Mercedes-AMG F1', handle: 'MercedesAMGF1', followers: '7.2M', verified: true, avatar: 'https://pbs.twimg.com/profile_images/2006665433651290112/bZZ9Ywke_400x400.jpg' },
  { name: 'Scuderia Ferrari', handle: 'ScuderiaFerrari', followers: '6.8M', verified: true, avatar: 'https://pbs.twimg.com/profile_images/947659786555940865/P5eYYYIx_400x400.jpg' },
  { name: 'Red Bull Racing', handle: 'redbullracing', followers: '5.9M', verified: true, avatar: 'https://pbs.twimg.com/profile_images/2006634351702810624/dl-eH03X_400x400.jpg' },
  { name: 'Daniel Ricciardo', handle: 'danielricciardo', followers: '3.2M', verified: true, avatar: 'https://pbs.twimg.com/profile_images/1595403026789023746/BhuqlZx8_400x400.jpg' },
  { name: 'Charles Leclerc', handle: 'Charles_Leclerc', followers: '2.9M', verified: true, avatar: 'https://pbs.twimg.com/profile_images/1276567411240681472/8KdXHFdK_400x400.jpg' },
  { name: 'Lando Norris', handle: 'LandoNorris', followers: '3.5M', verified: true, avatar: 'https://pbs.twimg.com/profile_images/1752288661746454529/uAS75ARP_400x400.jpg' },
]

// Fallback F1 images (used when API fails or for F1 keyword)
const fallbackF1Images: ImageDisplay[] = [
  { url: 'https://f1chronicle.com/wp-content/uploads/2024/01/SI202412010400-1920x1080.jpg', size: 'normal' },
  { url: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTmwCYq7k6P-BUzdkHiXoypKKzubkcHfSQS7haStcWhvyf27tgzeeqyyF2iU5gPGLEyXaA&usqp=CAU', size: 'wide' },
  { url: 'https://media.formula1.com/image/upload/f_auto,c_limit,w_1440,q_auto/f_auto/q_auto/fom-website/Campaign/BGT/BGT%20Everything', size: 'tall' },
  { url: 'https://cdn-7.motorsport.com/images/amp/2d1Zz5LY/s1000/max-verstappen-red-bull-racing.jpg', size: 'large' },
  { url: 'https://cdn.mos.cms.futurecdn.net/qe8W2K7rMNLVTbim6hiXpS.jpg', size: 'normal' },
  { url: 'https://e0.365dm.com/22/03/1600x900/skysports-f1-2022-driver-preview_5706316.jpg?20220314161233', size: 'normal' },
  { url: 'https://www.racefans.net/wp-content/uploads/2023/02/racefansdotnet-23-02-23-06-14-48-3.jpg', size: 'wide' },
  { url: 'https://r.testifier.nl/Acbs8526SDKI/resizing_type:fill/width:3840/height:2560/plain/https://s3-newsifier.ams3.digitaloceanspaces.com/gpblog.com/images/2025-04/20250420-0669-680f7ee454279.jpg@webp', size: 'normal' },
  { url: 'https://cdn-4.motorsport.com/images/amp/2d1QlRDY/s6/formula-1-emilia-romagna-gp-20-1006067.jpg', size: 'tall' },
  { url: 'https://img.redbull.com/images/c_crop,x_0,y_1,h_3143,w_4715/c_fill,w_450,h_300/q_auto:low,f_auto/redbullcom/2024/9/4/hvrmsd1slsrlc2uvj3b7/formula-one-car', size: 'normal' },
  { url: 'https://f1chronicle.com/wp-content/uploads/2024/01/SI202412010400-1920x1080.jpg', size: 'normal' },
  { url: 'https://cdn-7.motorsport.com/images/amp/2d1Zz5LY/s1000/max-verstappen-red-bull-racing.jpg', size: 'normal' },
]

// Fallback F1 tweets (used when API fails or for F1 keyword)
const fallbackF1Tweets: TweetDisplay[] = [
  {
    text: "That last lap battle between Hamilton and Verstappen was absolutely incredible! Best race of the season so far! #F1 #MonacoGP",
    likes: '1,243',
    comments: '89',
    retweets: '356',
    views: '28,500'
  },
  {
    text: "Breaking: Ferrari announces major upgrades for the next race. Could this be the turning point of their season? #F1 #ScuderiaFerrari",
    likes: '876',
    comments: '124',
    retweets: '231',
    views: '15,700'
  },
  {
    text: "The weather forecast for Sunday's race looks unpredictable. Rain could definitely mix things up! #F1 #WeatherWatch",
    likes: '542',
    comments: '67',
    retweets: '98',
    views: '9,800'
  }
]

// Format follower count
const formatFollowers = (count: number): string => {
  if (count >= 1000000) return (count / 1000000).toFixed(1).replace(/\.0$/, '') + 'M'
  if (count >= 1000) return (count / 1000).toFixed(1).replace(/\.0$/, '') + 'K'
  return count.toString()
}

// Format number with commas
const formatNumber = (num: number | null | undefined): string => {
  if (num === null || num === undefined) return '0'
  return num.toLocaleString()
}

// Format community size
const formatSize = (count: number): string => {
  if (count >= 1000000) return (count / 1000000).toFixed(1).replace(/\.0$/, '') + 'M+'
  if (count >= 1000) return (count / 1000).toFixed(1).replace(/\.0$/, '') + 'K+'
  return count.toString() + '+'
}

// Fetch community size from API
const fetchCommunitySize = async (ids: string[]) => {
  if (!ids || ids.length === 0) return
  
  sizeLoading.value = true
  try {
    const idsParams = ids.map((id: string) => `ids=${id}`).join('&')
    const sizeResponse = await $fetch<{ size: string }>(
      `${config.public.apiBase}/grokathon/fetch-grokathon-size/?${idsParams}`
    )
    
    if (sizeResponse.size) {
      // API returns pre-formatted string like '27.9M'
      communitySize.value = sizeResponse.size + '+'
    }
  } catch (err) {
    console.error('Error fetching community size:', err)
    // Keep the default value on error
  } finally {
    sizeLoading.value = false
  }
}

// Assign varied sizes to images for grid layout
const assignImageSizes = (urls: string[]): ImageDisplay[] => {
  const sizes: Array<'normal' | 'wide' | 'tall' | 'large'> = ['normal', 'wide', 'tall', 'large', 'normal', 'normal', 'wide', 'normal', 'tall', 'normal', 'normal', 'normal']
  return urls.map((url, index) => ({
    url,
    size: sizes[index % sizes.length],
    error: false
  }))
}

// Handle image load errors
const handleImageError = (index: number) => {
  if (images.value[index]) {
    images.value[index].error = true
  }
}

// Fetch images from posts API
const fetchImages = async (ids: string[]) => {
  if (!ids || ids.length === 0) return
  
  imagesLoading.value = true
  try {
    const idsParams = ids.map((id: string) => `ids=${id}`).join('&')
    const postsResponse = await $fetch<{ posts: ApiPost[] }>(
      `${config.public.apiBase}/grokathon/fetch-posts/?${idsParams}`
    )
    
    if (postsResponse.posts && postsResponse.posts.length > 0) {
      // Extract media URLs from posts (photos only, not videos)
      const mediaUrls: string[] = []
      for (const item of postsResponse.posts) {
        if (item.post.media && item.post.media.length > 0) {
          for (const media of item.post.media) {
            // Only include photos, skip videos
            if (media.type === 'video' || media.type === 'animated_gif') {
              continue
            }
            const url = media.url || media.preview_image_url
            if (url && !mediaUrls.includes(url)) {
              mediaUrls.push(url)
            }
          }
        }
      }
      
      if (mediaUrls.length > 0) {
        // Assign sizes and limit to 12 images
        images.value = assignImageSizes(mediaUrls.slice(0, 12))
      } else {
        // No media found, keep fallback
        images.value = fallbackF1Images
      }
      
      // Extract top 3 posts for conversations section
      tweets.value = postsResponse.posts.slice(0, 3).map((item: ApiPost) => ({
        text: item.post.text,
        likes: formatNumber(item.post.like_count),
        comments: formatNumber(item.post.reply_count),
        retweets: formatNumber(item.post.retweet_count),
        views: formatNumber(item.post.impression_count)
      }))
    } else {
      images.value = fallbackF1Images
      tweets.value = fallbackF1Tweets
    }
  } catch (err) {
    console.error('Error fetching images:', err)
    // Keep empty on error - no fallback
  } finally {
    imagesLoading.value = false
  }
}

// Fetch accounts from API
const fetchAccounts = async (keyword: string) => {
  loading.value = true
  error.value = null
  // Reset data while loading
  accounts.value = []
  images.value = []
  tweets.value = []
  communitySize.value = '--'

  try {
    // Step 1: Fetch IDs for the keyword (backend returns strings)
    const idsResponse = await $fetch<{ ids: string[] }>(
      `${config.public.apiBase}/grokathon/fetch-ids/?input_query=${encodeURIComponent(keyword)}`
    )

    if (!idsResponse.ids || idsResponse.ids.length === 0) {
      // No results found
      error.value = 'No community found for this topic'
      return
    }

    // Take first 10 IDs for size calculation and images
    const idsForSizeAndImages = idsResponse.ids.slice(0, 10)
    
    // Take more IDs for accounts (for scrollable list)
    // Request 50 to show a good scrollable list
    const idsForAccounts = idsResponse.ids.slice(0, 50)

    // Fetch community size and images with top 10 IDs (in parallel with accounts)
    fetchCommunitySize(idsForSizeAndImages)
    fetchImages(idsForSizeAndImages)

    // Step 2: Fetch account details
    const idsParams = idsForAccounts.map((id: string) => `ids=${id}`).join('&')
    const accountsResponse = await $fetch<{ accounts: ApiAccount[] }>(
      `${config.public.apiBase}/grokathon/fetch-accounts/?${idsParams}`
    )

    if (accountsResponse.accounts && accountsResponse.accounts.length > 0) {
      // Map API response to our format (keep all accounts for scrollable list)
      accounts.value = accountsResponse.accounts.map((acc: ApiAccount) => ({
        name: acc.name,
        handle: acc.username,
        followers: formatFollowers(acc.public_metrics?.followers_count || 0),
        verified: acc.verified || false,
        avatar: acc.profile_image_url?.replace('_normal', '_400x400') || ''
      }))
    }
  } catch (err) {
    console.error('Error fetching accounts:', err)
    error.value = 'Failed to load community data'
  } finally {
    loading.value = false
  }
}

// Computed properties for left/right columns (alternating for row-first order)
// Left column gets odd positions (1, 3, 5, 7...), Right gets even (2, 4, 6, 8...)
const accountsLeft = computed(() => {
  return accounts.value.filter((_, index) => index % 2 === 0)
})
const accountsRight = computed(() => {
  return accounts.value.filter((_, index) => index % 2 === 1)
})

// Fetch on mount and when keyword changes
watch(() => props.keyword, (newKeyword: string) => {
  if (newKeyword) {
    fetchAccounts(newKeyword)
  }
}, { immediate: true })

</script>

<style scoped>
.overview-container {
  width: 100%;
}

/* Loading State */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  min-height: 300px;
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

.loading-text {
  margin-top: 1.5rem;
  color: #71767b;
  font-size: 1rem;
}

/* Stats Card */
.stats-card {
  max-width: 800px;
  margin: 0 auto 2rem;
  background-color: #16181c;
  border-radius: 16px;
  border: 1px solid #2f3336;
  padding: 2.5rem;
  text-align: center;
}

.stats-number {
  font-size: clamp(3rem, 8vw, 4.5rem);
  font-weight: 700;
  color: #fff;
  line-height: 1;
  margin-bottom: 0.5rem;
  transition: opacity 0.2s ease;
}

.stats-number.loading {
  opacity: 0.5;
}

.stats-label {
  font-size: 1rem;
  color: #71767b;
}

.keyword-highlight {
  color: #1d9bf0;
  font-weight: 600;
}

.loading-indicator {
  font-size: 0.85rem;
  color: #71767b;
  font-weight: 400;
  margin-left: auto;
}

/* Cards */
.card {
  max-width: 800px;
  margin: 0 auto 2rem;
  background-color: #16181c;
  border-radius: 16px;
  border: 1px solid #2f3336;
  padding: 1.5rem;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.1rem;
  font-weight: 600;
  color: #e7e9ea;
  margin-bottom: 1.5rem;
}

.title-bar {
  width: 4px;
  height: 20px;
  background-color: #fff;
  border-radius: 2px;
}

/* Accounts List */
.accounts-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  max-height: 320px;
  overflow-y: auto;
  padding-right: 0.5rem;
}

.accounts-grid::-webkit-scrollbar {
  width: 6px;
}

.accounts-grid::-webkit-scrollbar-track {
  background: transparent;
}

.accounts-grid::-webkit-scrollbar-thumb {
  background-color: #2f3336;
  border-radius: 3px;
}

.accounts-grid::-webkit-scrollbar-thumb:hover {
  background-color: #3f4347;
}

.accounts-list {
  display: flex;
  flex-direction: column;
}

.account-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.5rem 0;
}

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

.account-info {
  flex: 1;
  min-width: 0;
}

.account-name {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  font-weight: 600;
  color: #e7e9ea;
  font-size: 0.95rem;
}

.verified-badge {
  flex-shrink: 0;
}

.account-handle {
  color: #71767b;
  font-size: 0.85rem;
}

.separator {
  margin: 0 0.2rem;
  opacity: 0.5;
}

/* Image Grid */
.image-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 0.5rem;
}

.grid-item {
  border-radius: 8px;
  overflow: hidden;
  aspect-ratio: 1;
}

.grid-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: opacity 0.2s ease;
}

.grid-item:hover img {
  opacity: 0.8;
}

.grid-item.normal {
  aspect-ratio: 1;
}

.grid-item.tall {
  grid-row: span 2;
  aspect-ratio: auto;
}

.grid-item.large {
  grid-column: span 2;
  grid-row: span 2;
  aspect-ratio: auto;
}

.grid-item.wide {
  grid-column: span 2;
  aspect-ratio: 2/1;
}

.grid-item.image-error {
  display: none;
}

/* CTA Section */
.cta-section {
  text-align: center;
  padding: 3rem 1rem;
}

.cta-text {
  font-size: 1.25rem;
  color: #e7e9ea;
  margin-bottom: 1.5rem;
}

.cta-button {
  display: inline-block;
  padding: 1rem 3rem;
  background-color: #fff;
  color: #000;
  font-size: 1.05rem;
  font-weight: 600;
  font-family: inherit;
  border-radius: 50px;
  border: none;
  cursor: pointer;
  transition: opacity 0.15s ease;
}

.cta-button:hover {
  opacity: 0.9;
}

/* Tweets */
.tweets-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.tweet-card {
  background-color: #000;
  border: 1px solid #2f3336;
  border-radius: 12px;
  padding: 1.25rem;
}

.tweet-text {
  color: #e7e9ea;
  font-size: 0.95rem;
  line-height: 1.5;
  margin-bottom: 1rem;
}

.tweet-stats {
  display: flex;
  gap: 1.5rem;
  flex-wrap: wrap;
}

.stat {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  color: #71767b;
  font-size: 0.85rem;
}

.stat svg {
  opacity: 0.7;
}

/* Final CTA */
.final-cta {
  text-align: center;
  padding: 2rem 0 1rem;
}

.join-button {
  display: inline-block;
  padding: 0.75rem 2rem;
  background: transparent;
  color: #e7e9ea;
  font-size: 1rem;
  font-weight: 500;
  border: 1px solid #536471;
  border-radius: 50px;
  text-decoration: none;
  transition: background-color 0.15s ease;
}

.join-button:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

/* Responsive */
@media (max-width: 600px) {
  .accounts-grid {
    grid-template-columns: 1fr;
  }
  
  .account-item {
    flex-wrap: wrap;
  }
  
  .image-grid {
    grid-template-columns: repeat(3, 1fr);
  }
  
  .grid-item.normal,
  .grid-item.tall,
  .grid-item.large,
  .grid-item.wide {
    grid-column: span 1;
    grid-row: span 1;
    aspect-ratio: 1;
  }
}
</style>
