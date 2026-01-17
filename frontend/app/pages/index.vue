<template>
  <div class="container" @mousemove="handleMouseMove" @mouseleave="handleMouseLeave">
    <!-- Orbital Topics Background -->
    <div class="orbit-container" ref="orbitContainer">
      <div 
        v-for="(topic, index) in orbitTopics" 
        :key="topic.name"
        :ref="(el: any) => setTopicRef(el, index)"
        class="orbit-topic"
        :style="[getOrbitStyle(index), { '--proximity': topicProximities[index] || 0 }]"
        @click="selectTopic(topic.name)"
      >
        {{ topic.name }}
      </div>
    </div>

    <h1 class="title">
      Is <span class="x-logo">𝕏</span> For Me?
    </h1>
    
    <form class="search-form" @submit.prevent="handleSearch">
      <div class="input-wrapper">
        <input
          v-model="searchQuery"
          type="text"
          class="search-input"
          placeholder="Tell us your interests, passions, or what makes your heart tick..."
        />
        <button type="submit" class="submit-btn" :disabled="!searchQuery.trim()">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M5 12H19M19 12L12 5M19 12L12 19" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
const searchQuery = ref('')
const orbitContainer = ref<HTMLElement | null>(null)
const topicRefs = ref<(HTMLElement | null)[]>([])
const topicProximities = ref<number[]>([])
const mousePos = ref({ x: 0, y: 0 })

// Set topic element refs
const setTopicRef = (el: any, index: number) => {
  topicRefs.value[index] = el as HTMLElement | null
}

// Handle mouse movement - calculate proximity to each topic
const handleMouseMove = (event: MouseEvent) => {
  mousePos.value = { x: event.clientX, y: event.clientY }
  updateProximities()
}

// Reset proximities when mouse leaves
const handleMouseLeave = () => {
  topicProximities.value = orbitTopics.map(() => 0)
}

// Calculate proximity for each topic based on mouse distance
const updateProximities = () => {
  const maxDistance = 200 // Max distance for effect (in pixels)
  
  topicProximities.value = topicRefs.value.map((el: HTMLElement | null) => {
    if (!el) return 0
    
    const rect = el.getBoundingClientRect()
    const centerX = rect.left + rect.width / 2
    const centerY = rect.top + rect.height / 2
    
    const distance = Math.sqrt(
      Math.pow(mousePos.value.x - centerX, 2) + 
      Math.pow(mousePos.value.y - centerY, 2)
    )
    
    // Calculate proximity (1 = closest, 0 = far)
    const proximity = Math.max(0, 1 - distance / maxDistance)
    return proximity
  })
}

// Curated topics relevant to X users
const orbitTopics = [
  // Inner orbit - most popular
  { name: 'AI', orbit: 1 },
  { name: 'Sports', orbit: 1 },
  { name: 'Music', orbit: 1 },
  { name: 'News', orbit: 1 },
  { name: 'Gaming', orbit: 1 },
  { name: 'Crypto', orbit: 1 },
  { name: 'Movies', orbit: 1 },
  { name: 'Fashion', orbit: 1 },
  { name: 'Tech', orbit: 1 },
  { name: 'Memes', orbit: 1 },
  
  // Second orbit
  { name: 'Science', orbit: 2 },
  { name: 'Business', orbit: 2 },
  { name: 'Politics', orbit: 2 },
  { name: 'Art', orbit: 2 },
  { name: 'Food', orbit: 2 },
  { name: 'Travel', orbit: 2 },
  { name: 'Fitness', orbit: 2 },
  { name: 'Photography', orbit: 2 },
  { name: 'Anime', orbit: 2 },
  { name: 'Comedy', orbit: 2 },
  { name: 'Finance', orbit: 2 },
  { name: 'Basketball', orbit: 2 },
  { name: 'Football', orbit: 2 },
  { name: 'Soccer', orbit: 2 },
  
  // Third orbit
  { name: 'Motorsports', orbit: 3 },
  { name: 'Space', orbit: 3 },
  { name: 'Books', orbit: 3 },
  { name: 'Design', orbit: 3 },
  { name: 'Startups', orbit: 3 },
  { name: 'Marketing', orbit: 3 },
  { name: 'History', orbit: 3 },
  { name: 'Wellness', orbit: 3 },
  { name: 'Real Estate', orbit: 3 },
  { name: 'Environment', orbit: 3 },
  { name: 'Investing', orbit: 3 },
  { name: 'Celebrities', orbit: 3 },
  { name: 'Automotive', orbit: 3 },
  { name: 'Education', orbit: 3 },
  { name: 'Podcast', orbit: 3 },
  { name: 'Hip Hop', orbit: 3 },
  { name: 'Esports', orbit: 3 },
  { name: 'NFTs', orbit: 3 },
  
  // Fourth orbit - extends beyond screen
  { name: 'Architecture', orbit: 4 },
  { name: 'Economics', orbit: 4 },
  { name: 'Philosophy', orbit: 4 },
  { name: 'Psychology', orbit: 4 },
  { name: 'Streaming', orbit: 4 },
  { name: 'Healthcare', orbit: 4 },
  { name: 'Entrepreneurship', orbit: 4 },
  { name: 'Data Science', orbit: 4 },
  { name: 'Machine Learning', orbit: 4 },
  { name: 'Venture Capital', orbit: 4 },
  { name: 'Climate', orbit: 4 },
  { name: 'Journalism', orbit: 4 },
  { name: 'Television', orbit: 4 },
  { name: 'Dance', orbit: 4 },
  { name: 'Beauty', orbit: 4 },
  { name: 'Cooking', orbit: 4 },
  { name: 'Pets', orbit: 4 },
  { name: 'Parenting', orbit: 4 },
  { name: 'Religion', orbit: 4 },
  { name: 'Spirituality', orbit: 4 },
  
  // Fifth orbit - far beyond screen
  { name: 'Aviation', orbit: 5 },
  { name: 'Tennis', orbit: 5 },
  { name: 'Golf', orbit: 5 },
  { name: 'Boxing', orbit: 5 },
  { name: 'MMA', orbit: 5 },
  { name: 'Wrestling', orbit: 5 },
  { name: 'Cybersecurity', orbit: 5 },
  { name: 'Robotics', orbit: 5 },
  { name: 'Biotechnology', orbit: 5 },
  { name: 'Sustainability', orbit: 5 },
  { name: 'Luxury', orbit: 5 },
  { name: 'Watches', orbit: 5 },
  { name: 'Sneakers', orbit: 5 },
  { name: 'Streetwear', orbit: 5 },
  { name: 'Vinyl', orbit: 5 },
  { name: 'Concerts', orbit: 5 },
  { name: 'Festivals', orbit: 5 },
  { name: 'Theater', orbit: 5 },
  { name: 'Stand-up', orbit: 5 },
  { name: 'Documentaries', orbit: 5 },
  { name: 'True Crime', orbit: 5 },
  { name: 'Horror', orbit: 5 },
  { name: 'Sci-Fi', orbit: 5 },
  { name: 'Fantasy', orbit: 5 },
]

const getOrbitStyle = (index: number) => {
  const topic = orbitTopics[index]
  const orbit = topic.orbit
  
  // Radius based on orbit level - extends beyond screen edges
  const radii: Record<number, number> = {
    1: 240,
    2: 360,
    3: 500,
    4: 680,
    5: 900,
  }
  const baseRadius = radii[orbit] || 500
  
  // Get count of items in this orbit
  const orbitItems = orbitTopics.filter(t => t.orbit === orbit)
  const orbitIndex = orbitItems.findIndex(t => t.name === topic.name)
  
  // Calculate angle based on position in orbit
  const angleStep = 360 / orbitItems.length
  const startAngle = orbit * 25 // Offset each orbit
  const angle = startAngle + (orbitIndex * angleStep)
  
  // Animation duration - very slow, varies by orbit
  const durations: Record<number, number> = {
    1: 200,
    2: 260,
    3: 320,
    4: 400,
    5: 500,
  }
  const duration = durations[orbit] || 300
  const delay = -(index * 2.5) // Stagger animations
  
  return {
    '--radius': `${baseRadius}px`,
    '--angle': `${angle}deg`,
    '--duration': `${duration}s`,
    '--delay': `${delay}s`,
    '--orbit': orbit,
  }
}

const selectTopic = (topic: string) => {
  searchQuery.value = topic
  handleSearch()
}

const handleSearch = () => {
  if (searchQuery.value.trim()) {
    navigateTo({
      path: '/result',
      query: { q: searchQuery.value }
    })
  }
}

definePageMeta({
  layout: false
})
</script>

<style scoped>
.container {
  min-height: 100vh;
  min-width: 100vw;
  background-color: #000;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 2rem;
  position: relative;
  overflow: hidden;
}

/* Orbit Container */
.orbit-container {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.orbit-topic {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%) rotate(var(--angle)) translateX(var(--radius)) rotate(calc(-1 * var(--angle))) scale(calc(1 + var(--proximity) * 0.15));
  font-size: 0.9rem;
  font-weight: 500;
  color: #fff;
  /* Base opacity + proximity boost */
  opacity: calc(0.15 + var(--proximity) * 0.85);
  cursor: pointer;
  pointer-events: auto;
  white-space: nowrap;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  transition: opacity 0.15s ease-out, transform 0.15s ease-out, background-color 0.15s ease-out, box-shadow 0.15s ease-out, text-shadow 0.15s ease-out;
  animation: orbit var(--duration) linear infinite;
  animation-delay: var(--delay);
  user-select: none;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  /* Proximity-based glow */
  background-color: rgba(255, 255, 255, calc(var(--proximity) * 0.1));
  box-shadow: 
    0 0 calc(var(--proximity) * 25px) rgba(255, 255, 255, calc(var(--proximity) * 0.4)),
    0 0 calc(var(--proximity) * 50px) rgba(255, 255, 255, calc(var(--proximity) * 0.15));
  text-shadow: 0 0 calc(var(--proximity) * 12px) rgba(255, 255, 255, calc(var(--proximity) * 0.6));
}

.orbit-topic:hover {
  opacity: 1 !important;
  animation-play-state: paused;
  background-color: rgba(255, 255, 255, 0.15) !important;
  box-shadow: 
    0 0 30px rgba(255, 255, 255, 0.5),
    0 0 60px rgba(255, 255, 255, 0.2) !important;
  text-shadow: 0 0 15px rgba(255, 255, 255, 0.7) !important;
}

.orbit-topic:active {
  animation-play-state: paused;
  opacity: 0.8 !important;
}

@keyframes orbit {
  from {
    transform: translate(-50%, -50%) rotate(var(--angle)) translateX(var(--radius)) rotate(calc(-1 * var(--angle)));
  }
  to {
    transform: translate(-50%, -50%) rotate(calc(var(--angle) + 360deg)) translateX(var(--radius)) rotate(calc(-1 * (var(--angle) + 360deg)));
  }
}

.title {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  font-size: clamp(2.5rem, 6vw, 3.5rem);
  font-weight: 700;
  color: #e7e9ea;
  margin-bottom: 3rem;
  letter-spacing: -0.03em;
  position: relative;
  z-index: 10;
}

.x-logo {
  color: #fff;
}

.search-form {
  width: 100%;
  max-width: 680px;
  position: relative;
  z-index: 10;
}

.input-wrapper {
  display: flex;
  align-items: center;
  background-color: #16181c;
  border-radius: 28px;
  border: 1px solid #2f3336;
  transition: border-color 0.2s ease;
}

.input-wrapper:focus-within {
  border-color: #fff;
}

.search-input {
  flex: 1;
  background: transparent;
  border: none;
  outline: none;
  padding: 1.1rem 1.5rem;
  font-size: 1.05rem;
  color: #e7e9ea;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.search-input::placeholder {
  color: #9a9fa5;
}

.submit-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: none;
  padding: 0.75rem 1.25rem;
  color: #fff;
  cursor: pointer;
  transition: opacity 0.15s ease;
}

.submit-btn:hover:not(:disabled) {
  opacity: 0.7;
}

.submit-btn:disabled {
  color: #38444d;
  cursor: not-allowed;
}

/* Responsive - hide some orbits on smaller screens */
@media (max-width: 900px) {
  .orbit-topic {
    --radius: calc(var(--radius) * 0.7);
    font-size: 0.75rem;
  }
}

@media (max-width: 600px) {
  .orbit-container {
    display: none;
  }
}
</style>
