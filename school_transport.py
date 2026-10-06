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
