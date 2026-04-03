from abc import ABC, abstractmethod
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')

class Vehicle(ABC):
    def __init__(self, make: str, model: str) -> None:
        self.make = make
        self.model = model

    @abstractmethod
    def start_engine(self) -> None:
        pass

class Car(Vehicle, ABC):
    pass

class Motorcycle(Vehicle, ABC):
    pass

class USCar(Car):
    def start_engine(self) -> None:
        logging.info(f"Car: {self.make} {self.model} (US Spec) - Двигун запущено")

class USMotorcycle(Motorcycle):
    def start_engine(self) -> None:
        logging.info(f"Motorcycle: {self.make} {self.model} (US Spec) - Мотор заведено")

class EUCar(Car):
    def start_engine(self) -> None:
        logging.info(f"Car: {self.make} {self.model} (EU Spec) - Двигун запущено")

class EUMotorcycle(Motorcycle):
    def start_engine(self) -> None:
        logging.info(f"Motorcycle: {self.make} {self.model} (EU Spec) - Мотор заведено")

class VehicleFactory(ABC):
    @abstractmethod
    def create_car(self, make: str, model: str) -> Car:
        pass

    @abstractmethod
    def create_motorcycle(self, make: str, model: str) -> Motorcycle:
        pass

class USVehicleFactory(VehicleFactory):
    def create_car(self, make: str, model: str) -> Car:
        return USCar(make, model)

    def create_motorcycle(self, make: str, model: str) -> Motorcycle:
        return USMotorcycle(make, model)

class EUVehicleFactory(VehicleFactory):
    def create_car(self, make: str, model: str) -> Car:
        return EUCar(make, model)

    def create_motorcycle(self, make: str, model: str) -> Motorcycle:
        return EUMotorcycle(make, model)


def client_code(factory: VehicleFactory) -> None:
    car = factory.create_car("Ford", "Mustang")
    bike = factory.create_motorcycle("Harley-Davidson", "Sportster")
    
    car.start_engine()
    bike.start_engine()

if __name__ == "__main__":
    print("--- USA market ---")
    client_code(USVehicleFactory())

    print("--- EU market ---")
    client_code(EUVehicleFactory())