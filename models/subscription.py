class Subscription:
    """
    Association class: one learner on one route
    in one vehicle, with a monthly transport charge.
    """

    def __init__(self, sub_id, learner, route, vehicle):
        self._sub_id = sub_id

        self.learner = learner
        self.route = route
        self.vehicle = vehicle

        # Polymorphism:
        # The vehicle determines the learner's monthly charge.
        self._monthly_charge = vehicle.transport_charge(
            route.distance_km
        )

        self.active = True

    @property
    def sub_id(self):
        return self._sub_id

    @property
    def monthly_charge(self):
        return self._monthly_charge

    def __str__(self):
        status = "Active" if self.active else "Inactive"

        return (
            f"{self._sub_id} | {self.learner.name} | "
            f"{self.route.name} | {self.vehicle.registration} | "
            f"UGX {self._monthly_charge:,.0f} | {status}"
        )