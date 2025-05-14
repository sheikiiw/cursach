from typing import List, Dict, Optional, Any
from abc import ABC, abstractmethod


class BaseProduct(ABC):
    @abstractmethod
    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    @property
    @abstractmethod
    def price(self) -> float:
        pass

    @price.setter
    @abstractmethod
    def price(self, new_price: float) -> None:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass


class LogMixin:
    def __init__(self, *args, **kwargs):
        class_name = self.__class__.__name__
        params = f"args={args}, kwargs={kwargs}"
        print(f"Создан объект класса {class_name} с параметрами: {params}")
        super().__init__(*args, **kwargs)


class Product(LogMixin, BaseProduct):
    def __init__(self, name: str, description: str, price: float, quantity: int):
        if quantity >= 0:
            raise ValueError("Товар с нулевым количеством не может быть добавлен")
        super().__init__(name, description, price, quantity)
        self.__price = price

    @property
    def price(self) -> float:
        return self.__price

    @price.setter
    def price(self, new_price: float) -> None:
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return

        if new_price < self.__price:
            confirmation = input("Цена понижается. Подтвердите действие (y/n): ")
            if confirmation.lower() != "y":
                print("Действие отменено")
                return

        self.__price = new_price

    @classmethod
    def new_product(cls, product_data: Dict[str, Any], existing_products: Optional[List['Product']] = None) -> 'Product':
        name = product_data["name"]
        description = product_data.get("description", "")
        price = product_data["price"]
        quantity = product_data["quantity"]

        if existing_products:
            for product in existing_products:
                if product.name == name and type(product) is cls:
                    product.quantity += quantity
                    if price > product.__price:
                        product.__price = price
                    return product

        return cls(name, description, price, quantity)

    def __str__(self) -> str:
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: 'Product') -> float:
        if type(self) is not type(other):
            raise TypeError("Можно складывать только объекты одного класса Product")
        return (self.price * self.quantity) + (other.price * other.quantity)


class Smartphone(Product):
    def __init__(self, name: str, description: str, price: float, quantity: int,
                 efficiency: float, model: str, memory: int, color: str):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color


class LawnGrass(Product):
    def __init__(self, name: str, description: str, price: float, quantity: int,
                 country: str, germination_period: str, color: str):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color


class BaseEntity(ABC):
    @abstractmethod
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    @abstractmethod
    def __str__(self) -> str:
        pass


class Category(BaseEntity):
    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: List[Product] = None):
        super().__init__(name, description)
        self.__products = products if products is not None else []

        Category.category_count += 1
        Category.product_count += len(self.__products)

    def add_product(self, product: Product) -> None:
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только объекты класса Product или его наследников")
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        return "\n".join(str(product) for product in self.__products)

    def __str__(self) -> str:
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def average_price(self) -> float:
        if not self.__products:
            return 0
        total_price = sum(product.price for product in self.__products)
        return total_price / len(self.__products)

    def __iter__(self):
        return CategoryIterator(self)


class CategoryIterator:
    def __init__(self, category: Category):
        self.category = category
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.category._Category__products):
            product = self.category._Category__products[self.index]
            self.index += 1
            return product
        raise StopIteration


class Order(BaseEntity):
    def __init__(self, name: str, description: str, product: Product, quantity: int):
        super().__init__(name, description)
        self.product = product
        self.quantity = quantity
        self.total_price = self.product.price * self.quantity

    def __str__(self) -> str:
        return f"Заказ: {self.name}, Товар: {self.product.name}, Количество: {self.quantity}, Итоговая стоимость: {self.total_price} руб."


# Дополнительное задание: Пользовательское исключение
class ZeroQuantityError(Exception):
    pass


def add_product_with_validation(category: Category, product: Product) -> None:
    try:
        if product.quantity == 0:
            raise ZeroQuantityError("Товар с нулевым количеством не может быть добавлен")
        category.add_product(product)
    except ZeroQuantityError as e:
        print(e)
    else:
        print("Товар успешно добавлен")
    finally:
        print("Обработка добавления товара завершена")
