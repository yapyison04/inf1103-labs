import json


def load_inventory():
    try:
        with open("inventory.json", "r") as file:
            inventory = json.load(file)

        print("Inventory loaded successfully.")
        return inventory

    except FileNotFoundError:
        print("No inventory file found. Starting empty.")
        return []


def save_inventory(inventory):
    with open("inventory.json", "w") as file:
        json.dump(inventory, file, indent=4)

    print("Inventory saved successfully.")


def get_number(prompt, whole_number=False):
    while True:
        try:
            if whole_number:
                number = int(input(prompt))
            else:
                number = float(input(prompt))

            if number < 0:
                print("Please enter a non-negative number.")
            else:
                return number

        except ValueError:
            print("Please enter a valid number.")


def find_product(inventory, product_id):
    for product in inventory:
        if product["id"] == product_id:
            return product

    return None


def add_product(inventory):
    product_id = input("Product ID: ").strip().upper()

    if product_id == "":
        print("Product ID cannot be empty.")
        return

    if find_product(inventory, product_id) is not None:
        print("Product ID already exists.")
        return

    name = input("Product Name: ").strip()

    if name == "":
        print("Product name cannot be empty.")
        return

    price = get_number("Price: ")
    stock = get_number("Stock Quantity: ", whole_number=True)

    product = {
        "id": product_id,
        "name": name,
        "price": price,
        "stock": stock
    }

    inventory.append(product)
    print("Product added successfully.")


def update_stock(inventory):
    product_id = input("Product ID: ").strip().upper()
    product = find_product(inventory, product_id)

    if product is None:
        print("Product not found.")
    else:
        print("Current Stock:", product["stock"])
        product["stock"] = get_number(
            "New Stock Quantity: ", whole_number=True
        )
        print("Stock updated successfully.")


def show_product(product):
    print(
        f"ID: {product['id']} | "
        f"Name: {product['name']} | "
        f"Price: ${product['price']:.2f} | "
        f"Stock: {product['stock']}"
    )


def search_product(inventory):
    product_id = input("Product ID: ").strip().upper()
    product = find_product(inventory, product_id)

    if product is None:
        print("Product not found.")
    else:
        show_product(product)


def display_all(inventory):
    if not inventory:
        print("No products in inventory.")
    else:
        for product in inventory:
            show_product(product)


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
            display_all(inventory)
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