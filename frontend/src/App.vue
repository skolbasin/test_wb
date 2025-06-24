<template>
  <div class="container">
    <h1>Аналитика товаров Wildberries</h1>

    <div class="filters">
      <div class="filter-group">
        <label>Категория/запрос:</label>
        <input v-model="query" @change="fetchProducts" placeholder="Введите запрос">
      </div>

      <div class="filter-group">
        <label>Диапазон цен:</label>
        <div class="slider-container">
          <input type="range" v-model="minPrice" :min="priceRange.min" :max="priceRange.max" @input="fetchProducts">
          <span>{{ minPrice.toLocaleString() }} ₽</span>
          <span>—</span>
          <input type="range" v-model="maxPrice" :min="priceRange.min" :max="priceRange.max" @input="fetchProducts">
          <span>{{ maxPrice.toLocaleString() }} ₽</span>
        </div>
      </div>

      <div class="filter-group">
        <label>Минимальный рейтинг:</label>
        <input type="number" v-model="minRating" min="0" max="5" step="0.1" @change="fetchProducts">
      </div>

      <div class="filter-group">
        <label>Минимальное количество отзывов:</label>
        <input type="number" v-model="minFeedback" min="0" @change="fetchProducts">
      </div>

      <button @click="parseProducts">Парсить товары</button>
    </div>

    <ProductTable :products="filteredProducts" />

    <div class="charts">
      <PriceHistogram :products="filteredProducts" />
      <DiscountRatingChart :products="filteredProducts" />
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import ProductTable from './components/ProductTable.vue'
import PriceHistogram from './components/PriceHistogram.vue'
import DiscountRatingChart from './components/DiscountRatingChart.vue'

export default {
  components: {
    ProductTable,
    PriceHistogram,
    DiscountRatingChart
  },
  data() {
    return {
      query: '',
      minPrice: 0,
      maxPrice: 100000,
      minRating: 0,
      minFeedback: 0,
      allProducts: [],
      priceRange: {
        min: 0,
        max: 100000
      }
    }
  },
  computed: {
    filteredProducts() {
      return this.allProducts.filter(product => {
        return product.price >= this.minPrice &&
               product.price <= this.maxPrice &&
               product.rating >= this.minRating &&
               product.feedback_count >= this.minFeedback
      })
    }
  },
  methods: {
    async fetchProducts() {
      try {
        const params = {
          min_price: this.minPrice,
          max_price: this.maxPrice,
          min_rating: this.minRating,
          min_feedback: this.minFeedback,
          query: this.query
        }

        const response = await axios.get('http://localhost:8000/api/products/', { params })
        this.allProducts = response.data

        // Обновляем диапазон цен
        if (this.allProducts.length) {
          const prices = this.allProducts.map(p => p.price)
          this.priceRange = {
            min: Math.floor(Math.min(...prices)),
            max: Math.ceil(Math.max(...prices))
          }
          this.minPrice = this.priceRange.min
          this.maxPrice = this.priceRange.max
        }
      } catch (error) {
        console.error('Error fetching products:', error)
      }
    },
    async parseProducts() {
      if (!this.query) {
        alert('Введите запрос для парсинга')
        return
      }

      try {
        await axios.post('http://localhost:8000/parse/', { query: this.query })
        this.fetchProducts()
        alert('Парсинг завершен успешно')
      } catch (error) {
        console.error('Error parsing products:', error)
        alert('Ошибка при парсинге товаров')
      }
    }
  },
  mounted() {
    this.fetchProducts()
  }
}
</script>