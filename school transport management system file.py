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