
from Inventory_Manager_10 import (
    Supplier, Product, PhysicalProduct, DigitalProduct,
    Inventory, Order, load_inventory
)


def show_product_details(product: Product) -> None:
    product.display_information()
    print(product.get_fulfilment_info())


def main() -> None:

    supplier = Supplier(
        "S001", "Example Supplier", "sales@example.com"
    )

    physical = PhysicalProduct(
        "P100", "Mouse", 30.0, 12, 0.3, supplier
    )

    digital = DigitalProduct(
        "D100", "Ebook", 12.0, 50, 10.0, supplier
    )

    # TEST 1: ASSOCIATION
    print("\n1. ASSOCIATION")

    del supplier

    assert physical.supplier is digital.supplier

    physical.supplier.display_information()
    digital.supplier.display_information()

    print("PASS: Both products retain the Supplier reference.")

    # TEST 2: AGGREGATION
    print("\n2. AGGREGATION")

    inventory_a = Inventory()
    inventory_b = Inventory()

    assert inventory_a.add_product(physical)
    assert inventory_a.remove_product("P100")
    assert inventory_a.find_product("P100") is None
    assert physical.get_stock() == 12

    assert inventory_b.add_product(physical)
    assert inventory_b.find_product("P100") is physical

    print("PASS: Product survives removal and transfer.")

    # TEST 3: COMPOSITION
    print("\n3. COMPOSITION")

    order_a = Order("O001")
    order_b = Order("O002")

    order_a.add_order_line(physical, 2)
    order_a.add_order_line(digital, 3)
    order_b.add_order_line(physical, 1)

    assert len(order_a.order_lines) + len(order_b.order_lines) == 3

    assert order_a.order_lines[0] is not order_b.order_lines[0]

    assert (
        order_a.order_lines[0].product
        is order_b.order_lines[0].product
    )

    assert order_a.calculate_total() == 96.0
    assert order_b.calculate_total() == 30.0

    order_a.display_order()
    order_b.display_order()

    print("PASS: Order and OrderLine composition works.")

    # TEST 4: LSP AND POLYMORPHISM
    print("\n4. LSP AND POLYMORPHISM")

    inventory_b.add_product(digital)

    for product in inventory_b.products:
        show_product_details(product)
        product.update_stock(product.get_stock())

    assert len(inventory_b.products) == 2

    print("PASS: Both product types work through Product.")

    # TEST 5: JSON
    print("\n5. JSON COMPATIBILITY")

    existing = load_inventory()

    assert len(existing.products) >= 2

    print("PASS: Inventory JSON loaded successfully.")

    print("\nALL TESTS PASSED")


if __name__ == "__main__":
    main()
