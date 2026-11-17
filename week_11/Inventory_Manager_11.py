from __future__ import annotations

import json
import math
from abc import ABC, abstractmethod
from pathlib import Path

DATA_FILE = Path(__file__).resolve().with_name("inventory.json")


def validate_number(value: int | float, label: str, whole_number: bool = False) -> int | float:
    if whole_number:
        valid = type(value) is int and value >= 0
    else:
        valid = type(value) in (int, float) and math.isfinite(value) and value >= 0
    if not valid:
        kind = "whole number" if whole_number else "finite number"
        raise ValueError(f"{label} must be a non-negative {kind}.")
    return value


class Supplier:

    def __init__(self, supplier_id: str, name: str, contact_email: str) -> None:
        if not supplier_id.strip() or not name.strip() or not contact_email.strip():
            raise ValueError("Supplier fields cannot be blank.")
        self.supplier_id: str = supplier_id.strip()
        self.name: str = name.strip()
        self.contact_email: str = contact_email.strip()

    def display_information(self) -> None:
        print(f"Supplier: {self.name} ({self.supplier_id}) | Email: {self.contact_email}")


class Product(ABC):

    def __init__(self, product_id: str, name: str, price: float,
                 stock: int, supplier: Supplier) -> None:
        if not product_id.strip() or not name.strip():
            raise ValueError("Product ID and name cannot be empty.")
        if not isinstance(supplier, Supplier):
            raise TypeError("supplier must be a Supplier object.")
        self.__product_id: str = product_id.strip().upper()
        self.__name: str = name.strip()
        self.__price: float = float(validate_number(price, "Price"))
        self.supplier: Supplier = supplier
        self.__stock: int = 0
        self.update_stock(stock)

    @property
    def product_id(self) -> str:
        return self.__product_id

    @property
    def price(self) -> float:
        return self.__price

    def get_product_id(self) -> str:
        return self.__product_id

    def get_stock(self) -> int:
        return self.__stock

    def update_stock(self, quantity: int) -> None:
        self.__stock = int(validate_number(quantity, "Stock", whole_number=True))

    def display_information(self) -> None:
        print(f"ID: {self.__product_id} | Name: {self.__name} | "
              f"Price: ${self.__price:.2f} | Stock: {self.__stock}")
        self.supplier.display_information()

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        pass

    def to_dict(self) -> dict:
        return {"id": self.__product_id, "name": self.__name,
                "price": self.__price, "stock": self.__stock,
                "supplier": {"supplier_id": self.supplier.supplier_id,
                             "name": self.supplier.name,
                             "contact_email": self.supplier.contact_email}}


class CanBeShipped(ABC):
    @abstractmethod
    def calculate_shipping_cost(self) -> float:
        pass


class PhysicalProduct(Product, CanBeShipped):
    def __init__(self, product_id: str, name: str, price: float,
                 stock: int, weight: float, supplier: Supplier) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        self.__weight: float = float(validate_number(weight, "Weight"))

    def display_information(self) -> None:
        super().display_information()
        print(f"  Type: Physical | Weight: {self.__weight} kg")
        print(f"  Delivery: {self.get_fulfilment_info()}")
        print(f"  Shipping Cost: ${self.calculate_shipping_cost():.2f}")

    def get_fulfilment_info(self) -> str:
        return "Requires physical shipping."

    def calculate_shipping_cost(self) -> float:
        return self.__weight * 2.0

    def to_dict(self) -> dict:
        data = super().to_dict()
        data.update({"type": "physical", "weight": self.__weight})
        return data


class DigitalProduct(Product):
    def __init__(self, product_id: str, name: str, price: float,
                 stock: int, download_size: float, supplier: Supplier) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        self.__download_size: float = float(validate_number(download_size, "Download size"))

    def display_information(self) -> None:
        super().display_information()
        print(f"  Type: Digital | Download Size: {self.__download_size} MB")
        print(f"  Delivery: {self.get_fulfilment_info()}")

    def get_fulfilment_info(self) -> str:
        return "Delivered digitally through a download."

    def to_dict(self) -> dict:
        data = super().to_dict()
        data.update({"type": "digital", "download_size": self.__download_size})
        return data


class Inventory:

    def __init__(self) -> None:
        self.products: list[Product] = []

    def add_product(self, product: Product) -> bool:
        if not isinstance(product, Product):
            raise TypeError("Inventory accepts Product objects only.")
        if self.find_product(product.product_id) is not None:
            return False
        self.products.append(product)
        return True

    def remove_product(self, product_id: str) -> bool:
        product = self.find_product(product_id)
        if product is None:
            return False
        self.products.remove(product)
        return True

    def find_product(self, product_id: str) -> Product | None:
        for product in self.products:
            if product.product_id == product_id.strip().upper():
                return product
        return None

    def search_product(self, product_id: str) -> Product | None:
        return self.find_product(product_id)

    def display_all(self) -> None:
        if not self.products:
            print("No products in inventory.")
        for product in self.products:
            product.display_information()
            print("-" * 60)

    def display_all_products(self) -> None:
        self.display_all()

    def to_list(self) -> list[dict]:
        return [product.to_dict() for product in self.products]


class OrderLine:

    def __init__(self, product: Product, quantity: int) -> None:
        if not isinstance(product, Product):
            raise TypeError("Order lines require a Product.")
        if type(quantity) is not int or quantity <= 0:
            raise ValueError("Order quantity must be a positive whole number.")
        self.product: Product = product
        self.quantity: int = quantity

    def calculate_subtotal(self) -> float:
        return self.product.price * self.quantity


class Order:

    def __init__(self, order_id: str) -> None:
        if not order_id.strip():
            raise ValueError("Order ID cannot be blank.")
        self.order_id: str = order_id
        self.order_lines: list[OrderLine] = []

    def add_order_line(self, product: Product, quantity: int) -> None:
        self.order_lines.append(OrderLine(product, quantity))

    def remove_order_line(self, index: int) -> None:
        self.order_lines.pop(index)

    def calculate_total(self) -> float:
        return sum(line.calculate_subtotal() for line in self.order_lines)

    def display_order(self) -> None:
        print(f"Order {self.order_id}")
        for line in self.order_lines:
            print(f"  {line.product.product_id} x {line.quantity}: ${line.calculate_subtotal():.2f}")
        print(f"Total: ${self.calculate_total():.2f}")


def load_inventory(filename: Path = DATA_FILE) -> Inventory:
    inventory = Inventory()
    try:
        with open(filename, "r", encoding="utf-8") as file:
            saved_products = json.load(file)
    except FileNotFoundError:
        print("No inventory file found. Starting empty.")
        return inventory
    if not isinstance(saved_products, list):
        raise ValueError("Inventory data must be a list.")
    # Cache suppliers by ID so multiple saved products share the same supplier object.
    suppliers: dict[str, Supplier] = {}
    for item in saved_products:
        if not isinstance(item, dict):
            raise ValueError("Each saved product must be an object.")
        details = item.get("supplier") or {
            "supplier_id": "LEGACY", "name": "Unassigned Supplier",
            "contact_email": "unassigned@example.com"}
        supplier_id = details["supplier_id"]
        if supplier_id not in suppliers:
            suppliers[supplier_id] = Supplier(**details)
        supplier = suppliers[supplier_id]
        common = (item["id"], item["name"], item["price"], item["stock"])
        if item["type"] == "physical":
            product = PhysicalProduct(*common, item["weight"], supplier)
        elif item["type"] == "digital":
            product = DigitalProduct(*common, item["download_size"], supplier)
        else:
            raise ValueError(f"Unknown product type: {item['type']}")
        if not inventory.add_product(product):
            raise ValueError(f"Duplicate product ID: {item['id']}")
    print("Inventory loaded successfully.")
    return inventory


def save_inventory(inventory: Inventory, filename: Path = DATA_FILE) -> bool:
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(inventory.to_list(), file, indent=4, allow_nan=False)
        print("Inventory saved successfully.")
        return True
    except (OSError, ValueError) as error:
        print(f"Could not save inventory: {error}")
        return False


def get_number(prompt: str, whole_number: bool = False) -> int | float:
    while True:
        try:
            number = int(input(prompt)) if whole_number else float(input(prompt))
            return validate_number(number, "Value", whole_number)
        except ValueError as error:
            print(f"Invalid input: {error}")


def add_product(inventory: Inventory) -> None:
    print("\n1. Physical Product\n2. Digital Product")
    product_type = input("Choose product type: ").strip()
    if product_type not in ("1", "2"):
        print("Please choose 1 or 2.")
        return
    product_id = input("Product ID: ").strip().upper()
    if not product_id or inventory.search_product(product_id) is not None:
        print("Product ID missing or already exists.")
        return
    name = input("Product Name: ").strip()
    if not name:
        print("Product name cannot be empty.")
        return
    price = get_number("Price: ")
    stock = get_number("Stock Quantity: ", whole_number=True)
    supplier = Supplier(input("Supplier ID: "), input("Supplier Name: "), input("Supplier Email: "))
    if product_type == "1":
        weight = get_number("Weight (kg): ")
        product = PhysicalProduct(product_id, name, float(price), int(stock), float(weight), supplier)
    else:
        size = get_number("Download Size (MB): ")
        product = DigitalProduct(product_id, name, float(price), int(stock), float(size), supplier)
    inventory.add_product(product)
    print("Product added successfully.")


def update_stock(inventory: Inventory) -> None:
    product = inventory.search_product(input("Product ID: "))
    if product is None:
        print("Product not found.")
    else:
        print("Current Stock:", product.get_stock())
        product.update_stock(int(get_number("New Stock Quantity: ", whole_number=True)))
        print("Stock updated successfully.")


def search_product(inventory: Inventory) -> None:
    product = inventory.search_product(input("Product ID: "))
    if product is None:
        print("Product not found.")
    else:
        product.display_information()


def main() -> None:
    print("INVENTORY MANAGEMENT SYSTEM - LAB 8")
    try:
        inventory = load_inventory()
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"Could not load inventory data: {error}")
        return
    while True:
        print("\n1. Display All Products\n2. Add Product\n3. Update Stock")
        print("4. Search Product\n5. Save Inventory\n6. Exit")
        option = input("Enter option: ").strip()
        if option == "1":
            inventory.display_all()
        elif option == "2":
            add_product(inventory)
        elif option == "3":
            update_stock(inventory)
        elif option == "4":
            search_product(inventory)
        elif option == "5":
            save_inventory(inventory)
        elif option == "6":
            if save_inventory(inventory):
                print("Goodbye!")
                break
        else:
            print("Please choose 1 to 6.")


if __name__ == "__main__":
    main()
