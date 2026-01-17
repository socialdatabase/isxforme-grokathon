<template>
  <div class="timeline-container">
    <div class="timeline-layout">
      <!-- Timeline Feed -->
      <div class="timeline-feed">
        <!-- Loading Spinner for Posts -->
        <div v-if="loadingPosts" class="posts-loading">
          <div class="posts-spinner"></div>
          <p class="posts-loading-text">Loading posts...</p>
        </div>
        
        <!-- Posts List -->
        <template v-else>
          <div v-for="tweet in timelineTweets" :key="tweet.id" class="tweet">
            <div class="tweet-avatar">
              <img :src="tweet.avatar" :alt="tweet.displayName" />
            </div>
            <div class="tweet-content">
              <div class="tweet-header">
                <span class="tweet-name">{{ tweet.displayName }}</span>
                <svg v-if="tweet.verified" class="tweet-verified" width="16" height="16" viewBox="0 0 24 24" fill="#1d9bf0">
                  <path d="M22.5 12.5c0-1.58-.875-2.95-2.148-3.6.154-.435.238-.905.238-1.4 0-2.21-1.71-3.998-3.818-3.998-.47 0-.92.084-1.336.25C14.818 2.415 13.51 1.5 12 1.5s-2.816.917-3.437 2.25c-.415-.165-.866-.25-1.336-.25-2.11 0-3.818 1.79-3.818 4 0 .494.083.964.237 1.4-1.272.65-2.147 2.018-2.147 3.6 0 1.495.782 2.798 1.942 3.486-.02.17-.032.34-.032.514 0 2.21 1.708 4 3.818 4 .47 0 .92-.086 1.335-.25.62 1.334 1.926 2.25 3.437 2.25 1.512 0 2.818-.916 3.437-2.25.415.163.865.248 1.336.248 2.11 0 3.818-1.79 3.818-4 0-.174-.012-.344-.033-.513 1.158-.687 1.943-1.99 1.943-3.484zm-6.616-3.334l-4.334 6.5c-.145.217-.382.334-.625.334-.143 0-.288-.04-.416-.126l-.115-.094-2.415-2.415c-.293-.293-.293-.768 0-1.06s.768-.294 1.06 0l1.77 1.767 3.825-5.74c.23-.345.696-.436 1.04-.207.346.23.44.696.21 1.04z"/>
                </svg>
                <span class="tweet-handle">@{{ tweet.username }}</span>
                <span class="tweet-dot">·</span>
                <span class="tweet-date"><a target="_blank" :href="'https://www.x.com/i/status/' + tweet.id">{{ tweet.date }}</a></span>
              </div>
            <p class="tweet-body">{{ formatText(tweet.text) }}</p>
            <div v-if="tweet.photo" class="tweet-media">
              <img :src="tweet.photo" alt="Tweet media" />
            </div>
            <div class="tweet-actions">
              <button class="tweet-action reply">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
                  <path d="M1.751 10c0-4.42 3.584-8 8.005-8h4.366c4.49 0 8.129 3.64 8.129 8.13 0 2.96-1.607 5.68-4.196 7.11l-8.054 4.46v-3.69h-.067c-4.49.1-8.183-3.51-8.183-8.01z" stroke="currentColor" stroke-width="1.5"/>
                </svg>
                <span>{{ formatNumber(tweet.replies) }}</span>
              </button>
              <button class="tweet-action retweet">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
                  <path d="M4.5 3.88l4.432 4.14-1.364 1.46L5.5 7.55V16c0 1.1.896 2 2 2H13v2H7.5c-2.209 0-4-1.79-4-4V7.55L1.432 9.48.068 8.02 4.5 3.88zM16.5 6H11V4h5.5c2.209 0 4 1.79 4 4v8.45l2.068-1.93 1.364 1.46-4.432 4.14-4.432-4.14 1.364-1.46 2.068 1.93V8c0-1.1-.896-2-2-2z" fill="currentColor"/>
                </svg>
                <span>{{ formatNumber(tweet.retweets) }}</span>
              </button>
              <button class="tweet-action like">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
                  <path d="M16.697 5.5c-1.222-.06-2.679.51-3.89 2.16l-.805 1.09-.806-1.09C9.984 6.01 8.526 5.44 7.304 5.5c-1.243.07-2.349.78-2.91 1.91-.552 1.12-.633 2.78.479 4.82 1.074 1.97 3.257 4.27 7.129 6.61 3.87-2.34 6.052-4.64 7.126-6.61 1.111-2.04 1.03-3.7.477-4.82-.561-1.13-1.666-1.84-2.908-1.91z" stroke="currentColor" stroke-width="1.5"/>
                </svg>
                <span>{{ formatNumber(tweet.likes) }}</span>
              </button>
              <button class="tweet-action views">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
                  <path d="M8.75 21V3h2v18h-2zM18.75 21V8.5h2V21h-2zM13.75 21v-9h2v9h-2zM3.75 21v-4h2v4h-2z" fill="currentColor"/>
                </svg>
                <span>{{ formatNumber(tweet.impressions) }}</span>
              </button>
            </div>
          </div>
        </div>
        </template>
      </div>

      <!-- Authority Index Sidebar -->
      <div class="who-to-follow">
        <h3 class="wtf-title">
          Authority Index
          <span v-if="loading" class="wtf-loading">Loading...</span>
        </h3>
        <!-- Loading Spinner -->
        <div v-if="loading" class="wtf-loading-container">
          <div class="wtf-spinner"></div>
        </div>
        <div v-else class="wtf-list">
          <div v-for="(account, index) in whoToFollow" :key="account.username" class="wtf-item">
            <div class="wtf-avatar">
              <img :src="account.avatar" :alt="account.displayName" />
            </div>
            <div class="wtf-info">
              <div class="wtf-name">
                {{ account.displayName }}
                <svg v-if="account.verified" class="wtf-verified" width="14" height="14" viewBox="0 0 24 24" fill="#1d9bf0">
                  <path d="M22.5 12.5c0-1.58-.875-2.95-2.148-3.6.154-.435.238-.905.238-1.4 0-2.21-1.71-3.998-3.818-3.998-.47 0-.92.084-1.336.25C14.818 2.415 13.51 1.5 12 1.5s-2.816.917-3.437 2.25c-.415-.165-.866-.25-1.336-.25-2.11 0-3.818 1.79-3.818 4 0 .494.083.964.237 1.4-1.272.65-2.147 2.018-2.147 3.6 0 1.495.782 2.798 1.942 3.486-.02.17-.032.34-.032.514 0 2.21 1.708 4 3.818 4 .47 0 .92-.086 1.335-.25.62 1.334 1.926 2.25 3.437 2.25 1.512 0 2.818-.916 3.437-2.25.415.163.865.248 1.336.248 2.11 0 3.818-1.79 3.818-4 0-.174-.012-.344-.033-.513 1.158-.687 1.943-1.99 1.943-3.484zm-6.616-3.334l-4.334 6.5c-.145.217-.382.334-.625.334-.143 0-.288-.04-.416-.126l-.115-.094-2.415-2.415c-.293-.293-.293-.768 0-1.06s.768-.294 1.06 0l1.77 1.767 3.825-5.74c.23-.345.696-.436 1.04-.207.346.23.44.696.21 1.04z"/>
                </svg>
              </div>
              <div class="wtf-handle">@{{ account.username }}</div>
            </div>
            <div class="wtf-rank">
              <span class="rank-number">#{{ Number(index) + 1 }}</span>
              <span v-if="currentTopic" class="rank-topic">{{ currentTopic }}</span>
            </div>
          </div>
        </div>
        <div v-if="!loading" class="wtf-scroll-hint">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
            <path d="M7 10L12 15L17 10" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </div>
        
        <!-- Grok Times Button -->
        <button v-if="!loading" class="grok-times-btn" @click="emit('open-newspaper')">
          <span class="grok-times-icon">📰</span>
          <span class="grok-times-text">The Grok Times</span>
          <span class="grok-times-subtitle">AI-generated newspaper</span>
        </button>
        
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const config = useRuntimeConfig()

const props = defineProps<{
  keyword: string
  podcastMode?: boolean
}>()

const emit = defineEmits<{
  (e: 'open-newspaper'): void
  (e: 'podcast-state-change', playing: boolean, loading: boolean): void
}>()

// Types
interface AuthorityAccount {
  displayName: string
  username: string
  avatar: string
  followers: string
  verified: boolean
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

interface TimelineTweet {
  id: string
  displayName: string
  username: string
  avatar: string
  verified: boolean
  date: string
  text: string
  likes: number
  retweets: number
  replies: number
  impressions: number
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

const currentTopic = ref('F1')
const loading = ref(false)
const loadingPosts = ref(false)

// Podcast state
const isPodcastPlaying = ref(false)
const isPodcastLoading = ref(false)
const podcastAudio = ref<HTMLAudioElement | null>(null)
const podcastScript = ref('')

const podcastButtonText = computed(() => {
  if (isPodcastLoading.value) return 'Generating...'
  if (isPodcastPlaying.value) return 'Pause Podcast'
  return 'Listen to Podcast'
})

const podcastSubtitle = computed(() => {
  if (isPodcastLoading.value) return 'Creating audio summary'
  if (isPodcastPlaying.value) return 'AI-narrated timeline'
  return 'AI-narrated summary'
})

// Toggle podcast play/pause
const togglePodcast = async () => {
  console.log('Podcast button clicked!', { 
    isPlaying: isPodcastPlaying.value, 
    hasAudio: !!podcastAudio.value,
    tweetsCount: timelineTweets.value.length 
  })
  
  // If already playing, pause
  if (isPodcastPlaying.value && podcastAudio.value) {
    podcastAudio.value.pause()
    isPodcastPlaying.value = false
    return
  }
  
  // If we have cached audio, resume
  if (podcastAudio.value && podcastAudio.value.src) {
    podcastAudio.value.play()
    isPodcastPlaying.value = true
    return
  }
  
  // Generate new podcast
  await generatePodcast()
}

// Generate podcast from timeline
const generatePodcast = async () => {
  if (timelineTweets.value.length === 0) return
  
  isPodcastLoading.value = true
  
  try {
    // Step 1: Prepare posts context for Grok
    const postsContext = timelineTweets.value.slice(0, 15).map((tweet: TimelineTweet) => ({
      author: tweet.displayName,
      username: tweet.username,
      text: tweet.text,
      likes: tweet.likes,
      retweets: tweet.retweets
    }))
    
    // Step 2: Generate podcast script using Grok
    const keyword = props.keyword || currentTopic.value || 'trending topics'
    console.log('Generating podcast for:', keyword, 'with', postsContext.length, 'posts')
    
    const scriptResponse = await fetch(`${config.public.apiBase}/grokathon/generate-podcast-script/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        keyword: keyword,
        posts: postsContext
      })
    })
    
    if (!scriptResponse.ok) {
      const errText = await scriptResponse.text()
      console.error('Script generation failed:', scriptResponse.status, errText)
      throw new Error('Failed to generate podcast script')
    }
    
    const scriptData = await scriptResponse.json()
    podcastScript.value = scriptData.script
    console.log('Generated script:', podcastScript.value.substring(0, 100) + '...')
    
    // Step 3: Convert script to speech using xAI TTS
    console.log('Converting to speech...')
    const ttsResponse = await fetch(`${config.public.apiBase}/grokathon/xai-text-to-speech/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        text: podcastScript.value,
        voice: 'rex' // Using Rex voice for podcast-style narration
      })
    })
    
    if (!ttsResponse.ok) {
      const errText = await ttsResponse.text()
      console.error('TTS failed:', ttsResponse.status, errText)
      throw new Error('Failed to generate audio')
    }
    
    console.log('TTS successful, creating audio element...')
    
    // Step 4: Create audio element and play
    const audioBlob = await ttsResponse.blob()
    const audioUrl = URL.createObjectURL(audioBlob)
    
    // Clean up previous audio if exists
    if (podcastAudio.value) {
      podcastAudio.value.pause()
      URL.revokeObjectURL(podcastAudio.value.src)
    }
    
    podcastAudio.value = new Audio(audioUrl)
    
    // Set up event listeners
    podcastAudio.value.onended = () => {
      isPodcastPlaying.value = false
    }
    
    podcastAudio.value.onerror = () => {
      console.error('Audio playback error')
      isPodcastPlaying.value = false
    }
    
    // Play the audio
    await podcastAudio.value.play()
    isPodcastPlaying.value = true
    
  } catch (error) {
    console.error('Error generating podcast:', error)
    alert('Failed to generate podcast. Please try again.')
  } finally {
    isPodcastLoading.value = false
  }
}

// Clean up audio on unmount
onUnmounted(() => {
  if (podcastAudio.value) {
    podcastAudio.value.pause()
    URL.revokeObjectURL(podcastAudio.value.src)
  }
})

const formatNumber = (num: number): string => {
  if (num >= 1000000) return (num / 1000000).toFixed(1).replace(/\.0$/, '') + 'M'
  if (num >= 1000) return (num / 1000).toFixed(1).replace(/\.0$/, '') + 'K'
  return num.toString()
}

// Reactive timeline posts
const timelineTweets = ref<TimelineTweet[]>([])

// Fallback F1 tweets
const fallbackF1Tweets: TimelineTweet[] = [
  { id: '1', displayName: 'Lewis Hamilton', username: 'LewisHamilton', avatar: 'https://pbs.twimg.com/profile_images/1874472051517296640/anm3Q000_normal.jpg', verified: true, date: 'Dec 30', text: '@slhfw yeah', likes: 156337, retweets: 4288, replies: 748, impressions: 2740080, photo: null },
  { id: '2', displayName: 'Sergio Pérez', username: 'SChecoPerez', avatar: 'https://pbs.twimg.com/profile_images/1962635381330849792/IgxrlWNj_normal.jpg', verified: true, date: 'Dec 19', text: 'The story continues with #11', likes: 91246, retweets: 7584, replies: 597, impressions: 2539692, photo: 'https://pbs.twimg.com/media/G8kLaq-WUAEi1lr.jpg' },
  { id: '3', displayName: 'Lewis Hamilton', username: 'LewisHamilton', avatar: 'https://pbs.twimg.com/profile_images/1874472051517296640/anm3Q000_normal.jpg', verified: true, date: 'Jan 7', text: 'Another return ~', likes: 63118, retweets: 4787, replies: 2169, impressions: 908576, photo: 'https://pbs.twimg.com/media/G-EOezUW8AAseW4.jpg' },
  { id: '4', displayName: 'Formula 1', username: 'F1', avatar: 'https://pbs.twimg.com/profile_images/1612433922733887489/7f5XFklA_normal.jpg', verified: true, date: 'Jan 7', text: '41 years of redefining the record book 🤝 @LewisHamilton\n\n#F1', likes: 54785, retweets: 8253, replies: 367, impressions: 1931860, photo: 'https://pbs.twimg.com/media/G-EEl6iXIAA9Dt0.jpg' },
  { id: '5', displayName: 'Charles Leclerc', username: 'Charles_Leclerc', avatar: 'https://pbs.twimg.com/profile_images/1276567411240681472/8KdXHFdK_normal.jpg', verified: true, date: 'Dec 30', text: 'A very good year off the track.\nA very difficult year on the track.\nThank you so much to all of you that follows and supports me throughout the ups and downs. Count on me to give absolutely everything for 2026 for us to have more wins and success on the track.', likes: 41243, retweets: 3311, replies: 465, impressions: 1123595, photo: 'https://pbs.twimg.com/media/G9b3nd8WYAE4I08.jpg' },
  { id: '6', displayName: 'Lewis Hamilton', username: 'LewisHamilton', avatar: 'https://pbs.twimg.com/profile_images/1874472051517296640/anm3Q000_normal.jpg', verified: true, date: 'Dec 19', text: "I'm still so proud to have been a producer on The F1 Movie. Being a part of bringing the world of F1 to the big screen was a major rush. If you want to experience that energy yourself, we've recreated some of the best moments from the film in F1 '25.", likes: 40525, retweets: 2251, replies: 486, impressions: 1239845, photo: null },
  { id: '7', displayName: 'Sergio Pérez', username: 'SChecoPerez', avatar: 'https://pbs.twimg.com/profile_images/1962635381330849792/IgxrlWNj_normal.jpg', verified: true, date: 'Dec 25', text: 'Les deseo una muy feliz navidad a todos.\n\nY quiero pedir en especial por todos aquellos que van a pasar una navidad difícil, que Dios les traiga mucha paz.\n\nDios los bendiga siempre y que santa les traiga muchos regalos a todos.', likes: 40370, retweets: 3649, replies: 583, impressions: 514795, photo: null },
  { id: '8', displayName: 'Formula 1', username: 'F1', avatar: 'https://pbs.twimg.com/profile_images/1612433922733887489/7f5XFklA_normal.jpg', verified: true, date: 'Dec 25', text: 'Merry Christmas from the Formula 1 family! 🎅🎄\n\n#F1', likes: 39116, retweets: 5651, replies: 358, impressions: 1524636, photo: 'https://pbs.twimg.com/media/G8xCnpLWQAA1YpB.jpg' },
  { id: '9', displayName: 'Mercedes-AMG PETRONAS F1 Team', username: 'MercedesAMGF1', avatar: 'https://pbs.twimg.com/profile_images/2006665433651290112/bZZ9Ywke_normal.jpg', verified: true, date: 'Jan 7', text: 'Happy Birthday, @LewisHamilton 🎂🥳 Tanti auguri! 🙏', likes: 37091, retweets: 5723, replies: 163, impressions: 319385, photo: 'https://pbs.twimg.com/media/G-DJZ7_W0AAZYkY.jpg' },
  { id: '10', displayName: 'Formula 1', username: 'F1', avatar: 'https://pbs.twimg.com/profile_images/1612433922733887489/7f5XFklA_normal.jpg', verified: true, date: 'Jan 11', text: '11 Formula 1 cars to reveal 👀\n\nComing soon.\n\n#F1', likes: 36346, retweets: 3943, replies: 247, impressions: 842674, photo: 'https://pbs.twimg.com/media/G-PS7nXWQAARgyM.jpg' },
]

// Reactive authority accounts
const whoToFollow = ref<AuthorityAccount[]>([])

// Fetch accounts from API
const fetchAccounts = async (keyword: string) => {
  loading.value = true
  currentTopic.value = '' // Reset while loading (don't show topic until inferred)
  whoToFollow.value = [] // Reset while loading

  try {
    // Step 1: Fetch IDs and infer topic in parallel
    const [idsResponse, topicResponse] = await Promise.all([
      $fetch<{ ids: string[] }>(
        `${config.public.apiBase}/grokathon/fetch-ids/?input_query=${encodeURIComponent(keyword)}`
      ),
      $fetch<{ topic: string | null }>(
        `${config.public.apiBase}/grokathon/infer-topic-in-query/?input_query=${encodeURIComponent(keyword)}`
      ).catch(() => ({ topic: null })) // Fallback if topic inference fails
    ])

    // Update currentTopic only if the API returns a topic (otherwise leave empty)
    if (topicResponse.topic) {
      currentTopic.value = topicResponse.topic
    }

    if (!idsResponse.ids || idsResponse.ids.length === 0) {
      return // No results found
    }

    // Take up to 20 IDs for the sidebar
    const idsToFetch = idsResponse.ids.slice(0, 20)

    // Step 2: Fetch account details
    const idsParams = idsToFetch.map((id: string) => `ids=${id}`).join('&')
    const accountsResponse = await $fetch<{ accounts: ApiAccount[] }>(
      `${config.public.apiBase}/grokathon/fetch-accounts/?${idsParams}`
    )

    if (accountsResponse.accounts && accountsResponse.accounts.length > 0) {
      whoToFollow.value = accountsResponse.accounts.map((acc: ApiAccount) => ({
        displayName: acc.name,
        username: acc.username,
        avatar: acc.profile_image_url || '',
        followers: formatFollowers(acc.public_metrics?.followers_count || 0),
        verified: acc.verified || false
      }))
    }
  } catch (err) {
    console.error('Error fetching accounts:', err)
    // Keep empty on error
  } finally {
    loading.value = false
  }
}

// Format follower count
const formatFollowers = (count: number): string => {
  if (count >= 1000000) return (count / 1000000).toFixed(1).replace(/\.0$/, '') + 'M'
  if (count >= 1000) return (count / 1000).toFixed(1).replace(/\.0$/, '') + 'K'
  return count.toString()
}

// Format date for display
const formatDate = (dateString: string): string => {
  const date = new Date(dateString)
  const now = new Date()
  const diffMs = now.getTime() - date.getTime()
  const diffHours = Math.floor(diffMs / (1000 * 60 * 60))
  const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24))
  
  if (diffHours < 24) {
    return `${diffHours}h`
  } else if (diffDays < 7) {
    return `${diffDays}d`
  } else {
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
  }
}

const formatText = (text: string): string => {
  return text.replace(/https:\/\/t\.co\/\w+/gi, '');
}

// Fetch posts from API
const fetchPosts = async (keyword: string) => {
  loadingPosts.value = true
  timelineTweets.value = [] // Reset while loading

  try {
    // Step 1: Fetch IDs for the keyword (backend returns strings)
    const idsResponse = await $fetch<{ ids: string[] }>(
      `${config.public.apiBase}/grokathon/fetch-ids/?input_query=${encodeURIComponent(keyword)}`
    )

    if (!idsResponse.ids || idsResponse.ids.length === 0) {
      return // No results found
    }

    // Take up to 50 IDs for posts
    const idsToFetch = idsResponse.ids.slice(0, 50)

    // Step 2: Fetch posts for those accounts using timeline endpoint (filters for higher engagement posts)
    const idsParams = idsToFetch.map((id: string) => `ids=${id}`).join('&')
    const postsResponse = await $fetch<{ posts: ApiPost[] }>(
      `${config.public.apiBase}/grokathon/fetch-posts-timeline/?${idsParams}`
    )

    if (postsResponse.posts && postsResponse.posts.length > 0) {
      // Map API response to timeline tweet format
      timelineTweets.value = postsResponse.posts.slice(0, 150).map((item: ApiPost) => {
        // Extract first media photo if available
        let photo: string | null = null
        if (item.post.media && item.post.media.length > 0) {
          const firstMedia = item.post.media[0]
          if (firstMedia.url) {
            photo = firstMedia.url
          } if (firstMedia.preview_image_url) {
            photo = firstMedia.preview_image_url
          }
        }

        return {
          id: item.post.id,
          displayName: item.account.username, // Using username as displayName since name isn't available
          username: item.account.username,
          avatar: item.account.profile_image_url || '',
          verified: item.account.verified || false,
          date: formatDate(item.post.created_at),
          text: item.post.text,
          likes: item.post.like_count || 0,
          retweets: item.post.retweet_count || 0,
          replies: item.post.reply_count || 0,
          impressions: item.post.impression_count || 0,
          photo
        }
      })
    }
  } catch (err) {
    console.error('Error fetching posts:', err)
    // Keep empty on error
  } finally {
    loadingPosts.value = false
  }
}

// Watch for keyword changes
watch(() => props.keyword, (newKeyword: string) => {
  if (newKeyword) {
    fetchAccounts(newKeyword)
    fetchPosts(newKeyword)
    
    // Reset podcast when topic changes
    if (podcastAudio.value) {
      podcastAudio.value.pause()
      URL.revokeObjectURL(podcastAudio.value.src)
      podcastAudio.value = null
    }
    isPodcastPlaying.value = false
    podcastScript.value = ''
  }
}, { immediate: true })

// Watch for podcast mode changes from parent
watch(() => props.podcastMode, async (newMode: boolean | undefined) => {
  console.log('Podcast mode changed:', newMode)
  
  if (newMode && !isPodcastPlaying.value) {
    // Start podcast
    await togglePodcast()
  } else if (!newMode && isPodcastPlaying.value) {
    // Stop podcast
    if (podcastAudio.value) {
      podcastAudio.value.pause()
      isPodcastPlaying.value = false
    }
  }
})

// Emit state changes to parent
watch([isPodcastPlaying, isPodcastLoading], ([playing, loading]) => {
  emit('podcast-state-change', playing, loading)
})
</script>

<style scoped>
.timeline-container {
  width: 100%;
}

/* Prompt Bar */
.prompt-bar-container {
  max-width: 1000px;
  margin: 0 auto 1.5rem;
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

.prompt-input {
  flex: 1;
  background: transparent;
  border: none;
  outline: none;
  padding: 0.85rem 1.25rem;
  font-size: 0.95rem;
  color: #e7e9ea;
  font-family: inherit;
}

.prompt-input::placeholder {
  color: #71767b;
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

/* Topic Selector */
.topic-selector {
  margin-top: 2rem;
  text-align: center;
}

.topic-intro {
  color: #71767b;
  font-size: 0.95rem;
  margin-bottom: 1.5rem;
}

.topic-buttons {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 0.75rem;
}

.topic-btn {
  background-color: #16181c;
  border: 1px solid #2f3336;
  border-radius: 50px;
  padding: 0.75rem 1.5rem;
  color: #e7e9ea;
  font-size: 0.95rem;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.15s ease;
}

.topic-btn:hover {
  background-color: #1d1f23;
  border-color: #fff;
}

/* Timeline Layout */
.timeline-layout {
  display: grid;
  grid-template-columns: 1fr 350px;
  gap: 1.5rem;
  max-width: 1000px;
  margin: 0 auto;
}

/* Timeline Feed */
.timeline-feed {
  border: 1px solid #2f3336;
  border-radius: 16px;
  overflow: hidden;
}

/* Posts Loading */
.posts-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
}

.posts-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #2f3336;
  border-top-color: #1d9bf0;
  border-radius: 50%;
  animation: posts-spin 1s linear infinite;
}

@keyframes posts-spin {
  to {
    transform: rotate(360deg);
  }
}

.posts-loading-text {
  margin-top: 1rem;
  color: #71767b;
  font-size: 0.95rem;
}

.tweet {
  display: flex;
  gap: 0.75rem;
  padding: 1rem;
  border-bottom: 1px solid #2f3336;
  transition: background-color 0.15s ease;
}

.tweet:hover {
  background-color: rgba(255, 255, 255, 0.03);
}

.tweet:last-child {
  border-bottom: none;
}

.tweet-avatar {
  flex-shrink: 0;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  overflow: hidden;
}

.tweet-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.tweet-content {
  flex: 1;
  min-width: 0;
}

.tweet-header {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  flex-wrap: wrap;
  margin-bottom: 0.25rem;
}

.tweet-name {
  font-weight: 700;
  color: #e7e9ea;
  font-size: 0.95rem;
}

.tweet-verified {
  flex-shrink: 0;
}

.tweet-handle,
.tweet-dot,
.tweet-date {
  color: #71767b;
  font-size: 0.95rem;
}

.tweet-body {
  color: #e7e9ea;
  font-size: 0.95rem;
  line-height: 1.4;
  white-space: pre-wrap;
  margin-bottom: 0.75rem;
}

.tweet-media {
  margin-bottom: 0.75rem;
  overflow: hidden;
}

.tweet-media img {
  /* width: 100%; */
  max-height: 600px;
  object-fit: cover;
  display: block;
  border-radius: 16px;
  border: 1px solid #2f3336;
}

.tweet-actions {
  display: flex;
  justify-content: space-between;
  max-width: 400px;
}

.tweet-action {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  background: none;
  border: none;
  color: #71767b;
  font-size: 0.8rem;
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 50px;
  transition: all 0.15s ease;
}

.tweet-action:hover {
  color: #1d9bf0;
}

.tweet-action.reply:hover {
  color: #1d9bf0;
  background-color: rgba(29, 155, 240, 0.1);
}

.tweet-action.retweet:hover {
  color: #00ba7c;
  background-color: rgba(0, 186, 124, 0.1);
}

.tweet-action.like:hover {
  color: #f91880;
  background-color: rgba(249, 24, 128, 0.1);
}

.tweet-action.views:hover {
  color: #1d9bf0;
  background-color: rgba(29, 155, 240, 0.1);
}

/* Who to Follow */
.who-to-follow {
  background-color: #16181c;
  border-radius: 16px;
  padding: 1rem;
  height: fit-content;
  position: sticky;
  top: 1rem;
}

.wtf-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.25rem;
  font-weight: 700;
  color: #e7e9ea;
  margin-bottom: 1rem;
}

.wtf-loading {
  font-size: 0.75rem;
  font-weight: 400;
  color: #71767b;
}

.wtf-loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 3rem 0;
}

.wtf-spinner {
  width: 32px;
  height: 32px;
  border: 3px solid #2f3336;
  border-top-color: #1d9bf0;
  border-radius: 50%;
  animation: wtf-spin 1s linear infinite;
}

@keyframes wtf-spin {
  to {
    transform: rotate(360deg);
  }
}

.wtf-list {
  display: flex;
  flex-direction: column;
  max-height: 500px;
  overflow-y: auto;
  padding-right: 0.75rem;
}

.wtf-list::-webkit-scrollbar {
  width: 4px;
}

.wtf-list::-webkit-scrollbar-track {
  background: transparent;
}

.wtf-list::-webkit-scrollbar-thumb {
  background: #2f3336;
  border-radius: 4px;
}

.wtf-list::-webkit-scrollbar-thumb:hover {
  background: #404448;
}

.wtf-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 0;
  transition: background-color 0.15s ease;
}

.wtf-avatar {
  flex-shrink: 0;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  overflow: hidden;
}

.wtf-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.wtf-info {
  flex: 1;
  min-width: 0;
}

.wtf-name {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-weight: 700;
  color: #e7e9ea;
  font-size: 0.9rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.wtf-verified {
  flex-shrink: 0;
}

.wtf-handle {
  color: #71767b;
  font-size: 0.85rem;
}

.wtf-rank {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.15rem;
}

.rank-number {
  font-size: 0.95rem;
  font-weight: 700;
  color: #e7e9ea;
}

.rank-topic {
  font-size: 0.7rem;
  color: #71767b;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.wtf-scroll-hint {
  display: flex;
  justify-content: center;
  padding: 0.5rem 0 0.25rem;
  color: #71767b;
  animation: bounce 2s infinite;
}

@keyframes bounce {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(3px);
  }
}

/* Grok Times Button */
.grok-times-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.25rem;
  width: 100%;
  padding: 1rem;
  margin-top: 1rem;
  background: linear-gradient(135deg, #1a1815 0%, #2a2520 100%);
  border: 1px solid #3d3830;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.grok-times-btn:hover {
  background: linear-gradient(135deg, #2a2520 0%, #3d3830 100%);
  border-color: #4d4840;
  transform: translateY(-1px);
}

.grok-times-icon {
  font-size: 1.5rem;
}

.grok-times-text {
  font-family: 'Times New Roman', Georgia, serif;
  font-size: 1rem;
  font-weight: 700;
  color: #f5f0e6;
  letter-spacing: 0.02em;
}

.grok-times-subtitle {
  font-size: 0.7rem;
  color: #71767b;
  font-weight: 400;
}

/* Podcast Button */
.podcast-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.25rem;
  width: 100%;
  padding: 1rem;
  margin-top: 0.75rem;
  background: linear-gradient(135deg, #1a1520 0%, #2a2030 100%);
  border: 1px solid #3d3040;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
  color: #e7e9ea;
}

.podcast-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #2a2030 0%, #3d3040 100%);
  border-color: #4d4050;
  transform: translateY(-1px);
}

.podcast-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.podcast-btn.playing {
  background: linear-gradient(135deg, #1d3a1d 0%, #2d4a2d 100%);
  border-color: #3d5a3d;
}

.podcast-btn.loading {
  background: linear-gradient(135deg, #1a2530 0%, #2a3540 100%);
  border-color: #3d4550;
}

.podcast-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255, 255, 255, 0.2);
  border-top-color: #1d9bf0;
  border-radius: 50%;
  animation: podcast-spin 0.8s linear infinite;
}

@keyframes podcast-spin {
  to { transform: rotate(360deg); }
}

.podcast-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  margin-bottom: 0.25rem;
}

.podcast-btn.playing .podcast-icon {
  background-color: rgba(0, 186, 124, 0.2);
  color: #00ba7c;
}

.podcast-text {
  font-size: 0.95rem;
  font-weight: 600;
  color: #e7e9ea;
}

.podcast-subtitle {
  font-size: 0.7rem;
  color: #71767b;
  font-weight: 400;
}

/* Audio Visualizer */
.audio-visualizer {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 3px;
  height: 32px;
  margin-top: 0.75rem;
  padding: 0.5rem;
  background-color: rgba(0, 186, 124, 0.1);
  border-radius: 8px;
}

.viz-bar {
  width: 4px;
  background-color: #00ba7c;
  border-radius: 2px;
  animation: viz-bounce 1s ease-in-out infinite;
}

.viz-bar:nth-child(1) { height: 40%; animation-delay: 0s; }
.viz-bar:nth-child(2) { height: 70%; animation-delay: 0.1s; }
.viz-bar:nth-child(3) { height: 100%; animation-delay: 0.15s; }
.viz-bar:nth-child(4) { height: 60%; animation-delay: 0.2s; }
.viz-bar:nth-child(5) { height: 90%; animation-delay: 0.25s; }
.viz-bar:nth-child(6) { height: 50%; animation-delay: 0.3s; }
.viz-bar:nth-child(7) { height: 80%; animation-delay: 0.35s; }
.viz-bar:nth-child(8) { height: 45%; animation-delay: 0.4s; }

@keyframes viz-bounce {
  0%, 100% { transform: scaleY(0.5); }
  50% { transform: scaleY(1); }
}

/* Responsive */
@media (max-width: 900px) {
  .timeline-layout {
    grid-template-columns: 1fr;
  }
  
  .who-to-follow {
    position: static;
  }
}
</style>
