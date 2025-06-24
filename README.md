# 🛒 Wildberries Analytics Service

**Сервис для сбора и анализа данных о товарах с Wildberries**  
Получайте статистику, визуализируйте тенденции и находите лучшие предложения.

## 🚀 Быстрый старт

### Требования
- Docker 20.10+
- Docker Compose 2.0+
- 4GB свободной памяти

```bash
git clone https://github.com/yourrepo/wb-analytics.git
cd wb-analytics
docker-compose up --build
```

После запуска:
- Frontend: http://localhost:8080
- Backend API: http://localhost:8000
- PGAdmin: http://localhost:5050 (admin@admin.com / admin)

## Стек технологий
| Компонент    | Технологии                          |
|--------------|-------------------------------------|
| **Frontend** | Vue 3, Chart.js, Vite, Axios        |
| **Backend**  | FastAPI, SQLAlchemy, BeautifulSoup  |
| **Database** | PostgreSQL 13                       |
| **Infra**    | Docker, Nginx                       |


## 🛠 API Endpoints

### Основные методы

```http
POST /parse/
Content-Type: application/json

{
  "query": "ноутбуки"
}
```

```http
GET /api/products/?min_price=5000&min_rating=4
```

### Схемы данных

```python
class Product(BaseModel):
    id: int
    name: str
    price: float
    sale_price: float
    rating: float
    feedback_count: int
    query: str
```

## 📊 Особенности фронтенда

### Компоненты
1. ProductTable.vue - Таблица с сортировкой
2. PriceHistogram.vue - Распределение цен
3. DiscountRatingChart.vue - Анализ скидок

```javascript
// Пример работы с API
async fetchProducts() {
  const response = await axios.get('/api/products/', {
    params: {
      min_price: this.minPrice,
      max_price: this.maxPrice
    }
  })
  this.products = response.data
}
```

## 🐳 Деплой

### Production сборка
```bash
docker-compose -f docker-compose.prod.yml up --build -d
```

### Переменные окружения
.env.example:

```ini
DB_HOST=db
DB_PORT=5432
DB_NAME=wb_prod
DB_USER=wb_user
DB_PASSWORD=strongpassword
```

## 🔄 Жизненный цикл данных
Парсинг → 2. Очистка → 3. Анализ → 4. Визуализация