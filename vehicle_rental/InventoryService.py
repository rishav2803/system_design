from typing import Dict, List

from vehicle_rental.Vehicle import Vehicle


class InventoryFilterBuilder:
    def __init__(self, vehicles: List[Vehicle]):
        self._vehicles = vehicles

    def filter_by_state(self, state: str):
        self._vehicles = [
            v for v in self._vehicles if v._parking_stall.branch.state == state
        ]
        return self

    def filter_by_city(self, city: str):
        self._vehicles = [
            v for v in self._vehicles if v._parking_stall.branch.city == city
        ]
        return self

    def get(self):
        return self._vehicles


class InventoryService:
    _INSTANCE = None

    @classmethod
    def get_instance(cls):
        if not cls._INSTANCE:
            cls._INSTANCE = cls()

        return cls._INSTANCE

    def __init__(self):
        self._vehicles: List[Vehicle] = []
        # Indexed Filters
        # self._city_to_vehicle_map: Dict[str, List[Vehicle]] = {}
        # self._state_to_vehicle_map: Dict[str, List[Vehicle]] = {}

    def query(self) -> InventoryFilterBuilder:
        return InventoryFilterBuilder(self._vehicles)

    def add_vehicle(self, vehicle: Vehicle):
        self._vehicles.append(vehicle)

    def list_all_vehicles(self):
        for vehicle in self._vehicles:
            print(vehicle.__repr__())


