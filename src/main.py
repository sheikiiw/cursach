from typing import List, Dict, Optional, Any


class Product:
    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.__price = price  # Приватный атрибут цены
        self.quantity = quantity

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
    def new_product(cls, product_data: Dict[str, Any],
                    existing_products: Optional[List['Product']] = None) -> 'Product':
        name = product_data["name"]
        description = product_data.get("description", "")
        price = product_data["price"]
        quantity = product_data["quantity"]

        if existing_products:
            for product in existing_products:
                if product.name == name and type(product) is cls:  # Убедитесь, что отступы — 4 пробела
                    product.quantity += quantity
                    if price > product.__price:
                        product.__price = price
                    return product

        return cls(name, description, price, quantity)


class LawnGrass:
    pass