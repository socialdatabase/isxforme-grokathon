<template>
  <div class="race-tracker-container">
    <!-- Back Navigation -->
    <nav class="back-nav">
      <NuxtLink to="/AudienceInsights" class="back-link">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
          <path d="M19 12H5M5 12L12 19M5 12L12 5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <span>Audience Insights</span>
      </NuxtLink>
    </nav>

    <!-- Page Header -->
    <header class="page-header">
      <div class="header-badge">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
          <path d="M3 21L12 2L21 21H3Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        Chicago Mayor Race 2027
      </div>
    </header>

    <!-- View Toggle -->
    <div class="view-toggle-container">
      <div class="view-toggle">
        <button 
          class="toggle-btn" 
          :class="{ active: activeView === 'overview' }"
          @click="activeView = 'overview'"
        >
          Overview
        </button>
        <button 
          class="toggle-btn" 
          :class="{ active: activeView === 'conversation' }"
          @click="activeView = 'conversation'"
        >
          Conversation
        </button>
        <button 
          class="toggle-btn" 
          :class="{ active: activeView === 'ai-summary' }"
          @click="switchToAISummary"
        >
          AI Summary
        </button>
      </div>
    </div>

    <!-- Overview View -->
    <div v-show="activeView === 'overview'" class="view-content">
      <!-- All Candidates Row -->
    <section class="candidates-section">
      <div class="candidates-row">
        <!-- Alexi - Featured First -->
        <div class="candidate-card featured">
          <div class="tracking-badge">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none">
              <path d="M12 2L15.09 8.26L22 9.27L17 14.14L18.18 21.02L12 17.77L5.82 21.02L7 14.14L2 9.27L8.91 8.26L12 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            Tracking
          </div>
          <div class="candidate-avatar featured-avatar">
            <img :src="alexiData.avatar" :alt="alexiData.displayName" />
          </div>
          <div class="candidate-info">
            <div class="candidate-name-row">
              <span class="candidate-name">{{ alexiData.displayName }}</span>
              <svg v-if="alexiData.verified" class="verified-badge" width="16" height="16" viewBox="0 0 24 24" fill="#1d9bf0">
                <path d="M22.5 12.5c0-1.58-.875-2.95-2.148-3.6.154-.435.238-.905.238-1.4 0-2.21-1.71-3.998-3.818-3.998-.47 0-.92.084-1.336.25C14.818 2.415 13.51 1.5 12 1.5s-2.816.917-3.437 2.25c-.415-.165-.866-.25-1.336-.25-2.11 0-3.818 1.79-3.818 4 0 .494.083.964.237 1.4-1.272.65-2.147 2.018-2.147 3.6 0 1.495.782 2.798 1.942 3.486-.02.17-.032.34-.032.514 0 2.21 1.708 4 3.818 4 .47 0 .92-.086 1.335-.25.62 1.334 1.926 2.25 3.437 2.25 1.512 0 2.818-.916 3.437-2.25.415.163.865.248 1.336.248 2.11 0 3.818-1.79 3.818-4 0-.174-.012-.344-.033-.513 1.158-.687 1.943-1.99 1.943-3.484zm-6.616-3.334l-4.334 6.5c-.145.217-.382.334-.625.334-.143 0-.288-.04-.416-.126l-.115-.094-2.415-2.415c-.293-.293-.293-.768 0-1.06s.768-.294 1.06 0l1.77 1.767 3.825-5.74c.23-.345.696-.436 1.04-.207.346.23.44.696.21 1.04z"/>
              </svg>
            </div>
            <div class="candidate-handle">@{{ alexiData.username }}</div>
            <p class="candidate-bio">{{ truncateBio(alexiData.bio, 60) }}</p>
          </div>
          <div class="candidate-footer">
            <div class="candidate-followers">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none">
                <path d="M17 21V19C17 17.9391 16.5786 16.9217 15.8284 16.1716C15.0783 15.4214 14.0609 15 13 15H5C3.93913 15 2.92172 15.4214 2.17157 16.1716C1.42143 16.9217 1 17.9391 1 19V21" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M9 11C11.2091 11 13 9.20914 13 7C13 4.79086 11.2091 3 9 3C6.79086 3 5 4.79086 5 7C5 9.20914 6.79086 11 9 11Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              {{ formatNumber(alexiData.followers) }}
            </div>
          </div>
        </div>

        <!-- Other Candidates -->
        <div 
          v-for="candidate in otherCandidates" 
          :key="candidate.username" 
          class="candidate-card"
        >
          <div class="candidate-avatar">
            <img :src="candidate.avatar" :alt="candidate.displayName" />
          </div>
          <div class="candidate-info">
            <div class="candidate-name-row">
              <span class="candidate-name">{{ candidate.displayName }}</span>
              <svg v-if="candidate.verified" class="verified-badge" width="16" height="16" viewBox="0 0 24 24" fill="#1d9bf0">
                <path d="M22.5 12.5c0-1.58-.875-2.95-2.148-3.6.154-.435.238-.905.238-1.4 0-2.21-1.71-3.998-3.818-3.998-.47 0-.92.084-1.336.25C14.818 2.415 13.51 1.5 12 1.5s-2.816.917-3.437 2.25c-.415-.165-.866-.25-1.336-.25-2.11 0-3.818 1.79-3.818 4 0 .494.083.964.237 1.4-1.272.65-2.147 2.018-2.147 3.6 0 1.495.782 2.798 1.942 3.486-.02.17-.032.34-.032.514 0 2.21 1.708 4 3.818 4 .47 0 .92-.086 1.335-.25.62 1.334 1.926 2.25 3.437 2.25 1.512 0 2.818-.916 3.437-2.25.415.163.865.248 1.336.248 2.11 0 3.818-1.79 3.818-4 0-.174-.012-.344-.033-.513 1.158-.687 1.943-1.99 1.943-3.484zm-6.616-3.334l-4.334 6.5c-.145.217-.382.334-.625.334-.143 0-.288-.04-.416-.126l-.115-.094-2.415-2.415c-.293-.293-.293-.768 0-1.06s.768-.294 1.06 0l1.77 1.767 3.825-5.74c.23-.345.696-.436 1.04-.207.346.23.44.696.21 1.04z"/>
              </svg>
            </div>
            <div class="candidate-handle">@{{ candidate.username }}</div>
            <p class="candidate-bio">{{ truncateBio(candidate.bio, 60) }}</p>
          </div>
          <div class="candidate-footer">
            <div class="candidate-followers">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none">
                <path d="M17 21V19C17 17.9391 16.5786 16.9217 15.8284 16.1716C15.0783 15.4214 14.0609 15 13 15H5C3.93913 15 2.92172 15.4214 2.17157 16.1716C1.42143 16.9217 1 17.9391 1 19V21" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M9 11C11.2091 11 13 9.20914 13 7C13 4.79086 11.2091 3 9 3C6.79086 3 5 4.79086 5 7C5 9.20914 6.79086 11 9 11Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              {{ formatNumber(candidate.followers) }}
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Stats Row: Follower Comparison + Growth -->
    <section class="stats-row">
      <!-- Follower Comparison -->
      <div class="stat-card">
        <div class="section-header">
          <h3 class="section-title">Follower Comparison</h3>
          <p class="section-subtitle">Social reach across candidates</p>
        </div>
        
        <div class="comparison-bars">
          <div 
            v-for="candidate in allCandidatesSorted" 
            :key="candidate.username"
            class="comparison-row"
          >
            <div class="comparison-label">
              <img :src="candidate.avatar" :alt="candidate.displayName" class="comparison-avatar" />
              <span class="comparison-name">{{ candidate.displayName.split(' ')[0] }}</span>
            </div>
            <div class="comparison-bar-container">
              <div 
                class="comparison-bar" 
                :class="{ 'is-alexi': candidate.username === 'Giannoulias' }"
                :style="{ width: getBarWidth(candidate.followers) + '%' }"
              >
                <span class="comparison-value">{{ formatNumber(candidate.followers) }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Follower Growth Comparison -->
      <div class="stat-card">
        <div class="section-header">
          <h3 class="section-title">Growth Comparison</h3>
          <p class="section-subtitle">Net follower change (last 7 months)</p>
        </div>
        
        <div class="growth-comparison">
          <div 
            v-for="candidate in candidateGrowthSorted" 
            :key="candidate.username"
            class="growth-row"
          >
            <div class="growth-label">
              <img :src="candidate.avatar" :alt="candidate.name" class="growth-avatar" />
              <span class="growth-name">{{ candidate.name.split(' ')[0] }}</span>
            </div>
            <div class="growth-bar-track">
              <div 
                class="growth-bar-fill" 
                :class="{ 
                  'is-positive': candidate.change > 0, 
                  'is-negative': candidate.change < 0,
                  'is-alexi': candidate.username === 'Giannoulias'
                }"
                :style="{ width: getGrowthWidth(candidate.change) + '%' }"
              >
              </div>
            </div>
            <div class="growth-stats">
              <span class="growth-change-value" :class="{ positive: candidate.change > 0, negative: candidate.change < 0 }">
                {{ candidate.change >= 0 ? '+' : '' }}{{ formatNumber(candidate.change) }}
              </span>
              <span class="growth-percent-value" :class="{ positive: candidate.percent > 0, negative: candidate.percent < 0 }">
                {{ candidate.percent >= 0 ? '+' : '' }}{{ candidate.percent.toFixed(1) }}%
              </span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Share of Voice & Mentions Section -->
    <section class="stats-row">
      <!-- Share of Voice -->
      <div class="stat-card">
        <div class="section-header">
          <h3 class="section-title">Share of Voice</h3>
          <p class="section-subtitle">Conversation volume (Dec 22 - Jan 22)</p>
        </div>
        
        <div class="voice-comparison">
          <div 
            v-for="candidate in shareOfVoiceSorted" 
            :key="candidate.username"
            class="voice-row"
          >
            <div class="voice-label">
              <img :src="candidate.avatar" :alt="candidate.name" class="voice-avatar" />
              <span class="voice-name">{{ candidate.name.split(' ')[0] }}</span>
            </div>
            <div class="voice-bar-container">
              <div 
                class="voice-bar" 
                :class="{ 'is-alexi': candidate.username === 'Giannoulias' }"
                :style="{ width: getVoiceWidth(candidate.posts) + '%' }"
              >
              </div>
            </div>
            <div class="voice-stats">
              <span class="voice-count">{{ formatNumber(candidate.posts) }}</span>
              <span class="voice-percent">{{ getVoicePercent(candidate.posts) }}%</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Alexi Mentions Over Time -->
      <div class="stat-card">
        <div class="section-header">
          <h3 class="section-title">Alexi Giannoulias mentions over time</h3>
          <p class="section-subtitle">Dec 22 - Jan 22</p>
        </div>
        
        <div class="mentions-chart">
          <div class="chart-stats">
            <div class="chart-total">
              <span class="chart-total-value">28K</span>
              <span class="chart-total-label">Total Posts</span>
            </div>
            <div class="chart-authors">
              <span class="chart-authors-value">19K</span>
              <span class="chart-authors-label">Unique Authors</span>
            </div>
          </div>
          
          <div class="chart-container">
            <svg class="mentions-svg" viewBox="0 0 400 150" preserveAspectRatio="none">
              <!-- Grid lines -->
              <line x1="0" y1="30" x2="400" y2="30" stroke="#2f3336" stroke-width="1"/>
              <line x1="0" y1="60" x2="400" y2="60" stroke="#2f3336" stroke-width="1"/>
              <line x1="0" y1="90" x2="400" y2="90" stroke="#2f3336" stroke-width="1"/>
              <line x1="0" y1="120" x2="400" y2="120" stroke="#2f3336" stroke-width="1"/>
              
              <!-- The mentions spike line -->
              <path 
                d="M0,145 L50,145 L80,144 L120,143 L160,142 L200,140 L220,135 L240,120 L260,80 L280,20 L300,80 L320,130 L340,142 L360,144 L380,145 L400,145" 
                fill="none" 
                stroke="#1d9bf0" 
                stroke-width="2"
              />
              
              <!-- Gradient fill under the line -->
              <defs>
                <linearGradient id="mentionsGradient" x1="0%" y1="0%" x2="0%" y2="100%">
                  <stop offset="0%" style="stop-color:#1d9bf0;stop-opacity:0.3"/>
                  <stop offset="100%" style="stop-color:#1d9bf0;stop-opacity:0"/>
                </linearGradient>
              </defs>
              <path 
                d="M0,145 L50,145 L80,144 L120,143 L160,142 L200,140 L220,135 L240,120 L260,80 L280,20 L300,80 L320,130 L340,142 L360,144 L380,145 L400,145 L400,150 L0,150 Z" 
                fill="url(#mentionsGradient)"
              />
            </svg>
            
            <div class="chart-x-axis">
              <span>Dec 25</span>
              <span>Jan 1</span>
              <span>Jan 7</span>
              <span>Jan 13</span>
              <span>Jan 19</span>
            </div>
          </div>
          
          <div class="chart-peak">
            <span class="peak-label">Peak:</span>
            <span class="peak-value">~11K posts on Jan 13</span>
          </div>
        </div>
      </div>
    </section>

    <!-- Coming Soon Sections -->
    <section class="coming-soon-section">
      <div class="coming-soon-grid">
        <div class="coming-soon-card">
          <div class="coming-soon-icon">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
              <path d="M12 20V10" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M18 20V4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M6 20V16" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <h4 class="coming-soon-title">Strong / Weak Topics</h4>
          <p class="coming-soon-desc">Topic performance analysis</p>
        </div>
      </div>
    </section>
    </div>
    <!-- End Overview View -->

    <!-- Conversation View -->
    <div v-show="activeView === 'conversation'" class="view-content">
      <div class="timeline-container">
        <div class="timeline-layout">
          <!-- Timeline Feed -->
          <div class="timeline-feed">
            <!-- Loading Spinner for Posts -->
            <div v-if="loadingPosts" class="posts-loading">
              <div class="posts-spinner"></div>
              <p class="posts-loading-text">Loading posts from candidates...</p>
            </div>
            
            <!-- Posts List -->
            <template v-else>
              <div v-if="timelineTweets.length === 0" class="posts-empty">
                <p>No posts found. Click "Load Posts" to fetch latest posts from candidates.</p>
              </div>
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
                    <span class="tweet-date">
                      <a target="_blank" :href="'https://x.com/i/status/' + tweet.id">{{ tweet.date }}</a>
                    </span>
                  </div>
                  <p class="tweet-body">{{ formatTweetText(tweet.text) }}</p>
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

          <!-- Accounts Sidebar -->
          <div class="candidates-sidebar">
            <!-- Sidebar Toggle -->
            <div class="sidebar-toggle">
              <button 
                class="sidebar-toggle-btn" 
                :class="{ active: conversationMode === 'candidates' }"
                @click="switchConversationMode('candidates')"
              >
                Candidates
              </button>
              <button 
                class="sidebar-toggle-btn" 
                :class="{ active: conversationMode === 'chicago' }"
                @click="switchConversationMode('chicago')"
              >
                Chicago
              </button>
            </div>

            <!-- Loading state for Chicago accounts -->
            <div v-if="loadingChicagoAccounts" class="sidebar-loading">
              <div class="sidebar-spinner"></div>
              <p>Loading Chicago accounts...</p>
            </div>

            <!-- Candidates List -->
            <div v-else-if="conversationMode === 'candidates'" class="sidebar-list">
              <!-- Alexi First -->
              <div class="sidebar-item featured">
                <div class="sidebar-avatar">
                  <img :src="alexiData.avatar" :alt="alexiData.displayName" />
                </div>
                <div class="sidebar-info">
                  <div class="sidebar-name">
                    {{ alexiData.displayName }}
                    <svg v-if="alexiData.verified" class="sidebar-verified" width="14" height="14" viewBox="0 0 24 24" fill="#1d9bf0">
                      <path d="M22.5 12.5c0-1.58-.875-2.95-2.148-3.6.154-.435.238-.905.238-1.4 0-2.21-1.71-3.998-3.818-3.998-.47 0-.92.084-1.336.25C14.818 2.415 13.51 1.5 12 1.5s-2.816.917-3.437 2.25c-.415-.165-.866-.25-1.336-.25-2.11 0-3.818 1.79-3.818 4 0 .494.083.964.237 1.4-1.272.65-2.147 2.018-2.147 3.6 0 1.495.782 2.798 1.942 3.486-.02.17-.032.34-.032.514 0 2.21 1.708 4 3.818 4 .47 0 .92-.086 1.335-.25.62 1.334 1.926 2.25 3.437 2.25 1.512 0 2.818-.916 3.437-2.25.415.163.865.248 1.336.248 2.11 0 3.818-1.79 3.818-4 0-.174-.012-.344-.033-.513 1.158-.687 1.943-1.99 1.943-3.484zm-6.616-3.334l-4.334 6.5c-.145.217-.382.334-.625.334-.143 0-.288-.04-.416-.126l-.115-.094-2.415-2.415c-.293-.293-.293-.768 0-1.06s.768-.294 1.06 0l1.77 1.767 3.825-5.74c.23-.345.696-.436 1.04-.207.346.23.44.696.21 1.04z"/>
                    </svg>
                  </div>
                  <div class="sidebar-handle">@{{ alexiData.username }}</div>
                </div>
                <div class="sidebar-followers">{{ formatNumber(alexiData.followers) }}</div>
              </div>
              <!-- Other Candidates -->
              <div v-for="candidate in otherCandidates" :key="candidate.username" class="sidebar-item">
                <div class="sidebar-avatar">
                  <img :src="candidate.avatar" :alt="candidate.displayName" />
                </div>
                <div class="sidebar-info">
                  <div class="sidebar-name">
                    {{ candidate.displayName.split(' ').slice(0, 2).join(' ') }}
                    <svg v-if="candidate.verified" class="sidebar-verified" width="14" height="14" viewBox="0 0 24 24" fill="#1d9bf0">
                      <path d="M22.5 12.5c0-1.58-.875-2.95-2.148-3.6.154-.435.238-.905.238-1.4 0-2.21-1.71-3.998-3.818-3.998-.47 0-.92.084-1.336.25C14.818 2.415 13.51 1.5 12 1.5s-2.816.917-3.437 2.25c-.415-.165-.866-.25-1.336-.25-2.11 0-3.818 1.79-3.818 4 0 .494.083.964.237 1.4-1.272.65-2.147 2.018-2.147 3.6 0 1.495.782 2.798 1.942 3.486-.02.17-.032.34-.032.514 0 2.21 1.708 4 3.818 4 .47 0 .92-.086 1.335-.25.62 1.334 1.926 2.25 3.437 2.25 1.512 0 2.818-.916 3.437-2.25.415.163.865.248 1.336.248 2.11 0 3.818-1.79 3.818-4 0-.174-.012-.344-.033-.513 1.158-.687 1.943-1.99 1.943-3.484zm-6.616-3.334l-4.334 6.5c-.145.217-.382.334-.625.334-.143 0-.288-.04-.416-.126l-.115-.094-2.415-2.415c-.293-.293-.293-.768 0-1.06s.768-.294 1.06 0l1.77 1.767 3.825-5.74c.23-.345.696-.436 1.04-.207.346.23.44.696.21 1.04z"/>
                    </svg>
                  </div>
                  <div class="sidebar-handle">@{{ candidate.username }}</div>
                </div>
                <div class="sidebar-followers">{{ formatNumber(candidate.followers) }}</div>
              </div>
            </div>

            <!-- Chicago Accounts List -->
            <div v-else class="sidebar-list">
              <div v-if="chicagoAccounts.length === 0" class="sidebar-empty">
                <p>No Chicago accounts found</p>
              </div>
              <div v-for="account in chicagoAccounts" :key="account.id" class="sidebar-item">
                <div class="sidebar-avatar">
                  <img :src="account.profile_image_url" :alt="account.name" />
                </div>
                <div class="sidebar-info">
                  <div class="sidebar-name">
                    {{ account.name.split(' ').slice(0, 2).join(' ') }}
                    <svg v-if="account.verified" class="sidebar-verified" width="14" height="14" viewBox="0 0 24 24" fill="#1d9bf0">
                      <path d="M22.5 12.5c0-1.58-.875-2.95-2.148-3.6.154-.435.238-.905.238-1.4 0-2.21-1.71-3.998-3.818-3.998-.47 0-.92.084-1.336.25C14.818 2.415 13.51 1.5 12 1.5s-2.816.917-3.437 2.25c-.415-.165-.866-.25-1.336-.25-2.11 0-3.818 1.79-3.818 4 0 .494.083.964.237 1.4-1.272.65-2.147 2.018-2.147 3.6 0 1.495.782 2.798 1.942 3.486-.02.17-.032.34-.032.514 0 2.21 1.708 4 3.818 4 .47 0 .92-.086 1.335-.25.62 1.334 1.926 2.25 3.437 2.25 1.512 0 2.818-.916 3.437-2.25.415.163.865.248 1.336.248 2.11 0 3.818-1.79 3.818-4 0-.174-.012-.344-.033-.513 1.158-.687 1.943-1.99 1.943-3.484zm-6.616-3.334l-4.334 6.5c-.145.217-.382.334-.625.334-.143 0-.288-.04-.416-.126l-.115-.094-2.415-2.415c-.293-.293-.293-.768 0-1.06s.768-.294 1.06 0l1.77 1.767 3.825-5.74c.23-.345.696-.436 1.04-.207.346.23.44.696.21 1.04z"/>
                    </svg>
                  </div>
                  <div class="sidebar-handle">@{{ account.username }}</div>
                </div>
                <div class="sidebar-followers">{{ formatNumber(account.followers_count) }}</div>
              </div>
            </div>
            
            <!-- Load Posts Button -->
            <button 
              class="load-posts-btn" 
              :disabled="loadingPosts || loadingChicagoAccounts"
              @click="fetchPosts"
            >
              <svg v-if="!loadingPosts" width="18" height="18" viewBox="0 0 24 24" fill="none">
                <path d="M23 4V10H17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M20.49 15C19.84 16.8399 18.6096 18.4187 16.9842 19.5073C15.3588 20.5959 13.4265 21.1355 11.4784 21.0462C9.53038 20.9568 7.65871 20.2433 6.14617 19.0109C4.63364 17.7785 3.55953 16.0931 3.08407 14.2003C2.60861 12.3074 2.75767 10.3067 3.50915 8.50319C4.26063 6.69972 5.57466 5.18819 7.25578 4.18819C8.9369 3.18819 10.8977 2.7531 12.8387 2.94914C14.7797 3.14518 16.5996 3.96155 18.04 5.27L23 10" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              <div v-else class="btn-spinner"></div>
              {{ loadingPosts ? 'Loading...' : 'Load Posts' }}
            </button>
          </div>
        </div>
      </div>
    </div>
    <!-- End Conversation View -->

    <!-- AI Summary View -->
    <div v-show="activeView === 'ai-summary'" class="view-content">
      <div class="ai-summary-container">
        <div class="ai-summary-layout">
          <!-- AI Chat Section -->
          <div class="ai-chat">
            <!-- Chicago Experts Found -->
            <div class="ai-accordion">
              <button class="ai-accordion-header" @click="toggleAIEntities">
                <span>{{ aiEntitiesCountDisplay }}</span>
                <div v-if="aiEntityAvatars.length > 0" class="ai-entity-avatars">
                  <img v-for="(avatar, index) in aiEntityAvatars" :key="index" :src="avatar" alt="Expert" class="ai-entity-avatar" />
                </div>
                <svg class="ai-accordion-arrow" :class="{ open: aiEntitiesOpen }" width="20" height="20" viewBox="0 0 24 24" fill="none">
                  <path d="M6 9L12 15L18 9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </button>
              <div v-if="aiEntitiesOpen" class="ai-accordion-content">
                <div v-if="aiLoadingEntities" class="ai-entity-loading">
                  <div class="ai-spinner-small"></div>
                  <span>Loading Chicago experts...</span>
                </div>
                <div v-else class="ai-entity-list">
                  <div v-for="account in aiEntityAccountsDisplay" :key="account.username" class="ai-entity-item">
                    <img :src="account.avatar" :alt="account.displayName" />
                    <span>{{ account.displayName }}</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Content Sources -->
            <div class="ai-accordion">
              <button class="ai-accordion-header" @click="toggleAISources">
                <span>{{ aiContentPostsCountDisplay }}</span>
                <svg class="ai-accordion-arrow" :class="{ open: aiSourcesOpen }" width="20" height="20" viewBox="0 0 24 24" fill="none">
                  <path d="M6 9L12 15L18 9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </button>
              <div v-if="aiSourcesOpen" class="ai-accordion-content">
                <div v-if="aiLoadingPosts" class="ai-entity-loading">
                  <div class="ai-spinner-small"></div>
                  <span>Loading posts...</span>
                </div>
                <div v-else-if="aiContentPosts.length > 0" class="ai-content-posts-list">
                  <div v-for="post in aiContentPosts" :key="post.id" class="ai-content-post-item">
                    <img :src="post.avatar" :alt="post.username" class="ai-content-post-avatar" />
                    <div class="ai-content-post-body">
                      <a :href="`https://x.com/${post.username}/status/${post.id}`" target="_blank" class="ai-content-post-link">
                        <span class="ai-content-post-username">@{{ post.username }}</span>
                        <span class="ai-content-post-text">{{ truncateAIText(post.text, 80) }}</span>
                      </a>
                      <span class="ai-content-post-likes">❤️ {{ formatNumber(post.likes) }}</span>
                    </div>
                  </div>
                </div>
                <p v-else class="ai-no-posts">No posts found</p>
              </div>
            </div>

            <!-- User Query -->
            <div class="ai-query">
              <span class="ai-query-text">{{ aiCurrentQuestion }}</span>
            </div>

            <!-- AI Response -->
            <div class="ai-response">
              <div v-if="aiLoadingResponse && !aiDisplayedResponse" class="ai-response-loading">
                <div class="ai-spinner-small"></div>
                <span>Analyzing Chicago political landscape...</span>
              </div>
              <template v-else>
                <p v-html="aiDisplayedResponse"></p>
                <span v-if="aiIsTyping" class="ai-typing-cursor">|</span>
              </template>
            </div>

            <!-- Follow-up Prompt -->
            <form class="ai-followup" @submit.prevent="handleAIFollowup">
              <input
                v-model="aiFollowupInput"
                type="text"
                class="ai-followup-input"
                placeholder="Ask a follow-up question..."
              />
              <button type="submit" class="ai-followup-submit" :disabled="!aiFollowupInput.trim()">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
                  <path d="M5 12H19M19 12L12 5M19 12L12 19" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </button>
            </form>
          </div>

          <!-- Expert Views Sidebar -->
          <div class="ai-expert-views">
            <h3 class="ai-expert-title">Expert Views</h3>
            <p class="ai-expert-subtitle">Filter by perspective</p>
            <div class="ai-expert-categories">
              <div v-if="aiLoadingCategories" class="ai-categories-loading">
                <div class="ai-spinner-small"></div>
                <span>Loading categories...</span>
              </div>
              <template v-else-if="aiExpertCategories.length > 0">
                <button 
                  v-for="category in aiExpertCategories" 
                  :key="category.name"
                  class="ai-expert-category"
                  :class="{ active: aiSelectedExpertView === category.name }"
                  @click="selectAIExpertView(category.name)"
                >
                  <span class="ai-category-name">{{ category.name }}</span>
                  <span class="ai-category-count">{{ category.count }}</span>
                </button>
              </template>
              <p v-else class="ai-no-categories">No expert categories found</p>
            </div>
          </div>
        </div>
      </div>
    </div>
    <!-- End AI Summary View -->
  </div>
</template>

<script setup lang="ts">
interface Candidate {
  id: number
  username: string
  displayName: string
  avatar: string
  followers: number
  verified: boolean
  bio: string
}

definePageMeta({
  layout: false
})

// View toggle state
const activeView = ref<'overview' | 'conversation' | 'ai-summary'>('overview')

// Conversation sidebar toggle state
const conversationMode = ref<'candidates' | 'chicago'>('candidates')

// =============================================================================
// AI SUMMARY STATE
// =============================================================================
const aiSummaryLoaded = ref(false)
const aiEntitiesOpen = ref(false)
const aiSourcesOpen = ref(false)
const aiIsTyping = ref(false)
const aiDisplayedResponse = ref('')
const aiFollowupInput = ref('')
const aiSelectedExpertView = ref<string | null>(null)
const aiLoadingEntities = ref(false)
const aiLoadingCategories = ref(false)
const aiLoadingPosts = ref(false)
const aiLoadingResponse = ref(false)
const aiTotalEntitiesCount = ref(0)

interface AIEntityAccount {
  id: string
  displayName: string
  username: string
  avatar: string
}

interface AIContentPost {
  id: string
  text: string
  username: string
  avatar: string
  likes: number
}

interface AIExpertCategory {
  name: string
  count: number | string
  ids: number[]
}

interface AIConversationMessage {
  role: 'user' | 'assistant'
  content: string
}

const aiEntityAccounts = ref<AIEntityAccount[]>([])
const aiEntityIds = ref<string[]>([])
const aiContentPosts = ref<AIContentPost[]>([])
const aiExpertCategories = ref<AIExpertCategory[]>([])
const aiConversationHistory = ref<AIConversationMessage[]>([])

// Initial question for Chicago politics
const aiInitialQuestion = "What are relevant (political) topics discussed in Chicago right now? and what's the current sentiment for each candidate running for mayor in Chicago?"

const aiCurrentQuestion = computed(() => {
  if (aiSelectedExpertView.value) {
    return `What's the latest from ${aiSelectedExpertView.value} on Chicago politics?`
  }
  return aiInitialQuestion
})

const aiEntitiesCountDisplay = computed(() => {
  if (aiLoadingEntities.value) return 'Loading Chicago experts...'
  const count = aiTotalEntitiesCount.value
  if (count === 0) return 'No experts found'
  if (count >= 1000) return `${Math.floor(count / 1000)}K+ Chicago experts found...`
  return `${count}+ Chicago experts found...`
})

const aiContentPostsCountDisplay = computed(() => {
  if (aiLoadingPosts.value) return 'Loading content...'
  if (aiContentPosts.value.length === 0) return 'Content found on:'
  return `Content found on: ${aiContentPosts.value.length} posts`
})

const aiEntityAvatars = computed(() => 
  aiEntityAccounts.value.slice(0, 10).map((acc: AIEntityAccount) => acc.avatar)
)

const aiEntityAccountsDisplay = computed(() => 
  aiEntityAccounts.value.slice(0, 25)
)

// Truncate text helper
const truncateAIText = (text: string, maxLength: number): string => {
  if (text.length <= maxLength) return text
  return text.slice(0, maxLength).trim() + '...'
}

// =============================================================================
// TIMELINE / CONVERSATION DATA
// =============================================================================
const config = useRuntimeConfig()

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

const loadingPosts = ref(false)
const timelineTweets = ref<TimelineTweet[]>([])

// Chicago accounts state
interface ChicagoAccount {
  id: string
  username: string
  name: string
  profile_image_url: string
  followers_count: number
  verified: boolean
  description: string
}
const chicagoAccounts = ref<ChicagoAccount[]>([])
const loadingChicagoAccounts = ref(false)

// Fetch Chicago accounts
const fetchChicagoAccounts = async () => {
  if (chicagoAccounts.value.length > 0) return // Already loaded
  
  loadingChicagoAccounts.value = true
  try {
    const response = await fetch(
      `${config.public.apiBase}/grokathon/get-accounts-with-ranks/?input_query=@chicago`
    )
    const data = await response.json() as { accounts: any[] }
    
    if (data.accounts && data.accounts.length > 0) {
      chicagoAccounts.value = data.accounts.slice(0, 20).map((acc: any) => ({
        id: acc.id,
        username: acc.username,
        name: acc.name,
        profile_image_url: acc.profile_image_url || '',
        followers_count: acc.public_metrics?.followers_count || 0,
        verified: acc.verified || false,
        description: acc.description || ''
      }))
    }
  } catch (err) {
    console.error('Error fetching Chicago accounts:', err)
  } finally {
    loadingChicagoAccounts.value = false
  }
}

// Candidate IDs for fetching posts
const candidateIds = [
  '71360328',           // Alexi Giannoulias
  '1577490840179691521', // Brandon Johnson  
  '56864092',           // Mike Quigley
  '22939964',           // Susana Mendoza
  '777071247398240257', // Maria Pappas
  '16639612',           // Joe Holberg
]

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

const formatTweetText = (text: string): string => {
  return text.replace(/https:\/\/t\.co\/\w+/gi, '')
}

// Get IDs based on current conversation mode
const getActiveIds = (): string[] => {
  if (conversationMode.value === 'chicago') {
    return chicagoAccounts.value.map((acc: ChicagoAccount) => acc.id)
  }
  return candidateIds
}

// Fetch posts from active accounts (candidates or chicago)
const fetchPosts = async () => {
  const ids = getActiveIds()
  if (ids.length === 0) {
    timelineTweets.value = []
    return
  }

  loadingPosts.value = true
  timelineTweets.value = []

  try {
    const idsParams = ids.map((id: string) => `ids=${id}`).join('&')
    const response = await fetch(
      `${config.public.apiBase}/grokathon/alexi-posts-timeline/?${idsParams}&n_per_account=15`
    )
    const data = await response.json() as { posts: any[] }

    if (data.posts && data.posts.length > 0) {
      timelineTweets.value = data.posts.slice(0, 100).map((item: any) => {
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
          displayName: item.account.username,
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
  } finally {
    loadingPosts.value = false
  }
}

// Switch conversation mode
const switchConversationMode = async (mode: 'candidates' | 'chicago') => {
  if (conversationMode.value === mode) return
  
  conversationMode.value = mode
  timelineTweets.value = [] // Clear current posts
  
  if (mode === 'chicago') {
    await fetchChicagoAccounts()
  }
  
  // Automatically fetch posts for the new mode
  await fetchPosts()
}

// =============================================================================
// AI SUMMARY FUNCTIONS
// =============================================================================

// Fetch Chicago experts and start AI analysis
const fetchAIChicagoExperts = async () => {
  if (aiEntityIds.value.length > 0) return // Already loaded
  
  aiLoadingEntities.value = true
  aiLoadingCategories.value = true
  aiLoadingPosts.value = true
  
  try {
    // Fetch IDs for @chicago accounts
    const response = await fetch(
      `${config.public.apiBase}/grokathon/fetch-ids/?input_query=${encodeURIComponent('@chicago')}`
    )
    const data = await response.json() as { ids: string[] }
    
    if (data.ids && data.ids.length > 0) {
      aiTotalEntitiesCount.value = data.ids.length
      aiEntityIds.value = data.ids.slice(0, 100)
      
      // Fetch account details for display
      const idsParams = data.ids.slice(0, 25).map((id: string) => `ids=${id}`).join('&')
      const accountsResponse = await fetch(
        `${config.public.apiBase}/grokathon/fetch-accounts/?${idsParams}`
      )
      const accountsData = await accountsResponse.json() as { accounts: any[] }
      
      if (accountsData.accounts) {
        aiEntityAccounts.value = accountsData.accounts.map((acc: any) => ({
          id: acc.id,
          displayName: acc.name,
          username: acc.username,
          avatar: acc.profile_image_url || ''
        }))
      }
      
      // Fetch expert categories
      await fetchAIExpertCategories(aiEntityIds.value)
      
      // Fetch content posts
      await fetchAIContentPosts(aiEntityIds.value)
    }
  } catch (err) {
    console.error('Error fetching AI Chicago experts:', err)
  } finally {
    aiLoadingEntities.value = false
  }
}

const fetchAIExpertCategories = async (ids: string[]) => {
  if (ids.length === 0) return
  
  try {
    const idsParams = ids.map((id: string) => `ids=${id}`).join('&')
    const response = await fetch(
      `${config.public.apiBase}/grokathon/fetch-expert-categories/?${idsParams}`
    )
    const data = await response.json() as { categories: Record<string, number[]> }
    
    if (data.categories) {
      aiExpertCategories.value = Object.entries(data.categories)
        .map(([name, categoryIds]: [string, number[]]) => ({
          name,
          count: categoryIds.length >= 1000 ? `${Math.floor(categoryIds.length / 1000)}K+` : categoryIds.length,
          ids: categoryIds
        }))
        .sort((a, b) => {
          const countA = typeof a.count === 'string' ? parseInt(a.count) * 1000 : a.count
          const countB = typeof b.count === 'string' ? parseInt(b.count) * 1000 : b.count
          return countB - countA
        })
    }
  } catch (err) {
    console.error('Error fetching AI expert categories:', err)
  } finally {
    aiLoadingCategories.value = false
  }
}

const fetchAIContentPosts = async (ids: string[]) => {
  if (ids.length === 0) return
  
  try {
    const idsParams = ids.slice(0, 20).map((id: string) => `ids=${id}`).join('&')
    const response = await fetch(
      `${config.public.apiBase}/grokathon/fetch-posts/?${idsParams}`
    )
    const data = await response.json() as { posts: any[] }
    
    if (data.posts) {
      aiContentPosts.value = data.posts
        .map((item: any) => ({
          id: item.post.id,
          text: item.post.text,
          username: item.account.username,
          avatar: item.account.profile_image_url || '',
          likes: item.post.like_count || 0
        }))
        .sort((a: AIContentPost, b: AIContentPost) => b.likes - a.likes)
        .slice(0, 20)
    }
  } catch (err) {
    console.error('Error fetching AI content posts:', err)
  } finally {
    aiLoadingPosts.value = false
  }
}

// Stream AI response
const streamAIResponse = async () => {
  if (aiEntityIds.value.length === 0) return
  
  aiLoadingResponse.value = true
  aiIsTyping.value = true
  aiDisplayedResponse.value = ''
  aiConversationHistory.value = []
  
  try {
    const idsParams = aiEntityIds.value.slice(0, 50).map((id: string) => `ids=${id}`).join('&')
    const url = `${config.public.apiBase}/grokathon/stream-expert-overview/?input_query=${encodeURIComponent('@chicago')}&${idsParams}`
    
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
      aiDisplayedResponse.value += chunk
    }
    
    aiConversationHistory.value = [
      { role: 'user', content: aiInitialQuestion },
      { role: 'assistant', content: aiDisplayedResponse.value }
    ]
    
    aiSummaryLoaded.value = true
  } catch (err) {
    console.error('Error streaming AI response:', err)
    aiDisplayedResponse.value = 'Failed to load AI analysis. Please try again.'
  } finally {
    aiLoadingResponse.value = false
    aiIsTyping.value = false
  }
}

// Select expert view in AI Summary
const selectAIExpertView = async (category: string) => {
  if (aiSelectedExpertView.value === category) {
    aiSelectedExpertView.value = null
    aiSummaryLoaded.value = false
    await streamAIResponse()
  } else {
    aiSelectedExpertView.value = category
    aiDisplayedResponse.value = ''
    aiIsTyping.value = true
    
    const selectedCategory = aiExpertCategories.value.find((c: AIExpertCategory) => c.name === category)
    if (selectedCategory && selectedCategory.ids.length > 0) {
      try {
        const idsParams = selectedCategory.ids.slice(0, 50).map((id: number) => `ids=${id}`).join('&')
        const url = `${config.public.apiBase}/grokathon/stream-expert-perspective/?input_query=${encodeURIComponent('@chicago')}&expert_category=${encodeURIComponent(category)}&${idsParams}`
        
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
          aiDisplayedResponse.value += chunk
        }
        
        aiConversationHistory.value = [
          { role: 'user', content: `What's the latest from ${category} on Chicago politics?` },
          { role: 'assistant', content: aiDisplayedResponse.value }
        ]
      } catch (err) {
        console.error('Error streaming expert perspective:', err)
        aiDisplayedResponse.value = `Failed to load ${category} perspective. Please try again.`
      } finally {
        aiIsTyping.value = false
      }
    }
  }
}

// Handle AI follow-up question
const handleAIFollowup = async () => {
  const question = aiFollowupInput.value.trim()
  if (!question || aiEntityIds.value.length === 0) return
  
  let idsToUse: (string | number)[] = []
  if (aiSelectedExpertView.value) {
    const selectedCategory = aiExpertCategories.value.find((c: AIExpertCategory) => c.name === aiSelectedExpertView.value)
    if (selectedCategory) {
      idsToUse = selectedCategory.ids
    }
  } else {
    idsToUse = aiEntityIds.value
  }
  
  if (idsToUse.length === 0) return
  
  aiDisplayedResponse.value += `<div class="followup-separator"></div><div class="followup-question">${question}</div><div class="followup-answer">`
  aiConversationHistory.value.push({ role: 'user', content: question })
  aiFollowupInput.value = ''
  aiIsTyping.value = true
  
  try {
    const response = await fetch(`${config.public.apiBase}/grokathon/stream-followup/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        followup_question: question,
        conversation_history: aiConversationHistory.value.slice(0, -1),
        input_query: '@chicago',
        ids: idsToUse.slice(0, 50),
        expert_category: aiSelectedExpertView.value || null
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
      aiDisplayedResponse.value += chunk
    }
    
    aiDisplayedResponse.value += '</div>'
    aiConversationHistory.value.push({ role: 'assistant', content: followupResponse })
  } catch (err) {
    console.error('Error sending AI follow-up:', err)
    aiDisplayedResponse.value += 'Failed to get response. Please try again.</div>'
    aiConversationHistory.value.pop()
  } finally {
    aiIsTyping.value = false
  }
}

// Toggle AI accordions
const toggleAIEntities = () => {
  aiEntitiesOpen.value = !aiEntitiesOpen.value
}

const toggleAISources = () => {
  aiSourcesOpen.value = !aiSourcesOpen.value
}

// Switch to AI Summary view
const switchToAISummary = async () => {
  activeView.value = 'ai-summary'
  
  if (!aiSummaryLoaded.value && aiEntityIds.value.length === 0) {
    await fetchAIChicagoExperts()
    if (aiEntityIds.value.length > 0) {
      await streamAIResponse()
    }
  }
}

// Auto-fetch posts when switching to conversation view
watch(activeView, (newView: 'overview' | 'conversation' | 'ai-summary') => {
  if (newView === 'conversation' && timelineTweets.value.length === 0) {
    fetchPosts()
  }
})

// =============================================================================
// HISTORICAL FOLLOWER DATA
// Run: curl "http://localhost:8000/api/grokathon/fetch-accounts/?ids=71360328,1577490840179691521,56864092,22939964,777071247398240257,16639612"
// =============================================================================
const followerHistory = {
  // Date: Jan 22, 2026
  '2026-01-22': {
    'Giannoulias': 36917,
    'Brandon4Chicago': 44537,
    'RepMikeQuigley': 48436,
    'susanamendoza10': 15995,
    'themariapappas': 413,
    'holbergj': 263,
  },
  // Add future snapshots here...
}

// =============================================================================
// CANDIDATE DATA (Updated: Jan 22, 2026)
// =============================================================================

// Alexi Giannoulias - Featured Candidate
const alexiData: Candidate = {
  id: 71360328,
  username: 'Giannoulias',
  displayName: 'Alexi Giannoulias',
  avatar: 'https://pbs.twimg.com/profile_images/1348661691626696705/NuEa_sf3_normal.jpg',
  followers: 36917,
  verified: true,
  bio: 'Proud dad & husband, ex-hooper and 38th Illinois Secretary of State.'
}

// Other Candidates
const otherCandidates: Candidate[] = [
  {
    id: 1577490840179691521,
    username: 'Brandon4Chicago',
    displayName: 'Brandon Johnson',
    avatar: 'https://pbs.twimg.com/profile_images/1884294863165825026/Q18yIddb_normal.jpg',
    followers: 44537,
    verified: false,
    bio: 'Husband, father, teacher, and the 57th Mayor of the City of Chicago. Political account. Follow @ChicagosMayor for government account.'
  },
  {
    id: 56864092,
    username: 'RepMikeQuigley',
    displayName: 'Mike Quigley',
    avatar: 'https://pbs.twimg.com/profile_images/1930280149758418945/flTVmLcq_normal.jpg',
    followers: 48436,
    verified: true,
    bio: "Representing Illinois' 5th District. House Appropriations & Intel member, amateur hockey player, proud Cubs fan. He/Him."
  },
  {
    id: 22939964,
    username: 'susanamendoza10',
    displayName: 'Susana A. Mendoza ☮️',
    avatar: 'https://pbs.twimg.com/profile_images/1104177259957633025/F0mzpCa7_normal.png',
    followers: 15995,
    verified: true,
    bio: 'Wife, mom, Illinois Comptroller, former Chicago City Clerk, Illinois State Representative, soccer fan, and big-time foodie. Retweet ≠ endorsement. 🎗️'
  },
  {
    id: 777071247398240257,
    username: 'themariapappas',
    displayName: 'Maria Pappas',
    avatar: 'https://pbs.twimg.com/profile_images/1947373023931084800/9lf0WCJv_normal.jpg',
    followers: 413,
    verified: false,
    bio: 'Maria Pappas is an American attorney and politician who has served as the Cook County Treasurer since 1998.'
  },
  {
    id: 16639612,
    username: 'holbergj',
    displayName: 'Joe Holberg',
    avatar: 'https://pbs.twimg.com/profile_images/891599101304819712/TnBJqoLt_normal.jpg',
    followers: 263,
    verified: false,
    bio: 'Democratic Candidate for Mayor of Chicago | Entrepreneur, Educator, Author'
  }
]

// Candidate Growth Data (last 7 months: Jul 2025 - Jan 2026)
interface CandidateGrowth {
  username: string
  name: string
  avatar: string
  change: number  // net follower change
  percent: number // percentage change
}

const candidateGrowthData: CandidateGrowth[] = [
  { 
    username: 'Giannoulias', 
    name: 'Alexi Giannoulias',
    avatar: 'https://pbs.twimg.com/profile_images/1348661691626696705/NuEa_sf3_normal.jpg',
    change: 1515,  // +111 +21 +53 +607 +525 +169 +29
    percent: 4.3 
  },
  { 
    username: 'RepMikeQuigley', 
    name: 'Mike Quigley',
    avatar: 'https://pbs.twimg.com/profile_images/1930280149758418945/flTVmLcq_normal.jpg',
    change: -160,  // +76 +89 +56 +34 +118 -678 +145
    percent: -0.3 
  },
  // Placeholder data for other candidates - will update when you provide
  { 
    username: 'Brandon4Chicago', 
    name: 'Brandon Johnson',
    avatar: 'https://pbs.twimg.com/profile_images/1884294863165825026/Q18yIddb_normal.jpg',
    change: 0,
    percent: 0 
  },
  { 
    username: 'susanamendoza10', 
    name: 'Susana A. Mendoza',
    avatar: 'https://pbs.twimg.com/profile_images/1104177259957633025/F0mzpCa7_normal.png',
    change: 0,
    percent: 0 
  },
  { 
    username: 'themariapappas', 
    name: 'Maria Pappas',
    avatar: 'https://pbs.twimg.com/profile_images/1947373023931084800/9lf0WCJv_normal.jpg',
    change: 0,
    percent: 0 
  },
  { 
    username: 'holbergj', 
    name: 'Joe Holberg',
    avatar: 'https://pbs.twimg.com/profile_images/891599101304819712/TnBJqoLt_normal.jpg',
    change: 0,
    percent: 0 
  },
]

// Sort by growth (highest first)
const candidateGrowthSorted = computed(() => {
  return [...candidateGrowthData].sort((a, b) => b.change - a.change)
})

// =============================================================================
// SHARE OF VOICE DATA (Dec 22, 2025 - Jan 22, 2026)
// =============================================================================
interface ShareOfVoice {
  username: string
  name: string
  avatar: string
  posts: number
}

const shareOfVoiceData: ShareOfVoice[] = [
  { 
    username: 'Giannoulias', 
    name: 'Alexi Giannoulias',
    avatar: 'https://pbs.twimg.com/profile_images/1348661691626696705/NuEa_sf3_normal.jpg',
    posts: 28000
  },
  { 
    username: 'Brandon4Chicago', 
    name: 'Brandon Johnson',
    avatar: 'https://pbs.twimg.com/profile_images/1884294863165825026/Q18yIddb_normal.jpg',
    posts: 76000
  },
  { 
    username: 'RepMikeQuigley', 
    name: 'Mike Quigley',
    avatar: 'https://pbs.twimg.com/profile_images/1930280149758418945/flTVmLcq_normal.jpg',
    posts: 7300
  },
  { 
    username: 'susanamendoza10', 
    name: 'Susana A. Mendoza',
    avatar: 'https://pbs.twimg.com/profile_images/1104177259957633025/F0mzpCa7_normal.png',
    posts: 729
  },
  { 
    username: 'themariapappas', 
    name: 'Maria Pappas',
    avatar: 'https://pbs.twimg.com/profile_images/1947373023931084800/9lf0WCJv_normal.jpg',
    posts: 94
  },
  { 
    username: 'holbergj', 
    name: 'Joe Holberg',
    avatar: 'https://pbs.twimg.com/profile_images/891599101304819712/TnBJqoLt_normal.jpg',
    posts: 33
  },
]

// Sort by posts (highest first)
const shareOfVoiceSorted = computed(() => {
  return [...shareOfVoiceData].sort((a, b) => b.posts - a.posts)
})

// Total posts for percentage calculation
const totalShareOfVoice = computed(() => {
  return shareOfVoiceData.reduce((sum, c) => sum + c.posts, 0)
})

// Max posts for bar width scaling
const maxShareOfVoice = computed(() => {
  return Math.max(...shareOfVoiceData.map((c: ShareOfVoice) => c.posts))
})

// Get voice bar width (scaled to max)
const getVoiceWidth = (posts: number): number => {
  if (maxShareOfVoice.value === 0) return 0
  return (posts / maxShareOfVoice.value) * 100
}

// Get voice percentage
const getVoicePercent = (posts: number): string => {
  if (totalShareOfVoice.value === 0) return '0'
  return ((posts / totalShareOfVoice.value) * 100).toFixed(1)
}

// All candidates for comparison
const allCandidatesSorted = computed(() => {
  return [alexiData, ...otherCandidates].sort((a, b) => b.followers - a.followers)
})

// Get max followers for bar scaling
const maxFollowers = computed(() => {
  return Math.max(...allCandidatesSorted.value.map((c: Candidate) => c.followers))
})

// Get growth bar width (scaled to max absolute change)
const maxAbsGrowth = computed(() => {
  return Math.max(...candidateGrowthData.map((c: CandidateGrowth) => Math.abs(c.change)))
})

const getGrowthWidth = (change: number): number => {
  if (maxAbsGrowth.value === 0) return 0
  return (Math.abs(change) / maxAbsGrowth.value) * 100
}

const formatNumber = (num: number): string => {
  if (num >= 1000) {
    return (num / 1000).toFixed(1).replace(/\.0$/, '') + 'K'
  }
  return num.toString()
}

const truncateBio = (bio: string, maxLength = 60): string => {
  if (bio.length <= maxLength) return bio
  return bio.substring(0, maxLength).trim() + '...'
}

const getBarWidth = (followers: number): number => {
  return (followers / maxFollowers.value) * 100
}
</script>

<style scoped>
.race-tracker-container {
  min-height: 100vh;
  background-color: #000;
  padding: 1.5rem 2rem;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* Back Navigation */
.back-nav {
  max-width: 100%;
  margin: 0 0 1.5rem;
}

.back-link {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  color: #71767b;
  text-decoration: none;
  font-size: 0.95rem;
  transition: color 0.2s ease;
}

.back-link:hover {
  color: #e7e9ea;
}

/* Page Header */
.page-header {
  text-align: center;
  margin: 0 auto 2rem;
}

.header-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: linear-gradient(135deg, #1d4ed8 0%, #3b82f6 100%);
  color: #fff;
  font-size: 0.8rem;
  font-weight: 600;
  padding: 0.5rem 1rem;
  border-radius: 50px;
  margin-bottom: 0.75rem;
}

.page-title {
  font-size: clamp(1.5rem, 3vw, 2rem);
  font-weight: 700;
  color: #fff;
  margin-bottom: 0.35rem;
  letter-spacing: -0.02em;
}

.page-subtitle {
  font-size: 0.95rem;
  color: #71767b;
}

/* View Toggle */
.view-toggle-container {
  display: flex;
  justify-content: center;
  margin-bottom: 2rem;
}

.view-toggle {
  display: inline-flex;
  background-color: #16181c;
  border-radius: 28px;
  padding: 6px;
  gap: 6px;
}

.toggle-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border: none;
  background: transparent;
  color: #71767b;
  font-size: 0.95rem;
  font-weight: 500;
  border-radius: 22px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-family: inherit;
}

.toggle-btn:hover {
  color: #e7e9ea;
}

.toggle-btn.active {
  background-color: #fff;
  color: #000;
}

.toggle-btn.active svg {
  color: #000;
}

/* View Content */
.view-content {
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

/* Candidates Section */
.candidates-section {
  margin-bottom: 2.5rem;
}

.candidates-row {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 1rem;
}

/* Candidate Card */
.candidate-card {
  background-color: #16181c;
  border: 1px solid #2f3336;
  border-radius: 16px;
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  transition: all 0.2s ease;
  position: relative;
}

.candidate-card:hover {
  border-color: #3f4347;
  background-color: #1d1f23;
}

.candidate-card.featured {
  border: 2px solid #1d9bf0;
  background: linear-gradient(135deg, #16181c 0%, #0c1929 100%);
}

.candidate-card.featured:hover {
  border-color: #1d9bf0;
  background: linear-gradient(135deg, #1d1f23 0%, #0f1f33 100%);
}

/* Tracking Badge */
.tracking-badge {
  position: absolute;
  top: -10px;
  left: 50%;
  transform: translateX(-50%);
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  background: linear-gradient(135deg, #1d9bf0 0%, #38bdf8 100%);
  color: #fff;
  font-size: 0.7rem;
  font-weight: 600;
  padding: 0.3rem 0.75rem;
  border-radius: 50px;
  white-space: nowrap;
}

/* Avatar */
.candidate-avatar {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  overflow: hidden;
  margin: 0 auto 0.75rem;
  background-color: #2f3336;
  flex-shrink: 0;
}

.candidate-card.featured .candidate-avatar {
  border: 3px solid #1d9bf0;
  width: 72px;
  height: 72px;
}

.candidate-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* Info */
.candidate-info {
  flex: 1;
  text-align: center;
  min-height: 100px;
}

.candidate-name-row {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.35rem;
  margin-bottom: 0.1rem;
}

.candidate-name {
  font-weight: 700;
  color: #e7e9ea;
  font-size: 0.9rem;
  line-height: 1.2;
}

.verified-badge {
  flex-shrink: 0;
}

.candidate-handle {
  color: #71767b;
  font-size: 0.8rem;
  margin-bottom: 0.5rem;
}

.candidate-bio {
  color: #8b8f94;
  font-size: 0.75rem;
  line-height: 1.4;
}

/* Footer */
.candidate-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 0.75rem;
  margin-top: auto;
  border-top: 1px solid #2f3336;
}

.candidate-followers {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  color: #71767b;
  font-size: 0.85rem;
  font-weight: 600;
}

.candidate-card.featured .candidate-followers {
  color: #1d9bf0;
}

.view-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.35rem 0.85rem;
  background-color: transparent;
  border: 1px solid #536471;
  border-radius: 50px;
  color: #e7e9ea;
  font-size: 0.75rem;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s ease;
}

.view-btn:hover {
  background-color: rgba(231, 233, 234, 0.1);
  border-color: #e7e9ea;
}

.candidate-card.featured .view-btn {
  background-color: #1d9bf0;
  border-color: #1d9bf0;
  color: #fff;
}

.candidate-card.featured .view-btn:hover {
  background-color: #1a8cd8;
}

/* Section Headers */
.section-header {
  text-align: center;
  margin-bottom: 1.25rem;
}

.section-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: #e7e9ea;
  margin-bottom: 0.2rem;
}

.section-subtitle {
  font-size: 0.85rem;
  color: #71767b;
}


/* Stats Row */
.stats-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-bottom: 2rem;
}

.stat-card {
  background-color: #16181c;
  border: 1px solid #2f3336;
  border-radius: 16px;
  padding: 1.5rem;
}

.comparison-bars {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.comparison-row {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.comparison-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  width: 140px;
  flex-shrink: 0;
}

.comparison-avatar {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  object-fit: cover;
}

.comparison-name {
  color: #e7e9ea;
  font-size: 0.85rem;
  font-weight: 500;
}

.comparison-bar-container {
  flex: 1;
  height: 28px;
  background-color: #2f3336;
  border-radius: 6px;
  overflow: hidden;
}

.comparison-bar {
  height: 100%;
  background: linear-gradient(90deg, #536471 0%, #71767b 100%);
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding-right: 0.75rem;
  transition: width 0.5s ease;
  min-width: 50px;
}

.comparison-bar.is-alexi {
  background: linear-gradient(90deg, #1d9bf0 0%, #38bdf8 100%);
}

.comparison-value {
  color: #fff;
  font-size: 0.75rem;
  font-weight: 700;
}

/* Growth Comparison */
.growth-comparison {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.growth-row {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.growth-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  width: 100px;
  flex-shrink: 0;
}

.growth-avatar {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  object-fit: cover;
}

.growth-name {
  color: #e7e9ea;
  font-size: 0.85rem;
  font-weight: 500;
}

.growth-bar-track {
  flex: 1;
  height: 28px;
  background-color: #2f3336;
  border-radius: 6px;
  overflow: hidden;
}

.growth-bar-fill {
  height: 100%;
  border-radius: 6px;
  transition: width 0.5s ease;
  min-width: 4px;
}

.growth-bar-fill.is-positive {
  background: linear-gradient(90deg, #14532d 0%, #22c55e 100%);
}

.growth-bar-fill.is-negative {
  background: linear-gradient(90deg, #7f1d1d 0%, #ef4444 100%);
}

.growth-bar-fill.is-alexi.is-positive {
  background: linear-gradient(90deg, #1d9bf0 0%, #38bdf8 100%);
}

.growth-stats {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  min-width: 70px;
}

.growth-change-value {
  font-size: 0.9rem;
  font-weight: 700;
  color: #71767b;
}

.growth-change-value.positive {
  color: #22c55e;
}

.growth-change-value.negative {
  color: #ef4444;
}

.growth-percent-value {
  font-size: 0.7rem;
  font-weight: 600;
  color: #71767b;
}

.growth-percent-value.positive {
  color: #22c55e;
}

.growth-percent-value.negative {
  color: #ef4444;
}

/* Share of Voice */
.voice-comparison {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.voice-row {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.voice-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  width: 100px;
  flex-shrink: 0;
}

.voice-avatar {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  object-fit: cover;
}

.voice-name {
  color: #e7e9ea;
  font-size: 0.85rem;
  font-weight: 500;
}

.voice-bar-container {
  flex: 1;
  height: 28px;
  background-color: #2f3336;
  border-radius: 6px;
  overflow: hidden;
}

.voice-bar {
  height: 100%;
  border-radius: 6px;
  transition: width 0.5s ease;
  min-width: 4px;
  background: linear-gradient(90deg, #6b7280 0%, #9ca3af 100%);
}

.voice-bar.is-alexi {
  background: linear-gradient(90deg, #1d9bf0 0%, #38bdf8 100%);
}

.voice-stats {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  min-width: 70px;
}

.voice-count {
  font-size: 0.9rem;
  font-weight: 700;
  color: #e7e9ea;
}

.voice-percent {
  font-size: 0.7rem;
  font-weight: 600;
  color: #71767b;
}

/* Mentions Chart */
.mentions-chart {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.chart-stats {
  display: flex;
  gap: 2rem;
}

.chart-total,
.chart-authors {
  display: flex;
  flex-direction: column;
}

.chart-total-value,
.chart-authors-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: #e7e9ea;
}

.chart-total-label,
.chart-authors-label {
  font-size: 0.75rem;
  color: #71767b;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.chart-container {
  position: relative;
}

.mentions-svg {
  width: 100%;
  height: 150px;
}

.chart-x-axis {
  display: flex;
  justify-content: space-between;
  padding-top: 0.5rem;
  font-size: 0.7rem;
  color: #71767b;
}

.chart-peak {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding-top: 0.5rem;
  font-size: 0.8rem;
}

.peak-label {
  color: #71767b;
}

.peak-value {
  color: #1d9bf0;
  font-weight: 600;
}

/* Coming Soon Section */
.coming-soon-section {
  margin: 0;
}

.coming-soon-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

.coming-soon-card {
  background-color: #16181c;
  border: 1px dashed #2f3336;
  border-radius: 16px;
  padding: 1.25rem;
  text-align: center;
  opacity: 0.7;
}

.coming-soon-icon {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #2f3336;
  border-radius: 10px;
  margin: 0 auto 0.75rem;
  color: #71767b;
}

.coming-soon-title {
  font-size: 0.9rem;
  font-weight: 700;
  color: #71767b;
  margin-bottom: 0.25rem;
}

.coming-soon-desc {
  font-size: 0.8rem;
  color: #536471;
}

/* Timeline Container */
.timeline-container {
  width: 100%;
}

.timeline-layout {
  display: grid;
  grid-template-columns: 1fr 350px;
  gap: 1.5rem;
  max-width: 1000px;
  margin: 0 auto;
}

/* Timeline Feed */
.timeline-feed {
  background-color: #16181c;
  border: 1px solid #2f3336;
  border-radius: 16px;
  overflow: hidden;
  min-height: 400px;
}

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
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.posts-loading-text {
  margin-top: 1rem;
  color: #71767b;
  font-size: 0.95rem;
}

.posts-empty {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  color: #71767b;
  text-align: center;
}

/* Tweet Styles */
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

.tweet-date a {
  color: #71767b;
  text-decoration: none;
}

.tweet-date a:hover {
  text-decoration: underline;
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
  max-height: 400px;
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

/* Candidates Sidebar */
.candidates-sidebar {
  background-color: #16181c;
  border-radius: 16px;
  padding: 1rem;
  height: fit-content;
  position: sticky;
  top: 1rem;
}

.sidebar-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #e7e9ea;
  margin-bottom: 1rem;
}

.sidebar-toggle {
  display: flex;
  background: #16181c;
  border-radius: 9999px;
  padding: 4px;
  margin-bottom: 1rem;
}

.sidebar-toggle-btn {
  flex: 1;
  padding: 0.5rem 1rem;
  border: none;
  background: transparent;
  color: #71767b;
  font-size: 0.85rem;
  font-weight: 600;
  border-radius: 9999px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.sidebar-toggle-btn:hover {
  color: #e7e9ea;
}

.sidebar-toggle-btn.active {
  background: #1d9bf0;
  color: #fff;
}

.sidebar-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem 1rem;
  color: #71767b;
  font-size: 0.9rem;
}

.sidebar-spinner {
  width: 24px;
  height: 24px;
  border: 2px solid #2f3336;
  border-top-color: #1d9bf0;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 0.75rem;
}

.sidebar-empty {
  text-align: center;
  padding: 2rem 1rem;
  color: #71767b;
  font-size: 0.9rem;
}

.sidebar-list {
  display: flex;
  flex-direction: column;
}

.sidebar-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 0;
  border-bottom: 1px solid #2f3336;
}

.sidebar-item:last-child {
  border-bottom: none;
}

.sidebar-item.featured {
  background-color: rgba(29, 155, 240, 0.1);
  margin: -0.5rem -0.5rem 0;
  padding: 0.75rem 0.5rem;
  border-radius: 8px;
  border-bottom: none;
  margin-bottom: 0.5rem;
}

.sidebar-avatar {
  flex-shrink: 0;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  overflow: hidden;
}

.sidebar-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.sidebar-info {
  flex: 1;
  min-width: 0;
}

.sidebar-name {
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

.sidebar-verified {
  flex-shrink: 0;
}

.sidebar-handle {
  color: #71767b;
  font-size: 0.8rem;
}

.sidebar-followers {
  font-size: 0.85rem;
  font-weight: 600;
  color: #71767b;
}

/* Load Posts Button */
.load-posts-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  width: 100%;
  padding: 0.75rem 1rem;
  margin-top: 1rem;
  background-color: #1d9bf0;
  border: none;
  border-radius: 50px;
  color: #fff;
  font-size: 0.9rem;
  font-weight: 600;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.2s ease;
}

.load-posts-btn:hover:not(:disabled) {
  background-color: #1a8cd8;
}

.load-posts-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.btn-spinner {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

/* Conversation Placeholder */
.conversation-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 4rem 2rem;
  background-color: #16181c;
  border: 1px dashed #2f3336;
  border-radius: 20px;
  min-height: 400px;
}

.placeholder-icon {
  width: 80px;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #2f3336;
  border-radius: 20px;
  color: #71767b;
  margin-bottom: 1.5rem;
}

.placeholder-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #e7e9ea;
  margin-bottom: 0.5rem;
}

.placeholder-subtitle {
  font-size: 1rem;
  color: #71767b;
  max-width: 400px;
  margin-bottom: 2rem;
}

.placeholder-features {
  display: flex;
  gap: 2rem;
  margin-bottom: 2rem;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #71767b;
  font-size: 0.9rem;
}

.feature-item svg {
  color: #1d9bf0;
}

.placeholder-note {
  font-size: 0.85rem;
  color: #536471;
  font-style: italic;
}

/* Responsive */
@media (max-width: 1400px) {
  .candidates-row {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 1100px) {
  .stats-row {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 900px) {
  .candidates-row {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .timeline-layout {
    grid-template-columns: 1fr;
  }
  
  .candidates-sidebar {
    position: static;
    order: -1;
  }
}

@media (max-width: 600px) {
  .race-tracker-container {
    padding: 1rem;
  }
  
  .candidates-row {
    grid-template-columns: 1fr;
  }
  
  .coming-soon-grid {
    grid-template-columns: 1fr;
  }
  
  .comparison-label {
    width: 100px;
  }
  
  .comparison-name {
    font-size: 0.75rem;
  }
  
  .growth-label {
    width: 80px;
  }
  
  .growth-name {
    font-size: 0.75rem;
  }
  
  .growth-stats {
    min-width: 60px;
  }
  
  .growth-change-value {
    font-size: 0.8rem;
  }
  
  .toggle-btn {
    padding: 0.6rem 1rem;
    font-size: 0.85rem;
  }
  
  .placeholder-features {
    flex-direction: column;
    gap: 1rem;
  }
  
  .conversation-placeholder {
    padding: 2rem 1rem;
    min-height: 300px;
  }
}

/* =============================================================================
   AI SUMMARY STYLES
   ============================================================================= */
.ai-summary-container {
  width: 100%;
}

.ai-summary-layout {
  display: grid;
  grid-template-columns: 1fr 300px;
  gap: 1.5rem;
  max-width: 1000px;
  margin: 0 auto;
}

.ai-chat {
  min-width: 0;
}

.ai-query {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 1.5rem;
}

.ai-query-text {
  background-color: #16181c;
  border: 1px solid #2f3336;
  border-radius: 20px;
  padding: 0.85rem 1.25rem;
  color: #e7e9ea;
  font-size: 0.95rem;
  max-width: 80%;
  text-align: right;
}

.ai-accordion {
  margin-bottom: 0.75rem;
}

.ai-accordion-header {
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

.ai-accordion-header:hover {
  background-color: #1d1f23;
}

.ai-entity-avatars {
  display: flex;
  margin-left: auto;
  margin-right: 0.5rem;
}

.ai-entity-avatar {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  border: 2px solid #16181c;
  margin-left: -8px;
  object-fit: cover;
}

.ai-entity-avatar:first-child {
  margin-left: 0;
}

.ai-accordion-arrow {
  flex-shrink: 0;
  transition: transform 0.2s ease;
}

.ai-accordion-arrow.open {
  transform: rotate(180deg);
}

.ai-accordion-content {
  background-color: #16181c;
  border: 1px solid #2f3336;
  border-top: none;
  border-radius: 0 0 12px 12px;
  padding: 1rem;
  margin-top: -0.5rem;
}

.ai-entity-loading {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #71767b;
  font-size: 0.85rem;
}

.ai-spinner-small {
  width: 16px;
  height: 16px;
  border: 2px solid #2f3336;
  border-top-color: #1d9bf0;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.ai-entity-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}

.ai-entity-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background-color: #202020;
  border-radius: 50px;
  padding: 0.35rem 0.75rem 0.35rem 0.35rem;
  font-size: 0.85rem;
  color: #e7e9ea;
}

.ai-entity-item img {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  object-fit: cover;
}

.ai-content-posts-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  max-height: 400px;
  overflow-y: auto;
  padding-right: 0.5rem;
}

.ai-content-posts-list::-webkit-scrollbar {
  width: 6px;
}

.ai-content-posts-list::-webkit-scrollbar-track {
  background: #16181c;
  border-radius: 3px;
}

.ai-content-posts-list::-webkit-scrollbar-thumb {
  background: #3a3f47;
  border-radius: 3px;
}

.ai-content-post-item {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  padding: 0.5rem;
  border-radius: 8px;
  transition: background-color 0.2s ease;
}

.ai-content-post-item:hover {
  background-color: rgba(255, 255, 255, 0.03);
}

.ai-content-post-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  flex-shrink: 0;
}

.ai-content-post-body {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.ai-content-post-link {
  color: #e7e9ea;
  text-decoration: none;
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
}

.ai-content-post-link:hover {
  color: #1d9bf0;
}

.ai-content-post-username {
  color: #1d9bf0;
  font-size: 0.8rem;
  font-weight: 500;
}

.ai-content-post-text {
  font-size: 0.85rem;
  color: #71767b;
  line-height: 1.4;
}

.ai-content-post-likes {
  font-size: 0.75rem;
  color: #71767b;
}

.ai-no-posts {
  color: #71767b;
  font-size: 0.85rem;
  text-align: center;
  padding: 0.75rem;
}

.ai-response {
  margin-top: 1.5rem;
  color: #e7e9ea;
  font-size: 0.95rem;
  line-height: 1.6;
}

.ai-response :deep(h4) {
  font-size: 1.05rem;
  font-weight: 600;
  margin: 1.5rem 0 0.75rem;
  color: #fff;
}

.ai-response :deep(ul) {
  margin: 0.75rem 0;
  padding-left: 1.25rem;
}

.ai-response :deep(li) {
  margin-bottom: 0.5rem;
}

.ai-response :deep(strong) {
  color: #fff;
  font-weight: 600;
}

.ai-response-loading {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: #71767b;
  font-size: 0.95rem;
  padding: 1rem 0;
}

.ai-typing-cursor {
  display: inline-block;
  color: #fff;
  animation: blink 0.8s infinite;
}

.ai-followup {
  display: flex;
  align-items: center;
  background-color: #16181c;
  border-radius: 50px;
  border: 1px solid #2f3336;
  margin-top: 2rem;
  transition: border-color 0.2s ease;
}

.ai-followup:focus-within {
  border-color: #fff;
}

.ai-followup-input {
  flex: 1;
  background: transparent;
  border: none;
  outline: none;
  padding: 0.85rem 1.25rem;
  font-size: 0.95rem;
  color: #e7e9ea;
  font-family: inherit;
}

.ai-followup-input::placeholder {
  color: #71767b;
}

.ai-followup-submit {
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

.ai-followup-submit:hover:not(:disabled) {
  opacity: 0.7;
}

.ai-followup-submit:disabled {
  color: #38444d;
  cursor: not-allowed;
}

/* Expert Views Sidebar */
.ai-expert-views {
  background-color: #16181c;
  border-radius: 16px;
  padding: 1rem;
  height: fit-content;
  position: sticky;
  top: 1rem;
}

.ai-expert-title {
  font-size: 1.15rem;
  font-weight: 700;
  color: #e7e9ea;
  margin-bottom: 0.25rem;
}

.ai-expert-subtitle {
  font-size: 0.85rem;
  color: #71767b;
  margin-bottom: 1rem;
}

.ai-expert-categories {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.ai-categories-loading {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #71767b;
  font-size: 0.85rem;
  padding: 0.75rem;
}

.ai-no-categories {
  color: #71767b;
  font-size: 0.85rem;
  text-align: center;
  padding: 0.75rem;
}

.ai-expert-category {
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

.ai-expert-category:hover {
  background-color: #1d1f23;
  border-color: #3f4347;
}

.ai-expert-category.active {
  background-color: #1d1f23;
  border-color: #fff;
}

.ai-category-name {
  flex: 1;
  font-weight: 500;
}

.ai-category-count {
  font-size: 0.8rem;
  color: #71767b;
}

/* Follow-up styling for AI */
.ai-response :deep(.followup-separator) {
  height: 1px;
  background-color: #2f3336;
  margin: 2rem 0;
}

.ai-response :deep(.followup-question) {
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

.ai-response :deep(.followup-answer) {
  clear: both;
}

@media (max-width: 900px) {
  .ai-summary-layout {
    grid-template-columns: 1fr;
  }
  
  .ai-expert-views {
    position: static;
  }
}
</style>
