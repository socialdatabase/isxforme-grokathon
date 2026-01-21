<template>
  <div class="audience-page-container">
    <!-- Back Navigation -->
    <nav class="back-nav">
      <NuxtLink to="/AudienceInsights" class="back-link">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
          <path d="M19 12H5M5 12L12 19M5 12L12 5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <span>Audience Insights</span>
      </NuxtLink>
    </nav>

    <!-- Audience Header -->
    <header class="audience-header">
      <div class="audience-icon">
        <img src="https://pbs.twimg.com/profile_images/1687033172905644032/ZjFPPLUM_normal.jpg" alt="Rust Engineers" class="audience-logo" />
      </div>
      <h1 class="audience-title">Rust Engineers</h1>
      <p class="audience-description">
        Rust Engineers active on X. 
        <span class="highlight-cta">Request a Custom Audience from Socialdatabase</span> 
        to reach these specific users effectively on X Ads.
      </p>
      <div class="audience-stats">
        <span class="stat-badge">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
            <path d="M17 21V19C17 17.9391 16.5786 16.9217 15.8284 16.1716C15.0783 15.4214 14.0609 15 13 15H5C3.93913 15 2.92172 15.4214 2.17157 16.1716C1.42143 16.9217 1 17.9391 1 19V21" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M9 11C11.2091 11 13 9.20914 13 7C13 4.79086 11.2091 3 9 3C6.79086 3 5 4.79086 5 7C5 9.20914 6.79086 11 9 11Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M23 21V19C22.9993 18.1137 22.7044 17.2528 22.1614 16.5523C21.6184 15.8519 20.8581 15.3516 20 15.13" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M16 3.13C16.8604 3.35031 17.623 3.85071 18.1676 4.55232C18.7122 5.25392 19.0078 6.11683 19.0078 7.005C19.0078 7.89318 18.7122 8.75608 18.1676 9.45769C17.623 10.1593 16.8604 10.6597 16 10.88" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          241,000 global users
        </span>
        <span class="stat-badge">
          🇬🇧 7,900 UK users
        </span>
      </div>
    </header>

    <!-- View Toggle -->
    <div class="view-toggle-container">
      <div class="view-toggle">
        <button 
          class="toggle-btn" 
          :class="{ active: viewMode === 'influencers' }"
          @click="viewMode = 'influencers'"
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
            <path d="M12 2L15.09 8.26L22 9.27L17 14.14L18.18 21.02L12 17.77L5.82 21.02L7 14.14L2 9.27L8.91 8.26L12 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          Audience Influencers
        </button>
        <button 
          class="toggle-btn" 
          :class="{ active: viewMode === 'users' }"
          @click="viewMode = 'users'"
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
            <path d="M17 21V19C17 17.9391 16.5786 16.9217 15.8284 16.1716C15.0783 15.4214 14.0609 15 13 15H5C3.93913 15 2.92172 15.4214 2.17157 16.1716C1.42143 16.9217 1 17.9391 1 19V21" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M9 11C11.2091 11 13 9.20914 13 7C13 4.79086 11.2091 3 9 3C6.79086 3 5 4.79086 5 7C5 9.20914 6.79086 11 9 11Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          Audience Users
          <span class="count-badge">241,000</span>
        </button>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-container">
      <div class="spinner"></div>
      <p class="loading-message">Loading {{ viewMode === 'influencers' ? 'influencers' : 'users' }}...</p>
    </div>

    <!-- Influencers View -->
    <template v-else-if="viewMode === 'influencers'">
      <div class="list-header">
        <h2 class="list-title">Top 100 Influencers</h2>
        <p class="list-subtitle">Key voices shaping the Rust community on X</p>
      </div>
      <div class="accounts-grid">
        <div 
          v-for="(account, index) in influencerAccounts" 
          :key="account.username" 
          class="account-card"
        >
          <div class="account-rank" :class="getRankClass(Number(index))">
            {{ Number(index) + 1 }}
          </div>
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
          <a 
            :href="`https://x.com/${account.username}`" 
            target="_blank" 
            rel="noopener noreferrer"
            class="follow-btn"
            @click.stop
          >
            View
          </a>
        </div>
      </div>
    </template>

    <!-- Users View -->
    <template v-else-if="viewMode === 'users'">
      <div class="list-header">
        <h2 class="list-title">Audience Sample</h2>
        <p class="list-subtitle">100 members of the Rust Engineers audience</p>
      </div>
      <div class="accounts-grid">
        <div 
          v-for="(account, index) in userAccounts" 
          :key="account.username" 
          class="account-card"
        >
          <div class="account-rank user-rank">
            {{ Number(index) + 1 }}
          </div>
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
          <a 
            :href="`https://x.com/${account.username}`" 
            target="_blank" 
            rel="noopener noreferrer"
            class="follow-btn"
            @click.stop
          >
            View
          </a>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
interface Account {
  id: string
  displayName: string
  username: string
  avatar: string
  followers: string
  verified: boolean
}

definePageMeta({
  layout: false
})

const viewMode = ref<'influencers' | 'users'>('influencers')
const loading = ref(true)

// Hardcoded Rust influencer accounts in specified order (real data from X API)
const RUST_INFLUENCERS: Account[] = [
  { id: '1', displayName: 'Rust Language', username: 'rustlang', avatar: 'https://pbs.twimg.com/profile_images/1687033172905644032/ZjFPPLUM_normal.jpg', followers: '153K', verified: true },
  { id: '2', displayName: 'Rust Foundation', username: 'rust_foundation', avatar: 'https://pbs.twimg.com/profile_images/1748119952698335232/FOpk5qMo_normal.png', followers: '40.4K', verified: false },
  { id: '3', displayName: 'This Week in Rust', username: 'ThisWeekInRust', avatar: 'https://pbs.twimg.com/profile_images/633365450760458240/SpZ17g_B_normal.png', followers: '33K', verified: false },
  { id: '4', displayName: 'Jon Gjengset', username: 'jonhoo', avatar: 'https://pbs.twimg.com/profile_images/1775850273795174400/qYKZscFO_normal.jpg', followers: '35.5K', verified: false },
  { id: '5', displayName: 'Rust Trending', username: 'RustTrending', avatar: 'https://pbs.twimg.com/profile_images/1050614142199975936/wREBJN0V_normal.jpg', followers: '35.3K', verified: false },
  { id: '6', displayName: 'Mara', username: 'm_ou_se', avatar: 'https://pbs.twimg.com/profile_images/1378283500349054976/ikBbFGV1_normal.jpg', followers: '44.4K', verified: false },
  { id: '7', displayName: 'RustConf', username: 'rustconf', avatar: 'https://pbs.twimg.com/profile_images/1880320657986342912/87DVj2D9_normal.png', followers: '18.7K', verified: true },
  { id: '8', displayName: 'Luca Palmieri', username: 'algo_luca', avatar: 'https://pbs.twimg.com/profile_images/1145238381955309570/PzfBkBEz_normal.png', followers: '15.9K', verified: false },
  { id: '9', displayName: 'Tim McNamara', username: 'timClicks', avatar: 'https://pbs.twimg.com/profile_images/1666154869059911681/2UMbAEai_normal.jpg', followers: '24.6K', verified: true },
  { id: '10', displayName: 'rust-analyzer', username: 'rust_analyzer', avatar: 'https://pbs.twimg.com/profile_images/1217461647377420289/HXHa6hZU_normal.jpg', followers: '12.6K', verified: false },
  { id: '11', displayName: 'Tokio', username: 'tokio_rs', avatar: 'https://pbs.twimg.com/profile_images/1039634366207414272/bC40df3r_normal.jpg', followers: '11.3K', verified: false },
  { id: '12', displayName: 'Rust Jobs 🦀', username: 'rustjobs_dev', avatar: 'https://pbs.twimg.com/profile_images/2013609385604284416/mqDoKyQL_normal.jpg', followers: '7.2K', verified: false },
  { id: '13', displayName: 'Read Rust', username: 'read_rust', avatar: 'https://pbs.twimg.com/profile_images/959596847596584961/JnHCZrFx_normal.jpg', followers: '12.7K', verified: false },
  { id: '14', displayName: 'David Tolnay', username: 'davidtolnay', avatar: 'https://pbs.twimg.com/profile_images/1401241943951118336/Ll6KqbJf_normal.png', followers: '9.3K', verified: true },
  { id: '15', displayName: 'Rust Embedded Working Group', username: 'rustembedded', avatar: 'https://pbs.twimg.com/profile_images/1019576096289951744/Oa8igvj-_normal.jpg', followers: '11.9K', verified: false },
  { id: '16', displayName: 'RustFest', username: 'RustFest', avatar: 'https://pbs.twimg.com/profile_images/1580490987905994752/wY5xeNM5_normal.jpg', followers: '7.2K', verified: false },
  { id: '17', displayName: 'Patrick Walton', username: 'pcwalton', avatar: 'https://pbs.twimg.com/profile_images/619088718/twitter-icon_normal.jpeg', followers: '18K', verified: false },
  { id: '18', displayName: 'Andrew Gallant', username: 'burntsushi5', avatar: 'https://pbs.twimg.com/profile_images/1720119828097249280/fJpZiVFw_normal.jpg', followers: '9.9K', verified: false },
  { id: '19', displayName: 'FerrousSystems', username: 'FerrousSystems', avatar: 'https://pbs.twimg.com/profile_images/1121784110173659136/1PAf0_9F_normal.png', followers: '7.6K', verified: false },
  { id: '20', displayName: 'Sean McArthur', username: 'seanmonstar', avatar: 'https://pbs.twimg.com/profile_images/378800000830458563/98d7e0d9e09efa4ad0e95123e9ae4708_normal.jpeg', followers: '5K', verified: false },
  { id: '21', displayName: 'Ryan Levick', username: 'ryan_levick', avatar: 'https://pbs.twimg.com/profile_images/1085529188285796352/LTnlDlKc_normal.jpg', followers: '7.9K', verified: false },
  { id: '22', displayName: 'RustRover, a JetBrains IDE', username: 'rustrover', avatar: 'https://pbs.twimg.com/profile_images/1797579736006164480/ti2cZNQM_normal.png', followers: '7.5K', verified: false },
  { id: '23', displayName: 'Rust GameDev WG 🦀🎮', username: 'rust_gamedev', avatar: 'https://pbs.twimg.com/profile_images/1172438339829428225/Y1gYG9UH_normal.jpg', followers: '8.9K', verified: false },
  { id: '24', displayName: 'Servo', username: 'ServoDev', avatar: 'https://pbs.twimg.com/profile_images/1328560578776997888/cFUrstSq_normal.jpg', followers: '8.7K', verified: false },
  { id: '25', displayName: 'Rust and WebAssembly', username: 'rustwasm', avatar: 'https://pbs.twimg.com/profile_images/990866034671398912/2kHcNXqA_normal.jpg', followers: '7.3K', verified: false },
  { id: '26', displayName: 'Golang News & Libs & Jobs', username: 'golangch', avatar: 'https://pbs.twimg.com/profile_images/1559145356851646465/wj9eRXIQ_normal.jpg', followers: '35.8K', verified: true },
  { id: '27', displayName: 'neural oscillator of uncertain significance', username: 'mycoliza', avatar: 'https://pbs.twimg.com/profile_images/1491815309346414595/PyQdNSS0_normal.jpg', followers: '21.6K', verified: false },
  { id: '28', displayName: 'Charlie Marsh', username: 'charliermarsh', avatar: 'https://pbs.twimg.com/profile_images/1490182599981125634/ex0Jezvf_normal.jpg', followers: '33.4K', verified: true },
  { id: '29', displayName: 'crates.io status', username: 'cratesiostatus', avatar: 'https://pbs.twimg.com/profile_images/738068999859212288/ZdqKi8y9_normal.jpg', followers: '5.9K', verified: false },
  { id: '30', displayName: 'Tauri', username: 'TauriApps', avatar: 'https://pbs.twimg.com/profile_images/1427375984475578389/jWzgho1b_normal.png', followers: '18.5K', verified: false },
  { id: '31', displayName: 'William Rudenmalm🇪🇺', username: 'w_hgm', avatar: 'https://pbs.twimg.com/profile_images/1275456218203471872/F85H6nhG_normal.jpg', followers: '9.2K', verified: false },
  { id: '32', displayName: 'Manish', username: 'ManishEarth', avatar: 'https://pbs.twimg.com/profile_images/2902505817/5ff15a47a60ae0b71fcf1529e9e676f8_normal.png', followers: '14.5K', verified: false },
  { id: '33', displayName: '@yaah@hachyderm.io', username: 'yaahc_', avatar: 'https://pbs.twimg.com/profile_images/1260746238527324162/oMJHrHFC_normal.jpg', followers: '6.1K', verified: false },
  { id: '34', displayName: 'Bevy Engine', username: 'BevyEngine', avatar: 'https://pbs.twimg.com/profile_images/1769863296243642369/QlAeZfmQ_normal.png', followers: '10.2K', verified: false },
  { id: '35', displayName: 'Shuttle', username: 'shuttle_dev', avatar: 'https://pbs.twimg.com/profile_images/1598349525147680770/ZQkR1shE_normal.png', followers: '5.7K', verified: true },
  { id: '36', displayName: 'ashley williams', username: 'ag_dubs', avatar: 'https://pbs.twimg.com/profile_images/1916473723986550785/weBtJRIQ_normal.jpg', followers: '19.3K', verified: false },
  { id: '37', displayName: 'Rust Security 🦀 🏴‍☠️', username: 'RustSecurity', avatar: 'https://pbs.twimg.com/profile_images/1208154331683459073/A8AMfRzT_normal.jpg', followers: '3.7K', verified: false },
  { id: '38', displayName: '🦀 RustLab', username: 'rustlab_conf', avatar: 'https://pbs.twimg.com/profile_images/1922650744542343168/sxQ_PKG-_normal.jpg', followers: '5.1K', verified: false },
  { id: '39', displayName: 'Daily Rust', username: 'rustoftheday', avatar: 'https://pbs.twimg.com/profile_images/1721626001174908928/qli1L9iB_normal.jpg', followers: '3.4K', verified: false },
  { id: '40', displayName: 'Sophia J. Turner 🏳️‍⚧️', username: 'sophiajturner', avatar: 'https://pbs.twimg.com/profile_images/1965920040257204225/FJxmMjj5_normal.jpg', followers: '10.3K', verified: false },
  { id: '41', displayName: 'Rust LibHunt', username: 'RustLibHunt', avatar: 'https://pbs.twimg.com/profile_images/776346813012074496/S7kCezGv_normal.jpg', followers: '4.7K', verified: false },
  { id: '42', displayName: 'Orhun Parmaksız 👾', username: 'orhundev', avatar: 'https://pbs.twimg.com/profile_images/1887898013336543232/MnPXlrU7_normal.jpg', followers: '6.7K', verified: true },
  { id: '43', displayName: 'nrc', username: 'nick_r_cameron', avatar: 'https://pbs.twimg.com/profile_images/344513261579814111/7a2e364ff2b85cbec4ff7196ce7260d1_normal.png', followers: '6.3K', verified: false },
  { id: '44', displayName: 'Zig', username: 'ziglang', avatar: 'https://pbs.twimg.com/profile_images/1256729385824129024/c6HblNfV_normal.png', followers: '16.9K', verified: false },
  { id: '45', displayName: 'AstraKernel 💫', username: 'AstraKernel', avatar: 'https://pbs.twimg.com/profile_images/1907215140463992832/B3WpuxjW_normal.jpg', followers: '6.3K', verified: false },
  { id: '46', displayName: 'Rust Weekly 🦀', username: 'RustDiscussions', avatar: 'https://pbs.twimg.com/profile_images/1468518313990967301/fbmGbRbQ_normal.jpg', followers: '4.1K', verified: false },
  { id: '47', displayName: "Let's Get Rusty 🦀", username: 'letsgetrusty', avatar: 'https://pbs.twimg.com/profile_images/1373674788665716736/5A2tJ0My_normal.jpg', followers: '3.9K', verified: true },
  { id: '48', displayName: 'Dioxus 🧬', username: 'dioxuslabs', avatar: 'https://pbs.twimg.com/profile_images/1610370276289646592/r2Vb3yZj_normal.jpg', followers: '5.9K', verified: true },
  { id: '49', displayName: 'Guillaume Gomez', username: 'imperioworld_', avatar: 'https://pbs.twimg.com/profile_images/1107392834787778560/bI1QfTYh_normal.png', followers: '2.8K', verified: false },
  { id: '50', displayName: 'Redox OS', username: 'redox_os', avatar: 'https://pbs.twimg.com/profile_images/1053333895653933057/s1vLQdak_normal.jpg', followers: '6.7K', verified: false },
  { id: '51', displayName: 'llogiq', username: 'llogiq', avatar: 'https://pbs.twimg.com/profile_images/1863606399697027072/FA0QN6WD_normal.jpg', followers: '2.6K', verified: false },
  { id: '52', displayName: 'Augmented Coding Weekly', username: 'AugmentCoding', avatar: 'https://pbs.twimg.com/profile_images/1975800516664836096/1CEeS2fi_normal.jpg', followers: '12.7K', verified: false },
  { id: '53', displayName: 'Turso', username: 'tursodatabase', avatar: 'https://pbs.twimg.com/profile_images/1969028622536097793/aAUcXoF6_normal.jpg', followers: '15K', verified: true },
  { id: '54', displayName: 'Aria Desires', username: 'Gankra_', avatar: 'https://pbs.twimg.com/profile_images/1237155522614366208/lhhkUAX9_normal.jpg', followers: '7.7K', verified: false },
  { id: '55', displayName: 'Rustacean Station', username: 'rustaceanfm', avatar: 'https://pbs.twimg.com/profile_images/1149191647307149313/D05vQUe0_normal.png', followers: '2.4K', verified: false },
  { id: '56', displayName: 'nushell', username: 'nu_shell', avatar: 'https://pbs.twimg.com/profile_images/1165012513903108096/0JtpgAk3_normal.png', followers: '5K', verified: false },
  { id: '57', displayName: 'Zero To Production In Rust', username: 'zero2prod', avatar: 'https://pbs.twimg.com/profile_images/1317824917908430854/1mYc98Ph_normal.jpg', followers: '3.7K', verified: false },
  { id: '58', displayName: 'Matthias', username: 'matthiasendler', avatar: 'https://pbs.twimg.com/profile_images/1891466231506509824/txbh4Gyz_normal.jpg', followers: '3.4K', verified: false },
  { id: '59', displayName: 'Pekka Enberg', username: 'penberg', avatar: 'https://pbs.twimg.com/profile_images/1788896683851431936/xDcdmOSH_normal.jpg', followers: '15.4K', verified: true },
  { id: '60', displayName: 'yuki', username: 'helloyuki_', avatar: 'https://pbs.twimg.com/profile_images/1908148223509979136/VEWecsSY_normal.png', followers: '6.9K', verified: true },
  { id: '61', displayName: 'Rust Nation UK 🦀', username: 'RustNationUK', avatar: 'https://pbs.twimg.com/profile_images/1960631398835904512/xTZ6c3cD_normal.png', followers: '4.1K', verified: true },
  { id: '62', displayName: 'Florian Gilcher', username: 'Argorak', avatar: 'https://pbs.twimg.com/profile_images/2902714965/86f0a67b9b1f1e5e5d1f443580842ddb_normal.png', followers: '4.7K', verified: false },
  { id: '63', displayName: 'Michael Gattozzi', username: 'mgattozzi', avatar: 'https://pbs.twimg.com/profile_images/1841258226655911939/fNZR6Vhw_normal.jpg', followers: '5.3K', verified: false },
  { id: '64', displayName: 'Samuel Colvin', username: 'samuel_colvin', avatar: 'https://pbs.twimg.com/profile_images/1678332260569710594/of0Ed11O_normal.jpg', followers: '18.2K', verified: true },
  { id: '65', displayName: 'Josh Triplett', username: 'josh_triplett', avatar: 'https://pbs.twimg.com/profile_images/1160249970215096321/a6xs3OoG_normal.jpg', followers: '3.9K', verified: false },
  { id: '66', displayName: 'The Rust Dev', username: 'the_Rust_Dev', avatar: 'https://pbs.twimg.com/profile_images/1103095346090205184/xsmRgk2U_normal.png', followers: '3.2K', verified: false },
  { id: '67', displayName: 'EuroRust', username: 'euro_rust', avatar: 'https://pbs.twimg.com/profile_images/1897586624000557056/AFY0Kosp_normal.jpg', followers: '3.4K', verified: true },
  { id: '68', displayName: 'Lucretiel 🦀', username: 'Lucretiel', avatar: 'https://pbs.twimg.com/profile_images/469826285586223105/QPARx1pH_normal.png', followers: '3K', verified: false },
  { id: '69', displayName: 'Glauber Costa', username: 'glcst', avatar: 'https://pbs.twimg.com/profile_images/1986909545273155584/V08BerFl_normal.jpg', followers: '14.5K', verified: true },
  { id: '70', displayName: 'Marco Ieni 🦀', username: 'marcoieni', avatar: 'https://pbs.twimg.com/profile_images/1830235001603977216/mwq1zHmR_normal.jpg', followers: '2.2K', verified: false },
  { id: '71', displayName: 'Archie', username: 'Archie_Amari', avatar: 'https://pbs.twimg.com/profile_images/1991146649863798784/8mKAIoLc_normal.jpg', followers: '1.1K', verified: true },
  { id: '72', displayName: 'Josh (🦀/acc)', username: 'joshmo_dev', avatar: 'https://pbs.twimg.com/profile_images/1887863909962407936/WTNpHgos_normal.jpg', followers: '3.4K', verified: true },
  { id: '73', displayName: 'Rust Bytes 🦀', username: 'rustaceans_rs', avatar: 'https://pbs.twimg.com/profile_images/1785754752103366656/CQJ0vvGU_normal.jpg', followers: '3.2K', verified: false },
  { id: '74', displayName: 'carl.tokio', username: 'carllerche', avatar: 'https://pbs.twimg.com/profile_images/1108645829/4031134264_c87a759f10_normal.jpg', followers: '5.8K', verified: false },
  { id: '75', displayName: 'Geoffroy Couprie', username: 'gcouprie', avatar: 'https://pbs.twimg.com/profile_images/1786821546356477952/-pVFFwHg_normal.jpg', followers: '5.3K', verified: false },
  { id: '76', displayName: 'Will Crichton', username: 'tonofcrates', avatar: 'https://pbs.twimg.com/profile_images/1290099259409174529/j-T2oIMA_normal.jpg', followers: '7.1K', verified: false },
  { id: '77', displayName: 'RustCast', username: 'RustCast', avatar: 'https://pbs.twimg.com/profile_images/1022614090290790400/mERKDBfG_normal.jpg', followers: '2.9K', verified: false },
  { id: '78', displayName: 'KOBA789', username: 'KOBA789', avatar: 'https://pbs.twimg.com/profile_images/1424333466271842315/gv--S_l8_normal.png', followers: '11.1K', verified: false },
  { id: '79', displayName: 'Herbert "TheBracket" Wolverson', username: 'herberticus', avatar: 'https://pbs.twimg.com/profile_images/1230128522372550658/1tzusyzM_normal.jpg', followers: '2.6K', verified: false },
  { id: '80', displayName: 'Rust Videos', username: 'RustVideos', avatar: 'https://pbs.twimg.com/profile_images/778165115757727746/XFU-P3vQ_normal.jpg', followers: '3.3K', verified: false },
  { id: '81', displayName: 'Carter Barrows', username: 'cart_cart', avatar: 'https://abs.twimg.com/sticky/default_profile_images/default_profile_normal.png', followers: '105', verified: false },
  { id: '82', displayName: 'Dmitriy Kovalenko', username: 'neogoose_btw', avatar: 'https://pbs.twimg.com/profile_images/1875534938289627136/UINQoJ24_normal.jpg', followers: '12.7K', verified: true },
  { id: '83', displayName: 'Wasmer', username: 'wasmerio', avatar: 'https://pbs.twimg.com/profile_images/1934920853822885888/Y-tiT_3K_normal.jpg', followers: '10.4K', verified: false },
  { id: '84', displayName: "Björkus 'No time_t to Die' Dorkus", username: '__phantomderp', avatar: 'https://pbs.twimg.com/profile_images/1696222936892350464/tPMPysSa_normal.jpg', followers: '13K', verified: false },
  { id: '85', displayName: 'RustSec', username: 'RustSec', avatar: 'https://pbs.twimg.com/profile_images/825186818278584320/zVKr7DJa_normal.jpg', followers: '2.4K', verified: false },
  { id: '86', displayName: 'RustLondon 🦀', username: 'RustLondon_', avatar: 'https://pbs.twimg.com/profile_images/1354807429821657091/vXuKlW_A_normal.png', followers: '3.2K', verified: true },
  { id: '87', displayName: 'The V Programming Language', username: 'v_language', avatar: 'https://pbs.twimg.com/profile_images/1183559167086333953/fUOK2Eqi_normal.jpg', followers: '9.5K', verified: false },
  { id: '88', displayName: 'Rust CLI Working Group', username: 'CliRust', avatar: 'https://pbs.twimg.com/profile_images/1108138507049025547/LrvY3F6l_normal.png', followers: '2.2K', verified: false },
  { id: '89', displayName: 'AeroRust ( ÄR )', username: 'AeroRust', avatar: 'https://pbs.twimg.com/profile_images/1345655184249266177/fYFHlg3m_normal.jpg', followers: '1.9K', verified: false },
  { id: '90', displayName: 'Awesome Rust Repositories', username: 'RustRepos', avatar: 'https://pbs.twimg.com/profile_images/1375128761977409541/9xnibSpE_normal.jpg', followers: '3.4K', verified: false },
  { id: '91', displayName: 'Matt Boyle', username: 'MattJamesBoyle', avatar: 'https://pbs.twimg.com/profile_images/1356149791835754497/XejDgFhC_normal.jpg', followers: '14.2K', verified: true },
  { id: '92', displayName: 'Loris Cro ⚡', username: 'croloris', avatar: 'https://pbs.twimg.com/profile_images/1687397710502952960/U0WyCKgQ_normal.jpg', followers: '7.7K', verified: true },
  { id: '93', displayName: 'Dimitar', username: 'dimitrov2k', avatar: 'https://pbs.twimg.com/profile_images/1621657385575108608/fIhYmIyf_normal.jpg', followers: '2.3K', verified: true },
  { id: '94', displayName: 'Lucio Franco', username: 'lucio_d_franco', avatar: 'https://pbs.twimg.com/profile_images/1385705887877279749/002eTuvW_normal.jpg', followers: '2.8K', verified: false },
  { id: '95', displayName: 'Ratatui', username: 'ratatui_rs', avatar: 'https://pbs.twimg.com/profile_images/1957578031330934786/4-qTEXzb_normal.jpg', followers: '3.3K', verified: false },
  { id: '96', displayName: 'κeen', username: 'blackenedgold', avatar: 'https://pbs.twimg.com/profile_images/1481043234952736768/_ctoqt7h_normal.jpg', followers: '7.4K', verified: false },
  { id: '97', displayName: 'Rust.Tokyo', username: 'rustlang_tokyo', avatar: 'https://pbs.twimg.com/profile_images/1842527733378883584/eDkpYuOL_normal.jpg', followers: '2.4K', verified: false },
  { id: '98', displayName: 'Tyler Mandry', username: 'tmandry', avatar: 'https://pbs.twimg.com/profile_images/1054187688742584320/pQZrPGBp_normal.jpg', followers: '2.3K', verified: false },
  { id: '99', displayName: 'David Pedersen', username: 'DavidPdrsn', avatar: 'https://pbs.twimg.com/profile_images/1047178833038856193/h_g3L1wc_normal.jpg', followers: '2.3K', verified: false },
  { id: '100', displayName: 'Pablo Galindo Salgado', username: 'pyblogsal', avatar: 'https://pbs.twimg.com/profile_images/1984681312674791424/JSvwDqih_normal.jpg', followers: '13.1K', verified: false },
]

// Hardcoded Rust audience users in specified order (real data from X API)
const RUST_USERS: Account[] = [
  { id: 'u1', displayName: 'Amirreza Gh', username: 'amrzgh', avatar: 'https://pbs.twimg.com/profile_images/1645029834546987009/Tmm5q-RF_normal.jpg', followers: '166', verified: false },
  { id: 'u3', displayName: 'The 5422m4n 🦀', username: '5422m4n', avatar: 'https://pbs.twimg.com/profile_images/1485742607074566148/LuzRgfeZ_normal.png', followers: '457', verified: false },
  { id: 'u4', displayName: 'AlexZ 🦀', username: 'blackanger', avatar: 'https://pbs.twimg.com/profile_images/1588061971714256896/Rwi_kcm7_normal.jpg', followers: '15.1K', verified: true },
  { id: 'u5', displayName: 'Vanius Bittencourt', username: 'vaniusrb', avatar: 'https://pbs.twimg.com/profile_images/1620887758125375500/MwBxo3TN_normal.jpg', followers: '653', verified: true },
  { id: 'u6', displayName: 'llogiq', username: 'llogiq', avatar: 'https://pbs.twimg.com/profile_images/1863606399697027072/FA0QN6WD_normal.jpg', followers: '2.6K', verified: false },
  { id: 'u7', displayName: 'Zak Horton 🦀 Rust Enthusiast', username: 'cleancodestudio', avatar: 'https://pbs.twimg.com/profile_images/1517439051980165120/YtagO5ip_normal.jpg', followers: '1.3K', verified: true },
  { id: 'u8', displayName: 'nsuz', username: 'nsuz_', avatar: 'https://pbs.twimg.com/profile_images/1563859759052226562/p7GIDaGM_normal.jpg', followers: '192', verified: false },
  { id: 'u9', displayName: 'Binh Nguyen', username: 'ngbinh', avatar: 'https://pbs.twimg.com/profile_images/542157473319100416/YuczLpxb_normal.jpeg', followers: '412', verified: false },
  { id: 'u10', displayName: 'max.rss', username: 'tekknolagi', avatar: 'https://pbs.twimg.com/profile_images/1582650764249354241/g7Zm6iKG_normal.jpg', followers: '1.7K', verified: false },
  { id: 'u11', displayName: 'ABAB↑↓BA', username: 'ababupdownba', avatar: 'https://pbs.twimg.com/profile_images/378800000418279831/d4265ecb1cc22f66c64abdc4dc700cfc_normal.jpeg', followers: '1.9K', verified: false },
  { id: 'u12', displayName: 'Serge Kovalenko', username: 'sergkovalenko_', avatar: 'https://pbs.twimg.com/profile_images/778403271119544322/2hIFU1HN_normal.jpg', followers: '110', verified: false },
  { id: 'u13', displayName: 'Surma', username: 'DasSurma', avatar: 'https://pbs.twimg.com/profile_images/1568254009634430976/Q0jsTVnt_normal.jpg', followers: '38.1K', verified: false },
  { id: 'u14', displayName: 'Miguel Ángel Pastor', username: 'miguelinlas3', avatar: 'https://pbs.twimg.com/profile_images/1984524245242679296/4_SIKtft_normal.jpg', followers: '3K', verified: false },
  { id: 'u15', displayName: 'Stefano Lanzavecchia', username: 'wildy2k', avatar: 'https://pbs.twimg.com/profile_images/691084908/Ranma_ico_normal.jpg', followers: '130', verified: false },
  { id: 'u16', displayName: 'Sean', username: 'mankykitty', avatar: 'https://pbs.twimg.com/profile_images/1284127574675861504/tEm8LlVQ_normal.jpg', followers: '237', verified: false },
  { id: 'u17', displayName: 'Arjun Sunil Kumar', username: 'arjunsk15', avatar: 'https://pbs.twimg.com/profile_images/1039583403857694720/cfxNhAdE_normal.jpg', followers: '60', verified: false },
  { id: 'u18', displayName: 'irving', username: '1107026942', avatar: 'https://pbs.twimg.com/profile_images/1488710539274424321/MYgeKdqh_normal.jpg', followers: '3', verified: false },
  { id: 'u19', displayName: 'David Gregory', username: 'DavidGregory084', avatar: 'https://pbs.twimg.com/profile_images/1397285319133868048/YvfGqW2o_normal.jpg', followers: '120', verified: false },
  { id: 'u20', displayName: 'Benjamin Tan', username: 'bnjmnt4n', avatar: 'https://pbs.twimg.com/profile_images/1726601419023958016/YlmWjv-F_normal.jpg', followers: '210', verified: false },
  { id: 'u21', displayName: 'はろ〜', username: 'Permanjeam', avatar: 'https://pbs.twimg.com/profile_images/465330071415185408/KIwOIWA5_normal.jpeg', followers: '48', verified: false },
  { id: 'u22', displayName: 'Pedro Girardi', username: 'pedrorgirardi', avatar: 'https://pbs.twimg.com/profile_images/1519043790165708801/SSLJ3ssr_normal.jpg', followers: '248', verified: false },
  { id: 'u23', displayName: '子茄', username: 'ant_sz', avatar: 'https://pbs.twimg.com/profile_images/490436556985884672/LqDWeDkl_normal.jpeg', followers: '9.5K', verified: false },
  { id: 'u24', displayName: 'Bighelmet7', username: 'bighelmet7', avatar: 'https://pbs.twimg.com/profile_images/1185587454486687745/oVIUeLpY_normal.jpg', followers: '46', verified: false },
  { id: 'u25', displayName: 'Carlos Gustavo', username: 'carlosgruiz_dev', avatar: 'https://pbs.twimg.com/profile_images/1979891144440868864/x8ibt5lL_normal.jpg', followers: '150', verified: false },
  { id: 'u26', displayName: 'EmNudge', username: 'emnudge', avatar: 'https://pbs.twimg.com/profile_images/1681088744538136576/ER9oRi1S_normal.jpg', followers: '368', verified: false },
  { id: 'u27', displayName: 'Hideaki Takahashi', username: 'hideaki_t', avatar: 'https://pbs.twimg.com/profile_images/378800000216883209/71206a3c1e6af3b0756e378824a6adab_normal.jpeg', followers: '602', verified: false },
  { id: 'u28', displayName: 'Zaid Humayun', username: 'redixhumayun', avatar: 'https://pbs.twimg.com/profile_images/2000892304777994241/QNBSJdB0_normal.jpg', followers: '2K', verified: true },
  { id: 'u29', displayName: 'NadeshikoManju', username: 'Manjusaka_Lee', avatar: 'https://pbs.twimg.com/profile_images/1935620728704872448/pGPf6U_2_normal.jpg', followers: '35.4K', verified: true },
  { id: 'u30', displayName: 'Mayank Shah', username: 'mayankshah__', avatar: 'https://pbs.twimg.com/profile_images/1908917982123982848/ETF-pvjQ_normal.jpg', followers: '415', verified: false },
  { id: 'u31', displayName: 'AbulAsar S.', username: 'abul_asar', avatar: 'https://pbs.twimg.com/profile_images/1836654365630775299/_G5QzELG_normal.jpg', followers: '330', verified: false },
  { id: 'u32', displayName: 'Bryan Russett', username: 'bcrussett', avatar: 'https://pbs.twimg.com/profile_images/1830385633421832192/PSvFVlmh_normal.jpg', followers: '1.2K', verified: true },
  { id: 'u33', displayName: 'Javier Honduvilla Coto', username: 'javierhonduco', avatar: 'https://pbs.twimg.com/profile_images/1702014220613632000/SSs3b9u5_normal.jpg', followers: '947', verified: false },
  { id: 'u34', displayName: 'Bruno Carballo Zama', username: 'brunocaza', avatar: 'https://pbs.twimg.com/profile_images/1830313276434980866/Uuz0eJb1_normal.jpg', followers: '180', verified: false },
  { id: 'u35', displayName: 'Vendy', username: 'vendydev', avatar: 'https://pbs.twimg.com/profile_images/2004032715436576768/3sfj2Ytw_normal.jpg', followers: '232', verified: false },
  { id: 'u36', displayName: 'Nikolay Rusev', username: 'nrusev', avatar: 'https://pbs.twimg.com/profile_images/2243194946/avatar_100504_normal.jpg', followers: '139', verified: false },
  { id: 'u37', displayName: '2gua', username: 'im2gua', avatar: 'https://pbs.twimg.com/profile_images/766441986610106369/7gye_kUR_normal.jpg', followers: '11.2K', verified: false },
  { id: 'u38', displayName: 'Famazet', username: 'famazet', avatar: 'https://pbs.twimg.com/profile_images/1249699177652727808/Ex-UgMVq_normal.jpg', followers: '22', verified: false },
  { id: 'u39', displayName: 'Enrico Secondulfo', username: 'enriSecondulfo', avatar: 'https://pbs.twimg.com/profile_images/748184299690672130/Vvuvww3o_normal.jpg', followers: '65', verified: false },
  { id: 'u40', displayName: 'Siraj', username: 'syhner', avatar: 'https://pbs.twimg.com/profile_images/1944898240337334272/ZN7BaQWg_normal.jpg', followers: '43', verified: false },
  { id: 'u41', displayName: 'Matri𝕏tang⚡️', username: 'matrixkook67', avatar: 'https://pbs.twimg.com/profile_images/1563202660190556168/b0GdTEdR_normal.jpg', followers: '171', verified: false },
  { id: 'u42', displayName: 'Amir', username: 'callmeamirv', avatar: 'https://pbs.twimg.com/profile_images/1871437899125641216/GNcr_kPB_normal.jpg', followers: '232', verified: false },
  { id: 'u43', displayName: '.', username: 'a_swe_daily', avatar: 'https://pbs.twimg.com/profile_images/1755043797850034176/4Ki94GiI_normal.jpg', followers: '33', verified: false },
  { id: 'u44', displayName: 'Jan Scheer', username: 'jhscheer', avatar: 'https://pbs.twimg.com/profile_images/1016143729101606916/FZe3aFey_normal.jpg', followers: '53', verified: false },
  { id: 'u45', displayName: 'Alexandre', username: 'kooparse', avatar: 'https://pbs.twimg.com/profile_images/1287767406929215489/AJEMWqXN_normal.jpg', followers: '265', verified: false },
  { id: 'u46', displayName: '.', username: 'irp854_', avatar: 'https://pbs.twimg.com/profile_images/1194494833/52512_1610253777444_1269227985_1678959_5360431_o__1__normal.jpg', followers: '221', verified: false },
  { id: 'u47', displayName: 'Philip Weir', username: 'philip_weir', avatar: 'https://pbs.twimg.com/profile_images/698142098650824705/0_95v9N5_normal.jpg', followers: '166', verified: false },
  { id: 'u48', displayName: 'Mukilan Thiyagarajan', username: 'mukilan_t', avatar: 'https://pbs.twimg.com/profile_images/599200790914273282/NKJd5LrS_normal.png', followers: '42', verified: false },
  { id: 'u49', displayName: 'nerdyet', username: 'nerdyet', avatar: 'https://pbs.twimg.com/profile_images/1915406050808954880/gnB49bhe_normal.jpg', followers: '42', verified: false },
  { id: 'u50', displayName: 'Ed Minnix', username: 'egregius313', avatar: 'https://pbs.twimg.com/profile_images/1513534119392731136/CS-RvmQm_normal.jpg', followers: '56', verified: false },
  { id: 'u51', displayName: 'Kushashwa Ravi Shrimali', username: 'kushashwa', avatar: 'https://pbs.twimg.com/profile_images/1956753184820436992/cAJ3CtoY_normal.jpg', followers: '547', verified: true },
  { id: 'u52', displayName: 'nah', username: 'panic_pistol', avatar: 'https://pbs.twimg.com/profile_images/1082172765204070400/YnN3LRDW_normal.jpg', followers: '23', verified: false },
  { id: 'u53', displayName: '✋', username: 'suhtnamsoi', avatar: 'https://pbs.twimg.com/profile_images/1850541046712909824/Z8NGnpfr_normal.jpg', followers: '129', verified: false },
  { id: 'u54', displayName: 'Alex R. Pascual', username: 'AleRpascual', avatar: 'https://pbs.twimg.com/profile_images/1522956245115748352/2lN-9pym_normal.jpg', followers: '14', verified: false },
  { id: 'u55', displayName: 'Pavlo', username: 'fxposter', avatar: 'https://pbs.twimg.com/profile_images/378800000062279608/feebef6a55e2c626d182013b9742a4b0_normal.jpeg', followers: '389', verified: false },
  { id: 'u56', displayName: 'Seo Sanghyeon', username: 'sanxiyn', avatar: 'https://pbs.twimg.com/profile_images/1933349319639511042/Cz1WriPK_normal.jpg', followers: '3.9K', verified: true },
  { id: 'u57', displayName: '@timvw@fosstodon.org', username: 'timvw', avatar: 'https://pbs.twimg.com/profile_images/789938493514510336/yYCtDhy7_normal.jpg', followers: '426', verified: false },
  { id: 'u58', displayName: 'Jasim', username: 'jasim_ab', avatar: 'https://pbs.twimg.com/profile_images/1976228900419084288/QjEJhfbM_normal.jpg', followers: '1.6K', verified: true },
  { id: 'u59', displayName: 'yofri', username: 'yofriadi', avatar: 'https://pbs.twimg.com/profile_images/1429842697347473411/kPnEat85_normal.jpg', followers: '259', verified: false },
  { id: 'u60', displayName: 'DrKJam', username: 'drkjam', avatar: 'https://pbs.twimg.com/profile_images/1955957495039434752/49o-91QD_normal.jpg', followers: '95', verified: false },
  { id: 'u61', displayName: 'Tingwei', username: 'sbvq6p199xe', avatar: 'https://pbs.twimg.com/profile_images/1609605676200005634/x4l7urWW_normal.jpg', followers: '139', verified: false },
  { id: 'u62', displayName: 'ta7ik0', username: 'ta7ik0', avatar: 'https://pbs.twimg.com/profile_images/1664361226233839616/sZU6a_t2_normal.jpg', followers: '6', verified: false },
  { id: 'u63', displayName: 'Atom Chaipreecha', username: 'attomos', avatar: 'https://pbs.twimg.com/profile_images/1231155440525824001/4AN82t50_normal.jpg', followers: '36', verified: false },
  { id: 'u64', displayName: 'vados', username: 'vadosware', avatar: 'https://pbs.twimg.com/profile_images/1949257801697792000/Rjf5U6e0_normal.jpg', followers: '199', verified: false },
  { id: 'u65', displayName: 'ReedSoul', username: 'Reed_soul', avatar: 'https://pbs.twimg.com/profile_images/1228554944363421696/O20MBTWd_normal.jpg', followers: '25', verified: false },
  { id: 'u66', displayName: 'Kunal', username: 'machines_fail', avatar: 'https://pbs.twimg.com/profile_images/1575469929683628033/KgARX4h2_normal.jpg', followers: '195', verified: false },
  { id: 'u67', displayName: 'Filipe Regadas', username: 'regadas', avatar: 'https://pbs.twimg.com/profile_images/1022494804481998849/2Baar0OV_normal.jpg', followers: '579', verified: false },
  { id: 'u68', displayName: 'Brandon Barker', username: 'b_barker', avatar: 'https://pbs.twimg.com/profile_images/1720953989431283713/yc4gjALe_normal.jpg', followers: '224', verified: false },
  { id: 'u69', displayName: 'Bing Ye', username: 'yebingcrack', avatar: 'https://abs.twimg.com/sticky/default_profile_images/default_profile_normal.png', followers: '6', verified: false },
  { id: 'u70', displayName: 'Nils Harrison', username: 'NilsHarrison', avatar: 'https://pbs.twimg.com/profile_images/1324883539834396674/lU210isP_normal.jpg', followers: '7', verified: false },
  { id: 'u71', displayName: 'M', username: 'subnjet', avatar: 'https://pbs.twimg.com/profile_images/1375199831849848836/VP3kaWVk_normal.jpg', followers: '173', verified: false },
  { id: 'u72', displayName: 'Frédéric Masion', username: 'fmasion', avatar: 'https://pbs.twimg.com/profile_images/3406071546/8baa626d244097ea12ecdf7bb5c62556_normal.jpeg', followers: '66', verified: false },
  { id: 'u73', displayName: 'Shaun Broomfield', username: 'ShaunBroomfield', avatar: 'https://pbs.twimg.com/profile_images/1634589658783907840/J-OmMwC8_normal.jpg', followers: '53', verified: false },
  { id: 'u74', displayName: 'sontixyou', username: 'sontixyou', avatar: 'https://pbs.twimg.com/profile_images/1568584526083010560/deFNh_Bb_normal.jpg', followers: '365', verified: false },
  { id: 'u75', displayName: 'Akihiro Suda', username: '_AkihiroSuda_', avatar: 'https://abs.twimg.com/sticky/default_profile_images/default_profile_normal.png', followers: '3.5K', verified: false },
  { id: 'u76', displayName: 'engineer', username: 'engineer704', avatar: 'https://abs.twimg.com/sticky/default_profile_images/default_profile_normal.png', followers: '5', verified: false },
  { id: 'u77', displayName: 'Dispo Mail', username: 'MailDispo', avatar: 'https://abs.twimg.com/sticky/default_profile_images/default_profile_normal.png', followers: '18', verified: false },
  { id: 'u78', displayName: 'alf4s1erra', username: 'alf4s1erra', avatar: 'https://pbs.twimg.com/profile_images/1351479103300501505/UdyJwq2B_normal.jpg', followers: '125', verified: false },
  { id: 'u79', displayName: '@brendan@discuss.systems', username: 'brendancully', avatar: 'https://pbs.twimg.com/profile_images/826968119021166592/nbFX8wwJ_normal.jpg', followers: '89', verified: false },
  { id: 'u80', displayName: 'Jon Johnson', username: 'jonjonsonjr', avatar: 'https://pbs.twimg.com/profile_images/902438300362858497/6Y-gNNLV_normal.jpg', followers: '312', verified: false },
  { id: 'u81', displayName: '☕️ aris m 🐈', username: 'ag1m4t', avatar: 'https://pbs.twimg.com/profile_images/1635083971452084226/iJt0G9Za_normal.jpg', followers: '54', verified: false },
  { id: 'u82', displayName: 'もぷり', username: 'Mopp_jp', avatar: 'https://pbs.twimg.com/profile_images/919125609283969025/3F2-erNZ_normal.jpg', followers: '1.1K', verified: false },
  { id: 'u83', displayName: 'Gavin Meier', username: 'gavinmeier25', avatar: 'https://pbs.twimg.com/profile_images/1595420106405855237/d-iAbdfO_normal.jpg', followers: '233', verified: false },
  { id: 'u84', displayName: 'Gowtham Raj', username: 'GowthamRaj100', avatar: 'https://pbs.twimg.com/profile_images/1275334252859555845/AI5KTJEl_normal.jpg', followers: '106', verified: false },
  { id: 'u85', displayName: 'longerpop', username: 'longerpop', avatar: 'https://abs.twimg.com/sticky/default_profile_images/default_profile_normal.png', followers: '15', verified: false },
  { id: 'u86', displayName: 'Anuradha', username: 'indikaanu83', avatar: 'https://pbs.twimg.com/profile_images/1413841068466921472/fBQu7q0j_normal.jpg', followers: '16', verified: false },
  { id: 'u87', displayName: 'Legajzp', username: 'Legajzp', avatar: 'https://pbs.twimg.com/profile_images/1558507171624947712/AQClvIxX_normal.jpg', followers: '23', verified: false },
  { id: 'u88', displayName: 'nayihz', username: 'nayihzzy', avatar: 'https://pbs.twimg.com/profile_images/1564099240779030528/7JFjQr38_normal.jpg', followers: '32', verified: false },
  { id: 'u89', displayName: 'Rohan Chhabra', username: 'RohanChhabra23', avatar: 'https://pbs.twimg.com/profile_images/1454593481029074944/vHl2i68r_normal.jpg', followers: '86', verified: false },
  { id: 'u90', displayName: 'rohan kumar', username: 'rohanku43485614', avatar: 'https://pbs.twimg.com/profile_images/1770745579703848962/yjgXQoUb_normal.jpg', followers: '29', verified: false },
  { id: 'u91', displayName: 'Lambda Lille', username: 'lambdalille', avatar: 'https://pbs.twimg.com/profile_images/807181505772535808/8MgVCH7e_normal.jpg', followers: '255', verified: false },
  { id: 'u92', displayName: 'Rheakles', username: 'rheakles', avatar: 'https://pbs.twimg.com/profile_images/1876133553521786880/nCrDXMtc_normal.jpg', followers: '36', verified: false },
  { id: 'u93', displayName: 'LinuxModernism', username: 'LinuxModernism', avatar: 'https://pbs.twimg.com/profile_images/1174882764857991169/qpwnP-qp_normal.jpg', followers: '217', verified: false },
  { id: 'u94', displayName: 'Will', username: 'hnfmr', avatar: 'https://abs.twimg.com/sticky/default_profile_images/default_profile_normal.png', followers: '18', verified: false },
  { id: 'u95', displayName: 'Kyle Johnson', username: 'negcx', avatar: 'https://pbs.twimg.com/profile_images/1269089203490557952/A868ZGGJ_normal.jpg', followers: '140', verified: false },
  { id: 'u96', displayName: 'Bugen Zhao', username: 'BugenZhao', avatar: 'https://pbs.twimg.com/profile_images/1503665725411450880/liUzvs1y_normal.jpg', followers: '2.9K', verified: false },
  { id: 'u97', displayName: 'Quang Dang', username: 'xray_dang', avatar: 'https://pbs.twimg.com/profile_images/1816508070908092416/NZUkgqVF_normal.jpg', followers: '4', verified: false },
  { id: 'u98', displayName: 'R66', username: 'icppngame', avatar: 'https://pbs.twimg.com/profile_images/2886291933/95471ef2541442c2a74236fd5ee14d22_normal.jpeg', followers: '18', verified: false },
  { id: 'u98', displayName: 'Werner', username: 'guilhermeqwr', avatar: 'https://pbs.twimg.com/profile_images/2007862014236860416/4UBUZ7nD_normal.jpg', followers: '121', verified: false },
]

// Real accounts from API
const influencerAccounts = ref<Account[]>([])
const userAccounts = ref<Account[]>([])

// Initialize accounts
const initAccounts = () => {
  loading.value = true
  
  // Use hardcoded data for influencers
  influencerAccounts.value = RUST_INFLUENCERS
  
  // Use hardcoded data for users
  userAccounts.value = RUST_USERS
  
  loading.value = false
}

const getRankClass = (index: number) => {
  if (index === 0) return 'rank-gold'
  if (index === 1) return 'rank-silver'
  if (index === 2) return 'rank-bronze'
  return ''
}

// Initialize data on mount
onMounted(() => {
  initAccounts()
})
</script>

<style scoped>
.audience-page-container {
  min-height: 100vh;
  background-color: #000;
  padding: 1.5rem;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* Back Navigation */
.back-nav {
  max-width: 1200px;
  margin: 0 auto 2rem;
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

/* Audience Header */
.audience-header {
  text-align: center;
  max-width: 800px;
  margin: 0 auto 2rem;
}

.audience-icon {
  width: 80px;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 20px;
  overflow: hidden;
  margin: 0 auto 1.25rem;
}

.audience-logo {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.audience-title {
  font-size: clamp(1.75rem, 4vw, 2.5rem);
  font-weight: 700;
  color: #fff;
  margin-bottom: 0.5rem;
  letter-spacing: -0.02em;
}

.audience-description {
  font-size: 1.1rem;
  color: #71767b;
  margin-bottom: 1rem;
  max-width: 500px;
  line-height: 1.6;
  text-align: center;
  margin-left: auto;
  margin-right: auto;
}

.highlight-cta {
  color: #e7e9ea;
  font-weight: 600;
}

.audience-stats {
  display: flex;
  justify-content: center;
  gap: 1rem;
}

.stat-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background-color: #16181c;
  border: 1px solid #2f3336;
  color: #e7e9ea;
  font-size: 0.95rem;
  font-weight: 600;
  padding: 0.6rem 1.25rem;
  border-radius: 50px;
}

.stat-badge svg {
  color: #1d9bf0;
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

.count-badge {
  background-color: rgba(29, 155, 240, 0.2);
  color: #1d9bf0;
  font-size: 0.75rem;
  font-weight: 600;
  padding: 0.25rem 0.6rem;
  border-radius: 50px;
}

.toggle-btn.active .count-badge {
  background-color: rgba(0, 0, 0, 0.1);
  color: #000;
}

/* List Header */
.list-header {
  text-align: center;
  margin-bottom: 1.5rem;
}

.list-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #e7e9ea;
  margin-bottom: 0.35rem;
}

.list-subtitle {
  font-size: 0.95rem;
  color: #71767b;
}

/* Loading State */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
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

.loading-message {
  margin-top: 1.25rem;
  color: #71767b;
  font-size: 0.95rem;
}

/* Accounts Grid */
.accounts-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  grid-auto-flow: row;
  gap: 0.75rem;
  max-width: 1200px;
  margin: 0 auto;
}

.account-card {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  background-color: #16181c;
  border: 1px solid #2f3336;
  border-radius: 12px;
  padding: 0.875rem 1rem;
  transition: all 0.15s ease;
}

.account-card:hover {
  border-color: #3f4347;
  background-color: #1d1f23;
}

/* Account Rank */
.account-rank {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #2f3336;
  border-radius: 8px;
  font-size: 0.85rem;
  font-weight: 700;
  color: #e7e9ea;
  flex-shrink: 0;
}

.account-rank.rank-gold {
  background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
  color: #000;
}

.account-rank.rank-silver {
  background: linear-gradient(135deg, #C0C0C0 0%, #A8A8A8 100%);
  color: #000;
}

.account-rank.rank-bronze {
  background: linear-gradient(135deg, #CD7F32 0%, #A0522D 100%);
  color: #fff;
}

.account-rank.user-rank {
  background-color: #1d3a5c;
  color: #1d9bf0;
}

/* Account Avatar */
.account-avatar {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  overflow: hidden;
  flex-shrink: 0;
  background-color: #2f3336;
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
  max-width: 140px;
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

/* Follow Button */
.follow-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.5rem 1rem;
  background-color: transparent;
  border: 1px solid #536471;
  border-radius: 50px;
  color: #e7e9ea;
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  text-decoration: none;
  flex-shrink: 0;
}

.follow-btn:hover {
  background-color: rgba(231, 233, 234, 0.1);
  border-color: #e7e9ea;
}

/* Responsive */
@media (max-width: 900px) {
  .accounts-grid {
    grid-template-columns: 1fr;
  }
  
  .account-name {
    max-width: 200px;
  }
}

@media (max-width: 600px) {
  .audience-page-container {
    padding: 1rem;
  }
  
  .toggle-btn {
    padding: 0.6rem 1rem;
    font-size: 0.85rem;
  }
  
  .account-avatar {
    width: 38px;
    height: 38px;
  }
  
  .account-rank {
    width: 28px;
    height: 28px;
    font-size: 0.75rem;
  }
  
  .account-name {
    font-size: 0.85rem;
    max-width: 120px;
  }
  
  .follow-btn {
    padding: 0.4rem 0.75rem;
    font-size: 0.75rem;
  }
}
</style>
