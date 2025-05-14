from typing import Any
import pytest
from src.main import Category, Product, Smartphone, LawnGrass


@pytest.fixture
def test_product() -> Product:
    return Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)


@pytest.fixture
def test_smartphone() -> Smartphone:
    return Smartphone("iPhone 14 Pro", "256GB, Черный", 120000.0, 3, 2.5, "14 Pro", 256, "Black")


@pytest.fixture
def test_smartphone2() -> Smartphone:
    return Smartphone("Samsung S22", "128GB, Белый", 80000.0, 2, 2.0, "S22", 128, "White")


@pytest.fixture
def test_lawn_grass() -> LawnGrass:
    return LawnGrass("Green Lawn", "Газонная трава", 500.0, 100, "Russia", "7 days", "Green")


@pytest.fixture
def test_category() -> Category:
    product = Product('55" QLED 4K', "Фоновая подсветка", 123000.0, 7)
    category = Category(
        "Телевизоры",
        "Современный телевизор, который позволяет наслаждаться просмотром, станет вашим другом и помощником",
        [product],
    )
    return category


def test_product_init(test_product: Product) -> None:
    assert test_product.name == "Samsung Galaxy S23 Ultra"
    assert test_product.description == "256GB, Серый цвет, 200MP камера"
    assert test_product.price == 180000.0
    assert test_product.quantity == 5


def test_smartphone_init(test_smartphone: Smartphone) -> None:
    assert test_smartphone.name == "iPhone 14 Pro"
    assert test_smartphone.description == "256GB, Черный"
    assert test_smartphone.price == 120000.0
    assert test_smartphone.quantity == 3
    assert test_smartphone.efficiency == 2.5
    assert test_smartphone.model == "14 Pro"
    assert test_smartphone.memory == 256
    assert test_smartphone.color == "Black"


def test_lawn_grass_init(test_lawn_grass: LawnGrass) -> None:
    assert test_lawn_grass.name == "Green Lawn"
    assert test_lawn_grass.description == "Газонная трава"
    assert test_lawn_grass.price == 500.0
    assert test_lawn_grass.quantity == 100
    assert test_lawn_grass.country == "Russia"
    assert test_lawn_grass.germination_period == "7 days"
    assert test_lawn_grass.color == "Green"


def test_category_init(test_category: Category) -> None:
    assert test_category.name == "Телевизоры"
    assert (
        test_category.description
        == "Современный телевизор, который позволяет наслаждаться просмотром, станет вашим другом и помощником"
    )
    assert Category.category_count == 1
    assert Category.product_count == 1


def test_add_product(test_category: Category, test_smartphone: Smartphone) -> None:
    initial_count = Category.product_count
    test_category.add_product(test_smartphone)
    assert Category.product_count == initial_count + 1
    assert "iPhone 14 Pro, 120000.0 руб. Остаток: 3 шт." in test_category.products


def test_add_invalid_product(test_category: Category) -> None:
    with pytest.raises(TypeError, match="Можно добавлять только объекты класса Product или его наследников"):
        test_category.add_product("Invalid product")


def test_products_getter(test_category: Category) -> None:
    expected = '55" QLED 4K, 123000.0 руб. Остаток: 7 шт.'
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


def test_new_product_different_class() -> None:
    product_data = {
        "name": "iPhone 14 Pro",
        "description": "256GB, Черный",
        "price": 130000.0,
        "quantity": 5
    }
    existing = [Smartphone("iPhone 14 Pro", "256GB, Черный", 120000.0, 3, 2.5, "14 Pro", 256, "Black")]
    product = Product.new_product(product_data, existing)
    assert product.quantity == 5  # Новый продукт, так как классы разные
    assert product.price == 130000.0


def test_price_setter(test_product: Product, monkeypatch) -> None:
    # Тестируем повышение цены
    test_product.price = 200000.0
    assert test_product.price == 200000.0

    # Тестируем нулевую или отрицательную цену
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


def test_product_str(test_product: Product) -> None:
    assert str(test_product) == "Samsung Galaxy S23 Ultra, 180000.0 руб. Остаток: 5 шт."


def test_category_str(test_category: Category) -> None:
    assert str(test_category) == "Телевизоры, количество продуктов: 7 шт."


def test_product_add_same_class(test_smartphone: Smartphone, test_smartphone2: Smartphone) -> None:
    assert test_smartphone + test_smartphone2 == (120000.0 * 3 + 80000.0 * 2)


def test_product_add_different_class(test_smartphone: Smartphone, test_lawn_grass: LawnGrass) -> None:
    with pytest.raises(TypeError, match="Можно складывать только объекты одного класса Product"):
        test_smartphone + test_lawn_grass


def test_category_iterator(test_category: Category) -> None:
    products = list(test_category)
    assert len(products) == 1
    assert products[0].name == '55" QLED 4K'
