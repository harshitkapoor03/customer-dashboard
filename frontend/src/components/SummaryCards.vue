<template>
  <div class="cards">
    <div class="card">
      <p class="card-label">Total Customers</p>
      <p class="card-value">{{ summary.total_customers?.toLocaleString() }}</p>
    </div>
    <div class="card">
      <p class="card-label">Total Revenue</p>
      <p class="card-value accent2">${{ summary.total_revenue?.toLocaleString() }}</p>
    </div>
    <div class="card">
      <p class="card-label">Avg Spend / Customer</p>
      <p class="card-value accent3">${{ summary.avg_spend?.toLocaleString() }}</p>
    </div>
    <div class="card">
      <p class="card-label">Columns Detected</p>
      <p class="card-value" style="font-size:14px">{{ summary.columns_detected?.join(', ') }}</p>
    </div>
  </div>
</template>

<script>
export default { props: ['summary'] }
</script>

<style scoped>
.cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; }
.card { background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 24px; }
.card-label { color: var(--text-muted); font-size: 11px; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px; }
.card-value { font-family: 'Syne', sans-serif; font-size: 26px; font-weight: 800; color: var(--text); }
.card-value.accent2 { color: var(--accent2); }
.card-value.accent3 { color: var(--accent3); }
</style>