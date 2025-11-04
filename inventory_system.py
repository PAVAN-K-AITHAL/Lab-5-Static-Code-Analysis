"""
Module for basic inventory management.
Allows adding, removing, checking, loading, and saving stock data.
"""
import json
import logging
from datetime import datetime

# Setup logging to report issues
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def add_item(stock_data, item="default", qty=0, logs=None):
    """
    Adds a specified quantity of an item to the inventory.
    """
    if logs is None:
        logs = []

    if not isinstance(item, str) or not item:
        raise ValueError(f"Item name must be a non-empty string, got: {item}")
    if not isinstance(qty, int):
        raise ValueError(f"Quantity must be an integer, got: {qty}")
    if qty < 0:
        raise ValueError("Quantity cannot be negative for add_item.")

    stock_data[item] = stock_data.get(item, 0) + qty
    log_message = f"{datetime.now()}: Added {qty} of {item}"
    logs.append(log_message)
    logging.info(log_message)


def remove_item(stock_data, item, qty):
    """
    Removes a specified quantity of an item from the inventory.
    """
    if not isinstance(qty, int) or qty < 0:
        logging.warning("Quantity to remove must be a positive integer.")
        return

    try:
        current_qty = stock_data[item]
        if current_qty - qty <= 0:
            del stock_data[item]
            logging.info("Removed all stock for '%s'.", item)
        else:
            stock_data[item] -= qty
            logging.info("Removed %d of '%s'.", qty, item)
    except KeyError:
        logging.warning("Attempted to remove '%s', but it is not in stock.", item)


def get_qty(stock_data, item):
    """Gets the current quantity of a specific item."""
    return stock_data.get(item, 0)


def load_data(file="inventory.json"):
    """Loads inventory data from a JSON file."""
    try:
        with open(file, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        logging.warning("'%s' not found. Starting with an empty inventory.", file)
        return {}
    except json.JSONDecodeError:
        logging.error("Could not decode JSON from '%s'. Starting with empty inventory.", file)
        return {}
    except IOError as e:
        logging.error("Error loading data from '%s': %s", file, e)
        return {}


def save_data(stock_data, file="inventory.json"):
    """Saves the inventory data to a JSON file."""
    try:
        with open(file, "w", encoding="utf-8") as f:
            json.dump(stock_data, f, indent=4)
    except IOError as e:
        logging.error("Error saving data to '%s': %s", file, e)


def print_data(stock_data):
    """Prints a formatted report of all items and their quantities."""
    print("\n--- Items Report ---")
    if not stock_data:
        print("Inventory is empty.")
    else:
        for item, quantity in stock_data.items():
            print(f"{item} -> {quantity}")
    print("--------------------\n")


def check_low_items(stock_data, threshold=5):
    """Finds items with a quantity below a specified threshold."""
    return [item for item, qty in stock_data.items() if qty < threshold]


def main():
    """Main function to run the inventory management demo."""
    stock = load_data("inventory.json")
    print("Initial data loaded:")
    print_data(stock)

    try:
        add_item(stock, "apple", 10)
        add_item(stock, "banana", 20)
        add_item(stock, "banana", -2)  # invalid
    except ValueError as e:
        logging.error("Failed to add item: %s", e)

    try:
        add_item(stock, 123, "ten")  # invalid
    except ValueError as e:
        logging.error("Failed to add item: %s", e)

    remove_item(stock, "apple", 3)
    remove_item(stock, "orange", 1)
    remove_item(stock, "banana", 25)

    print(f"Apple stock: {get_qty(stock, 'apple')}")
    print(f"Banana stock: {get_qty(stock, 'banana')}")
    print(f"Orange stock: {get_qty(stock, 'orange')}")

    print(f"Low items (below 15): {check_low_items(stock, 15)}")

    print("Final data:")
    print_data(stock)

    save_data(stock, "inventory.json")
    print("Data saved.")
    logging.info("Demo finished. 'eval' call was removed.")


if __name__ == "__main__":
    main()
