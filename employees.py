# employees.py

# Employee Details CRUD System (CSV-backed)
# Place this file in the same folder as employees.csv

import csv
import os
import sys

CSV_FILE = "employees.csv"
FIELDNAMES = ["id", "name", "age", "department", "salary"]

def ensure_csv_exists():
    """Create CSV file with header if it doesn't exist."""
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()

def read_all_employees():
    """Read all employees from CSV and return a list of dicts."""
    ensure_csv_exists()
    with open(CSV_FILE, "r", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)

def write_all_employees(rows):
    """Write the provided list of dicts to the CSV (overwrite)."""
    with open(CSV_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

def generate_next_id(rows):
    """Generate the next integer id as string based on existing rows."""
    if not rows:
        return "1"
    ids = [int(r["id"]) for r in rows if r.get("id") and r["id"].isdigit()]
    return str(max(ids) + 1) if ids else "1"

def add_employee():
    rows = read_all_employees()
    new_id = generate_next_id(rows)
    name = input("Name: ").strip()
    age = input("Age: ").strip()
    department = input("Department: ").strip()
    salary = input("Salary: ").strip()

    if not name:
        print("Name is required. Aborting add.")
        return

    row = {"id": new_id, "name": name, "age": age, "department": department, "salary": salary}
    rows.append(row)
    write_all_employees(rows)
    print(f"Added employee with id {new_id}.")

def view_employees():
    rows = read_all_employees()
    if not rows:
        print("No employees found.")
        return

    print("\nAll Employees:")
    print(f"{'ID':<5} {'Name':<20} {'Age':<5} {'Department':<15} {'Salary':<10}")
    print("-" * 60)
    for r in rows:
        print(f"{r['id']:<5} {r['name']:<20} {r['age']:<5} {r['department']:<15} {r['salary']:<10}")
    print()

def search_employee():
    q = input("Search by id or name: ").strip()
    if not q:
        print("Empty search.")
        return
    rows = read_all_employees()
    found = [r for r in rows if r['id'] == q or q.lower() in r['name'].lower()]
    if not found:
        print("No matching employees.")
        return
    print(f"Found {len(found)} record(s):")
    for r in found:
        print(r)

def update_employee():
    rows = read_all_employees()
    target_id = input("Enter employee id to update: ").strip()
    for i, r in enumerate(rows):
        if r['id'] == target_id:
            print("Leave blank to keep current value.")
            name = input(f"Name [{r['name']}]: ").strip() or r['name']
            age = input(f"Age [{r['age']}]: ").strip() or r['age']
            department = input(f"Department [{r['department']}]: ").strip() or r['department']
            salary = input(f"Salary [{r['salary']}]: ").strip() or r['salary']

            rows[i] = {"id": r['id'], "name": name, "age": age, "department": department, "salary": salary}
            write_all_employees(rows)
            print(f"Employee {target_id} updated.")
            return
    print("Employee id not found.")

def delete_employee():
    rows = read_all_employees()
    target_id = input("Enter employee id to delete: ").strip()
    new_rows = [r for r in rows if r['id'] != target_id]
    if len(new_rows) == len(rows):
        print("Employee id not found. Nothing deleted.")
        return
    write_all_employees(new_rows)
    print(f"Employee {target_id} deleted.")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main_menu():
    while True:
        print("\nEmployee CRUD System")
        print("1. Add Employee")
        print("2. View All Employees")
        print("3. Search Employee")
        print("4. Update Employee")
        print("5. Delete Employee")
        print("6. Exit")

        choice = input("Choose an option [1-6]: ").strip()
        if choice == '1':
            add_employee()
        elif choice == '2':
            view_employees()
        elif choice == '3':
            search_employee()
        elif choice == '4':
            update_employee()
        elif choice == '5':
            delete_employee()
        elif choice == '6':
            print("Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice. Try again.")

if __name__ == '__main__':
    ensure_csv_exists()
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\nInterrupted. Exiting.")
        sys.exit(0)
