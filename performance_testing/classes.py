from dataclasses import dataclass


@dataclass(frozen=True)
class Flight:
    flight: str
    price: str
    airline: str
    fromPort: str
    toPort: str


@dataclass(frozen=True)
class User:
    inputName: str
    address: str
    city: str
    state: str
    zipCode: str
    cardType: str
    creditCardNumber: str
    creditCardMonth: str
    creditCardYear: str
    nameOnCard: str
