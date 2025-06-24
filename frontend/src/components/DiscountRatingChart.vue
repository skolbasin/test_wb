<template>
  <div class="chart-container">
    <canvas ref="chart"></canvas>
  </div>
</template>

<script>
import { Line } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement } from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement)

export default {
  extends: Line,
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
            text: 'Зависимость скидки от рейтинга'
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            title: {
              display: true,
              text: 'Размер скидки (%)'
            }
          },
          x: {
            title: {
              display: true,
              text: 'Рейтинг товара'
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

      // Группируем по рейтингу (округленному до 0.5)
      const ratingGroups = {}

      this.products.forEach(product => {
        if (product.sale_price >= product.price) return // нет скидки

        const discount = ((product.price - product.sale_price) / product.price) * 100
        const roundedRating = Math.round(product.rating * 2) / 2

        if (!ratingGroups[roundedRating]) {
          ratingGroups[roundedRating] = []
        }

        ratingGroups[roundedRating].push(discount)
      })

      const labels = Object.keys(ratingGroups).sort()
      const data = labels.map(rating => {
        const discounts = ratingGroups[rating]
        return discounts.reduce((a, b) => a + b, 0) / discounts.length
      })

      this.renderChart({
        labels,
        datasets: [{
          label: 'Средняя скидка',
          backgroundColor: '#4e73df',
          borderColor: '#4e73df',
          data,
          tension: 0.1
        }]
      }, this.chartOptions)
    }
  }
}
</script>