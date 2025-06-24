import requests
from bs4 import BeautifulSoup
from typing import List
from ..schemas import ProductCreate


def parse_wildberries(query: str) -> List[ProductCreate]:
    url = f"https://www.wildberries.ru/catalog/0/search.aspx?search={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    products = []
    items = soup.find_all('div', class_='product-card')

    for item in items:
        try:
            name = item.find('span', class_='goods-name').text.strip()
            price = float(
                item.find('span', class_='price-commission__current-price').text.strip().replace('₽', '').replace(' ',
                                                                                                                  ''))

            old_price_elem = item.find('del', class_='price-commission__old-price')
            sale_price = float(
                old_price_elem.text.strip().replace('₽', '').replace(' ', '')) if old_price_elem else price

            rating_elem = item.find('span', class_='address-rate-mini')
            rating = float(rating_elem.text.strip()) if rating_elem else 0.0

            feedback_elem = item.find('span', class_='product-card__count')
            feedback_count = int(
                feedback_elem.text.strip().replace('отзывов', '').replace('отзыв', '').strip()) if feedback_elem else 0

            products.append(ProductCreate(
                name=name,
                price=price,
                sale_price=sale_price,
                rating=rating,
                feedback_count=feedback_count,
                query=query
            ))
        except Exception as e:
            print(f"Error parsing product: {e}")
            continue

    return products