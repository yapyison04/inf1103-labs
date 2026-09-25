# Smart Inventory Auditor - Persistent Version

inventory = 0
failed_entries = 0
deliveries_processed = 0
transaction_history = []


def load_inventory():
    try:
        with open("inventory.txt", "r") as file:
            lines = file.readlines()

            saved_inventory = int(lines[0].strip())

            if len(lines) > 1 and lines[1].strip():
                saved_history = [
                    int(value)
                    for value in lines[1].strip().split(",")
                ]
            else:
                saved_history = []

            print("Previous inventory loaded successfully.")
            print("Current inventory:", saved_inventory)
            print("Transaction history:", saved_history)

            return saved_inventory, saved_history

    except FileNotFoundError:
        print("No previous inventory file found.")
        print("Starting with empty inventory.")

        return 0, []


def save_inventory(current_inventory, history):
    with open("inventory.txt", "w") as file:

        file.write(str(current_inventory) + "\n")

        history_text = ",".join(str(value) for value in history)
        file.write(history_text + "\n")

    print("Inventory successfully saved to inventory.txt")


def get_valid_input():
    global failed_entries

    while True:
        user_input = input("Enter stock quantity (or type 'quit' to finish): ")

        if user_input.lower() == "quit":
            return "quit"

        if not user_input.isdigit():

            if user_input.startswith("-") and user_input[1:].isdigit():
                print("Error: Negative numbers are not allowed.")
            else:
                print("Error: Invalid input. Please enter a whole number.")

            failed_entries += 1
            continue

        quantity = int(user_input)

        return quantity


def process_delivery(current_total, new_value):
    new_total = current_total + new_value
    return new_total


def calculate_tax(amount):
    tax = amount * 0.10
    return tax


def generate_report(total_units, failed_attempts, history):
    print("\n--- Inventory Report ---")
    print("Total Units:", total_units)
    print("Number of Failed/Rejected Entries:", failed_attempts)
    print("Transaction History:", history)


# Main Program

inventory, transaction_history = load_inventory()

while True:

    quantity = get_valid_input()

    if quantity == "quit":
        save_inventory(inventory, transaction_history)
        break

    inventory = process_delivery(inventory, quantity)

    transaction_history.append(quantity)

    tax = calculate_tax(quantity)

    deliveries_processed += 1

    print("Stock added successfully.")
    print("Current inventory:", inventory)
    print("Tax for this delivery:", tax)

    if inventory > 500:
        print("OVERSTOCK ALERT: Total Inventory exceeds 500 units")


generate_report(
    inventory,
    failed_entries,
    transaction_history
)

print("Total Deliveries Processed:", deliveries_processed)
print("Total Tax:", calculate_tax(inventory))