<template>
  <div class="debate-container">
    <!-- Header -->
    <div class="debate-header">
      <div class="header-row">
        <div class="header-text">
          <h2 class="debate-title">Expert Debate</h2>
          <p class="debate-subtitle">Top experts discuss: <span class="topic-highlight">{{ keyword || 'Loading...' }}</span></p>
        </div>
        <!-- Voice Mode Toggle -->
        <div class="voice-mode" :class="{ active: voiceMode }">
          <button class="voice-toggle" @click="toggleVoiceMode">
            <div class="voice-icon">
              <svg v-if="voiceMode" width="20" height="20" viewBox="0 0 24 24" fill="none">
                <path d="M12 1C10.34 1 9 2.34 9 4V12C9 13.66 10.34 15 12 15C13.66 15 15 13.66 15 12V4C15 2.34 13.66 1 12 1Z" fill="currentColor"/>
                <path d="M19 10V12C19 15.87 15.87 19 12 19C8.13 19 5 15.87 5 12V10H3V12C3 16.41 6.28 20.06 10.5 20.82V24H13.5V20.82C17.72 20.06 21 16.41 21 12V10H19Z" fill="currentColor"/>
              </svg>
              <svg v-else width="20" height="20" viewBox="0 0 24 24" fill="none">
                <path d="M12 1C10.34 1 9 2.34 9 4V12C9 13.66 10.34 15 12 15C13.66 15 15 13.66 15 12V4C15 2.34 13.66 1 12 1Z" stroke="currentColor" stroke-width="2"/>
                <path d="M19 10V12C19 15.87 15.87 19 12 19C8.13 19 5 15.87 5 12V10M12 19V23M8 23H16" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                <path d="M3 3L21 21" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
            </div>
            <span class="voice-label">{{ voiceMode ? 'Voice On' : 'Voice Off' }}</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Participants Bar -->
    <div class="participants-bar">
      <div class="participants-label">Participants</div>
      <div v-if="loadingExperts" class="participants-loading">
        <div class="spinner-small"></div>
        <span>Loading experts...</span>
      </div>
      <div v-else-if="experts.length === 0" class="participants-empty">
        No experts found
      </div>
      <div v-else class="participants-list">
        <div 
          v-for="expert in experts" 
          :key="expert.username" 
          class="participant"
          :class="{ speaking: currentSpeaker === expert.username }"
        >
          <img :src="expert.avatar" :alt="expert.name" class="participant-avatar" />
          <div class="participant-info">
            <span class="participant-name">{{ expert.name }}</span>
            <span class="participant-role">{{ expert.role }}</span>
          </div>
          <div v-if="currentSpeaker === expert.username" class="speaking-indicator">
            <span class="dot"></span>
            <span class="dot"></span>
            <span class="dot"></span>
          </div>
        </div>
      </div>
    </div>

    <!-- Ask Question Prompt (before debate starts) -->
    <div v-if="!debateStarted && !loadingExperts && experts.length > 0" class="ask-prompt">
      <button 
        class="mic-button" 
        :class="{ recording: isRecording, processing: isProcessingAudio }"
        @click="toggleRecording"
        :disabled="isProcessingAudio"
      >
        <!-- Recording animation -->
        <div v-if="isRecording" class="recording-pulse"></div>
        
        <!-- Processing spinner -->
        <div v-if="isProcessingAudio" class="processing-spinner"></div>
        
        <!-- Mic icon -->
        <svg v-if="!isProcessingAudio" width="48" height="48" viewBox="0 0 24 24" fill="none">
          <path d="M12 1C10.34 1 9 2.34 9 4V12C9 13.66 10.34 15 12 15C13.66 15 15 13.66 15 12V4C15 2.34 13.66 1 12 1Z" fill="currentColor"/>
          <path d="M19 10V12C19 15.87 15.87 19 12 19C8.13 19 5 15.87 5 12V10H3V12C3 16.41 6.28 20.06 10.5 20.82V24H13.5V20.82C17.72 20.06 21 16.41 21 12V10H19Z" fill="currentColor"/>
        </svg>
      </button>
      <p class="ask-prompt-text">
        <span v-if="isProcessingAudio">Processing your question...</span>
        <span v-else-if="isRecording">Recording... Tap to stop</span>
        <span v-else>Tap to ask your question</span>
      </p>
      
      <!-- Show transcribed text if available -->
      <div v-if="transcribedQuestion" class="transcribed-question">
        <p class="transcribed-label">Your question:</p>
        <p class="transcribed-text">"{{ transcribedQuestion }}"</p>
        <div class="transcribed-actions">
          <button class="action-btn cancel" @click="cancelQuestion">Try again</button>
          <button class="action-btn confirm" @click="confirmQuestion">Start debate</button>
        </div>
      </div>
    </div>

    <!-- Chat Area (only show when debate started) -->
    <div v-if="debateStarted" class="chat-area" ref="chatArea">
      <div 
        v-for="(message, index) in displayedMessages" 
        :key="index" 
        class="chat-message"
        :class="{ 'typing': index === displayedMessages.length - 1 && isTyping }"
      >
        <img :src="getExpert(message.speaker).avatar" :alt="message.speaker" class="message-avatar" />
        <div class="message-content">
          <div class="message-header">
            <span class="message-name">{{ getExpert(message.speaker).name }}</span>
            <svg v-if="getExpert(message.speaker).verified" class="verified-badge" width="14" height="14" viewBox="0 0 24 24" fill="#1d9bf0">
              <path d="M22.5 12.5c0-1.58-.875-2.95-2.148-3.6.154-.435.238-.905.238-1.4 0-2.21-1.71-3.998-3.818-3.998-.47 0-.92.084-1.336.25C14.818 2.415 13.51 1.5 12 1.5s-2.816.917-3.437 2.25c-.415-.165-.866-.25-1.336-.25-2.11 0-3.818 1.79-3.818 4 0 .494.083.964.237 1.4-1.272.65-2.147 2.018-2.147 3.6 0 1.495.782 2.798 1.942 3.486-.02.17-.032.34-.032.514 0 2.21 1.708 4 3.818 4 .47 0 .92-.086 1.335-.25.62 1.334 1.926 2.25 3.437 2.25 1.512 0 2.818-.916 3.437-2.25.415.163.865.248 1.336.248 2.11 0 3.818-1.79 3.818-4 0-.174-.012-.344-.033-.513 1.158-.687 1.943-1.99 1.943-3.484zm-6.616-3.334l-4.334 6.5c-.145.217-.382.334-.625.334-.143 0-.288-.04-.416-.126l-.115-.094-2.415-2.415c-.293-.293-.293-.768 0-1.06s.768-.294 1.06 0l1.77 1.767 3.825-5.74c.23-.345.696-.436 1.04-.207.346.23.44.696.21 1.04z"/>
            </svg>
            <span class="message-handle">@{{ message.speaker }}</span>
          </div>
          <p class="message-text" v-html="message.displayedText || message.text"></p>
        </div>
      </div>
      
      <!-- Typing Indicator -->
      <div v-if="isTyping && nextSpeaker" class="typing-indicator">
        <img :src="getExpert(nextSpeaker).avatar" :alt="nextSpeaker" class="typing-avatar" />
        <div class="typing-bubble">
          <span class="typing-dot"></span>
          <span class="typing-dot"></span>
          <span class="typing-dot"></span>
        </div>
      </div>
    </div>

    <!-- Debate Controls (only show when debate started) -->
    <div v-if="debateStarted" class="debate-controls">
      <div class="control-info">
        <span class="message-count">{{ displayedMessages.length }} / {{ experts.length }} experts</span>
      </div>

      <!-- Now Speaking (inline) -->
      <div v-if="voiceMode && currentSpeaker && isTyping" class="now-speaking-inline">
        <img :src="getExpert(currentSpeaker).avatar" :alt="currentSpeaker" class="speaker-avatar-small" />
        <div class="audio-visualizer-small">
          <span class="bar"></span>
          <span class="bar"></span>
          <span class="bar"></span>
          <span class="bar"></span>
          <span class="bar"></span>
          <span class="bar"></span>
          <span class="bar"></span>
          <span class="bar"></span>
        </div>
        <span class="speaker-name-small">{{ getExpert(currentSpeaker).name }}</span>
      </div>

      <div class="control-buttons">
        <button class="control-btn" @click="restartDebate" :disabled="isTyping">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
            <path d="M1 4V10H7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M3.51 15C4.15 16.86 5.38 18.44 7.01 19.49C8.64 20.54 10.57 21 12.5 20.78C14.43 20.56 16.24 19.68 17.62 18.28C19 16.88 19.87 15.04 20.09 13.1C20.3 11.17 19.84 9.23 18.79 7.59C17.74 5.95 16.15 4.71 14.29 4.07C12.43 3.43 10.4 3.42 8.54 4.04C6.68 4.66 5.07 5.88 4 7.5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          Restart
        </button>
        <button class="control-btn primary" @click="togglePause">
          <svg v-if="isPaused" width="16" height="16" viewBox="0 0 24 24" fill="none">
            <polygon points="5,3 19,12 5,21" fill="currentColor"/>
          </svg>
          <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none">
            <rect x="6" y="4" width="4" height="16" fill="currentColor"/>
            <rect x="14" y="4" width="4" height="16" fill="currentColor"/>
          </svg>
          {{ isPaused ? 'Resume' : 'Pause' }}
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

interface Expert {
  name: string
  username: string
  avatar: string
  verified: boolean
  role: string
  posts?: ExpertPost[]
}

interface Message {
  speaker: string
  text: string
  displayedText?: string
}

interface ApiAccount {
  id: string
  name: string
  username: string
  profile_image_url?: string
  verified?: boolean
  description?: string
}

interface ExpertPost {
  text: string
  like_count: number
  retweet_count?: number
}

interface ConversationEntry {
  speaker_name: string
  speaker_role: string
  text: string
}

const debateTopic = ref('')
const currentSpeaker = ref<string | null>(null)
const nextSpeaker = ref<string | null>(null)
const isTyping = ref(false)
const isPaused = ref(false)
const chatArea = ref<HTMLElement | null>(null)
const voiceMode = ref(true) // Voice mode on by default
const loadingExperts = ref(false)
const debateStarted = ref(false)

// Voice recording state
const isRecording = ref(false)
const isProcessingAudio = ref(false)
const transcribedQuestion = ref('')
const mediaRecorder = ref<MediaRecorder | null>(null)
const audioChunks = ref<Blob[]>([])

// Toggle recording on/off
const toggleRecording = async () => {
  if (isRecording.value) {
    stopRecording()
  } else {
    await startRecording()
  }
}

// Start recording audio from microphone
const startRecording = async () => {
  try {
    // Reset state
    audioChunks.value = []
    transcribedQuestion.value = ''
    
    // Request microphone access
    const stream = await navigator.mediaDevices.getUserMedia({ 
      audio: {
        sampleRate: 16000,
        channelCount: 1,
        echoCancellation: true,
        noiseSuppression: true
      } 
    })
    
    // Create MediaRecorder with appropriate mime type
    const mimeType = MediaRecorder.isTypeSupported('audio/webm;codecs=opus') 
      ? 'audio/webm;codecs=opus' 
      : MediaRecorder.isTypeSupported('audio/webm')
        ? 'audio/webm'
        : 'audio/mp4'
    
    mediaRecorder.value = new MediaRecorder(stream, { mimeType })
    
    mediaRecorder.value.ondataavailable = (event: BlobEvent) => {
      if (event.data.size > 0) {
        audioChunks.value.push(event.data)
      }
    }
    
    mediaRecorder.value.onstop = async () => {
      // Stop all tracks
      stream.getTracks().forEach(track => track.stop())
      
      // Process the recorded audio
      await processRecordedAudio()
    }
    
    // Start recording
    mediaRecorder.value.start(100) // Collect data every 100ms
    isRecording.value = true
    
  } catch (error) {
    console.error('Error starting recording:', error)
    alert('Could not access microphone. Please ensure you have granted permission.')
  }
}

// Stop recording
const stopRecording = () => {
  if (mediaRecorder.value && isRecording.value) {
    mediaRecorder.value.stop()
    isRecording.value = false
  }
}

// Process recorded audio and send to STT endpoint
const processRecordedAudio = async () => {
  if (audioChunks.value.length === 0) {
    console.error('No audio recorded')
    return
  }
  
  isProcessingAudio.value = true
  
  try {
    // Create blob from recorded chunks
    const audioBlob = new Blob(audioChunks.value, { type: audioChunks.value[0].type })
    
    // Create FormData and append the audio file
    const formData = new FormData()
    formData.append('audio', audioBlob, 'recording.webm')
    
    // Send to xAI speech-to-text endpoint
    const response = await fetch(`${config.public.apiBase}/grokathon/xai-speech-to-text/`, {
      method: 'POST',
      body: formData
    })
    
    if (!response.ok) {
      throw new Error(`STT request failed: ${response.status}`)
    }
    
    const data = await response.json()
    
    if (data.text) {
      transcribedQuestion.value = data.text
    } else {
      throw new Error('No transcription returned')
    }
    
  } catch (error) {
    console.error('Error processing audio:', error)
    alert('Failed to transcribe audio. Please try again.')
  } finally {
    isProcessingAudio.value = false
  }
}

// Cancel the transcribed question and allow re-recording
const cancelQuestion = () => {
  transcribedQuestion.value = ''
  audioChunks.value = []
}

// Confirm the question and start the debate
const confirmQuestion = () => {
  if (transcribedQuestion.value) {
    debateTopic.value = transcribedQuestion.value
    debateStarted.value = true
    startDebate()
  }
}

const toggleVoiceMode = () => {
  voiceMode.value = !voiceMode.value
}

// Dynamic experts - will be populated from API
const experts = ref<Expert[]>([])

// Fetch experts from the top 5 expert categories
const fetchExperts = async (keyword: string) => {
  loadingExperts.value = true
  experts.value = []
  debateTopic.value = `What are the key insights on ${keyword}?`
  
  try {
    // Step 1: Fetch IDs for the keyword
    const idsResponse = await $fetch<{ ids: string[] }>(
      `${config.public.apiBase}/grokathon/fetch-ids/?input_query=${encodeURIComponent(keyword)}`
    )

    if (!idsResponse.ids || idsResponse.ids.length === 0) {
      return
    }

    // Step 2: Fetch expert categories
    const idsParams = idsResponse.ids.slice(0, 100).map((id: string) => `ids=${id}`).join('&')
    const categoriesResponse = await $fetch<{ categories: Record<string, number[]> }>(
      `${config.public.apiBase}/grokathon/fetch-expert-categories/?${idsParams}`
    )

    if (!categoriesResponse.categories) {
      return
    }

    // Sort categories by count and take top 5
    const sortedCategories = Object.entries(categoriesResponse.categories)
      .sort((a, b) => b[1].length - a[1].length)
      .slice(0, 5)

    // Get the first ID from each category
    const expertIds = sortedCategories.map(([_, ids]) => ids[0]).filter(Boolean)

    if (expertIds.length === 0) {
      return
    }

    // Step 3: Fetch account details for these experts
    const expertIdsParams = expertIds.map((id: number) => `ids=${id}`).join('&')
    const accountsResponse = await $fetch<{ accounts: ApiAccount[] }>(
      `${config.public.apiBase}/grokathon/fetch-accounts/?${expertIdsParams}`
    )

    // Step 4: Fetch posts for these experts
    const postsResponse = await $fetch<{ posts: Array<{ account: { username: string }, post: { text: string, like_count: number, retweet_count: number } }> }>(
      `${config.public.apiBase}/grokathon/fetch-posts/?${expertIdsParams}`
    )

    // Group posts by username
    const postsByUsername: Record<string, ExpertPost[]> = {}
    if (postsResponse.posts) {
      for (const item of postsResponse.posts) {
        const username = item.account?.username
        if (username) {
          if (!postsByUsername[username]) {
            postsByUsername[username] = []
          }
          postsByUsername[username].push({
            text: item.post?.text || '',
            like_count: item.post?.like_count || 0,
            retweet_count: item.post?.retweet_count || 0
          })
        }
      }
    }

    if (accountsResponse.accounts && accountsResponse.accounts.length > 0) {
      // Map accounts to experts with their category as role and posts
      experts.value = accountsResponse.accounts.map((acc: ApiAccount, index: number) => ({
        name: acc.name || acc.username,
        username: acc.username,
        avatar: acc.profile_image_url?.replace('_normal', '_400x400') || '',
        verified: acc.verified || false,
        role: sortedCategories[index]?.[0] || 'Expert',
        posts: postsByUsername[acc.username] || []
      }))
    }
  } catch (err) {
    console.error('Error fetching experts:', err)
  } finally {
    loadingExperts.value = false
  }
}

const displayedMessages = ref<Message[]>([])
const currentMessageIndex = ref(0)
const currentCharIndex = ref(0)

const getExpert = (username: string): Expert => {
  return experts.value.find(e => e.username === username) || experts.value[0] || {
    name: 'Expert',
    username: username,
    avatar: '',
    verified: false,
    role: 'Expert'
  }
}

// Conversation history for AI context
const conversationHistory = ref<ConversationEntry[]>([])

// Stream a single expert's response from the API
const streamExpertResponse = async (expert: Expert, isFirstSpeaker: boolean): Promise<string> => {
  const question = debateTopic.value || props.keyword || 'this topic'
  
  // Add message placeholder
  const messageIndex = displayedMessages.value.length
  displayedMessages.value.push({
    speaker: expert.username,
    text: '',
    displayedText: ''
  })
  scrollToBottom()
  
  currentSpeaker.value = expert.username
  isTyping.value = true
  
  let fullText = ''
  
  try {
    const response = await fetch(`${config.public.apiBase}/grokathon/stream-debate-response/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        question,
        expert_name: expert.name,
        expert_username: expert.username,
        expert_role: expert.role,
        expert_posts: expert.posts || [],
        conversation_history: conversationHistory.value,
        is_first_speaker: isFirstSpeaker
      })
    })
    
    if (!response.ok) {
      throw new Error(`Failed to get response: ${response.status}`)
    }
    
    const reader = response.body?.getReader()
    if (!reader) throw new Error('No reader available')
    
    const decoder = new TextDecoder()
    
    while (true) {
      if (isPaused.value) {
        // Wait while paused
        await new Promise(resolve => setTimeout(resolve, 100))
        continue
      }
      
      const { done, value } = await reader.read()
      if (done) break
      
      const chunk = decoder.decode(value, { stream: true })
      fullText += chunk
      
      // Update displayed text
      if (displayedMessages.value[messageIndex]) {
        displayedMessages.value[messageIndex].displayedText = fullText
        displayedMessages.value[messageIndex].text = fullText
      }
      scrollToBottom()
    }
    
    // Add to conversation history for next expert
    conversationHistory.value.push({
      speaker_name: expert.name,
      speaker_role: expert.role,
      text: fullText
    })
    
  } catch (err) {
    console.error('Error streaming expert response:', err)
    fullText = `As a ${expert.role}, I have some thoughts on this topic...`
    if (displayedMessages.value[messageIndex]) {
      displayedMessages.value[messageIndex].displayedText = fullText
      displayedMessages.value[messageIndex].text = fullText
    }
  }
  
  return fullText
}

const scrollToBottom = () => {
  nextTick(() => {
    if (chatArea.value) {
      chatArea.value.scrollTop = chatArea.value.scrollHeight
    }
  })
}

const startDebate = async () => {
  // First fetch experts if we have a keyword and don't have experts yet
  if (props.keyword && experts.value.length === 0) {
    await fetchExperts(props.keyword)
  }
  
  // Don't start if no experts
  if (experts.value.length === 0) {
    return
  }
  
  // Reset state
  displayedMessages.value = []
  conversationHistory.value = []
  currentMessageIndex.value = 0
  currentCharIndex.value = 0
  isTyping.value = true
  isPaused.value = false
  
  // Stream responses from each expert in sequence
  for (let i = 0; i < experts.value.length; i++) {
    const expert = experts.value[i]
    
    // Set next speaker for typing indicator
    if (i + 1 < experts.value.length) {
      nextSpeaker.value = experts.value[i + 1].username
    } else {
      nextSpeaker.value = null
    }
    
    // Stream this expert's response
    await streamExpertResponse(expert, i === 0)
    
    // Small pause between speakers
    if (i < experts.value.length - 1) {
      await new Promise(resolve => setTimeout(resolve, 1000))
    }
  }
  
  // Debate complete
  isTyping.value = false
  currentSpeaker.value = null
  nextSpeaker.value = null
}

const restartDebate = () => {
  conversationHistory.value = []
  startDebate()
}

const togglePause = () => {
  isPaused.value = !isPaused.value
}

// Load experts when component becomes active (but don't start debate)
watch(() => props.isActive, async (active: boolean) => {
  if (active && props.keyword && experts.value.length === 0) {
    await fetchExperts(props.keyword)
  }
}, { immediate: true })

// Re-fetch when keyword changes
watch(() => props.keyword, async (newKeyword: string | undefined) => {
  if (newKeyword && props.isActive) {
    experts.value = []
    displayedMessages.value = []
    conversationHistory.value = []
    debateStarted.value = false
    await fetchExperts(newKeyword)
  }
})
</script>

<style scoped>
.debate-container {
  max-width: 900px;
  margin: 0 auto;
}

.debate-header {
  margin-bottom: 1.5rem;
}

.header-row {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 1rem;
}

.header-text {
  text-align: left;
}

.debate-title {
  font-size: 1.75rem;
  font-weight: 700;
  color: #e7e9ea;
  margin-bottom: 0.5rem;
}

.debate-subtitle {
  font-size: 1rem;
  color: #71767b;
}

.topic-highlight {
  color: #1d9bf0;
  font-weight: 600;
}

/* Voice Mode Toggle */
.voice-mode {
  flex-shrink: 0;
}

.voice-toggle {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background-color: #16181c;
  border: 1px solid #2f3336;
  border-radius: 50px;
  padding: 0.5rem 1rem 0.5rem 0.65rem;
  color: #71767b;
  font-family: inherit;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.voice-toggle:hover {
  background-color: #1d1f23;
  border-color: #3f4347;
}

.voice-mode.active .voice-toggle {
  color: #e7e9ea;
  border-color: #3f4347;
}

.voice-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background-color: #202327;
  transition: all 0.2s ease;
}

.voice-mode.active .voice-icon {
  background-color: #1d9bf0;
  color: #fff;
}

.voice-label {
  font-weight: 500;
}

/* Now Speaking Inline (in controls bar) */
.now-speaking-inline {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background-color: #202327;
  border-radius: 50px;
  padding: 0.35rem 0.75rem 0.35rem 0.35rem;
}

.speaker-avatar-small {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #1d9bf0;
}

.speaker-name-small {
  font-size: 0.8rem;
  font-weight: 600;
  color: #e7e9ea;
  white-space: nowrap;
}

/* Audio Visualizer Small */
.audio-visualizer-small {
  display: flex;
  align-items: center;
  gap: 2px;
  height: 20px;
}

.audio-visualizer-small .bar {
  width: 3px;
  background-color: #1d9bf0;
  border-radius: 1px;
  animation: sound-wave 0.8s ease-in-out infinite;
}

.audio-visualizer-small .bar:nth-child(1) { height: 30%; animation-delay: 0s; }
.audio-visualizer-small .bar:nth-child(2) { height: 60%; animation-delay: 0.1s; }
.audio-visualizer-small .bar:nth-child(3) { height: 100%; animation-delay: 0.15s; }
.audio-visualizer-small .bar:nth-child(4) { height: 70%; animation-delay: 0.2s; }
.audio-visualizer-small .bar:nth-child(5) { height: 100%; animation-delay: 0.25s; }
.audio-visualizer-small .bar:nth-child(6) { height: 50%; animation-delay: 0.3s; }
.audio-visualizer-small .bar:nth-child(7) { height: 80%; animation-delay: 0.35s; }
.audio-visualizer-small .bar:nth-child(8) { height: 40%; animation-delay: 0.4s; }

@keyframes sound-wave {
  0%, 100% { transform: scaleY(0.5); opacity: 0.6; }
  50% { transform: scaleY(1); opacity: 1; }
}

/* Participants Bar */
.participants-bar {
  background-color: #16181c;
  border: 1px solid #2f3336;
  border-radius: 16px;
  padding: 1rem;
  margin-bottom: 1.5rem;
}

.participants-label {
  font-size: 0.85rem;
  color: #71767b;
  margin-bottom: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.participants-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}

.participants-loading,
.participants-empty {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #71767b;
  font-size: 0.9rem;
  padding: 0.5rem 0;
}

.spinner-small {
  width: 16px;
  height: 16px;
  border: 2px solid #2f3336;
  border-top-color: #1d9bf0;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.participant {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background-color: #202327;
  border: 1px solid #2f3336;
  border-radius: 50px;
  padding: 0.4rem 0.75rem 0.4rem 0.4rem;
  transition: all 0.2s ease;
}

.participant.speaking {
  border-color: #1d9bf0;
  background-color: rgba(29, 155, 240, 0.1);
}

.participant-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  object-fit: cover;
}

.participant-info {
  display: flex;
  flex-direction: column;
}

.participant-name {
  font-size: 0.85rem;
  font-weight: 600;
  color: #e7e9ea;
  line-height: 1.2;
}

.participant-handle {
  font-size: 0.75rem;
  color: #71767b;
}

.participant-role {
  font-size: 0.7rem;
  color: #1d9bf0;
  font-weight: 500;
}

/* Ask Question Prompt */
.ask-prompt {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  gap: 1.5rem;
}

.mic-button {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background-color: #fff;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #000;
  transition: all 0.2s ease;
  box-shadow: 0 4px 20px rgba(255, 255, 255, 0.2);
  position: relative;
  overflow: visible;
}

.mic-button:hover:not(:disabled) {
  transform: scale(1.05);
  box-shadow: 0 6px 30px rgba(255, 255, 255, 0.3);
}

.mic-button:active:not(:disabled) {
  transform: scale(0.95);
}

.mic-button:disabled {
  cursor: not-allowed;
  opacity: 0.8;
}

/* Recording state */
.mic-button.recording {
  background-color: #f91880;
  color: #fff;
  animation: pulse-glow 1.5s ease-in-out infinite;
}

@keyframes pulse-glow {
  0%, 100% {
    box-shadow: 0 0 20px rgba(249, 24, 128, 0.4);
  }
  50% {
    box-shadow: 0 0 40px rgba(249, 24, 128, 0.8);
  }
}

/* Recording pulse animation behind button */
.recording-pulse {
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background-color: rgba(249, 24, 128, 0.3);
  animation: recording-pulse-anim 1.5s ease-out infinite;
  pointer-events: none;
}

@keyframes recording-pulse-anim {
  0% {
    transform: scale(1);
    opacity: 0.8;
  }
  100% {
    transform: scale(1.8);
    opacity: 0;
  }
}

/* Processing state */
.mic-button.processing {
  background-color: #1d9bf0;
  color: #fff;
}

.processing-spinner {
  width: 48px;
  height: 48px;
  border: 4px solid rgba(255, 255, 255, 0.3);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

.ask-prompt-text {
  font-size: 1.1rem;
  color: #71767b;
  text-align: center;
  min-height: 1.5em;
}

/* Transcribed question display */
.transcribed-question {
  margin-top: 1.5rem;
  padding: 1.25rem;
  background-color: #16181c;
  border: 1px solid #2f3336;
  border-radius: 16px;
  max-width: 500px;
  width: 100%;
  animation: fadeIn 0.3s ease;
}

.transcribed-label {
  font-size: 0.85rem;
  color: #71767b;
  margin-bottom: 0.5rem;
}

.transcribed-text {
  font-size: 1.1rem;
  color: #e7e9ea;
  font-style: italic;
  line-height: 1.5;
  margin-bottom: 1rem;
}

.transcribed-actions {
  display: flex;
  gap: 0.75rem;
  justify-content: center;
}

.action-btn {
  padding: 0.6rem 1.25rem;
  border-radius: 50px;
  font-size: 0.9rem;
  font-weight: 600;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.15s ease;
}

.action-btn.cancel {
  background-color: transparent;
  border: 1px solid #536471;
  color: #e7e9ea;
}

.action-btn.cancel:hover {
  background-color: rgba(239, 243, 244, 0.1);
  border-color: #71767b;
}

.action-btn.confirm {
  background-color: #fff;
  border: 1px solid #fff;
  color: #000;
}

.action-btn.confirm:hover {
  background-color: #d1d1d1;
  border-color: #d1d1d1;
}

.speaking-indicator {
  display: flex;
  gap: 2px;
  margin-left: 0.5rem;
}

.speaking-indicator .dot {
  width: 4px;
  height: 4px;
  background-color: #1d9bf0;
  border-radius: 50%;
  animation: bounce 1.4s infinite ease-in-out;
}

.speaking-indicator .dot:nth-child(1) { animation-delay: 0s; }
.speaking-indicator .dot:nth-child(2) { animation-delay: 0.2s; }
.speaking-indicator .dot:nth-child(3) { animation-delay: 0.4s; }

@keyframes bounce {
  0%, 80%, 100% { transform: scale(0.8); opacity: 0.5; }
  40% { transform: scale(1.2); opacity: 1; }
}

/* Chat Area */
.chat-area {
  background-color: #16181c;
  border: 1px solid #2f3336;
  border-radius: 16px;
  padding: 1.5rem;
  height: 500px;
  overflow-y: auto;
  margin-bottom: 1rem;
}

.chat-message {
  display: flex;
  gap: 0.75rem;
  margin-bottom: 1.25rem;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.message-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
  flex-shrink: 0;
}

.message-content {
  flex: 1;
  min-width: 0;
}

.message-header {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  margin-bottom: 0.25rem;
}

.message-name {
  font-weight: 700;
  color: #e7e9ea;
  font-size: 0.95rem;
}

.verified-badge {
  flex-shrink: 0;
}

.message-handle {
  color: #71767b;
  font-size: 0.9rem;
}

.message-text {
  color: #e7e9ea;
  font-size: 0.95rem;
  line-height: 1.5;
}

.message-text :deep(strong) {
  color: #1d9bf0;
  font-weight: 600;
}

/* Typing Indicator */
.typing-indicator {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-top: 1rem;
}

.typing-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
}

.typing-bubble {
  display: flex;
  align-items: center;
  gap: 4px;
  background-color: #202327;
  border-radius: 20px;
  padding: 0.75rem 1rem;
}

.typing-dot {
  width: 8px;
  height: 8px;
  background-color: #71767b;
  border-radius: 50%;
  animation: typingBounce 1.4s infinite ease-in-out;
}

.typing-dot:nth-child(1) { animation-delay: 0s; }
.typing-dot:nth-child(2) { animation-delay: 0.2s; }
.typing-dot:nth-child(3) { animation-delay: 0.4s; }

@keyframes typingBounce {
  0%, 80%, 100% { transform: translateY(0); }
  40% { transform: translateY(-6px); }
}

/* Debate Controls */
.debate-controls {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: #16181c;
  border: 1px solid #2f3336;
  border-radius: 12px;
  padding: 0.75rem 1rem;
}

.control-info {
  color: #71767b;
  font-size: 0.85rem;
}

.control-buttons {
  display: flex;
  gap: 0.5rem;
}

.control-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background-color: transparent;
  border: 1px solid #2f3336;
  border-radius: 8px;
  padding: 0.5rem 1rem;
  color: #e7e9ea;
  font-size: 0.85rem;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.15s ease;
}

.control-btn:hover:not(:disabled) {
  background-color: #202327;
  border-color: #3f4347;
}

.control-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.control-btn.primary {
  background-color: #fff;
  border-color: #fff;
  color: #000;
}

.control-btn.primary:hover:not(:disabled) {
  background-color: #d1d1d1;
  border-color: #d1d1d1;
}

/* Scrollbar */
.chat-area::-webkit-scrollbar {
  width: 8px;
}

.chat-area::-webkit-scrollbar-track {
  background: transparent;
}

.chat-area::-webkit-scrollbar-thumb {
  background-color: #2f3336;
  border-radius: 4px;
}

.chat-area::-webkit-scrollbar-thumb:hover {
  background-color: #3f4347;
}

/* Responsive */
@media (max-width: 768px) {
  .header-row {
    flex-direction: column;
    gap: 1rem;
  }
  
  .header-text {
    text-align: center;
  }
  
  .voice-mode {
    align-self: center;
  }
  
  .participants-list {
    flex-direction: column;
  }
  
  .participant {
    width: 100%;
  }
  
  .chat-area {
    height: 400px;
    padding: 1rem;
  }
  
  .debate-controls {
    flex-wrap: wrap;
    gap: 0.75rem;
  }
  
  .now-speaking-inline {
    order: -1;
    width: 100%;
    justify-content: center;
  }
  
  .control-buttons {
    width: 100%;
    justify-content: center;
  }
}
</style>
