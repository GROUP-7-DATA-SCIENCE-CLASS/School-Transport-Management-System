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