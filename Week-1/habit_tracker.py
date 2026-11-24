import json
from datetime import date

# Data store karva mate JSON file nu naam
DATA_FILE = "habits_data.json"

def load_data():
    """JSON file mathi data load kare chhe, jo file na hoy to empty dictionary return kare chhe."""
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_data(data):
    """Data ne JSON file ma save kare chhe."""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def habit_tracker():
    habits = load_data()
    today = str(date.today())

    while True:
        print("\n==============================")
        print("       HABIT TRACKER          ")
        print("==============================")
        print("1. View Habits & Today's Status")
        print("2. Add New Habit")
        print("3. Mark Habit Complete for Today")
        print("4. Delete Habit")
        print("5. Exit")
        
        choice = input("\nSelect an option (1-5): ").strip()

        if choice == "1":
            if not habits:
                print("\n[Info] No habits tracked yet. Add a new habit first!")
                continue
            
            print(f"\n--- Today's Status ({today}) ---")
            for habit, records in habits.items():
                completed_dates = records.get("completed_dates", [])
                status = "Done ✅" if today in completed_dates else "Pending ⏳"
                streak = records.get("streak", 0)
                print(f"• {habit} -> Status: {status} | Streak: {streak} days")

        elif choice == "2":
            habit_name = input("\nEnter new habit name (e.g., Read 30 mins): ").strip()
            if habit_name:
                if habit_name not in habits:
                    habits[habit_name] = {"completed_dates": [], "streak": 0}
                    save_data(habits)
                    print(f"[Success] Habit '{habit_name}' added successfully!")
                else:
                    print("[Warning] This habit already exists.")
            else:
                print("[Error] Habit name cannot be empty.")

        elif choice == "3":
            if not habits:
                print("\n[Info] No habits available to mark complete.")
                continue
                
            habit_name = input("\nEnter habit name to mark complete: ").strip()
            if habit_name in habits:
                completed_dates = habits[habit_name]["completed_dates"]
                if today not in completed_dates:
                    completed_dates.append(today)
                    habits[habit_name]["streak"] += 1
                    save_data(habits)
                    print(f"[Success] Great job! '{habit_name}' marked complete for today.")
                else:
                    print("[Info] You have already marked this habit complete today!")
            else:
                print("[Error] Habit not found.")

        elif choice == "4":
            if not habits:
                print("\n[Info] No habits available to delete.")
                continue
                
            habit_name = input("\nEnter habit name to delete: ").strip()
            if habit_name in habits:
                del habits[habit_name]
                save_data(habits)
                print(f"[Success] Habit '{habit_name}' deleted successfully.")
            else:
                print("[Error] Habit not found.")

        elif choice == "5":
            print("\nExiting Habit Tracker. Keep building great habits!")
            break
        else:
            print("[Error] Invalid choice. Please select between 1 and 5.")

if __name__ == "__main__":
    habit_tracker()