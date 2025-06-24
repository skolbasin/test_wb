<template>
  <div class="chart-container">
    <canvas ref="chart"></canvas>
  </div>
</template>

<script>
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

export default {
  extends: Bar,
  props: {
    products: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      chartData: null,
      chartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          title: {
            display: true,
            text: 'Распределение цен товаров'
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            title: {
              display: true,
              text: 'Количество товаров'
            }
          },
          x: {
            title: {
              display: true,
              text: 'Диапазон цен (₽)'
            }
          }
        }
      }
    }
  },
  watch: {
    products: {
      handler: 'updateChart',
      deep: true
    }
  },
  mounted() {
    this.updateChart()
  },
  methods: {
    updateChart() {
      if (!this.products.length) return

      const prices = this.products.map(p => p.price)
      const maxPrice = Math.max(...prices)
      const step = Math.ceil(maxPrice / 10)

      const labels = []
      const data = []

      for (let i = 0; i < 10; i++) {
        const min = i * step
        const max = (i + 1) * step
        labels.push(`${min.toLocaleString()} - ${max.toLocaleString()}`)
        data.push(this.products.filter(p => p.price >= min && p.price < max).length)
      }

      this.renderChart({
        labels,
        datasets: [{
          label: 'Количество товаров',
          backgroundColor: '#4e73df',
          data
        }]
      }, this.chartOptions)
    }
  }
}
</script>