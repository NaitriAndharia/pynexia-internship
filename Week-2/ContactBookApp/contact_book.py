import json

CONTACTS_FILE = "contacts.json"


def load_contacts():
    try:
        with open(CONTACTS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_contacts(contacts):
    with open(CONTACTS_FILE, "w", encoding="utf-8") as f:
        json.dump(contacts, f, indent=4)


def add_contact(contacts):
    print("\n--- Add New Contact ---")
    name = input("Enter Name: ").strip()
    if not name:
        print("[Error] Name cannot be empty.")
        return

    phone = input("Enter Phone Number: ").strip()
    if not phone:
        print("[Error] Phone number cannot be empty.")
        return

    email = input("Enter Email Address: ").strip()
    address = input("Enter Address: ").strip()

    for c in contacts:
        if c["phone"] == phone:
            print(f"[Error] A contact with phone '{phone}' already exists ({c['name']}).")
            return

    contacts.append({
        "name": name,
        "phone": phone,
        "email": email,
        "address": address,
    })
    save_contacts(contacts)
    print(f"[Success] Contact '{name}' saved to {CONTACTS_FILE}.")


def view_contacts(contacts):
    if not contacts:
        print("\n[Info] No contacts found.")
        return

    sorted_contacts = sorted(contacts, key=lambda item: item["name"].lower())
    print(f"\n--- All Contacts (Alphabetized: {len(sorted_contacts)}) ---")
    for idx, c in enumerate(sorted_contacts, start=1):
        print(
            f"{idx}. Name: {c['name']} | Phone: {c['phone']} | "
            f"Email: {c['email'] or 'N/A'} | Address: {c['address'] or 'N/A'}"
        )


def search_contact(contacts):
    if not contacts:
        print("\n[Info] No contacts to search.")
        return

    query = input("\nEnter Name or Phone to search: ").strip().lower()
    if not query:
        print("[Error] Search query cannot be empty.")
        return

    matches = [
        c for c in contacts
        if query in c["name"].lower() or query in c["phone"].lower()
    ]

    if not matches:
        print(f"[Info] No matching contacts found for '{query}'.")
        return

    print(f"\n--- Search Results ({len(matches)}) ---")
    for idx, c in enumerate(matches, start=1):
        print(
            f"{idx}. Name: {c['name']} | Phone: {c['phone']} | "
            f"Email: {c['email'] or 'N/A'} | Address: {c['address'] or 'N/A'}"
        )


def edit_contact(contacts):
    if not contacts:
        print("\n[Info] No contacts available to edit.")
        return

    search_contact(contacts)
    phone_key = input("\nEnter exact Phone Number of the contact to edit: ").strip()

    for c in contacts:
        if c["phone"] == phone_key:
            print(f"Editing '{c['name']}' (press Enter to keep current value):")
            new_name = input(f"New Name [{c['name']}]: ").strip()
            new_phone = input(f"New Phone [{c['phone']}]: ").strip()
            new_email = input(f"New Email [{c['email']}]: ").strip()
            new_address = input(f"New Address [{c['address']}]: ").strip()

            if new_name:
                c["name"] = new_name
            if new_phone:
                c["phone"] = new_phone
            if new_email:
                c["email"] = new_email
            if new_address:
                c["address"] = new_address

            save_contacts(contacts)
            print("[Success] Contact updated.")
            return

    print("[Error] Contact with that phone number not found.")


def delete_contact(contacts):
    if not contacts:
        print("\n[Info] No contacts available to delete.")
        return

    phone_key = input("\nEnter exact Phone Number of the contact to delete: ").strip()
    for i, c in enumerate(contacts):
        if c["phone"] == phone_key:
            removed = contacts.pop(i)
            save_contacts(contacts)
            print(f"[Success] Deleted '{removed['name']}' ({removed['phone']}).")
            return

    print("[Error] Contact not found.")


def main():
    contacts = load_contacts()

    while True:
        print("\n==========================================")
        print("            CONTACT BOOK APP              ")
        print("==========================================")
        print("1. Add Contact")
        print("2. View All Contacts (A-Z)")
        print("3. Search Contact (Name / Phone)")
        print("4. Edit Contact")
        print("5. Delete Contact")
        print("6. Exit")

        choice = input("\nSelect an option (1-6): ").strip()

        if choice == "1":
            add_contact(contacts)
        elif choice == "2":
            view_contacts(contacts)
        elif choice == "3":
            search_contact(contacts)
        elif choice == "4":
            edit_contact(contacts)
        elif choice == "5":
            delete_contact(contacts)
        elif choice == "6":
            print("Exiting Contact Book App. Goodbye!")
            break
        else:
            print("[Error] Invalid choice. Please enter 1 to 6.")


if __name__ == "__main__":
    main()