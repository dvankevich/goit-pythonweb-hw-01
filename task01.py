from abc import ABC, abstractmethod
import logging

class Vehicle(ABC):
    def __init__(self, make, model, spec):
        self.make = make
        self.model = model
        self.spec = spec

    @abstractmethod
    def start_engine(self):
        pass

class Car(Vehicle):
    def start_engine(self):
        logging.info(f"Car: {self.make} {self.model} ({self.spec}) - Двигун запущено")
        
class Motorcycle(Vehicle):
    def start_engine(self):
        logging.info(f'Motorcycle: {self.make} {self.model} ({self.spec}) — Мотор заведено')

class VehicleFactory(ABC):
    @abstractmethod
    def create_car(self, make, model) -> Car:
        pass

    @abstractmethod
    def create_motorcycle(self, make, model) -> Motorcycle:
        pass

class USVehicleFactory(VehicleFactory):
    def create_car(self, make, model) -> Car:
        return Car(make, model, "US Spec")

    def create_motorcycle(self, make, model) -> Motorcycle:
        return Motorcycle(make, model, "US Spec")

class EUVehicleFactory(VehicleFactory):
    def create_car(self, make, model) -> Car:
        return Car(make, model, "EU Spec")

    def create_motorcycle(self, make, model) -> Motorcycle:
        return Motorcycle(make, model, "EU Spec")

def client_code(factory: VehicleFactory):
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
