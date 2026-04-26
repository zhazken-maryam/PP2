import csv
import json
import psycopg2
from config import load_config


# ---------- BASIC DB HELPERS ----------

def get_connection():
    """Returns PostgreSQL connection."""
    config = load_config()
    return psycopg2.connect(**config)


def run_sql_file(filename):
    """Reads and executes SQL file."""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            sql = file.read()

        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
            conn.commit()

        print(f"{filename} executed successfully.")

    except (Exception, psycopg2.DatabaseError) as error:
        print("SQL file error:", error)


def create_schema():
    """Creates tables from schema.sql."""
    run_sql_file("schema.sql")


def create_procedures():
    """Creates procedures and functions from procedures.sql."""
    run_sql_file("procedures.sql")


# ---------- PRINTING ----------

def print_rows(rows):
    """Prints rows in readable format."""
    if not rows:
        print("No data found.")
        return

    for row in rows:
        print(row)


def print_contact_rows(rows):
    """Prints contact rows with named columns."""
    if not rows:
        print("No contacts found.")
        return

    for row in rows:
        print("-" * 40)
        print(f"ID: {row[0]}")
        print(f"Name: {row[1]}")
        print(f"Email: {row[2]}")
        print(f"Birthday: {row[3]}")
        print(f"Group: {row[4]}")
        if len(row) > 5:
            print(f"Phone: {row[5]}")
        if len(row) > 6:
            print(f"Type: {row[6]}")


# ---------- CONTACT FUNCTIONS ----------

def get_group_id(cur, group_name):
    """
    Gets group id by name.
    If group does not exist, creates it.
    """
    cur.execute(
        "INSERT INTO groups(name) VALUES (%s) ON CONFLICT (name) DO NOTHING;",
        (group_name,)
    )

    cur.execute("SELECT id FROM groups WHERE name=%s;", (group_name,))
    result = cur.fetchone()

    if result:
        return result[0]
    return None


def add_contact():
    """Adds one contact with one phone number."""
    name = input("Name: ").strip()
    email = input("Email: ").strip()
    birthday = input("Birthday (YYYY-MM-DD): ").strip()
    group_name = input("Group (Family/Work/Friend/Other): ").strip()
    phone = input("Phone: ").strip()
    phone_type = input("Phone type (home/work/mobile): ").strip()

    if phone_type not in ("home", "work", "mobile"):
        print("Invalid phone type.")
        return

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                group_id = get_group_id(cur, group_name)

                cur.execute(
                    """
                    INSERT INTO contacts(name, email, birthday, group_id)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (name)
                    DO UPDATE SET
                        email = EXCLUDED.email,
                        birthday = EXCLUDED.birthday,
                        group_id = EXCLUDED.group_id
                    RETURNING id;
                    """,
                    (name, email, birthday, group_id)
                )

                contact_id = cur.fetchone()[0]

                cur.execute(
                    """
                    INSERT INTO phones(contact_id, phone, type)
                    VALUES (%s, %s, %s);
                    """,
                    (contact_id, phone, phone_type)
                )

            conn.commit()
            print("Contact added/updated successfully.")

    except (Exception, psycopg2.DatabaseError) as error:
        print("Add contact error:", error)


def add_phone_to_contact():
    """Calls PostgreSQL procedure add_phone."""
    name = input("Contact name: ").strip()
    phone = input("New phone: ").strip()
    phone_type = input("Type (home/work/mobile): ").strip()

    try:
        with get_connection() as conn:
            conn.notices.clear()

            with conn.cursor() as cur:
                cur.execute("CALL add_phone(%s, %s, %s);", (name, phone, phone_type))

            conn.commit()

            if conn.notices:
                for notice in conn.notices:
                    print(notice.strip())
            else:
                print("Phone added.")

    except (Exception, psycopg2.DatabaseError) as error:
        print("Add phone error:", error)


def move_contact_to_group():
    """Calls PostgreSQL procedure move_to_group."""
    name = input("Contact name: ").strip()
    group_name = input("New group: ").strip()

    try:
        with get_connection() as conn:
            conn.notices.clear()

            with conn.cursor() as cur:
                cur.execute("CALL move_to_group(%s, %s);", (name, group_name))

            conn.commit()

            if conn.notices:
                for notice in conn.notices:
                    print(notice.strip())
            else:
                print("Contact moved to group.")

    except (Exception, psycopg2.DatabaseError) as error:
        print("Move group error:", error)


def delete_contact():
    """Deletes contact by name."""
    name = input("Name to delete: ").strip()

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM contacts WHERE name=%s;", (name,))

                if cur.rowcount == 0:
                    print("No such contact.")
                else:
                    print("Contact deleted.")

            conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print("Delete error:", error)


# ---------- SEARCH / FILTER / SORT ----------

def search_all_fields():
    """Calls DB function search_contacts."""
    query = input("Search query: ").strip()

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM search_contacts(%s);", (query,))
                rows = cur.fetchall()
                print_contact_rows(rows)

    except (Exception, psycopg2.DatabaseError) as error:
        print("Search error:", error)


def search_by_email():
    """Searches contacts by partial email."""
    email_part = input("Email part: ").strip()

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT c.id, c.name, c.email, c.birthday, g.name
                    FROM contacts c
                    LEFT JOIN groups g ON c.group_id = g.id
                    WHERE c.email ILIKE %s
                    ORDER BY c.id;
                    """,
                    ("%" + email_part + "%",)
                )
                rows = cur.fetchall()
                print_contact_rows(rows)

    except (Exception, psycopg2.DatabaseError) as error:
        print("Email search error:", error)


def filter_by_group():
    """Shows contacts only from selected group."""
    group_name = input("Group name: ").strip()

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT c.id, c.name, c.email, c.birthday, g.name
                    FROM contacts c
                    LEFT JOIN groups g ON c.group_id = g.id
                    WHERE g.name ILIKE %s
                    ORDER BY c.id;
                    """,
                    (group_name,)
                )
                rows = cur.fetchall()
                print_contact_rows(rows)

    except (Exception, psycopg2.DatabaseError) as error:
        print("Filter error:", error)


def sort_contacts():
    """Sorts contacts by name, birthday, or date_added."""
    print("Sort by:")
    print("1. Name")
    print("2. Birthday")
    print("3. Date added")

    choice = input("Choose: ").strip()

    allowed_columns = {
        "1": "c.name",
        "2": "c.birthday",
        "3": "c.date_added"
    }

    if choice not in allowed_columns:
        print("Invalid choice.")
        return

    order_column = allowed_columns[choice]

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"""
                    SELECT c.id, c.name, c.email, c.birthday, g.name, c.date_added
                    FROM contacts c
                    LEFT JOIN groups g ON c.group_id = g.id
                    ORDER BY {order_column};
                    """
                )
                rows = cur.fetchall()
                print_rows(rows)

    except (Exception, psycopg2.DatabaseError) as error:
        print("Sort error:", error)


def show_all_contacts():
    """Shows all contacts with phones."""
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT c.id, c.name, c.email, c.birthday, g.name, p.phone, p.type
                    FROM contacts c
                    LEFT JOIN groups g ON c.group_id = g.id
                    LEFT JOIN phones p ON p.contact_id = c.id
                    ORDER BY c.id;
                    """
                )
                rows = cur.fetchall()
                print_contact_rows(rows)

    except (Exception, psycopg2.DatabaseError) as error:
        print("Show all error:", error)


# ---------- PAGINATION ----------

def paginated_navigation():
    """
    Console pagination loop.
    Uses pagination(lim, offs) function from PostgreSQL.
    """
    try:
        limit = int(input("Page size: ").strip())
    except ValueError:
        print("Page size must be integer.")
        return

    offset = 0

    while True:
        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT * FROM pagination(%s, %s);", (limit, offset))
                    rows = cur.fetchall()
                    print_rows(rows)

        except (Exception, psycopg2.DatabaseError) as error:
            print("Pagination error:", error)
            return

        print("\nCommands: next / prev / quit")
        command = input("Enter command: ").strip().lower()

        if command == "next":
            offset += limit
        elif command == "prev":
            offset = max(0, offset - limit)
        elif command == "quit":
            break
        else:
            print("Invalid command.")


# ---------- JSON IMPORT / EXPORT ----------

def export_to_json():
    """Exports all contacts with phones and group to JSON."""
    filename = input("JSON filename to export: ").strip()

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT c.id, c.name, c.email, c.birthday, g.name
                    FROM contacts c
                    LEFT JOIN groups g ON c.group_id = g.id
                    ORDER BY c.id;
                    """
                )
                contacts = cur.fetchall()

                result = []

                for contact in contacts:
                    contact_id = contact[0]

                    cur.execute(
                        """
                        SELECT phone, type
                        FROM phones
                        WHERE contact_id=%s
                        ORDER BY id;
                        """,
                        (contact_id,)
                    )

                    phones = cur.fetchall()

                    result.append({
                        "name": contact[1],
                        "email": contact[2],
                        "birthday": str(contact[3]) if contact[3] is not None else None,
                        "group": contact[4],
                        "phones": [
                            {"phone": p[0], "type": p[1]}
                            for p in phones
                        ]
                    })

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(result, file, indent=4, ensure_ascii=False)

        print("Exported to JSON.")

    except (Exception, psycopg2.DatabaseError) as error:
        print("Export error:", error)


def insert_contact_from_dict(cur, data, overwrite=False):
    """Inserts one contact from dictionary."""
    name = data.get("name")
    email = data.get("email")
    birthday = data.get("birthday")
    group_name = data.get("group", "Other")
    phones = data.get("phones", [])

    group_id = get_group_id(cur, group_name)

    if overwrite:
        cur.execute(
            """
            INSERT INTO contacts(name, email, birthday, group_id)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (name)
            DO UPDATE SET
                email = EXCLUDED.email,
                birthday = EXCLUDED.birthday,
                group_id = EXCLUDED.group_id
            RETURNING id;
            """,
            (name, email, birthday, group_id)
        )
    else:
        cur.execute(
            """
            INSERT INTO contacts(name, email, birthday, group_id)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (name) DO NOTHING
            RETURNING id;
            """,
            (name, email, birthday, group_id)
        )

    result = cur.fetchone()

    if result is None:
        return False

    contact_id = result[0]

    if overwrite:
        cur.execute("DELETE FROM phones WHERE contact_id=%s;", (contact_id,))

    for phone_data in phones:
        phone = phone_data.get("phone")
        phone_type = phone_data.get("type", "mobile")

        if phone_type not in ("home", "work", "mobile"):
            phone_type = "mobile"

        cur.execute(
            """
            INSERT INTO phones(contact_id, phone, type)
            VALUES (%s, %s, %s);
            """,
            (contact_id, phone, phone_type)
        )

    return True


def import_from_json():
    """
    Imports contacts from JSON.
    If duplicate name exists, asks skip or overwrite.
    """
    filename = input("JSON filename to import: ").strip()

    try:
        with open(filename, "r", encoding="utf-8") as file:
            contacts = json.load(file)

        with get_connection() as conn:
            with conn.cursor() as cur:
                for data in contacts:
                    name = data.get("name")

                    cur.execute("SELECT id FROM contacts WHERE name=%s;", (name,))
                    exists = cur.fetchone()

                    if exists:
                        action = input(f"{name} already exists. skip/overwrite? ").strip().lower()

                        if action == "skip":
                            print(f"Skipped {name}.")
                            continue
                        elif action == "overwrite":
                            inserted = insert_contact_from_dict(cur, data, overwrite=True)
                        else:
                            print("Invalid choice, skipped.")
                            continue
                    else:
                        inserted = insert_contact_from_dict(cur, data, overwrite=False)

                    if inserted:
                        print(f"Imported {name}.")

            conn.commit()

        print("JSON import finished.")

    except (Exception, psycopg2.DatabaseError) as error:
        print("Import JSON error:", error)


# ---------- CSV IMPORT ----------

def import_from_csv():
    """
    Imports contacts from CSV.
    Expected columns:
    name,email,birthday,group,phone,type
    """
    filename = input("CSV filename: ").strip()

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                with open(filename, "r", encoding="utf-8") as file:
                    reader = csv.DictReader(file)

                    for row in reader:
                        name = row["name"]
                        email = row["email"]
                        birthday = row["birthday"]
                        group_name = row["group"]
                        phone = row["phone"]
                        phone_type = row["type"]

                        if phone_type not in ("home", "work", "mobile"):
                            phone_type = "mobile"

                        group_id = get_group_id(cur, group_name)

                        cur.execute(
                            """
                            INSERT INTO contacts(name, email, birthday, group_id)
                            VALUES (%s, %s, %s, %s)
                            ON CONFLICT (name)
                            DO UPDATE SET
                                email = EXCLUDED.email,
                                birthday = EXCLUDED.birthday,
                                group_id = EXCLUDED.group_id
                            RETURNING id;
                            """,
                            (name, email, birthday, group_id)
                        )

                        contact_id = cur.fetchone()[0]

                        cur.execute(
                            """
                            INSERT INTO phones(contact_id, phone, type)
                            VALUES (%s, %s, %s);
                            """,
                            (contact_id, phone, phone_type)
                        )

            conn.commit()

        print("CSV imported.")

    except (Exception, psycopg2.DatabaseError) as error:
        print("CSV import error:", error)


# ---------- MAIN MENU ----------

def main():
    while True:
        print("\n========== TSIS1 PHONEBOOK ==========")
        print("1. Create schema")
        print("2. Create procedures/functions")
        print("3. Add contact")
        print("4. Add phone to contact")
        print("5. Move contact to group")
        print("6. Show all contacts")
        print("7. Search all fields")
        print("8. Search by email")
        print("9. Filter by group")
        print("10. Sort contacts")
        print("11. Paginated navigation")
        print("12. Export to JSON")
        print("13. Import from JSON")
        print("14. Import from CSV")
        print("15. Delete contact")
        print("16. Exit")

        choice = input("Choose option: ").strip()

        if choice == "1":
            create_schema()
        elif choice == "2":
            create_procedures()
        elif choice == "3":
            add_contact()
        elif choice == "4":
            add_phone_to_contact()
        elif choice == "5":
            move_contact_to_group()
        elif choice == "6":
            show_all_contacts()
        elif choice == "7":
            search_all_fields()
        elif choice == "8":
            search_by_email()
        elif choice == "9":
            filter_by_group()
        elif choice == "10":
            sort_contacts()
        elif choice == "11":
            paginated_navigation()
        elif choice == "12":
            export_to_json()
        elif choice == "13":
            import_from_json()
        elif choice == "14":
            import_from_csv()
        elif choice == "15":
            delete_contact()
        elif choice == "16":
            print("Bye.")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
