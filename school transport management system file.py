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

    def register_learner(self):
        print("  Registered:", self.s.register_learner(
            ask_text("Learner name: "), ask_text("Grade (e.g. P5): "), ask_text("Guardian contact: ")))

    def add_vehicle(self):
        vtype = ask_text("Vehicle type (bus/minibus/van): ")
        print("  Added:", self.s.add_vehicle(vtype, ask_text("Registration: "), ask_number("Seats: ")))

    def create_route(self):
        name = ask_text("Route name: ")
        stops = ask_text("Stops (comma-separated): ").split(",")
        print("  Created:", self.s.create_route(name, stops, ask_number("One-way distance (km): ", float)))

    def assign_vehicle(self):
        v, r = self.s.assign_vehicle_to_route(ask_text("Vehicle registration: "), ask_text("Route ID: "))
        print(f"  {v.TYPE_NAME} {v.registration} now serves '{r.name}'.")

    def assign_learner(self):
        sub = self.s.subscribe(ask_text("Learner ID: "), ask_text("Route ID: "), ask_text("Vehicle registration: "))
        print(f"  Assigned {sub.learner.name} to {sub.vehicle.registration}; fee {ugx(sub.monthly_charge)}/month.")

    def remove_learner(self):
        sub = self.s.unsubscribe(ask_text("Learner ID: "))
        print(f"  Removed {sub.learner.name}. {sub.vehicle.available_seats} seat(s) now free on {sub.vehicle.registration}.")

    def show_passengers(self):
        target = input("Vehicle registration, route ID, or Enter for all: ").strip()
        if not target:
            vehicles = self.s.vehicles
        else:
            try:
                vehicles = [self.s.get_vehicle(target)]
            except TransportError:
                vehicles = list(self.s.get_route(target).vehicles)
        for v in vehicles:
            print(f"\n{v}")
            for l in v.passengers:
                print(f"    - {l.learner_id} {l.name} ({l.grade})")
            print(f"    Available seats: {v.available_seats}")

    def search_learner(self):
        matches = self.s.search_learners(ask_text("Learner ID or part of name: "))
        for l in matches or []:
            sub = self.s.active_subscription(l.learner_id)
            where = (f"{sub.vehicle.TYPE_NAME} {sub.vehicle.registration} on '{sub.route.name}', "
                     f"{ugx(sub.monthly_charge)}/month") if sub else "not using school transport"
            print(f"  {l}\n      Transport: {where}")
        if not matches:
            print("  No learners matched.")

    def show_vehicles_routes(self):
        print("\nVEHICLES")
        for v in self.s.vehicles:
            print(f"  {v}")
        print("ROUTES")
        for r in self.s.routes:
            print(f"  {r}")

    def charges_report(self):
        print("\nMonthly fee per learner on a 10 km route (same method call, different results):")
        for v in self.s.vehicles:                           # polymorphism
            print(f"  {v.TYPE_NAME:<8}{v.registration:<10}{ugx(v.transport_charge(10))}")
        print("\nActual monthly position of vehicles on routes:")
        for v, income, cost in self.s.monthly_position():
            print(f"  {v.TYPE_NAME} {v.registration:<10} income {ugx(income):>14}  cost {ugx(cost):>14}  net {ugx(income - cost):>15}")

    def occupancy_summary(self):
        vehicles = self.s.vehicles
        seats = sum(v.capacity for v in vehicles)
        free = sum(v.available_seats for v in vehicles)
        print(f"\nOCCUPANCY SUMMARY - {len(self.s.learners)} learners, {len(vehicles)} vehicles, {len(self.s.routes)} routes")
        print(f"  Seats used: {seats - free}/{seats}   Free seats: {free}")
        for r in self.s.routes:
            used, total = r.seats_used_and_total()
            print(f"  Route {r.name}: {used}/{total} seats used")

    def load_sample(self):
        load_sample_data(self.s)
        print("  Sample data loaded. L011 and L012 are unassigned; van UBA 101A is full.")


if __name__ == "__main__":
    TransportMenu(TransportSystem()).run()