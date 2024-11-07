import random
import requests
import time

from dataclasses import asdict
from locust import HttpUser, task, constant
from typing import Dict, List
from bs4 import BeautifulSoup

from classes import Flight, User


class BlazeUser(HttpUser):
    abstract = True
    wait_time = constant(1) # I used constant in contrast to between to try and have some reproducibility in the results
    host = "https://blazedemo.com/"

    def __init__(self, parent):
        super().__init__(parent)
        self.departures_airports: List[str] = []
        self.destinations_airports: List[str] = []


    def add_departure_airport(self, airport: str) -> None:
        self.departures_airports.append(airport)


    def add_destination_airport(self, airport: str) -> None:
        self.destinations_airports.append(airport)


    def connect_to_base_url(self) -> requests.Response:
        url = self.host
        response = self.client.get(url)
        response.raise_for_status()
        print(f"Connected to {url}")
        return response


    def extract_airports(self, html: str) -> None:
        soup = BeautifulSoup(html, 'html.parser')
        
        from_port_select = soup.find('select', {'name': 'fromPort'})
        if from_port_select:
            for option in from_port_select.find_all('option'):
                self.add_departure_airport(option.text)
        else:
            raise ValueError("No departure airports found")

        to_port_select = soup.find('select', {'name': 'toPort'})
        if to_port_select:
            for option in to_port_select.find_all('option'):
                self.add_destination_airport(option.text)
        else:
            raise ValueError("No destination airports found")


    def on_start(self) -> None:
        response = self.connect_to_base_url()
        self.extract_airports(response.text)
        print("Departures:", self.departures_airports)
        print("Destinations:", self.destinations_airports)


    def on_stop(self) -> None:
        self.client.close()
        print("Session closed")


    def send_get_request(self, endpoint: str) -> None:
        url = f"{self.host}/{endpoint}"
        response = self.client.get(url)
        response.raise_for_status()


    def send_post_request(self, endpoint: str, payload: Dict[str, str]) -> requests.Response:
        url = f"{self.host}/{endpoint}"
        response = self.client.post(url, json=payload)
        response.raise_for_status()
        return response


    def extract_flight_attribute(self, tr, attribute_name: str) -> str:
        element = tr.find('input', {'name': attribute_name})
        if element:
            return element.get('value')
        else:
            raise ValueError(f"Attribute '{attribute_name}' not found in the row")


    def extract_flight(self, tr, origin: str, destination: str) -> Flight:
        flight = self.extract_flight_attribute(tr, 'flight')
        price = self.extract_flight_attribute(tr, 'price')
        airline = self.extract_flight_attribute(tr, 'airline')
        fromPort = origin
        toPort = destination
        return Flight(flight, price, airline, fromPort, toPort)


    def post_route(self, origin: str, destination: str) -> List[Flight]:
        payload = {
            "fromPort": origin,
            "toPort": destination
        }
        response = self.send_post_request(endpoint="reserve.php", payload=payload)
        assert response.status_code == 200

        soup = BeautifulSoup(response.text, 'html.parser')
        tbody = soup.find('tbody')
        return [self.extract_flight(tr, origin, destination) for tr in tbody.find_all('tr')]


    def post_purchase(self, flight: Flight) -> None:
        payload = asdict(flight)
        print("Purchase: ", payload)
        response = self.send_post_request(endpoint="purchase.php", payload=payload)
        assert response.status_code == 200


    def post_confirmation(self, user: User) -> None:
        payload = asdict(user)
        response = self.send_post_request(endpoint="confirmation.php", payload=payload)
        assert response.status_code == 200


    def login(self) -> None:
        payload = {
            "username": "user",
            "password": "password"
        }
        response = self.send_post_request(endpoint="login", payload=payload)


class RandomTravelerUser(BlazeUser):

    @task(1)
    def select_random_flight(self):
        origin = random.choice(self.departures_airports)
        destination = random.choice(self.destinations_airports)
        flights = self.post_route(origin, destination)
        flight = random.choice(flights)
        user = User(
            inputName="random_traveler",
            address="address",
            city="city",
            state="state",
            zipCode="zipCode",
            cardType="dinersclub",
            creditCardNumber="123456",
            creditCardMonth="11",
            creditCardYear="2026",
            nameOnCard="Mdm random_traveler"
        )
        self.post_purchase(flight)
        self.post_confirmation(user)


    @task(5)
    def select_cheapest_flight(self):
        origin = random.choice(self.departures_airports)
        destination = random.choice(self.destinations_airports)
        flights = self.post_route(origin, destination)
        flight = min(flights, key=lambda x: x.price)
        user = User(
            inputName="cheapest_traveler",
            address="address",
            city="city",
            state="state",
            zipCode="zipCode",
            cardType="visa",
            creditCardNumber="123456",
            creditCardMonth="11",
            creditCardYear="2026",
            nameOnCard="Mr cheapest_traveler"
        )
        self.post_purchase(flight)
        self.post_confirmation(user)


    @task(2)
    def select_luxury_flight(self):
        origin = random.choice(self.departures_airports)
        destination = random.choice(self.destinations_airports)
        flights = self.post_route(origin, destination)
        flight = max(flights, key=lambda x: x.price)
        user = User(
            inputName="luxury_traveler",
            address="address",
            city="city",
            state="state",
            zipCode="zipCode",
            cardType="amex",
            creditCardNumber="123456",
            creditCardMonth="11",
            creditCardYear="2026",
            nameOnCard="Miss luxury_traveler"
        )
        self.post_purchase(flight)
        self.post_confirmation(user)


class OnlyBrowsingUser(BlazeUser):

    @task(10)
    def browse_flights(self):
        origin = random.choice(self.departures_airports)
        destination = random.choice(self.destinations_airports)
        flights = self.post_route(origin, destination)
        print(flights)


class DesperateLoginUser(BlazeUser):

    @task(3)
    def trying_to_login(self):
        for _ in range(10):
            self.login()
            time.sleep(6)

