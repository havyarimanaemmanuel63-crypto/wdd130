# Enhancement: Added a "return by" date 30 days in the future at 9:00 PM.
import csv
from datetime import datetime, timedelta


# Column indexes in products.csv
PRODUCT_NUM_INDEX = 0
NAME_INDEX = 1
PRICE_INDEX = 2

# Column indexes in request.csv
REQ_PROD_NUM_INDEX = 0
REQ_QUANTITY_INDEX = 1

TAX_RATE = 0.06  # 6% sales tax


def main():
    try:
        # 1. Load the product catalog into a dictionary
        products_dict = read_dictionary("products.csv", PRODUCT_NUM_INDEX)

        print("Inkom Emporium\n")

        total_items = 0
        subtotal = 0.0

        # 2. Read the customer's order
        with open("request.csv", "rt") as request_file:
            reader = csv.reader(request_file)
            next(reader)  # Skip the header line

            for row in reader:
                if len(row) != 0:
                    prod_num = row[REQ_PROD_NUM_INDEX]
                    quantity = int(row[REQ_QUANTITY_INDEX])

                    # Look up the product in the dictionary (may raise KeyError)
                    product_info = products_dict[prod_num]
                    name = product_info[NAME_INDEX]
                    price = float(product_info[PRICE_INDEX])

                    # Display the item and update totals
                    print(f"{name}: {quantity} @ {price:.2f}")
                    total_items += quantity
                    subtotal += quantity * price

        # 3. Compute sales tax and total amount
        sales_tax = subtotal * TAX_RATE
        total = subtotal + sales_tax

        print(f"\nNumber of Items: {total_items}")
        print(f"Subtotal: {subtotal:.2f}")
        print(f"Sales Tax: {sales_tax:.2f}")
        print(f"Total: {total:.2f}")

        # 4. Closing message, current date/time, and return-by date
        print("\nThank you for shopping at the Inkom Emporium.")
        current_date_and_time = datetime.now()
        print(f"{current_date_and_time:%a %b %d %H:%M:%S %Y}")

        return_by_date = (current_date_and_time + timedelta(days=30)).replace(hour=21, minute=0, second=0)
        print(f"Return by: {return_by_date:%a %b %d %I:%M %p %Y}")

    except FileNotFoundError as not_found_err:
        print("Error: missing file")
        print(not_found_err)
    except PermissionError as perm_err:
        print("Error: permission denied")
        print(perm_err)
    except KeyError as key_err:
        print(f"Error: unknown product ID in the request.csv file\n{key_err}")


def read_dictionary(filename, key_column_index):
    """Read the contents of a CSV file into a compound
    dictionary and return the dictionary.
    """
    dictionary = {}
    with open(filename, "rt") as csv_file:
        reader = csv.reader(csv_file)
        next(reader)  # Skip the first line (headers)
        for row in reader:
            if len(row) != 0:  # Avoid empty lines
                key = row[key_column_index]
                dictionary[key] = row
    return dictionary


if __name__ == "__main__":
    main()
