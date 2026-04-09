<template>
  <div class="charts">
    <div v-if="data.spend_by_category" class="chart-card">
      <h3 class="chart-title">Revenue by {{ data.spend_by_category.category_col }}</h3>
      <v-chart :option="barOption" style="height:320px" autoresize />
    </div>
    <div v-if="data.age_distribution" class="chart-card">
      <h3 class="chart-title">Customer Age Distribution</h3>
      <v-chart :option="pieOption" style="height:320px" autoresize />
    </div>
    <div v-if="data.top_customers" class="chart-card full">
      <h3 class="chart-title">Top 10 Customers by Spend</h3>
      <table class="data-table">
        <thead>
          <tr>
            <th v-for="key in Object.keys(data.top_customers[0])" :key="key">{{ key }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, i) in data.top_customers" :key="i">
            <td v-for="key in Object.keys(row)" :key="key">{{ row[key] }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  props: ['data'],
  computed: {
    barOption() {
      const d = this.data.spend_by_category
      return {
        backgroundColor: 'transparent',
        tooltip: { trigger: 'axis', backgroundColor: '#1a1a24', borderColor: '#2a2a3a', textStyle: { color: '#e8e8f0' } },
        xAxis: { type: 'category', data: d.labels, axisLabel: { color: '#6b6b80', rotate: 30 }, axisLine: { lineStyle: { color: '#2a2a3a' } } },
        yAxis: { type: 'value', axisLabel: { color: '#6b6b80' }, splitLine: { lineStyle: { color: '#1a1a24' } } },
        series: [{ data: d.values, type: 'bar', itemStyle: { color: '#7c6fff', borderRadius: [6, 6, 0, 0] }, emphasis: { itemStyle: { color: '#9b8fff' } } }]
      }
    },
    pieOption() {
      const d = this.data.age_distribution
      const colors = ['#7c6fff', '#ff6b9d', '#00d9c0', '#ffd166', '#ff4d6d', '#a8ff78']
      return {
        backgroundColor: 'transparent',
        tooltip: { trigger: 'item', backgroundColor: '#1a1a24', borderColor: '#2a2a3a', textStyle: { color: '#e8e8f0' } },
        legend: { orient: 'vertical', right: 10, textStyle: { color: '#6b6b80' } },
        series: [{
          type: 'pie', radius: ['40%', '70%'], center: ['40%', '50%'],
          data: d.labels.map((l, i) => ({ name: l, value: d.values[i], itemStyle: { color: colors[i % colors.length] } })),
          label: { color: '#e8e8f0' }, emphasis: { itemStyle: { shadowBlur: 10, shadowColor: 'rgba(124,111,255,0.5)' } }
        }]
      }
    }
  }
}
</script>

<style scoped>
.charts { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
.chart-card { background: var(--surface); border: 1px solid var(--border); border-radius: 16px; padding: 24px; }
.chart-card.full { grid-column: 1 / -1; }
.chart-title { font-family: 'Syne', sans-serif; font-size: 14px; font-weight: 700; color: var(--text-muted); text-transform: uppercase; letter-spacing: 1px; margin-bottom: 20px; }

.data-table { width: 100%; border-collapse: collapse; font-size: 13px; }
.data-table th { color: var(--text-muted); text-align: left; padding: 10px 16px; border-bottom: 1px solid var(--border); text-transform: uppercase; font-size: 11px; letter-spacing: 1px; }
.data-table td { padding: 12px 16px; border-bottom: 1px solid #16161e; color: var(--text); }
.data-table tr:hover td { background: var(--surface2); }
</style>