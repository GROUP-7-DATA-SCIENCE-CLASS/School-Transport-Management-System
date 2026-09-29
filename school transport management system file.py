# ============================== MENU ==============================
def ask_text(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("  Input cannot be empty.")


def ask_number(prompt, kind=int):
    while True:
        try:
            return kind(input(prompt).strip())
        except ValueError:
            print("  Please enter a valid number.")


def ugx(amount):
    return f"UGX {amount:,.0f}"

class TransportMenu:
    """Only collects input and prints results; all rules live in the classes above."""

    def __init__(self, system):
        self.s = system
        self.actions = {
            "1": ("Register learner", self.register_learner),
            "2": ("Add vehicle", self.add_vehicle),
            "3": ("Create route", self.create_route),
            "4": ("Assign vehicle to route", self.assign_vehicle),
            "5": ("Assign learner to route and vehicle", self.assign_learner),
            "6": ("Remove learner from transport", self.remove_learner),
            "7": ("Display passengers (vehicle / route / all)", self.show_passengers),
            "8": ("Search for a learner", self.search_learner),
            "9": ("Display vehicles and routes", self.show_vehicles_routes),
            "10": ("Transport charges and operating costs", self.charges_report),
            "11": ("Occupancy summary", self.occupancy_summary),
            "12": ("Load sample data", self.load_sample),
        }

    def run(self):
        print(f"\n=== {self.s.school_name} - Transport Management System ===")
        while True:
            print("\nMAIN MENU")
            for key, (label, _) in self.actions.items():
                print(f"  {key:>2}. {label}")
            print("   0. Exit")
            try:
                choice = input("Choose an option: ").strip()
            except EOFError:
                break
            if choice == "0":
                print("Goodbye.")
                break
            if choice not in self.actions:
                print("  Invalid option. Choose a number from the menu.")
                continue
            try:
                self.actions[choice][1]()
            except (ValueError, TransportError) as err:
                print(f"  REJECTED: {err}")