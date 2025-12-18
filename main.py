import os
import csv
from datetime import datetime

FILE = "expenses.csv"


def ensure_csv_header():
    if not os.path.exists(FILE) or os.path.getsize(FILE) == 0:
        with open(FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["date", "category", "amount", "note"])


def add_expense():
    # -------------------------
    # Expense name validation
    # -------------------------
    while True:
        name = input("Expense name: ").strip().lower()

        if not name:
            print("Expense name cannot be empty.")
            continue

        if not any(char.isalpha() for char in name):
            print("Expense name must contain letters.")
            continue

        break


def choose_category():
    categories = [
        "food",
        "transport",
        "rent",
        "utilities",
        "personal",
        "other"
    ]

    print("\nChoose a category:")
    for i, category in enumerate(categories, start=1):
        print(f"{i}. {category}")

    while True:
        choice = input("Category number: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(categories):
            return categories[int(choice) - 1]
        else:
            print("Invalid choice. Try again.")


def get_valid_amount():
    while True:
        amount_input = input("Amount: ").strip()
        try:
            amount = float(amount_input)
            if amount <= 0:
                raise ValueError
            return amount
        except ValueError:
            print("Please enter a positive number.")


def get_note():
    note = input("Note (optional): ").strip()
    return note


def add_expense():
    category = choose_category()
    amount = get_valid_amount()
    note = get_note()

    date = datetime.now().strftime("%Y-%m-%d")

    with open(FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([date, category, amount, note])

    print("\nExpense saved successfully ✅")


def view_expenses():
    try:
        with open(FILE) as f:
            reader = csv.reader(f)
            rows = list(reader)

    except FileNotFoundError:
        print("\nNo expenses recorded yet.")
        return

    if len(rows) <= 1:
        print("\nNo expenses recorded yet.")
        return

    print("\n--- Recent Expenses ---")
    print("-" * 40)

    # Skip header
    for date, name, amount, category in rows[1:]:
        print(f"{date} | {name:<12} | {amount} | {category}")

    print("-" * 40)


def category_summary():
    totals = {}

    try:
        with open(FILE) as f:
            reader = csv.reader(f)
            next(reader)  # skip header

            for date, name, amount, category in reader:
                amount = float(amount)
                totals[category] = totals.get(category, 0) + amount

    except FileNotFoundError:
        print("\nNo expenses recorded yet.")
        return

    if not totals:
        print("\nNo expenses recorded yet.")
        return

    print("\n--- Category Summary ---")
    print("-" * 30)

    for category, total in totals.items():
        print(f"{category:<12} → {total:.2f}")

    print("-" * 30)


def monthly_summary():
    month = input("Enter month (YYYY-MM): ").strip()
    totals = {}

    try:
        with open(FILE) as f:
            reader = csv.reader(f)
            next(reader)  # skip header

            for date, name, amount, category in reader:
                if date.startswith(month):
                    amount = float(amount)
                    totals[category] = totals.get(category, 0) + amount

    except FileNotFoundError:
        print("\nNo expenses recorded yet.")
        return

    if not totals:
        print(f"\nNo expenses found for {month}.")
        return

    print(f"\n--- Monthly Summary: {month} ---")
    print("-" * 35)

    total_spent = 0
    for category, total in totals.items():
        print(f"{category:<12} → {total:.2f}")
        total_spent += total

    print("-" * 35)
    print(f"Total spent → {total_spent:.2f}")


def highest_expense_alert():
    highest = None  # will store (date, name, amount, category)

    try:
        with open(FILE) as f:
            reader = csv.reader(f)
            next(reader)  # skip header

            for row in reader:
                date, name, amount, category = row
                amount = float(amount)

                if highest is None or amount > highest[2]:
                    highest = (date, name, amount, category)

    except FileNotFoundError:
        print("\nNo expenses recorded yet.")
        return

    if highest is None:
        print("\nNo expenses recorded yet.")
        return

    date, name, amount, category = highest

    print("\n🚨 Highest Expense Alert 🚨")
    print("-" * 35)
    print(f"Item     : {name}")
    print(f"Category : {category}")
    print(f"Amount   : {amount:.2f}")
    print(f"Date     : {date}")
    print("-" * 35)


def export_report():
    totals = {}

    try:
        with open(FILE) as f:
            reader = csv.reader(f)
            next(reader)  # skip header

            for date, name, amount, category in reader:
                amount = float(amount)
                totals[category] = totals.get(category, 0) + amount

    except FileNotFoundError:
        print("\nNo expenses to export.")
        return

    if not totals:
        print("\nNo expenses to export.")
        return

    report_file = "expense_summary_report.csv"

    with open(report_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["category", "total_spent"])

        for category, total in totals.items():
            writer.writerow([category, f"{total:.2f}"])

    print(f"\n✅ Report exported successfully as '{report_file}'")


def main():
    ensure_csv_header()

    while True:
        print("\n--- Expense Tracker ---")
        print("1. Add expense")
        print("2. View expenses")
        print("3. Category summary")
        print("4. Monthly summary")
        print("5. Highest expense alert")
        print("6. Export report")
        print("7. Exit")

        choice = input("Choose: ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            category_summary()
        elif choice == "4":
            monthly_summary()
        elif choice == "5":
            highest_expense_alert()
        elif choice == "6":
            export_report()
        elif choice == "7":
            print("Goodbye 👋")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
