<template>
  <div class="debate-container">
    <!-- Header -->
    <div class="debate-header">
      <div class="header-row">
        <div class="header-text">
          <h2 class="debate-title">Expert Debate</h2>
          <p class="debate-subtitle">Top 5 F1 authorities discuss: <span class="topic-highlight">{{ debateTopic }}</span></p>
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
      <div class="participants-list">
        <div 
          v-for="expert in experts" 
          :key="expert.username" 
          class="participant"
          :class="{ speaking: currentSpeaker === expert.username }"
        >
          <img :src="expert.avatar" :alt="expert.name" class="participant-avatar" />
          <div class="participant-info">
            <span class="participant-name">{{ expert.name }}</span>
            <span class="participant-handle">@{{ expert.username }}</span>
          </div>
          <div v-if="currentSpeaker === expert.username" class="speaking-indicator">
            <span class="dot"></span>
            <span class="dot"></span>
            <span class="dot"></span>
          </div>
        </div>
      </div>
    </div>

    <!-- Chat Area -->
    <div class="chat-area" ref="chatArea">
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

    <!-- Debate Controls -->
    <div class="debate-controls">
      <div class="control-info">
        <span class="message-count">{{ displayedMessages.length }} / {{ debateMessages.length }} messages</span>
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
const props = defineProps<{
  isActive: boolean
}>()

interface Expert {
  name: string
  username: string
  avatar: string
  verified: boolean
  role: string
}

interface Message {
  speaker: string
  text: string
  displayedText?: string
}

const debateTopic = ref('Who will win the 2026 F1 Championship?')
const currentSpeaker = ref<string | null>(null)
const nextSpeaker = ref<string | null>(null)
const isTyping = ref(false)
const isPaused = ref(false)
const chatArea = ref<HTMLElement | null>(null)
const voiceMode = ref(true) // Voice mode on by default

const toggleVoiceMode = () => {
  voiceMode.value = !voiceMode.value
}

const experts: Expert[] = [
  { 
    name: 'Will Buxton', 
    username: 'wbuxtonofficial', 
    avatar: 'https://pbs.twimg.com/profile_images/1935077864577347584/EJo0lH27_normal.jpg',
    verified: true,
    role: 'F1 Journalist'
  },
  { 
    name: 'Karun Chandhok', 
    username: 'karaborun', 
    avatar: 'https://pbs.twimg.com/profile_images/1346044246108white_normal.jpg',
    verified: true,
    role: 'Former F1 Driver & Analyst'
  },
  { 
    name: 'Chris Medland', 
    username: 'ChrisMedlandF1', 
    avatar: 'https://pbs.twimg.com/profile_images/1683782659590848512/o6X8qGQp_normal.jpg',
    verified: true,
    role: 'F1 Correspondent'
  },
  { 
    name: 'Lawrence Barretto', 
    username: 'lawrobarretto', 
    avatar: 'https://pbs.twimg.com/profile_images/1463936071893504003/AwVYvpRd_normal.jpg',
    verified: true,
    role: 'F1 Senior Writer'
  },
  { 
    name: 'Matt Gallagher', 
    username: 'MattGallagherF1', 
    avatar: 'https://pbs.twimg.com/profile_images/1893327368464334848/swYpqR8N_normal.jpg',
    verified: true,
    role: 'F1 Content Creator'
  },
]

const debateMessages: Message[] = [
  {
    speaker: 'wbuxtonofficial',
    text: "Alright everyone, let's dive into it. 2026 is going to be massive with the new regulations. I think <strong>Ferrari</strong> finally has all the pieces in place. Hamilton joining, the new power unit, the momentum from their 2025 improvements..."
  },
  {
    speaker: 'karaborun',
    text: "I have to push back on that, Will. From a technical standpoint, <strong>Mercedes</strong> has been developing their 2026 power unit longer than anyone. They learned harsh lessons from the hybrid era and won't make the same mistakes. Their engine department is unmatched."
  },
  {
    speaker: 'ChrisMedlandF1',
    text: "Here's the thing though - we're forgetting about <strong>McLaren</strong>. They just won the constructors' in 2025, they have the best driver pairing on the grid with Norris and Piastri, and Zak Brown has built an incredible operation. Why would they suddenly fall off?"
  },
  {
    speaker: 'lawrobarretto',
    text: "Chris makes a good point, but regulation resets historically favor the big manufacturer teams. My money is still on Mercedes or Ferrari. <strong>Red Bull's transition to Ford</strong> is the real wild card here. That's a huge risk."
  },
  {
    speaker: 'MattGallagherF1',
    text: "Can we talk about <strong>Aston Martin</strong>? They have Adrian Newey now, Honda power, a brand new wind tunnel, and Lance's dad keeps writing checks. I think they're the dark horse that could shock everyone in 2026."
  },
  {
    speaker: 'wbuxtonofficial',
    text: "Matt, I love Aston's project, but Newey's cars typically take 2-3 years to really hit their stride. Remember when he joined Red Bull? The first year wasn't a championship winner. I'd say 2027 or 2028 for them."
  },
  {
    speaker: 'karaborun',
    text: "That's a fair point. But let's not underestimate the <strong>sustainable fuel regulations</strong>. This is completely new territory. Whoever has cracked that code in testing will have a massive advantage in the first half of the season."
  },
  {
    speaker: 'ChrisMedlandF1',
    text: "I've heard whispers that Ferrari's fuel partnership with Shell has produced some incredible results. If that's true, combined with Hamilton's experience and Leclerc's raw speed... that's a scary combination."
  },
  {
    speaker: 'lawrobarretto',
    text: "The driver factor is huge here. <strong>Hamilton at Ferrari</strong> is the storyline everyone's watching. But Verstappen is still Verstappen - if that Red Bull-Ford package is even 90% there, he'll drag it to victories."
  },
  {
    speaker: 'MattGallagherF1',
    text: "Final prediction time! I'm going bold: <strong>Ferrari wins constructors', but Verstappen wins drivers'</strong>. The Red Bull will be unreliable early on but Max will pull off some heroic drives to stay in it."
  },
  {
    speaker: 'wbuxtonofficial',
    text: "I'll say <strong>Ferrari double championship</strong> - Hamilton WDC, Ferrari WCC. It would be the perfect fairytale ending to Lewis's career and I genuinely believe they have the package to do it."
  },
  {
    speaker: 'karaborun',
    text: "You're all sleeping on Mercedes! <strong>George Russell WDC, Mercedes WCC</strong>. Mark my words. That team knows how to nail regulation changes and George is ready to lead."
  },
  {
    speaker: 'ChrisMedlandF1',
    text: "I'm sticking with <strong>McLaren</strong>. Norris WDC, McLaren WCC. They've built something special and I don't see why new regulations would change their trajectory. They have the best in-season development."
  },
  {
    speaker: 'lawrobarretto',
    text: "Safe pick from me: <strong>Verstappen WDC</strong> (4th title!), but <strong>Ferrari WCC</strong>. The two Ferrari drivers will take points off each other while Max stays consistent. Classic scenario."
  },
]

const displayedMessages = ref<Message[]>([])
const currentMessageIndex = ref(0)
const currentCharIndex = ref(0)

const getExpert = (username: string): Expert => {
  return experts.find(e => e.username === username) || experts[0]
}

const scrollToBottom = () => {
  nextTick(() => {
    if (chatArea.value) {
      chatArea.value.scrollTop = chatArea.value.scrollHeight
    }
  })
}

const typeMessage = () => {
  if (isPaused.value) return
  
  if (currentMessageIndex.value >= debateMessages.length) {
    isTyping.value = false
    currentSpeaker.value = null
    nextSpeaker.value = null
    return
  }

  const message = debateMessages[currentMessageIndex.value]
  
  // Set current speaker
  currentSpeaker.value = message.speaker
  
  // Set next speaker for typing indicator
  if (currentMessageIndex.value + 1 < debateMessages.length) {
    nextSpeaker.value = debateMessages[currentMessageIndex.value + 1].speaker
  } else {
    nextSpeaker.value = null
  }

  // If this is a new message, add it to displayed messages
  if (displayedMessages.value.length <= currentMessageIndex.value) {
    displayedMessages.value.push({
      speaker: message.speaker,
      text: message.text,
      displayedText: ''
    })
    scrollToBottom()
  }

  // Type out the message character by character
  const currentMessage = displayedMessages.value[currentMessageIndex.value]
  if (currentCharIndex.value < message.text.length) {
    isTyping.value = true
    const chunkSize = 3
    currentMessage.displayedText = message.text.slice(0, currentCharIndex.value + chunkSize)
    currentCharIndex.value += chunkSize
    scrollToBottom()
    setTimeout(typeMessage, 15)
  } else {
    // Message complete, move to next
    currentMessage.displayedText = message.text
    currentMessageIndex.value++
    currentCharIndex.value = 0
    
    // Pause between messages
    setTimeout(() => {
      if (!isPaused.value) {
        typeMessage()
      }
    }, 1500)
  }
}

const startDebate = () => {
  displayedMessages.value = []
  currentMessageIndex.value = 0
  currentCharIndex.value = 0
  isTyping.value = true
  isPaused.value = false
  setTimeout(typeMessage, 1000)
}

const restartDebate = () => {
  startDebate()
}

const togglePause = () => {
  isPaused.value = !isPaused.value
  if (!isPaused.value && currentMessageIndex.value < debateMessages.length) {
    typeMessage()
  }
}

// Start debate when component becomes active
watch(() => props.isActive, (active: boolean) => {
  if (active) {
    startDebate()
  }
}, { immediate: true })
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
