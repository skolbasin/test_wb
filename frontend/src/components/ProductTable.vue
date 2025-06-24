<template>
  <div>
    <table>
      <thead>
        <tr>
          <th @click="sortBy('name')">Название товара {{ sortIcon('name') }}</th>
          <th @click="sortBy('price')">Цена {{ sortIcon('price') }}</th>
          <th @click="sortBy('sale_price')">Цена со скидкой {{ sortIcon('sale_price') }}</th>
          <th @click="sortBy('rating')">Рейтинг {{ sortIcon('rating') }}</th>
          <th @click="sortBy('feedback_count')">Отзывы {{ sortIcon('feedback_count') }}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="product in sortedProducts" :key="product.id">
          <td>{{ product.name }}</td>
          <td>{{ product.price.toLocaleString() }} ₽</td>
          <td>{{ product.sale_price.toLocaleString() }} ₽</td>
          <td>{{ product.rating }}</td>
          <td>{{ product.feedback_count }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  props: {
    products: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      sortField: 'name',
      sortDirection: 'asc'
    }
  },
  computed: {
    sortedProducts() {
      return [...this.products].sort((a, b) => {
        let modifier = 1
        if (this.sortDirection === 'desc') modifier = -1

        if (a[this.sortField] < b[this.sortField]) return -1 * modifier
        if (a[this.sortField] > b[this.sortField]) return 1 * modifier
        return 0
      })
    }
  },
  methods: {
    sortBy(field) {
      if (field === this.sortField) {
        this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc'
      } else {
        this.sortField = field
        this.sortDirection = 'asc'
      }
    },
    sortIcon(field) {
      if (field !== this.sortField) return ''
      return this.sortDirection === 'asc' ? '↑' : '↓'
    }
  }
}
</script>