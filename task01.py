from abc import ABC, abstractmethod
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')

class Vehicle(ABC):
    def __init__(self, make: str, model:str, spec:str) -> None:
        self.make = make
        self.model = model
        self.spec = spec

    @abstractmethod
    def start_engine(self) -> None:
        pass

class Car(Vehicle):
    def start_engine(self) -> None:
        logging.info(f"Car: {self.make} {self.model} ({self.spec}) - Двигун запущено")
        
class Motorcycle(Vehicle):
    def start_engine(self) -> None:
        logging.info(f'Motorcycle: {self.make} {self.model} ({self.spec}) — Мотор заведено')

class VehicleFactory(ABC):
    @abstractmethod
    def create_car(self, make: str, model: str) -> Car:
        pass

    @abstractmethod
    def create_motorcycle(self, make: str, model: str) -> Motorcycle:
        pass

class USVehicleFactory(VehicleFactory):
    def create_car(self, make: str, model: str) -> Car:
        return Car(make, model, "US Spec")

    def create_motorcycle(self, make: str, model: str) -> Motorcycle:
        return Motorcycle(make, model, "US Spec")

class EUVehicleFactory(VehicleFactory):
    def create_car(self, make: str, model: str) -> Car:
        return Car(make, model, "EU Spec")

    def create_motorcycle(self, make: str, model: str) -> Motorcycle:
        return Motorcycle(make, model, "EU Spec")

def client_code(factory: VehicleFactory)-> None:
    car = factory.create_car("Ford", "Mustang")
    bike = factory.create_motorcycle("Harley-Davidson", "Sportster")
    
    car.start_engine()
    bike.start_engine()

print("--- USA market ---")
us_factory = USVehicleFactory()
client_code(us_factory)

print("--- EU market ---")
eu_factory = EUVehicleFactory()
client_code(eu_factory)
