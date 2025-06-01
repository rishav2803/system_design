from abc import ABC


class Branch:
    def __init__(self, name: str, state: str, city: str):
        self.name = name
        self.state = state
        self.city = city
        self.stalls = []


class ParkingStall:
    def __init__(self, stall_number: str, branch: Branch):
        self.stall_number = stall_number
        self.branch = branch


class Vehicle(ABC):
    def __init__(
        self,
        license_num,
        capacity,
        barcode,
        status,
        model,
        make,
        manufacturing_year,
        mileage,
        parking_stall: ParkingStall,
    ):
        self.__license_number = license_num
        self.__passenger_capacity = capacity
        self.__barcode = barcode
        self.__status = status
        self.__model = model
        self.__make = make
        self.__manufacturing_year = manufacturing_year
        self.__mileage = mileage
        self.__log = []
        self._parking_stall = parking_stall
