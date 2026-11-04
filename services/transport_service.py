
from exceptions import TransportError

from models.learner import Learner
from models.vehicle import Bus, Minibus, Van
from models.route import Route
from models.subscription import Subscription


class TransportService:
    """
    Coordinates the operations of the school transport system.

    Manages learners, vehicles, routes and subscriptions.
    """

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

    # -----------------------------------------
    # COLLECTION ACCESS
    # -----------------------------------------

    @property
    def learners(self):
        return list(self._learners.values())

    @property
    def vehicles(self):
        return list(self._vehicles.values())

    @property
    def routes(self):
        return list(self._routes.values())

    # -----------------------------------------
    # SEARCH AND RETRIEVAL
    # -----------------------------------------

    @staticmethod
    def _find(store, key, label):
        key = " ".join(str(key).split()).upper()

        if key not in store:
            raise TransportError(
                f"No {label} found with '{key}'."
            )

        return store[key]

    def get_learner(self, learner_id):
        return self._find(
            self._learners, learner_id, "learner"
        )

    def get_vehicle(self, registration):
        return self._find(
            self._vehicles, registration, "vehicle"
        )

    def get_route(self, route_id):
        return self._find(
            self._routes, route_id, "route"
        )

    # -----------------------------------------
    # LEARNER REGISTRATION
    # -----------------------------------------

    def register_learner(self, name, grade, contact):
        learner = Learner(
            f"L{len(self._learners) + 1:03d}",
            name,
            grade,
            contact
        )

        self._learners[learner.learner_id] = learner

        return learner

    # -----------------------------------------
    # VEHICLE MANAGEMENT
    # -----------------------------------------

    def add_vehicle(self, vehicle_type, registration, capacity):
        vehicle_class = self.VEHICLE_TYPES.get(
            str(vehicle_type).strip().lower()
        )

        if vehicle_class is None:
            raise TransportError(
                "Vehicle type must be bus, minibus or van."
            )

        vehicle = vehicle_class(registration, capacity)

        if vehicle.registration in self._vehicles:
            raise TransportError(
                f"Vehicle {vehicle.registration} already exists."
            )

        self._vehicles[vehicle.registration] = vehicle

        return vehicle

    # -----------------------------------------
    # ROUTE MANAGEMENT
    # -----------------------------------------

    def create_route(self, name, stops, distance_km):
        route = Route(
            f"R{len(self._routes) + 1:02d}",
            name,
            stops,
            distance_km
        )

        self._routes[route.route_id] = route

        return route

    def assign_vehicle_to_route(self, registration, route_id):
        vehicle = self.get_vehicle(registration)
        route = self.get_route(route_id)

        route.add_vehicle(vehicle)

        return vehicle, route

    # -----------------------------------------
    # SUBSCRIPTION MANAGEMENT
    # -----------------------------------------

    def active_subscription(self, learner_id):
        learner_id = str(learner_id).strip().upper()

        return next(
            (
                sub for sub in self._subscriptions
                if sub.active
                and sub.learner.learner_id == learner_id
            ),
            None
        )

    def subscribe(self, learner_id, route_id, registration):
        learner = self.get_learner(learner_id)
        route = self.get_route(route_id)
        vehicle = self.get_vehicle(registration)

        if self.active_subscription(learner.learner_id):
            raise TransportError(
                f"{learner.name} is already assigned to a vehicle. "
                "Remove the learner first."
            )

        if vehicle.route is not route:
            raise TransportError(
                f"Vehicle {vehicle.registration} does not serve "
                f"route '{route.name}'."
            )

        vehicle.board(learner)

        subscription = Subscription(
            f"S{len(self._subscriptions) + 1:03d}",
            learner,
            route,
            vehicle
        )

        self._subscriptions.append(subscription)

        return subscription

    def unsubscribe(self, learner_id):
        learner = self.get_learner(learner_id)

        subscription = self.active_subscription(
            learner.learner_id
        )

        if subscription is None:
            raise TransportError(
                f"{learner.name} is not using school transport."
            )

        subscription.vehicle.alight(learner)
        subscription.active = False

        return subscription

    # -----------------------------------------
    # LEARNER SEARCH
    # -----------------------------------------

    def search_learners(self, term):
        term = str(term).strip().lower()

        if not term:
            raise ValueError("Search term cannot be empty.")

        return [
            learner
            for learner in self._learners.values()
            if (
                term == learner.learner_id.lower()
                or term in learner.name.lower()
            )
        ]

    # -----------------------------------------
    # FINANCIAL REPORTING
    # -----------------------------------------

    def monthly_position(self):
        """
        Returns a list containing:
        (vehicle, monthly income, operating cost)
        """

        rows = []

        for vehicle in self._vehicles.values():

            if vehicle.route:

                income = sum(
                    sub.monthly_charge
                    for sub in self._subscriptions
                    if sub.active and sub.vehicle is vehicle
                )

                operating_cost = (
                    vehicle.calculate_operating_cost(
                        vehicle.route.distance_km
                    )
                )

                rows.append(
                    (vehicle, income, operating_cost)
                )

        return rows
