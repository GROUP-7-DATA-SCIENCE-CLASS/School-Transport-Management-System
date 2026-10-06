
import re
from abc import ABC, abstractmethod

# ============================== EXCEPTIONS ==============================
class TransportError(Exception):
    """A business rule of the system was broken."""


class VehicleFullError(TransportError):
    """The vehicle has no free seats."""

# ============================== LEARNER ==============================
class Learner:
    """Holds one learner's details. Name and contact are validated by setters."""

    def __init__(self, learner_id, name, grade, contact):
        self._learner_id = learner_id            # protected, read-only
        self.name = name                         # setter validates
        self.contact = contact                   # setter validates
        if not str(grade).strip():
            raise ValueError("Grade/class cannot be empty.")
        self.grade = str(grade).strip().upper()  # public attribute
    
    @property
    def learner_id(self):
        return self._learner_id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        value = " ".join(str(value).split())
        if len(value) < 2 or not all(c.isalpha() or c in " -'." for c in value):
            raise ValueError("Name must have at least 2 characters and contain letters only.")
        self._name = value.title()

    @property
    def contact(self):
        return self._contact

    @contact.setter
    def contact(self, value):
        value = str(value).replace(" ", "")
        if not re.fullmatch(r"0\d{9}|\+256\d{9}", value):
            raise ValueError("Guardian contact must be 10 digits starting with 0 (or +256 and 9 digits).")
        self._contact = value

    def __str__(self):
        return f"{self._learner_id} | {self._name} | {self.grade} | Guardian: {self._contact}"


# ============================== VEHICLES ==============================
class TransportVehicle(ABC):
    """Abstract superclass: cannot be instantiated. Subclasses must implement both abstract methods."""

    TYPE_NAME = "Vehicle"
    MIN_CAPACITY, MAX_CAPACITY = 1, 100
    SCHOOL_DAYS = 22

    def _init_(self, registration, capacity):
        self.__passengers = []                   # private: only board()/alight() may change it
        self._route = None                       # protected
        registration = str(registration).strip().upper()
        if not re.fullmatch(r"[A-Z0-9 ]{5,10}", registration):
            raise ValueError("Registration must be 5-10 letters/digits (e.g. UBA 123X).")
        self._registration = registration
        self.capacity = capacity                 # setter validates

    @property
    def registration(self):
        return self._registration

    @property
    def capacity(self):
        return self._capacity

    @capacity.setter
    def capacity(self, value):
        if not isinstance(value, int) or not self.MIN_CAPACITY <= value <= self.MAX_CAPACITY:
            raise ValueError(f"A {self.TYPE_NAME} must have {self.MIN_CAPACITY}-{self.MAX_CAPACITY} seats.")
        self._capacity = value

    @property
    def passengers(self):
        return tuple(self.__passengers)          # read-only copy

    @property
    def available_seats(self):
        return self.capacity - len(self._passengers)

    @property
    def route(self):
        return self._route

    def assign_route(self, route):
        if self._route is not None:
            raise TransportError(f"{self._registration} already serves route '{self._route.name}'.")
        self._route = route

    def board(self, learner):
        if self.available_seats == 0:
            raise VehicleFullError(f"{self.TYPE_NAME} {self._registration} is full ({self._capacity}/{self._capacity}).")
        self.__passengers.append(learner)

    def alight(self, learner):
        self.__passengers.remove(learner)

    @abstractmethod
    def calculate_operating_cost(self, distance_km):
        """Monthly cost of running the vehicle on a route of this one-way length."""

    @abstractmethod
    def transport_charge(self, distance_km):
        """Monthly fee for ONE learner on a route of this one-way length."""

    def _str_(self):
        route = self._route.name if self._route else "unassigned"
        used = self._capacity - self.available_seats
        return f"{self.TYPE_NAME:<8}{self._registration:<10} seats {used}/{self._capacity} | route: {route}"

class Bus(TransportVehicle):
    TYPE_NAME, MIN_CAPACITY, MAX_CAPACITY = "Bus", 31, 70

    def calculate_operating_cost(self, distance_km):       # driver + conductor, heavy fuel use
        return round(distance_km * 2 * self.SCHOOL_DAYS * 3500 + 600_000 + 250_000)

    def transport_charge(self, distance_km):
        return round(60_000 + 1_500 * distance_km)


class Minibus(TransportVehicle):
    TYPE_NAME, MIN_CAPACITY, MAX_CAPACITY = "Minibus", 15, 30

    def calculate_operating_cost(self, distance_km):       # driver only
        return round(distance_km * 2 * self.SCHOOL_DAYS * 2200 + 400_000 + 150_000)

    def transport_charge(self, distance_km):
        return round(80_000 + 2_000 * distance_km)


class Van(TransportVehicle):
    TYPE_NAME, MIN_CAPACITY, MAX_CAPACITY = "Van", 8, 14

    def calculate_operating_cost(self, distance_km):       # driver only, cheapest fuel
        return round(distance_km * 2 * self.SCHOOL_DAYS * 1400 + 300_000 + 100_000)

    def transport_charge(self, distance_km):               # few seats, so a higher fee each
        return round(100_000 + 2_500 * distance_km)
    
        return round(100_000 + 2_500 * distance_km)
    
    
# ============================== ROUTE ==============================
class Route:
    """A named route with stops. Aggregates the vehicles that serve it."""

    def __init__(self, route_id, name, stops, distance_km):
        self._route_id = route_id
        self._vehicles = []
        name = " ".join(str(name).split())
        stops = [s.strip() for s in stops if s.strip()]
        if len(name) < 3:
            raise ValueError("Route name must be at least 3 characters.")
        if len(stops) < 2:
            raise ValueError("A route needs at least 2 stops.")
        self.name, self.stops = name, stops
        self.distance_km = distance_km           # setter validates

    @property
    def route_id(self):
        return self._route_id

    @property
    def distance_km(self):
        return self._distance_km

    @distance_km.setter
    def distance_km(self, value):
        if not 0 < value <= 200:
            raise ValueError("Distance must be more than 0 and at most 200 km.")
        self._distance_km = float(value)

    @property
    def vehicles(self):
        return tuple(self._vehicles)

    def add_vehicle(self, vehicle):
        vehicle.assign_route(self)               # raises if the vehicle already has a route
        self._vehicles.append(vehicle)

    def seats_used_and_total(self):
        return (sum(len(v.passengers) for v in self._vehicles), sum(v.capacity for v in self._vehicles))

    def __str__(self):
        return f"{self._route_id} | {self.name} | {self._distance_km:g} km | {' > '.join(self.stops)}"

# ============================== SUBSCRIPTION ==============================
class Subscription:
    """Association class: one learner on one route in one vehicle, with the monthly charge."""

    def __init__(self, sub_id, learner, route, vehicle):
        self._sub_id = sub_id
        self.learner, self.route, self.vehicle = learner, route, vehicle
        self._monthly_charge = vehicle.transport_charge(route.distance_km)   # polymorphic call
        self.active = True

    @property
    def monthly_charge(self):
        return self._monthly_charge

# ============================== TRANSPORT SYSTEM ==============================
class TransportSystem:
    """Coordinator. Owns (composes) learners, vehicles, routes and subscriptions."""

    VEHICLE_TYPES = {"bus": Bus, "minibus": Minibus, "van": Van}

    def __init__(self, school_name="Sunrise Junior School"):
        self.school_name = school_name
        self._learners, self._vehicles, self._routes = {}, {}, {}
        self._subscriptions = []

    learners = property(lambda self: list(self._learners.values()))
    vehicles = property(lambda self: list(self._vehicles.values()))
    routes = property(lambda self: list(self._routes.values()))

    @staticmethod
    def _find(store, key, label):
        key = str(key).strip().upper()
        if key not in store:
            raise TransportError(f"No {label} found with '{key}'.")
        return store[key]

    def get_learner(self, learner_id):
        return self._find(self._learners, learner_id, "learner")

    def get_vehicle(self, registration):
        return self._find(self._vehicles, registration, "vehicle")

    def get_route(self, route_id):
        return self._find(self._routes, route_id, "route")

    # ---- registration ----
    def register_learner(self, name, grade, contact):
        learner = Learner(f"L{len(self._learners) + 1:03d}", name, grade, contact)
        self._learners[learner.learner_id] = learner
        return learner

    def add_vehicle(self, vehicle_type, registration, capacity):
        cls = self.VEHICLE_TYPES.get(str(vehicle_type).strip().lower())
        if cls is None:
            raise TransportError("Vehicle type must be bus, minibus or van.")
        vehicle = cls(registration, capacity)
        if vehicle.registration in self._vehicles:
            raise TransportError(f"Vehicle {vehicle.registration} already exists.")
        self._vehicles[vehicle.registration] = vehicle
        return vehicle

    def create_route(self, name, stops, distance_km):
        route = Route(f"R{len(self._routes) + 1:02d}", name, stops, distance_km)
        self._routes[route.route_id] = route
        return route

    def assign_vehicle_to_route(self, registration, route_id):
        vehicle, route = self.get_vehicle(registration), self.get_route(route_id)
        route.add_vehicle(vehicle)
        return vehicle, route

    # ---- transactions ----
    def active_subscription(self, learner_id):
        learner_id = str(learner_id).strip().upper()
        return next((s for s in self._subscriptions if s.active and s.learner.learner_id == learner_id), None)

    def subscribe(self, learner_id, route_id, registration):
        learner, route, vehicle = self.get_learner(learner_id), self.get_route(route_id), self.get_vehicle(registration)
        if self.active_subscription(learner.learner_id):
            raise TransportError(f"{learner.name} is already assigned to a vehicle. Remove the learner first.")
        if vehicle.route is not route:
            raise TransportError(f"Vehicle {vehicle.registration} does not serve route '{route.name}'.")
        vehicle.board(learner)                   # raises VehicleFullError when full
        sub = Subscription(f"S{len(self._subscriptions) + 1:03d}", learner, route, vehicle)
        self._subscriptions.append(sub)
        return sub

    def unsubscribe(self, learner_id):
        learner = self.get_learner(learner_id)
        sub = self.active_subscription(learner.learner_id)
        if sub is None:
            raise TransportError(f"{learner.name} is not using school transport.")
        sub.vehicle.alight(learner)
        sub.active = False
        return sub

    def search_learners(self, term):
        term = str(term).strip().lower()
        if not term:
            raise ValueError("Search term cannot be empty.")
        return [l for l in self._learners.values() if term == l.learner_id.lower() or term in l.name.lower()]

    def monthly_position(self):
        """(vehicle, income, operating cost) for every vehicle that serves a route."""
        rows = []
        for v in self._vehicles.values():
            if v.route:
                income = sum(s.monthly_charge for s in self._subscriptions if s.active and s.vehicle is v)
                rows.append((v, income, v.calculate_operating_cost(v.route.distance_km)))
        return rows


# ============================== SAMPLE DATA ==============================
def load_sample_data(system):
    names = ["Namukasa Grace", "Okello David", "Kato Brian", "Nakato Sarah", "Mugabi Joel", "Atim Ruth",
             "Ssemwogerere Paul", "Achieng Mercy", "Byaruhanga Ian", "Nabirye Faith", "Opio Samuel", "Tumusiime Esther"]
    learners = [system.register_learner(n, "P5", f"0772{100000 + i}") for i, n in enumerate(names)]
    ntinda = system.create_route("Ntinda - Kampala Road", ["Ntinda", "Kisaasi", "Bukoto", "Kampala Road"], 9.5)
    kireka = system.create_route("Kireka - Kyambogo", ["Kireka", "Banda", "Kyambogo"], 14)
    van = system.add_vehicle("van", "UBA 101A", 8)
    bus = system.add_vehicle("bus", "UBE 202B", 40)
    system.add_vehicle("minibus", "UBF 303C", 18)          # left unassigned on purpose
    system.assign_vehicle_to_route(van.registration, ntinda.route_id)
    system.assign_vehicle_to_route(bus.registration, kireka.route_id)
    for l in learners[:8]:                                 # fills the 8-seat van
        system.subscribe(l.learner_id, ntinda.route_id, van.registration)
    for l in learners[8:10]:
        system.subscribe(l.learner_id, kireka.route_id, bus.registration)
  
    
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