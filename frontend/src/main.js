import { createApp } from 'vue'
import ECharts from 'vue-echarts'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { BarChart, PieChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, LegendComponent, TitleComponent } from 'echarts/components'
import App from './App.vue'

use([CanvasRenderer, BarChart, PieChart, GridComponent, TooltipComponent, LegendComponent, TitleComponent])

const app = createApp(App)
app.component('v-chart', ECharts)
app.mount('#app')