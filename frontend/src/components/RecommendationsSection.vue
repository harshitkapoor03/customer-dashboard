<template>
  <div class="reco-section">
    <h2 class="section-title">⚡ Campaign Recommendations</h2>
    <div class="reco-grid">
      <div v-for="(r, i) in recommendations" :key="i" class="reco-card" :class="r.priority.toLowerCase()">
        <div class="reco-header">
          <span class="priority-badge" :class="r.priority.toLowerCase()">{{ r.priority }}</span>
          <span class="reco-index">#{{ i + 1 }}</span>
        </div>
        <h3 class="reco-segment">{{ r.segment }}</h3>
        <div class="reco-action">
          <span class="action-label">ACTION</span>
          <p>{{ r.action }}</p>
        </div>
        <p class="reco-reason">{{ r.reason }}</p>
      </div>
    </div>
  </div>
</template>

<script>
export default { props: ['recommendations'] }
</script>

<style scoped>
.reco-section {}
.section-title { font-family: 'Syne', sans-serif; font-size: 20px; font-weight: 800; margin-bottom: 24px; }
.reco-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }

.reco-card { background: var(--surface); border: 1px solid var(--border); border-radius: 16px; padding: 24px; display: flex; flex-direction: column; gap: 14px; transition: transform 0.2s; }
.reco-card:hover { transform: translateY(-2px); }
.reco-card.high { border-left: 3px solid var(--high); }
.reco-card.medium { border-left: 3px solid var(--med); }

.reco-header { display: flex; justify-content: space-between; align-items: center; }
.priority-badge { font-size: 11px; font-weight: 700; padding: 4px 10px; border-radius: 20px; letter-spacing: 1px; }
.priority-badge.high { background: rgba(255,77,109,0.15); color: var(--high); }
.priority-badge.medium { background: rgba(255,209,102,0.15); color: var(--med); }
.reco-index { color: var(--text-muted); font-size: 12px; }

.reco-segment { font-family: 'Syne', sans-serif; font-size: 16px; font-weight: 700; }

.action-label { font-size: 10px; color: var(--accent); text-transform: uppercase; letter-spacing: 1.5px; display: block; margin-bottom: 4px; }
.reco-action p { font-size: 14px; color: var(--accent3); }

.reco-reason { font-size: 13px; color: var(--text-muted); line-height: 1.6; }
</style>