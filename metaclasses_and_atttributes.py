from typing import Union
from datetime import datetime, timedelta


# this is not Pythonic
class OldResistor:

    def __init__(self, ohms):
        self._ohms = ohms

    def get_ohms(self):
        return self._ohms
    
    def set_ohms(self, ohms):
        self._ohms = ohms

r0 = OldResistor(50e3)
print('Before:', r0.get_ohms())
r0.set_ohms(10e3)
print('After: ', r0.get_ohms())

# for the start, try this instead
class Resistor:
    def __init__(self, ohms):
        self.ohms = ohms
        self.voltage = 0
        self.current = 0

r1 = Resistor(50e3)
print(r1.ohms)

# a better approach
class VoltageResistance(Resistor):
    
    def __init__(self, ohms: Union[int, float]):
        super().__init__(ohms)
        self._voltage = 0

    @property
    def voltage(self):
        return self._voltage
    
    @voltage.setter
    def voltage(self, voltage: int):
        print("Setting Value")
        self._voltage = voltage
        self.current = self._voltage / self.ohms
    
    @voltage.getter
    def voltage(self):
        print("Getting Value")
        return self._voltage

r2 = VoltageResistance(1e3)
print(f"Before: {r2.current:.2f} amps")
r2.voltage = 10
print(f"After: {r2.current:.2f} amps")
print(r2.voltage)


class BoundedResistance(Resistor):
    def __init__(self, ohms):
        super().__init__(ohms)

    @property
    def ohms(self):
        return self._ohms
    
    @ohms.setter
    def ohms(self, ohms):
        if ohms <= 0:
            raise ValueError(f"Ohms must be > 0; got {ohms}")
        self._ohmns = ohms

r3 = BoundedResistance(1e3)
r3.ohms = 0.5

# make attributes from parent class immutable

class FixedResistance(Resistor):
    
    def __init__(self, ohms):
        super().__init__(ohms)

    @property
    def ohms(self):
        return self._ohms
    
    @ohms.setter
    def ohms(self, ohms):
        if hasattr(self, "_ohms"):
            raise AttributeError("Ohms is immutable")
        self._ohms = ohms


r4 = FixedResistance(1e3)
# r4.ohms = 2e3


# @property instead of refactoring

class Bucket:
    """Leaky Bucket Quota"""
    def __init__(self, period):
        self.period_delta = timedelta(seconds=period)
        self.reset_time = datetime.now()
        self.quota = 0
    
    def __repr__(self) -> str:
        return f"Bucket(quota={self.quota})"
    
def fill(bucket: Bucket, amount: int):
    now = datetime.now()
    if (now - bucket.reset_time) > bucket.period_delta:
        bucket.quota = 0
        bucket.reset_time = now
    bucket.quota += amount

def deduct(bucket: Bucket, amount):
    now = datetime.now()
    if (now - bucket.reset_time) > bucket.period_delta:
        return False
    if bucket.quota - amount < 0:
        return False
    bucket.quota -= amount
    return False

bucket = Bucket(60)
fill(bucket, 100)
print(bucket)

if deduct(bucket, 99):
    print('Had 99 quota')
else:
    print('Not enough for 99 quota')
print(bucket)