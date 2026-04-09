<template>
  <div class="app">
    <header class="header">
      <div class="header-inner">
        <div class="logo">
          <span class="logo-icon">◈</span>
          <span class="logo-text">DataLens</span>
        </div>
        <p class="tagline">Customer Analytics · Powered by your data</p>
      </div>
    </header>

    <main class="main">
      <UploadSection @data-analyzed="onDataAnalyzed" />
      <div v-if="analysisData" class="results">
        <SummaryCards :summary="analysisData.summary" />
        <ChartsSection :data="analysisData" />
        <RecommendationsSection :recommendations="analysisData.recommendations" />
      </div>
    </main>
  </div>
</template>

<script>
import UploadSection from './components/UploadSection.vue'
import ChartsSection from './components/ChartsSection.vue'
import RecommendationsSection from './components/RecommendationsSection.vue'
import SummaryCards from './components/SummaryCards.vue'

export default {
  components: { UploadSection, ChartsSection, RecommendationsSection, SummaryCards },
  data() {
    return { analysisData: null }
  },
  methods: {
    onDataAnalyzed(data) {
      this.analysisData = data
    }
  }
}
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
  --bg: #0a0a0f;
  --surface: #111118;
  --surface2: #1a1a24;
  --border: #2a2a3a;
  --accent: #7c6fff;
  --accent2: #ff6b9d;
  --accent3: #00d9c0;
  --text: #e8e8f0;
  --text-muted: #6b6b80;
  --high: #ff4d6d;
  --med: #ffd166;
}

body {
  background: var(--bg);
  color: var(--text);
  font-family: 'DM Mono', monospace;
  min-height: 100vh;
}

.app { min-height: 100vh; }

.header {
  border-bottom: 1px solid var(--border);
  padding: 20px 40px;
  background: linear-gradient(180deg, #13131f 0%, transparent 100%);
}

.header-inner { max-width: 1200px; margin: 0 auto; display: flex; align-items: center; gap: 24px; }

.logo { display: flex; align-items: center; gap: 10px; }
.logo-icon { font-size: 24px; color: var(--accent); }
.logo-text { font-family: 'Syne', sans-serif; font-size: 22px; font-weight: 800; letter-spacing: -0.5px; }
.tagline { color: var(--text-muted); font-size: 12px; }

.main { max-width: 1200px; margin: 0 auto; padding: 40px; }

.results { margin-top: 40px; display: flex; flex-direction: column; gap: 40px; }
</style>