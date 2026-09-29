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
    
