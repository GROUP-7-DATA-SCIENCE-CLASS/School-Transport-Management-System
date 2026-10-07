import re
from abc import ABC, abstractmethod


# ============================================================
# CUSTOM EXCEPTIONS
# ============================================================

class TransportError(Exception):
    """Raised when a transport business rule is violated."""


class VehicleFullError(TransportError):
    """Raised when a vehicle has no available seats."""


# ============================================================
# LEARNER CLASS
# ============================================================

class Learner:
    """
    Represents a learner using the school transport system.

    Encapsulation is demonstrated through properties for
    name and contact.
    """

    def __init__(self, learner_id, name, grade, contact):
        self._learner_id = learner_id
        self.name = name
        self.contact = contact
        self.grade = str(grade).strip().upper()

        if not self.grade:
            raise ValueError("Grade/class cannot be empty.")

    @property
    def learner_id(self):
        return self._learner_id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        value = " ".join(str(value).split())

        if len(value) < 2 or not all(
            c.isalpha() or c in " -'." for c in value
        ):
            raise ValueError(
                "Name must contain letters and be at least 2 characters."
            )

        self._name = value.title()

    @property
    def contact(self):
        return self._contact

    @contact.setter
    def contact(self, value):
        value = str(value).replace(" ", "")

        if not re.fullmatch(r"0\d{9}|\+256\d{9}", value):
            raise ValueError("Enter a valid Ugandan contact number.")

        self._contact = value

    def __str__(self):
        return (
            f"{self.learner_id} | {self.name} | "
            f"{self.grade} | {self.contact}"
        )


# ============================================================
# ABSTRACT VEHICLE CLASS
# ============================================================

class TransportVehicle(ABC):
    """
    Abstract base class for all school transport vehicles.

    Abstraction:
        Defines the common structure of every vehicle.

    Encapsulation:
        Passenger information is stored privately.

    Inheritance:
        Bus, Minibus and Van inherit from this class.

    Polymorphism:
        Subclasses provide their own implementations of
        transport_charge() and calculate_operating_cost().
    """

    TYPE_NAME = "Vehicle"
    MIN_CAPACITY = 1
    MAX_CAPACITY = 100
    SCHOOL_DAYS = 22

    def __init__(self, registration, capacity):
        self._registration = str(registration).strip().upper()

        if not re.fullmatch(
            r"[A-Z0-9 ]{5,10}", self._registration
        ):
            raise ValueError(
                "Invalid registration. Example: UBA 123X."
            )

        self.capacity = capacity
        self._route = None

        # Encapsulation: private attribute
        self.__passengers = []

    @property
    def registration(self):
        return self._registration

    @property
    def capacity(self):
        return self._capacity

    @capacity.setter
    def capacity(self, value):
        if not isinstance(value, int):
            raise ValueError("Capacity must be a whole number.")

        if not self.MIN_CAPACITY <= value <= self.MAX_CAPACITY:
            raise ValueError(
                f"{self.TYPE_NAME} capacity must be between "
                f"{self.MIN_CAPACITY} and {self.MAX_CAPACITY}."
            )

        self._capacity = value

    @property
    def passengers(self):
        # Return a tuple so outside code cannot modify the list directly
        return tuple(self.__passengers)

    @property
    def available_seats(self):
        return self.capacity - len(self.__passengers)

    @property
    def route(self):
        return self._route

    def assign_route(self, route):
        if self._route is not None:
            raise TransportError(
                f"{self.registration} already serves "
                f"{self.route.name}."
            )

        self._route = route

    def board(self, learner):
        if learner in self.__passengers:
            raise TransportError(
                "Learner is already a passenger."
            )

        if self.available_seats <= 0:
            raise VehicleFullError(
                f"{self.registration} is full."
            )

        self.__passengers.append(learner)

    def alight(self, learner):
        if learner not in self.__passengers:
            raise TransportError(
                "Learner is not a passenger."
            )

        self.__passengers.remove(learner)

    @abstractmethod
    def calculate_operating_cost(self, distance_km):
        """Calculate the monthly operating cost."""

    @abstractmethod
    def transport_charge(self, distance_km):
        """Calculate the monthly charge per learner."""

    def __str__(self):
        route = self.route.name if self.route else "Unassigned"
        used = len(self.passengers)

        return (
            f"{self.TYPE_NAME:<8} "
            f"{self.registration:<10} "
            f"{used}/{self.capacity} seats | "
            f"{route}"
        )


# ============================================================
# INHERITED VEHICLE CLASSES
# ============================================================

class Bus(TransportVehicle):
    TYPE_NAME = "Bus"
    MIN_CAPACITY = 31
    MAX_CAPACITY = 70

    def calculate_operating_cost(self, distance_km):
        return round(
            distance_km * 2 * self.SCHOOL_DAYS * 3500
            + 850_000
        )

    def transport_charge(self, distance_km):
        return round(60_000 + 1_500 * distance_km)


class Minibus(TransportVehicle):
    TYPE_NAME = "Minibus"
    MIN_CAPACITY = 15
    MAX_CAPACITY = 30

    def calculate_operating_cost(self, distance_km):
        return round(
            distance_km * 2 * self.SCHOOL_DAYS * 2200
            + 550_000
        )

    def transport_charge(self, distance_km):
        return round(80_000 + 2_000 * distance_km)


class Van(TransportVehicle):
    TYPE_NAME = "Van"
    MIN_CAPACITY = 8
    MAX_CAPACITY = 14

    def calculate_operating_cost(self, distance_km):
        return round(
            distance_km * 2 * self.SCHOOL_DAYS * 1400
            + 400_000
        )

    def transport_charge(self, distance_km):
        return round(100_000 + 2_500 * distance_km)


# ============================================================
# ROUTE CLASS
# ============================================================

class Route:
    def __init__(self, route_id, name, stops, distance_km):
        self._route_id = route_id
        self.name = " ".join(str(name).split())

        self.stops = [
            str(stop).strip()
            for stop in stops
            if str(stop).strip()
        ]

        self.distance_km = distance_km
        self._vehicles = []

        if len(self.name) < 3:
            raise ValueError("Route name is too short.")

        if len(self.stops) < 2:
            raise ValueError(
                "A route needs at least two stops."
            )

    @property
    def route_id(self):
        return self._route_id

    @property
    def distance_km(self):
        return self._distance_km

    @distance_km.setter
    def distance_km(self, value):
        value = float(value)

        if not 0 < value <= 200:
            raise ValueError(
                "Distance must be between 0 and 200 km."
            )

        self._distance_km = value

    @property
    def vehicles(self):
        return tuple(self._vehicles)

    def add_vehicle(self, vehicle):
        vehicle.assign_route(self)
        self._vehicles.append(vehicle)

    def __str__(self):
        return (
            f"{self.route_id} | {self.name} | "
            f"{self.distance_km:g} km | "
            f"{' > '.join(self.stops)}"
        )


# ============================================================
# SUBSCRIPTION CLASS
# ============================================================

class Subscription:
    """
    Connects a learner, route and vehicle.

    The transport charge is calculated through the vehicle
    object, demonstrating polymorphism.
    """

    def __init__(self, subscription_id, learner, route, vehicle):
        self._subscription_id = subscription_id
        self.learner = learner
        self.route = route
        self.vehicle = vehicle

        # Polymorphism
        self._monthly_charge = vehicle.transport_charge(
            route.distance_km
        )

        self.active = True

    @property
    def monthly_charge(self):
        return self._monthly_charge


# ============================================================
# TRANSPORT SYSTEM
# ============================================================

class TransportSystem:

    VEHICLE_TYPES = {
        "bus": Bus,
        "minibus": Minibus,
        "van": Van
    }

    def __init__(self, school_name="Sunrise Junior School"):
        self.school_name = school_name

        self._learners = {}
        self._vehicles = {}
        self._routes = {}
        self._subscriptions = []

        self._learner_no = 0
        self._route_no = 0
        self._subscription_no = 0

    # -------------------- Helpers --------------------

    @staticmethod
    def _key(value):
        return str(value).strip().upper()

    def _get(self, store, key, label):
        key = self._key(key)

        if key not in store:
            raise TransportError(
                f"No {label} found with '{key}'."
            )

        return store[key]

    # -------------------- Properties --------------------

    @property
    def learners(self):
        return list(self._learners.values())

    @property
    def vehicles(self):
        return list(self._vehicles.values())

    @property
    def routes(self):
        return list(self._routes.values())

    # -------------------- Get objects --------------------

    def get_learner(self, learner_id):
        return self._get(
            self._learners, learner_id, "learner"
        )

    def get_vehicle(self, registration):
        return self._get(
            self._vehicles, registration, "vehicle"
        )

    def get_route(self, route_id):
        return self._get(
            self._routes, route_id, "route"
        )

    # -------------------- Learners --------------------

    def register_learner(self, name, grade, contact):
        self._learner_no += 1

        learner = Learner(
            f"L{self._learner_no:03d}",
            name,
            grade,
            contact
        )

        self._learners[learner.learner_id] = learner

        return learner

    # -------------------- Vehicles --------------------

    def add_vehicle(self, vehicle_type, registration, capacity):
        vehicle_class = self.VEHICLE_TYPES.get(
            str(vehicle_type).strip().lower()
        )

        if vehicle_class is None:
            raise TransportError(
                "Type must be bus, minibus or van."
            )

        vehicle = vehicle_class(
            registration,
            int(capacity)
        )

        if vehicle.registration in self._vehicles:
            raise TransportError(
                "Vehicle already exists."
            )

        self._vehicles[vehicle.registration] = vehicle

        return vehicle

    # -------------------- Routes --------------------

    def create_route(self, name, stops, distance):
        self._route_no += 1

        route = Route(
            f"R{self._route_no:02d}",
            name,
            stops,
            distance
        )

        self._routes[route.route_id] = route

        return route

    def assign_vehicle_to_route(
        self,
        registration,
        route_id
    ):
        vehicle = self.get_vehicle(registration)
        route = self.get_route(route_id)

        route.add_vehicle(vehicle)

        return vehicle, route

    # -------------------- Subscriptions --------------------

    def active_subscription(self, learner_id):
        learner_id = self._key(learner_id)

        return next(
            (
                subscription
                for subscription in self._subscriptions
                if (
                    subscription.active
                    and subscription.learner.learner_id
                    == learner_id
                )
            ),
            None
        )

    def subscribe(
        self,
        learner_id,
        route_id,
        registration
    ):
        learner = self.get_learner(learner_id)
        route = self.get_route(route_id)
        vehicle = self.get_vehicle(registration)

        if self.active_subscription(
            learner.learner_id
        ):
            raise TransportError(
                "Learner already has an active subscription."
            )

        if vehicle.route is not route:
            raise TransportError(
                "Vehicle does not serve this route."
            )

        vehicle.board(learner)

        try:
            self._subscription_no += 1

            subscription = Subscription(
                f"S{self._subscription_no:03d}",
                learner,
                route,
                vehicle
            )

            self._subscriptions.append(subscription)

            return subscription

        except Exception:
            vehicle.alight(learner)
            self._subscription_no -= 1
            raise

    def unsubscribe(self, learner_id):
        learner = self.get_learner(learner_id)

        subscription = self.active_subscription(
            learner.learner_id
        )

        if subscription is None:
            raise TransportError(
                "Learner has no active subscription."
            )

        subscription.vehicle.alight(learner)
        subscription.active = False

        return subscription

    # -------------------- Search --------------------

    def search_learners(self, term):
        term = str(term).strip().lower()

        if not term:
            raise ValueError(
                "Search term cannot be empty."
            )

        return [
            learner
            for learner in self.learners
            if (
                term == learner.learner_id.lower()
                or term in learner.name.lower()
            )
        ]

    # -------------------- Financial report --------------------

    def monthly_position(self):
        rows = []

        for vehicle in self.vehicles:

            if vehicle.route:

                income = sum(
                    subscription.monthly_charge
                    for subscription in self._subscriptions
                    if (
                        subscription.active
                        and subscription.vehicle is vehicle
                    )
                )

                # Polymorphism
                cost = vehicle.calculate_operating_cost(
                    vehicle.route.distance_km
                )

                rows.append(
                    (
                        vehicle,
                        income,
                        cost,
                        income - cost
                    )
                )

        return rows


# ============================================================
# SAMPLE DATA
# ============================================================

def load_sample_data(system):

    names = [
        "Namukasa Grace",
        "Okello David",
        "Kato Brian",
        "Nakato Sarah",
        "Mugabi Joel",
        "Atim Ruth",
        "Ssemwogerere Paul",
        "Achieng Mercy",
        "Byaruhanga Ian",
        "Nabirye Faith",
        "Opio Samuel",
        "Tumusiime Esther"
    ]

    learners = [
        system.register_learner(
            name,
            "P5",
            f"0772{100000 + i}"
        )
        for i, name in enumerate(names)
    ]

    route1 = system.create_route(
        "Ntinda - Kampala Road",
        [
            "Ntinda",
            "Kisaasi",
            "Bukoto",
            "Kampala Road"
        ],
        9.5
    )

    route2 = system.create_route(
        "Kireka - Kyambogo",
        [
            "Kireka",
            "Banda",
            "Kyambogo"
        ],
        14
    )

    van = system.add_vehicle(
        "van",
        "UBA 101A",
        8
    )

    bus = system.add_vehicle(
        "bus",
        "UBE 202B",
        40
    )

    system.add_vehicle(
        "minibus",
        "UBF 303C",
        18
    )

    system.assign_vehicle_to_route(
        van.registration,
        route1.route_id
    )

    system.assign_vehicle_to_route(
        bus.registration,
        route2.route_id
    )

    # Fill the van
    for learner in learners[:8]:
        system.subscribe(
            learner.learner_id,
            route1.route_id,
            van.registration
        )

    # Put two learners in the bus
    for learner in learners[8:10]:
        system.subscribe(
            learner.learner_id,
            route2.route_id,
            bus.registration
        )


# ============================================================
# MENU HELPERS
# ============================================================

def ask(prompt, converter=str):

    while True:

        value = input(prompt).strip()

        if not value:
            print("Input cannot be empty.")
            continue

        try:
            return converter(value)

        except ValueError:
            print("Enter a valid value.")


def money(value):
    return f"UGX {value:,.0f}"


# ============================================================
# MENU
# ============================================================

class TransportMenu:

    def __init__(self, system):
        self.system = system

    def run(self):

        actions = {
            "1": self.register_learner,
            "2": self.add_vehicle,
            "3": self.create_route,
            "4": self.assign_vehicle,
            "5": self.assign_learner,
            "6": self.remove_learner,
            "7": self.show_passengers,
            "8": self.search_learner,
            "9": self.show_vehicles_routes,
            "10": self.financial_report,
            "11": self.occupancy,
            "12": self.load_sample
        }

        while True:

            print(
                f"\n=== {self.system.school_name} "
                "Transport Management System ==="
            )

            print(
                "\n1. Register learner"
                "\n2. Add vehicle"
                "\n3. Create route"
                "\n4. Assign vehicle to route"
                "\n5. Assign learner"
                "\n6. Remove learner"
                "\n7. Display passengers"
                "\n8. Search learner"
                "\n9. Display vehicles/routes"
                "\n10. Charges and operating costs"
                "\n11. Occupancy summary"
                "\n12. Load sample data"
                "\n0. Exit"
            )

            choice = input("\nChoose an option: ").strip()

            if choice == "0":
                print("Goodbye.")
                return

            try:
                actions[choice]()

            except KeyError:
                print("Invalid menu option.")

            except (TransportError, ValueError) as error:
                print(f"Error: {error}")

    # --------------------------------------------------------
    # OPTION 1
    # --------------------------------------------------------

    def register_learner(self):

        learner = self.system.register_learner(
            ask("Name: "),
            ask("Grade: "),
            ask("Guardian contact: ")
        )

        print(f"Registered: {learner}")

    # --------------------------------------------------------
    # OPTION 2
    # --------------------------------------------------------

    def add_vehicle(self):

        vehicle = self.system.add_vehicle(
            ask("Type (bus/minibus/van): "),
            ask("Registration: "),
            ask("Capacity: ", int)
        )

        print(f"Added: {vehicle}")

    # --------------------------------------------------------
    # OPTION 3
    # --------------------------------------------------------

    def create_route(self):

        name = ask("Route name: ")

        stops = ask(
            "Stops separated by commas: "
        ).split(",")

        distance = ask(
            "Distance in km: ",
            float
        )

        route = self.system.create_route(
            name,
            stops,
            distance
        )

        print(f"Created: {route}")

    # --------------------------------------------------------
    # OPTION 4
    # --------------------------------------------------------

    def assign_vehicle(self):

        vehicle, route = (
            self.system.assign_vehicle_to_route(
                ask("Vehicle registration: "),
                ask("Route ID: ")
            )
        )

        print(
            f"{vehicle.registration} assigned "
            f"to {route.route_id}."
        )

    # --------------------------------------------------------
    # OPTION 5
    # --------------------------------------------------------

    def assign_learner(self):

        subscription = self.system.subscribe(
            ask("Learner ID: "),
            ask("Route ID: "),
            ask("Vehicle registration: ")
        )

        print(
            f"{subscription.learner.name} assigned "
            f"to {subscription.vehicle.registration}."
        )

        print(
            f"Monthly charge: "
            f"{money(subscription.monthly_charge)}"
        )

    # --------------------------------------------------------
    # OPTION 6
    # --------------------------------------------------------

    def remove_learner(self):

        subscription = self.system.unsubscribe(
            ask("Learner ID: ")
        )

        print(
            f"{subscription.learner.name} removed "
            f"from {subscription.vehicle.registration}."
        )

    # --------------------------------------------------------
    # OPTION 7
    # --------------------------------------------------------

    def show_passengers(self):

        registration = input(
            "Vehicle registration "
            "(blank for all): "
        ).strip()

        vehicles = (
            [self.system.get_vehicle(registration)]
            if registration
            else self.system.vehicles
        )

        for vehicle in vehicles:

            print(f"\n{vehicle}")

            if not vehicle.passengers:
                print("  No passengers.")
                continue

            for learner in vehicle.passengers:
                print(f"  {learner}")

    # --------------------------------------------------------
    # OPTION 8
    # --------------------------------------------------------

    def search_learner(self):

        results = self.system.search_learners(
            ask("Search ID or name: ")
        )

        if results:
            for learner in results:
                print(learner)
        else:
            print("No learners found.")

    # --------------------------------------------------------
    # OPTION 9
    # --------------------------------------------------------

    def show_vehicles_routes(self):

        print("\n--- VEHICLES ---")

        if self.system.vehicles:
            for vehicle in self.system.vehicles:
                print(vehicle)
        else:
            print("No vehicles registered.")

        print("\n--- ROUTES ---")

        if self.system.routes:
            for route in self.system.routes:
                print(route)
        else:
            print("No routes created.")

    # --------------------------------------------------------
    # OPTION 10
    # --------------------------------------------------------

    def financial_report(self):

        rows = self.system.monthly_position()

        if not rows:
            print("No vehicles are assigned to routes.")
            return

        print("\n--- MONTHLY FINANCIAL POSITION ---")

        for vehicle, income, cost, net in rows:

            print(
                f"\n{vehicle.registration} ({vehicle.TYPE_NAME})"
            )

            print(
                f"  Income: "
                f"{money(income)}"
            )

            print(
                f"  Operating cost: "
                f"{money(cost)}"
            )

            print(
                f"  Net position: "
                f"{money(net)}"
            )

    # --------------------------------------------------------
    # OPTION 11
    # --------------------------------------------------------

    def occupancy(self):

        print("\n--- OCCUPANCY ---")

        if not self.system.vehicles:
            print("No vehicles registered.")
            return

        for vehicle in self.system.vehicles:

            used = len(vehicle.passengers)

            percentage = (
                used / vehicle.capacity * 100
            )

            print(
                f"{vehicle.registration}: "
                f"{used}/{vehicle.capacity} "
                f"({percentage:.1f}%)"
            )

    # --------------------------------------------------------
    # OPTION 12
    # --------------------------------------------------------

    def load_sample(self):

        load_sample_data(self.system)

        print("Sample data loaded successfully.")


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":

    system = TransportSystem()

    menu = TransportMenu(system)

    menu.run()