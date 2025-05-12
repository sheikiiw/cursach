from typing import Any
import pytest
from src.main import Category, Product


@pytest.fixture
def test_product() -> Product:
    return Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)


def test_product_init(test_product: Product) -> None:
    assert test_product.name == "Samsung Galaxy S23 Ultra"
    assert test_product.description == "256GB, Серый цвет, 200MP камера"
    assert test_product.price == 180000.0
    assert test_product.quantity == 5


@pytest.fixture
def test_category() -> Category:
    product = Product('55" QLED 4K', "Фоновая подсветка", 123000.0, 7)
    category = Category(
        "Телевизоры",
        "Современный телевизор, который позволяет наслаждаться просмотром, станет вашим другом и помощником",
        [product],
    )
    return category


def test_category_init(test_category: Category) -> None:
    assert test_category.name == "Телевизоры"
    assert (
        test_category.description
        == "Современный телевизор, который позволяет наслаждаться просмотром, станет вашим другом и помощником"
    )
    assert Category.category_count == 1
    assert Category.product_count == 1


def test_add_product(test_category: Category, test_product: Product) -> None:
    initial_count = Category.product_count
    test_category.add_product(test_product)
    assert Category.product_count == initial_count + 1
    assert "Samsung Galaxy S23 Ultra, 180000.0 руб. Остаток: 5 шт.\n" in test_category.products


def test_products_getter(test_category: Category) -> None:
    expected = "55\" QLED 4K, 123000.0 руб. Остаток: 7 шт.\n"
    assert test_category.products == expected


def test_new_product() -> None:
    product_data = {
        "name": "Phone",
        "description": "Smartphone",
        "price": 50000.0,
        "quantity": 20
    }
    product = Product.new_product(product_data)
    assert product.name == "Phone"
    assert product.description == "Smartphone"
    assert product.price == 50000.0
    assert product.quantity == 20


def test_new_product_duplicate() -> None:
    product_data = {
        "name": "Phone",
        "description": "Smartphone",
        "price": 60000.0,
        "quantity": 10
    }
    existing = [Product("Phone", "Smartphone", 50000.0, 20)]
    product = Product.new_product(product_data, existing)
    assert product.quantity == 30
    assert product.price == 60000.0


def test_price_setter(test_product: Product, monkeypatch) -> None:
    # Тестируем повышение цены
    test_product.price = 200000.0
    assert test_product.price == 200000.0

    # Тестируем нулевую или отрицательную цену
    with pytest.raises(SystemExit):  # Для имитации print в тестах
        test_product.price = -100.0
    assert test_product.price == 200000.0  # Цена не изменилась

    # Тестируем снижение цены с подтверждением
    monkeypatch.setattr("builtins.input", lambda _: "y")
    test_product.price = 150000.0
    assert test_product.price == 150000.0

    # Тестируем снижение цены с отказом
    monkeypatch.setattr("builtins.input", lambda _: "n")
    test_product.price = 100000.0
    assert test_product.price == 150000.0  # Цена не изменилась