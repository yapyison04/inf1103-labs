import json


class Product:
    """Represents one product and manages its information and stock."""

    def __init__(self, product_id, name, price, stock):
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock

    def get_product_id(self):
        return self.__product_id

    def get_stock(self):
        return self.__stock

    def update_stock(self, quantity):
        if not isinstance(quantity, int) or quantity < 0:
            raise ValueError("Stock must be a non-negative whole number.")
        self.__stock = quantity

    def display_information(self):
        print(
            f"ID: {self.__product_id} | "
            f"Name: {self.__name} | "
            f"Price: ${self.__price:.2f} | "
            f"Stock: {self.__stock}"
        )

    def to_dict(self):
        """Convert a Product to the same JSON format used in Week 5."""
        return {
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
        }


class Inventory:
    """Manages a collection of Product objects."""

    def __init__(self):
        self.__products = []

    def add_product(self, product):
        if self.search_product(product.get_product_id()) is not None:
            return False
        self.__products.append(product)
        return True

    def search_product(self, product_id):
        for product in self.__products:
            if product.get_product_id() == product_id:
                return product
        return None

    def display_all(self):
        if not self.__products:
            print("No products in inventory.")
        else:
            for product in self.__products:
                product.display_information()

    def to_list(self):
        return [product.to_dict() for product in self.__products]


def load_inventory():
    inventory = Inventory()
    try:
        with open("inventory.json", "r") as file:
            saved_products = json.load(file)

        for item in saved_products:
            product = Product(
                item["id"], item["name"], item["price"], item["stock"]
            )
            inventory.add_product(product)

        print("Inventory loaded successfully.")
    except FileNotFoundError:
        print("No inventory file found. Starting empty.")
    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
        print(f"Could not load inventory data: {error}")
    return inventory


def save_inventory(inventory):
    with open("inventory.json", "w") as file:
        json.dump(inventory.to_list(), file, indent=4)
    print("Inventory saved successfully.")


def get_number(prompt, whole_number=False):
    while True:
        try:
            number = int(input(prompt)) if whole_number else float(input(prompt))
            if number < 0:
                print("Please enter a non-negative number.")
            else:
                return number
        except ValueError:
            print("Please enter a valid number.")


def add_product(inventory):
    product_id = input("Product ID: ").strip().upper()
    if product_id == "":
        print("Product ID cannot be empty.")
        return
    if inventory.search_product(product_id) is not None:
        print("Product ID already exists.")
        return

    name = input("Product Name: ").strip()
    if name == "":
        print("Product name cannot be empty.")
        return

    price = get_number("Price: ")
    stock = get_number("Stock Quantity: ", whole_number=True)
    product = Product(product_id, name, price, stock)
    inventory.add_product(product)
    print("Product added successfully.")


def update_stock(inventory):
    product_id = input("Product ID: ").strip().upper()
    product = inventory.search_product(product_id)
    if product is None:
        print("Product not found.")
    else:
        print("Current Stock:", product.get_stock())
        product.update_stock(get_number("New Stock Quantity: ", whole_number=True))
        print("Stock updated successfully.")


def search_product(inventory):
    product_id = input("Product ID: ").strip().upper()
    product = inventory.search_product(product_id)
    if product is None:
        print("Product not found.")
    else:
        product.display_information()


def main():
    print("INVENTORY MANAGEMENT SYSTEM")
    inventory = load_inventory()

    while True:
        print("\n1. Display All Products")
        print("2. Add Product")
        print("3. Update Stock")
        print("4. Search Product")
        print("5. Save Inventory")
        print("6. Exit")

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
            save_inventory(inventory)
            print("Goodbye!")
            break
        else:
            print("Please choose 1 to 6.")


if __name__ == "__main__":
    main()
