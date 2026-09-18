# Smart Inventory Auditor - Modular Version

inventory = 0
failed_entries = 0
deliveries_processed = 0


def get_valid_input():
    global failed_entries

    while True:
        user_input = input("Enter stock quantity (or type 'quit' to finish): ")

        # Quit the program
        if user_input.lower() == "quit":
            return "quit"

        # Check if the input is a number
        if not user_input.isdigit():

            # Check specifically for negative numbers
            if user_input.startswith("-") and user_input[1:].isdigit():
                print("Error: Negative numbers are not allowed.")
            else:
                print("Error: Invalid input. Please enter a whole number.")

            failed_entries += 1
            continue

        # Convert valid input to integer
        quantity = int(user_input)

        return quantity


def process_delivery(current_total, new_value):
    new_total = current_total + new_value
    return new_total


def calculate_tax(amount):
    tax = amount * 0.10
    return tax


def generate_report(total_units, failed_attempts):
    print("\n--- Inventory Report ---")
    print("Total Units Processed:", total_units)
    print("Number of Failed/Rejected Entries:", failed_attempts)


# Main Program

while True:

    quantity = get_valid_input()

    # Stop when user types quit
    if quantity == "quit":
        break

    # Process delivery
    inventory = process_delivery(inventory, quantity)

    # Calculate 10% tax
    tax = calculate_tax(quantity)

    # Count successful deliveries
    deliveries_processed += 1

    print("Stock added successfully.")
    print("Current inventory:", inventory)
    print("Tax for this delivery:", tax)

    # Overstock check
    if inventory > 500:
        print("OVERSTOCK ALERT: Total Inventory exceeds 500 units")


# Final report
generate_report(inventory, failed_entries)

print("Total Deliveries Processed:", deliveries_processed)