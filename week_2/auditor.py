# Smart Inventory Auditor

inventory = 0
failed_entries = 0

while True:
    user_input = input("Enter stock quantity (or type 'quit' to finish): ")

    # Quit the program
    if user_input.lower() == "quit":
        break

    # Check if the input is a number
    if not user_input.isdigit():

        # Check specifically for negative numbers
        if user_input.startswith("-") and user_input[1:].isdigit():
            print("Error: Negative numbers are not allowed.")
        else:
            print("Error: Invalid input. Please enter a whole number.")

        failed_entries += 1
        continue

    # Convert to integer
    quantity = int(user_input)

    # Add to inventory
    inventory += quantity

    print("Stock added successfully.")
    print("Current inventory:", inventory)

    # Overstock check
    if inventory > 500:
        print("OVERSTOCK ALERT: Total Inventory exceeds 500 units")
        break

# Final report
print("\n--- Inventory Report ---")
print("Total Units Processed:", inventory)
print("Number of Failed/Rejected Entries:", failed_entries)