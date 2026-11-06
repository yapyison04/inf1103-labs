"""INF1103 Lab 7: inheritance, overriding, abstraction and interfaces."""
import json
import math
from abc import ABC, abstractmethod
from pathlib import Path

# Keep data beside this script, even when launched from the repository root.
DATA_FILE = Path(__file__).resolve().with_name("inventory.json")


def validate_number(value, label, whole_number=False):
    if whole_number:
        valid = type(value) is int and value >= 0
    else:
        valid = type(value) in (int, float) and math.isfinite(value) and value >= 0
    if not valid:
        kind = "whole number" if whole_number else "finite number"
        raise ValueError(f"{label} must be a non-negative {kind}.")
    return value


class Product(ABC):
    """Abstract parent holding common product information and behaviour."""

    def __init__(self, product_id, name, price, stock):
        if not isinstance(product_id, str) or not product_id.strip():
            raise ValueError("Product ID cannot be empty.")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Product name cannot be empty.")
        self.__product_id = product_id.strip().upper()
        self.__name = name.strip()
        self.__price = validate_number(price, "Price")
        self.update_stock(stock)

    def get_product_id(self):
        return self.__product_id

    def get_stock(self):
        return self.__stock

    def update_stock(self, quantity):
        self.__stock = validate_number(quantity, "Stock", whole_number=True)

    def display_information(self):
        print(f"ID: {self.__product_id} | Name: {self.__name} | "
              f"Price: ${self.__price:.2f} | Stock: {self.__stock}")

    @abstractmethod
    def get_fulfilment_info(self):
        pass

    def to_dict(self):
        return {"id": self.__product_id, "name": self.__name,
                "price": self.__price, "stock": self.__stock}


class CanBeShipped(ABC):
    """Interface-style ABC: defines a contract, not product behaviour."""

    @abstractmethod
    def calculate_shipping_cost(self):
        pass


class PhysicalProduct(Product, CanBeShipped):
    """One product parent plus an interface-style ABC."""

    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)
        self.__weight = validate_number(weight, "Weight")

    def display_information(self):
        super().display_information()
        print(f"  Type: Physical | Weight: {self.__weight} kg")
        print(f"  Delivery: {self.get_fulfilment_info()}")
        print(f"  Shipping Cost: ${self.calculate_shipping_cost():.2f}")

    def get_fulfilment_info(self):
        return "Requires physical shipping."

    def calculate_shipping_cost(self):
        # Example rule: $2 per kg for one unit of this product.
        return self.__weight * 2.00

    def to_dict(self):
        data = super().to_dict()
        data.update({"type": "physical", "weight": self.__weight})
        return data


class DigitalProduct(Product):
    def __init__(self, product_id, name, price, stock, download_size):
        super().__init__(product_id, name, price, stock)
        self.__download_size = validate_number(download_size, "Download size")

    def display_information(self):
        super().display_information()
        print(f"  Type: Digital | Download Size: {self.__download_size} MB")
        print(f"  Delivery: {self.get_fulfilment_info()}")

    def get_fulfilment_info(self):
        return "Delivered digitally through a download."

    def to_dict(self):
        data = super().to_dict()
        data.update({"type": "digital", "download_size": self.__download_size})
        return data


class Inventory:
    """Manages product objects; delegates product behaviour to them."""

    def __init__(self):
        self.__products = []

    def add_product(self, product):
        if not isinstance(product, Product):
            raise TypeError("Inventory accepts Product objects only.")
        if self.search_product(product.get_product_id()) is not None:
            return False
        self.__products.append(product)
        return True

    def search_product(self, product_id):
        for product in self.__products:
            if product.get_product_id() == product_id.strip().upper():
                return product
        return None

    def display_all(self):
        if not self.__products:
            print("No products in inventory.")
        for product in self.__products:
            product.display_information()
            print("-" * 60)

    def to_list(self):
        return [product.to_dict() for product in self.__products]


def load_inventory(filename=DATA_FILE):
    inventory = Inventory()
    try:
        with open(filename, "r", encoding="utf-8") as file:
            saved_products = json.load(file)
    except FileNotFoundError:
        print("No inventory file found. Starting empty.")
        return inventory

    if not isinstance(saved_products, list):
        raise ValueError("Inventory data must be a list.")
    for item in saved_products:
        if not isinstance(item, dict):
            raise ValueError("Each saved product must be an object.")
        common = (item["id"], item["name"], item["price"], item["stock"])
        if item["type"] == "physical":
            product = PhysicalProduct(*common, item["weight"])
        elif item["type"] == "digital":
            product = DigitalProduct(*common, item["download_size"])
        else:
            raise ValueError(f"Unknown product type: {item['type']}")
        if not inventory.add_product(product):
            raise ValueError(f"Duplicate product ID: {item['id']}")
    print("Inventory loaded successfully.")
    return inventory


def save_inventory(inventory, filename=DATA_FILE):
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(inventory.to_list(), file, indent=4, allow_nan=False)
        print("Inventory saved successfully.")
        return True
    except (OSError, ValueError) as error:
        print(f"Could not save inventory: {error}")
        return False


def get_number(prompt, whole_number=False):
    while True:
        try:
            number = int(input(prompt)) if whole_number else float(input(prompt))
            return validate_number(number, "Value", whole_number)
        except ValueError as error:
            print(f"Invalid input: {error}")


def add_product(inventory):
    print("\n1. Physical Product\n2. Digital Product")
    product_type = input("Choose product type: ").strip()
    if product_type not in ("1", "2"):
        print("Please choose 1 or 2.")
        return
    product_id = input("Product ID: ").strip().upper()
    if not product_id:
        print("Product ID cannot be empty.")
        return
    if inventory.search_product(product_id) is not None:
        print("Product ID already exists.")
        return
    name = input("Product Name: ").strip()
    if not name:
        print("Product name cannot be empty.")
        return
    price = get_number("Price: ")
    stock = get_number("Stock Quantity: ", whole_number=True)
    if product_type == "1":
        weight = get_number("Weight (kg): ")
        product = PhysicalProduct(product_id, name, price, stock, weight)
    else:
        size = get_number("Download Size (MB): ")
        product = DigitalProduct(product_id, name, price, stock, size)
    inventory.add_product(product)
    print("Product added successfully.")


def update_stock(inventory):
    product = inventory.search_product(input("Product ID: "))
    if product is None:
        print("Product not found.")
    else:
        print("Current Stock:", product.get_stock())
        product.update_stock(get_number("New Stock Quantity: ", whole_number=True))
        print("Stock updated successfully.")


def search_product(inventory):
    product = inventory.search_product(input("Product ID: "))
    if product is None:
        print("Product not found.")
    else:
        product.display_information()


def main():
    print("INVENTORY MANAGEMENT SYSTEM - LAB 7")
    try:
        inventory = load_inventory()
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"Could not load inventory data: {error}")
        print("Please fix or rename inventory.json, then restart.")
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
