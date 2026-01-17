<template>
  <div class="newspaper-container">
    <!-- Loading State -->
    <div v-if="loading" class="loading-overlay">
      <div class="loading-content">
        <div class="printing-press">
          <div class="press-roller"></div>
          <div class="press-paper"></div>
        </div>
        <p class="loading-text">The presses are rolling...</p>
        <p class="loading-subtext">Grok is writing today's edition</p>
      </div>
    </div>

    <!-- Newspaper -->
    <div v-else class="newspaper">
      <!-- Masthead -->
      <header class="masthead">
        <div class="masthead-top">
          <span class="edition-info">{{ currentDate }}</span>
          <span class="motto">"All the News That's Fit to Grok"</span>
          <span class="edition-info">Vol. MMXXVI No. {{ issueNumber }}</span>
        </div>
        <h1 class="newspaper-title">The Grok Times</h1>
        <div class="masthead-bottom">
          <div class="topic-badge">{{ keyword }} Edition</div>
        </div>
        <div class="masthead-border"></div>
      </header>

      <!-- Main Content -->
      <main class="newspaper-content">
        <!-- Lead Story -->
        <article v-if="articles[0]" class="lead-story">
          <h2 class="headline headline-lead">{{ articles[0].headline }}</h2>
          <p class="byline">By {{ articles[0].author }} | {{ articles[0].section }}</p>
          <div class="lead-layout ">
            <div class="lead-image " v-if="articles[0].image">
              <div class="media-wrapper group">
                <video v-if="articles[0].video" :poster="articles[0].image" :src="articles[0].video" muted loop
                  @mouseenter="($event.target as HTMLVideoElement).play()"
                  @mouseleave="v => { (v.target as HTMLVideoElement).pause(); (v.target as HTMLVideoElement).currentTime = 0; }" />
                <img v-else :src="articles[0].image" :alt="articles[0].headline" @error="handleImageError($event, 0)" />
                <!-- Loading spinner when video is generating -->
                 
                <div v-if="articles[0].videoLoading" class="loading-spinner-bg" >
                  <div class="loading-spinner">  
                  </div>
                </div>
                <!-- Play button visual when video is ready -->
                <div v-if="articles[0].video && !articles[0].videoLoading" class="play-button flex! group-hover:hidden!">
                  <svg class="" xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24">
                    <path fill="currentColor" d="M8 17.175V6.825q0-.425.3-.713t.7-.287q.125 0 .263.037t.262.113l8.15 5.175q.225.15.338.375t.112.475t-.112.475t-.338.375l-8.15 5.175q-.125.075-.262.113T9 18.175q-.4 0-.7-.288t-.3-.712" />
                  </svg>
                </div>
              </div>
              <p class="image-caption">{{ articles[0].imageCaption }}</p>
            </div>
            <div class="lead-text">
              <p class="article-content" v-html="articles[0].content"></p>
            </div>
          </div>
        </article>

        <!-- Secondary Stories Grid -->
        <div class="stories-grid">
          <article v-for="(article, index) in articles.slice(1, 5)" :key="index" class="story-card">
            <div class="story-image" v-if="article.image">
              <div class="media-wrapper group">
                <video v-if="article.video" :poster="article.image" :src="article.video" muted loop
                  @mouseenter="($event.target as HTMLVideoElement).play()"
                  @mouseleave="v => { (v.target as HTMLVideoElement).pause(); (v.target as HTMLVideoElement).currentTime = 0; }" />
                <img v-else :src="article.image" :alt="article.headline" @error="handleImageError($event, Number(index) + 1)" />
                <!-- Loading spinner when video is generating -->
                  <div v-if="article.videoLoading" class="loading-spinner-bg" >
                  <div class="loading-spinner">  
                  </div>
                </div>
                <!-- Play button visual when video is ready -->
                <div v-if="article.video && !article.videoLoading" class="play-button flex! group-hover:hidden!">
                  <svg class="" xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24">
                    <path fill="currentColor" d="M8 17.175V6.825q0-.425.3-.713t.7-.287q.125 0 .263.037t.262.113l8.15 5.175q.225.15.338.375t.112.475t-.112.475t-.338.375l-8.15 5.175q-.125.075-.262.113T9 18.175q-.4 0-.7-.288t-.3-.712" />
                  </svg>
                </div>
              </div>
              
            </div>
            <h3 class="headline headline-secondary">{{ article.headline }}</h3>
            <p class="byline">{{ article.author }}</p>
            <p class="article-excerpt" v-html="article.content"></p>
          </article>
        </div>

        <!-- Bottom Stories -->
        <div class="bottom-stories" v-if="articles.length > 5">
          <article v-for="(article, index) in articles.slice(5)" :key="'bottom-' + index" class="bottom-story">
            <h4 class="headline headline-small">{{ article.headline }}</h4>
            <p class="article-brief" v-html="article.content"></p>
          </article>
        </div>
      </main>

      <!-- Footer -->
      <footer class="newspaper-footer">
        <div class="footer-border"></div>
        <p class="footer-text">Generated by Grok AI | Sources: {{ sourceCount }} verified accounts | {{ postCount }} posts analyzed</p>
      </footer>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, computed } from 'vue'

const config = useRuntimeConfig()

const props = defineProps<{
  keyword: string
}>()

interface Article {
  headline: string
  author: string
  section: string
  content: string
  image: string | null
  imageCaption: string
  source_usernames?: string[]  // New optional field
  video?: string | null  // New field for video URL
  prompt_text?: string
  videoLoading?: boolean  // New field to track video generation loading state
}

interface ApiPost {
  account: {
    username: string
    profile_image_url?: string
    verified?: boolean
  }
  post: {
    id: string
    text: string
    created_at: string
    like_count?: number
    retweet_count?: number
    reply_count?: number
    impression_count?: number
    media?: Array<{
      type: string
      url?: string
      preview_image_url?: string
    }>
  }
}

const loading = ref(true)
const articles = ref<Article[]>([])
const sourceCount = ref(0)
const postCount = ref(0)
const issueNumber = ref(Math.floor(Math.random() * 1000) + 1)
const collectedImages = ref<string[]>([])

const currentDate = computed(() => {
  const now = new Date()
  return now.toLocaleDateString('en-US', { 
    weekday: 'long', 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric' 
  })
})

const handleImageError = (event: Event, index: number) => {
  const img = event.target as HTMLImageElement
  img.style.display = 'none'
}

// Changed: Made assignVideos async and use a sequential for-await loop to generate videos one by one
const assignVideos = async () => {
  for (const article of articles.value) {
    if (article.image) {
      article.videoLoading = true
      try {
        const res = await $fetch<{ video_url: string }>(
          `${config.public.apiBase}/grokathon/xai-image-to-video/`,
          {
            method: 'POST',
            body: { image_url: article.image, text: article.content || '' }
          }
        )
        console.log(res.video_url)
        article.video = res.video_url || null
      } catch (e) {
        console.error('Video generation error for image:', article.image, e)
      } finally {
        article.videoLoading = false
      }
    }
  }
}

const generateNewspaper = async (keyword: string) => {
  loading.value = true
  articles.value = []
  collectedImages.value = []

  try {
    // Step 1: Fetch IDs for the keyword
    const idsResponse = await $fetch<{ ids: string[] }>(
      `${config.public.apiBase}/grokathon/fetch-ids/?input_query=${encodeURIComponent(keyword)}`
    )

    if (!idsResponse.ids || idsResponse.ids.length === 0) {
      articles.value = [{
        headline: 'No News Today',
        author: 'The Grok Times Staff',
        section: 'Editorial',
        content: 'Our correspondents found no news on this topic. Please try a different search.',
        image: null,
        imageCaption: ''
      }]
      loading.value = false
      return
    }

    // Take up to 50 IDs for posts
    const idsToFetch = idsResponse.ids.slice(0, 50)
    sourceCount.value = idsToFetch.length

    // Step 2: Fetch posts for those accounts
    const idsParams = idsToFetch.map((id: string) => `ids=${id}`).join('&')
    const postsResponse = await $fetch<{ posts: ApiPost[] }>(
      `${config.public.apiBase}/grokathon/fetch-posts/?${idsParams}`
    )

    if (!postsResponse.posts || postsResponse.posts.length === 0) {
      articles.value = [{
        headline: 'Breaking: Silence on the Wire',
        author: 'The Grok Times Staff',
        section: 'Editorial',
        content: 'Our sources have gone quiet. No posts found for this topic.',
        image: null,
        imageCaption: ''
      }]
      loading.value = false
      return
    }

    postCount.value = postsResponse.posts.length

    // Collect images from posts (flat list for fallback)
    for (const item of postsResponse.posts) {
      if (item.post?.media && item.post.media.length > 0) {
        for (const media of item.post.media) {
          if (media.type !== 'video' && media.type !== 'animated_gif') {
            const url = media.url || media.preview_image_url
            if (url && !collectedImages.value.includes(url)) {
              collectedImages.value.push(url)
            }
          }
        }
      }
    }

    // Collect images by username
    const imagesByUsername: Record<string, string[]> = {}
    for (const item of postsResponse.posts) {
      const username = item.account.username
      if (username) {
        if (!imagesByUsername[username]) {
          imagesByUsername[username] = []
        }
        if (item.post?.media && item.post.media.length > 0) {
          for (const media of item.post.media) {
            if (media.type !== 'video' && media.type !== 'animated_gif') {
              const url = media.url || media.preview_image_url
              if (url && !imagesByUsername[username].includes(url)) {
                imagesByUsername[username].push(url)
                // Still collect flat for fallback if not already added
                if (!collectedImages.value.includes(url)) {
                  collectedImages.value.push(url)
                }
              }
            }
          }
        }
      }
    }

    // Step 3: Prepare posts for Grok (filter out invalid posts)
    const postsContext = postsResponse.posts
      .filter((item: ApiPost) => item.post && item.account && item.post.text)
      .map((item: ApiPost) => ({
        author: item.account.username || 'Unknown',
        username: item.account.username || 'unknown',
        text: item.post.text,
        likes: item.post.like_count || 0,
        retweets: item.post.retweet_count || 0
      }))

    // Step 4: Call Grok to generate newspaper articles
    console.log('Calling generate-newspaper with', postsContext.length, 'posts')
    
    try {
      const grokData = await $fetch<{ articles: Article[] }>(
        `${config.public.apiBase}/grokathon/generate-newspaper/`,
        {
          method: 'POST',
          body: {
            keyword: keyword,
            posts: postsContext
          }
        }
      )
      
      console.log('Grok response:', grokData)
      
      if (grokData.articles && grokData.articles.length > 0) {
        // Assign collected images to articles, prioritizing source_usernames
        articles.value = grokData.articles.map((article: Article, index: number) => {
          let selectedImage: string | null = null
          
          // Prioritize image from source_usernames
          if (article.source_usernames && article.source_usernames.length > 0) {
            for (const user of article.source_usernames) {
              const userImages = imagesByUsername[user]
              if (userImages && userImages.length > 0) {
                selectedImage = userImages[0] ?? null;  // Or Math.floor(Math.random() * userImages.length) for random
                break
              }
            }
          }
          
          // Fallback to sequential if no match
          if (!selectedImage) {
            selectedImage = collectedImages.value[index] || null
          }
          
          return {
            ...article,
            image: selectedImage,
            videoLoading: true,
            imageCaption: article.imageCaption || `Related to ${keyword}`
          }
        })
        assignVideos()  // Start generating videos async
      } else {
        console.log('No articles returned, using fallback')
        generateFallbackArticles(postsResponse.posts, keyword)
      }
    } catch (grokErr) {
      console.error('Grok API error:', grokErr)
      // Fallback: Generate simple articles from posts
      generateFallbackArticles(postsResponse.posts, keyword)
    }

  } catch (err) {
    console.error('Error generating newspaper:', err)
    // Generate fallback content
    articles.value = [{
      headline: `Breaking News in ${keyword}`,
      author: 'The Grok Times Staff',
      section: 'General',
      content: 'Our printing press encountered an issue. Please refresh to try again.',
      image: null,
      imageCaption: ''
    }]
  } finally {
    loading.value = false
  }
}

const generateFallbackArticles = (posts: ApiPost[], keyword: string) => {
  // Generate articles directly from top posts
  const sortedPosts = [...posts]
    .filter(item => item.post && item.account)
    .sort((a, b) => 
      ((b.post.like_count || 0) + (b.post.retweet_count || 0)) -
      ((a.post.like_count || 0) + (a.post.retweet_count || 0))
    )

  const topPosts = sortedPosts.slice(0, 7)
  
  articles.value = topPosts.map((item, index) => {
    const post = item.post
    const account = item.account
    // Create headline from first sentence or truncated text
    const sentences = (post.text || '').split(/[.!?]+/)
    const headline = sentences[0] && sentences[0].length > 80 
      ? sentences[0].substring(0, 77) + '...'
      : sentences[0] || `${keyword} Update`

    return {
      headline: headline,
      author: account.username || 'Unknown',
      section: index === 0 ? 'Top Story' : 'News',
      content: post.text || '',
      image: collectedImages.value[index] || null,
      imageCaption: `Photo via @${account.username || 'unknown'}`,
      source_usernames: [account.username || 'unknown']  // Added for consistency
    }
  })
}

watch(() => props.keyword, (newKeyword: string) => {
  if (newKeyword) {
        console.log('generating keywords')

    generateNewspaper(newKeyword)
  }
}, { immediate: false })

onMounted(() => {
  if (props.keyword) {
    console.log('generating mounted')
    generateNewspaper(props.keyword)
  }
})
</script>

<style scoped>
.newspaper-container {
  min-height: 100vh;
  background: linear-gradient(to bottom, #f5f0e6, #ebe6d9);
  padding: 1rem;
}

/* Loading State */
.loading-overlay {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(to bottom, #f5f0e6, #ebe6d9);
}

.loading-content {
  text-align: center;
}

.printing-press {
  width: 120px;
  height: 80px;
  margin: 0 auto 2rem;
  position: relative;
}

.press-roller {
  width: 100%;
  height: 30px;
  background: linear-gradient(to bottom, #4a4a4a, #2a2a2a, #4a4a4a);
  border-radius: 15px;
  animation: roll 1s ease-in-out infinite;
}

.press-paper {
  width: 80%;
  height: 40px;
  background: #fff;
  margin: 5px auto 0;
  animation: paper 1s ease-in-out infinite;
  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}

@keyframes roll {
  0%, 100% { transform: rotate(0deg); }
  50% { transform: rotate(180deg); }
}

@keyframes paper {
  0%, 100% { height: 40px; opacity: 1; }
  50% { height: 60px; opacity: 0.8; }
}

.loading-text {
  font-family: 'Times New Roman', Georgia, serif;
  font-size: 1.5rem;
  font-style: italic;
  color: #2a2a2a;
  margin-bottom: 0.5rem;
}

.loading-subtext {
  font-family: 'Times New Roman', Georgia, serif;
  font-size: 1rem;
  color: #666;
}

/* Newspaper Styles */
.newspaper {
  max-width: 1400px;
  margin: 0 auto;
  background: #fefcf7;
  box-shadow: 
    0 0 0 1px rgba(0,0,0,0.1),
    0 4px 20px rgba(0,0,0,0.15),
    inset 0 0 100px rgba(0,0,0,0.03);
  position: relative;
}

.newspaper::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%' height='100%' filter='url(%23noise)' opacity='0.04'/%3E%3C/svg%3E");
  pointer-events: none;
}

/* Masthead */
.masthead {
  padding: 1rem 2rem;
  text-align: center;
  border-bottom: 3px double #2a2a2a;
  position: relative;
}

.masthead-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-family: 'Times New Roman', Georgia, serif;
  font-size: 0.75rem;
  color: #666;
  margin-bottom: 0.5rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
}

.motto {
  font-style: italic;
  text-transform: none;
  letter-spacing: normal;
}

.newspaper-title {
  font-family: 'Old English Text MT', 'UnifrakturMaguntia', 'Times New Roman', serif;
  font-size: 4rem;
  font-weight: 400;
  color: #1a1a1a;
  margin: 0.5rem 0;
  letter-spacing: 0.05em;
  text-shadow: 1px 1px 0 rgba(0,0,0,0.1);
  line-height: 1;
}

.masthead-bottom {
  margin-top: 0.5rem;
}

.topic-badge {
  display: inline-block;
  font-family: 'Times New Roman', Georgia, serif;
  font-size: 1rem;
  font-weight: 700;
  color: #fff;
  background: #1a1a1a;
  padding: 0.25rem 1rem;
  text-transform: uppercase;
  letter-spacing: 0.15em;
}

.masthead-border {
  height: 2px;
  background: linear-gradient(to right, transparent, #2a2a2a, transparent);
  margin-top: 1rem;
}

/* Main Content */
.newspaper-content {
  padding: 2rem;
  position: relative;
}

/* Lead Story */
.lead-story {
  border-bottom: 1px solid #ccc;
  padding-bottom: 2rem;
  margin-bottom: 2rem;
}

.headline {
  font-family: 'Times New Roman', Georgia, serif;
  color: #1a1a1a;
  margin: 0;
  line-height: 1.1;
}

.headline-lead {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  text-align: center;
}

.headline-secondary {
  font-size: 1.25rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.headline-small {
  font-size: 1rem;
  font-weight: 700;
  margin-bottom: 0.25rem;
}

.byline {
  font-family: 'Times New Roman', Georgia, serif;
  font-size: 0.875rem;
  font-style: italic;
  color: #666;
  margin-bottom: 1rem;
  text-align: center;
}

.lead-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  margin-top: 1rem;
}

.lead-image {
  position: relative;
}

.lead-image img {
  width: 100%;
  height: auto;
  filter: grayscale(30%) contrast(1.1);
  border: 1px solid #ccc;
}

.image-caption {
  font-family: 'Times New Roman', Georgia, serif;
  font-size: 0.75rem;
  font-style: italic;
  color: #666;
  margin-top: 0.5rem;
  text-align: center;
}

.lead-text {
  column-count: 2;
  column-gap: 1.5rem;
  column-rule: 1px solid #ddd;
}

.article-content {
  font-family: 'Times New Roman', Georgia, serif;
  font-size: 1rem;
  line-height: 1.6;
  color: #2a2a2a;
  text-align: justify;
  hyphens: auto;
  margin: 0;
}

.article-content::first-letter {
  font-size: 3.5rem;
  float: left;
  line-height: 1;
  padding-right: 0.5rem;
  padding-top: 0.1rem;
  font-weight: 700;
}

/* Stories Grid */
.stories-grid {
  display: flex;
  flex-direction: row;
  /* display: grid;
  grid-template-columns: repeat(4, 1fr); */
  gap: 1.5rem;
  border-bottom: 1px solid #ccc;
  padding-bottom: 2rem;
  margin-bottom: 2rem;
}

.story-card {
  border-right: 1px solid #ddd;
  padding-right: 1.5rem;
}

.story-card:last-child {
  border-right: none;
  padding-right: 0;
}

.story-image {
  margin-bottom: 0.75rem;
}

.story-image img {
  /* width: 100%; */
  height: 300px;
  object-fit: cover;
  filter: grayscale(30%) contrast(1.1);
  border: 1px solid #ccc;
}

.story-card .byline {
  text-align: left;
  font-size: 0.75rem;
  margin-bottom: 0.5rem;
}

.article-excerpt {
  font-family: 'Times New Roman', Georgia, serif;
  font-size: 0.875rem;
  line-height: 1.5;
  color: #2a2a2a;
  text-align: justify;
  display: -webkit-box;
  -webkit-line-clamp: 6;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Bottom Stories */
.bottom-stories {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
}

.bottom-story {
  padding-right: 1.5rem;
  border-right: 1px solid #ddd;
}

.bottom-story:last-child {
  border-right: none;
  padding-right: 0;
}

.article-brief {
  font-family: 'Times New Roman', Georgia, serif;
  font-size: 0.875rem;
  line-height: 1.5;
  color: #2a2a2a;
  display: -webkit-box;
  -webkit-line-clamp: 4;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Footer */
.newspaper-footer {
  padding: 1rem 2rem;
  text-align: center;
}

.footer-border {
  height: 3px;
  background: linear-gradient(to right, 
    transparent, 
    #2a2a2a 10%, 
    #2a2a2a 45%, 
    transparent 50%, 
    #2a2a2a 55%, 
    #2a2a2a 90%, 
    transparent
  );
  margin-bottom: 1rem;
}

.footer-text {
  font-family: 'Times New Roman', Georgia, serif;
  font-size: 0.75rem;
  color: #666;
  font-style: italic;
}

/* Responsive */
@media (max-width: 1200px) {
  .stories-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .story-card:nth-child(2) {
    border-right: none;
    padding-right: 0;
  }
  
  .story-card:nth-child(3) {
    border-right: 1px solid #ddd;
    padding-right: 1.5rem;
  }
}

@media (max-width: 900px) {
  .newspaper-title {
    font-size: 2.5rem;
  }
  
  .headline-lead {
    font-size: 1.75rem;
  }
  
  .lead-layout {
    grid-template-columns: 1fr;
  }
  
  .lead-text {
    column-count: 1;
  }
  
  .stories-grid {
    grid-template-columns: 1fr;
  }
  
  .story-card {
    border-right: none;
    padding-right: 0;
    border-bottom: 1px solid #ddd;
    padding-bottom: 1.5rem;
  }
  
  .story-card:last-child {
    border-bottom: none;
    padding-bottom: 0;
  }
  
  .bottom-stories {
    grid-template-columns: 1fr;
  }
  
  .bottom-story {
    border-right: none;
    padding-right: 0;
    border-bottom: 1px solid #ddd;
    padding-bottom: 1rem;
  }
  
  .bottom-story:last-child {
    border-bottom: none;
    padding-bottom: 0;
  }
}

@media (max-width: 600px) {
  .newspaper-container {
    padding: 0.5rem;
  }
  
  .masthead {
    padding: 1rem;
  }
  
  .masthead-top {
    flex-direction: column;
    gap: 0.25rem;
  }
  
  .newspaper-content {
    padding: 1rem;
  }
}

/* New: Styles for media wrapper, loading spinner, and play button */
.media-wrapper {
  position: relative;
  display: inline-block;
  /* width: 100%; */
}

.loading-spinner-bg {
  background: rgba(0, 0, 0, 0.5);
  border-radius: 50%;
  height: 50px;
  width: 50px;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  
}

.loading-spinner {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  border: 4px solid rgba(255, 255, 255, 0.1);
  border-left-color: #cfcfcf;
  border-radius: 50%;
  width: 30px;
  height: 30px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: translate(-50%, -50%) rotate(360deg); }
}

.play-button {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 2rem;
  color: rgba(255, 255, 255, 0.8);
  background: rgba(0, 0, 0, 0.5);
  border-radius: 50%;
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  pointer-events: none; /* So it doesn't interfere with hover */
}
</style>
