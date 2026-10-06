# School Transport Management System

A Python-based **Object-Oriented School Transport Management System** designed to manage learners, transport vehicles, routes, subscriptions, passenger allocation, occupancy, transport charges, and operating costs.

The project was developed as part of **CSC2105: Object-Oriented Programming Using Python** and demonstrates the four fundamental pillars of Object-Oriented Programming:

* Encapsulation
* Abstraction
* Inheritance
* Polymorphism

The system uses a console-based interface and applies object-oriented design principles to model a realistic school transportation environment.

---

## Table of Contents

* [Project Overview](#project-overview)
* [Problem Statement](#problem-statement)
* [Objectives](#objectives)
* [Key Features](#key-features)
* [System Architecture](#system-architecture)
* [OOP Concepts Demonstrated](#oop-concepts-demonstrated)
* [Class Structure](#class-structure)
* [System Components](#system-components)
* [Business Rules and Validation](#business-rules-and-validation)
* [Transport Cost Model](#transport-cost-model)
* [Example Workflow](#example-workflow)
* [Sample Data](#sample-data)
* [Error Handling](#error-handling)
* [Project Structure](#project-structure)
* [Installation and Setup](#installation-and-setup)
* [Running the Application](#running-the-application)
* [Technologies Used](#technologies-used)
* [Testing](#testing)
* [Design Decisions](#design-decisions)
* [Current Limitations](#current-limitations)
* [Future Improvements](#future-improvements)
* [Academic Purpose](#academic-purpose)
* [Author](#author)

---

## Project Overview

The **School Transport Management System** provides a simple digital solution for managing school transportation operations.

The system allows a school to:

1. Register learners.
2. Register transport vehicles.
3. Create transport routes.
4. Assign vehicles to routes.
5. Subscribe learners to transport services.
6. Monitor passengers and available seats.
7. Search for learners.
8. Remove learners from transport.
9. Calculate monthly transport charges.
10. Estimate vehicle operating costs.
11. Monitor vehicle and route occupancy.

The application separates the **business logic** from the **user interface**, allowing the underlying transport system to be managed independently from the console menu.

---

# Problem Statement

Managing school transportation manually can become difficult as the number of learners, vehicles, routes, and transport subscriptions increases.

A school needs to know:

* Which learners use school transport.
* Which vehicle each learner uses.
* Which routes vehicles serve.
* How many seats are available.
* How many learners are assigned to each vehicle.
* How much each learner should pay.
* How much each vehicle costs to operate.
* Whether a vehicle has reached its capacity.

This project addresses these requirements using an object-oriented Python application.

---

# Objectives

The main objectives of the project are to:

* Apply Object-Oriented Programming principles to a practical problem.
* Model real-world entities as Python classes.
* Demonstrate encapsulation through controlled access to object data.
* Demonstrate abstraction through abstract base classes.
* Demonstrate inheritance through specialized vehicle classes.
* Demonstrate polymorphism through vehicle-specific calculations.
* Implement validation and business rules.
* Handle application-level errors using custom exceptions.
* Build a maintainable console-based application.

---

# Key Features

## 1. Learner Management

The system allows administrators to register learners with:

* Learner ID
* Name
* Grade/Class
* Guardian contact

Learner information is validated before being stored.

Example:

```text
L001 | Namukasa Grace | P5 | Guardian: 0772100000
```

---

## 2. Vehicle Management

The system supports three vehicle types:

* Bus
* Minibus
* Van

Each vehicle has:

* Registration number
* Seating capacity
* Passenger list
* Assigned route
* Vehicle-specific transport charge
* Vehicle-specific operating cost

---

## 3. Route Management

Administrators can create routes containing:

* Route ID
* Route name
* Stops
* One-way distance

Example:

```text
R01 | Ntinda - Kampala Road | 9.5 km | Ntinda > Kisaasi > Bukoto > Kampala Road
```

---

## 4. Vehicle-to-Route Assignment

A registered vehicle can be assigned to a route.

The system prevents:

* Assigning a non-existent vehicle.
* Assigning a non-existent route.
* Assigning the same vehicle to multiple routes.
* Assigning the same vehicle to the same route more than once.

---

## 5. Learner Transport Subscription

A learner can be assigned to a vehicle and route.

Before the subscription is created, the system checks that:

* The learner exists.
* The route exists.
* The vehicle exists.
* The learner does not already have an active subscription.
* The vehicle serves the selected route.
* The vehicle has available seats.

---

## 6. Passenger Management

The system supports:

* Boarding learners.
* Removing learners from vehicles.
* Checking available seats.
* Preventing duplicate passengers.
* Preventing passengers from boarding a full vehicle.

Example:

```text
VAN UBA 101A
Seats: 8/8
Available seats: 0
```

---

## 7. Learner Search

Administrators can search for learners using:

* Learner ID
* Full name
* Part of a learner's name

The search result also displays the learner's current transport assignment when available.

---

## 8. Transport Charges

Each vehicle type has its own transport pricing model.

The system uses polymorphism so that the same method call:

```python
vehicle.transport_charge(distance)
```

can produce different results depending on whether `vehicle` is a:

* `Bus`
* `Minibus`
* `Van`

---

## 9. Operating Cost Analysis

The system estimates monthly operating costs based on:

* Route distance
* Number of school days
* Fuel cost per kilometre
* Driver costs
* Maintenance/conductor costs

The system can compare:

```text
Monthly income
Monthly operating cost
Net position
```

for each vehicle.

---

## 10. Occupancy Monitoring

The system provides an occupancy summary showing:

* Total learners.
* Total vehicles.
* Total routes.
* Seats used.
* Available seats.
* Occupancy by route.

Example:

```text
OCCUPANCY SUMMARY

Seats used: 10/66
Free seats: 56

Route Ntinda - Kampala Road: 8/8 seats used
Route Kireka - Kyambogo: 2/40 seats used
```

---

# System Architecture

The system follows a simple object-oriented architecture:

```text
                         TransportVehicle
                                │
               ┌────────────────┼────────────────┐
               │                │                │
              Bus            Minibus            Van
               │                │                │
               └────────────────┼────────────────┘
                                │
                         Polymorphism
                                │
                                ▼
                       TransportSystem
                         │      │      │
                         ▼      ▼      ▼
                     Learners Routes Vehicles
                                │
                                ▼
                          Subscriptions
                                │
                                ▼
                         TransportMenu
```

### Responsibility of each layer

**Domain classes**

Represent the core entities of the application.

Examples:

```text
Learner
Bus
Minibus
Van
Route
Subscription
```

**TransportSystem**

Coordinates the different domain objects and implements major business operations.

**TransportMenu**

Handles user input and output without containing the core business rules.

This separation helps keep the application easier to understand and maintain.

---

# OOP Concepts Demonstrated

The project intentionally demonstrates all four pillars of Object-Oriented Programming.

---

## 1. Encapsulation

Encapsulation involves keeping an object's internal state protected and controlling how that state can be accessed or modified.

For example, the passenger list inside `TransportVehicle` is private:

```python
self.__passengers = []
```

External code cannot directly manipulate this list.

Instead, passengers are managed through methods:

```python
vehicle.board(learner)
```

and:

```python
vehicle.alight(learner)
```

The system also uses properties:

```python
@property
def passengers(self):
    return tuple(self.__passengers)
```

The passenger collection is returned as a tuple, preventing external code from directly modifying the internal list.

### Other examples of encapsulation

The project also uses:

* Private attributes using `__name`.
* Protected attributes using `_route`.
* Properties.
* Getters.
* Setters.
* Validation inside setters.

For example:

```python
@property
def capacity(self):
    return self._capacity

@capacity.setter
def capacity(self, value):
    ...
```

This means invalid vehicle capacities can be rejected before they enter the object.

---

# 2. Abstraction

Abstraction means exposing the essential behavior of an object while hiding implementation details.

The project defines an abstract base class:

```python
class TransportVehicle(ABC):
```

It specifies methods that every vehicle must implement:

```python
@abstractmethod
def calculate_operating_cost(self, distance_km):
    pass
```

and:

```python
@abstractmethod
def transport_charge(self, distance_km):
    pass
```

The abstract class does not need to know exactly how every vehicle calculates its costs.

It simply establishes a contract:

> Every transport vehicle must know how to calculate its operating cost and transport charge.

The concrete subclasses then provide the implementation.

---

# 3. Inheritance

Inheritance allows one class to acquire and extend the attributes and behaviors of another class.

The project has one parent class:

```python
TransportVehicle
```

and three child classes:

```python
Bus
Minibus
Van
```

The relationship can be represented as:

```text
             TransportVehicle
                    │
        ┌───────────┼───────────┐
        │           │           │
       Bus       Minibus       Van
```

For example:

```python
class Bus(TransportVehicle):
    ...
```

The `Bus` class automatically receives functionality from `TransportVehicle`, including:

* Registration handling.
* Capacity handling.
* Passenger management.
* Route assignment.
* Available seat calculation.

It then adds its own vehicle-specific behavior.

This avoids duplicating common vehicle logic.

---

# 4. Polymorphism

Polymorphism allows objects of different classes to respond to the same method call in different ways.

For example:

```python
vehicle.transport_charge(10)
```

The same method call can be used for:

```python
Bus
Minibus
Van
```

but each class provides its own implementation.

For example:

```python
class Bus(TransportVehicle):

    def transport_charge(self, distance_km):
        return round(60_000 + 1_500 * distance_km)
```

while:

```python
class Minibus(TransportVehicle):

    def transport_charge(self, distance_km):
        return round(80_000 + 2_000 * distance_km)
```

and:

```python
class Van(TransportVehicle):

    def transport_charge(self, distance_km):
        return round(100_000 + 2_500 * distance_km)
```

Therefore:

```python
for vehicle in vehicles:
    print(vehicle.transport_charge(10))
```

does not need separate logic for each vehicle type.

Python determines which implementation should execute based on the actual object's class.

This is one of the clearest demonstrations of polymorphism in the project.

---

# Class Structure

## `TransportError`

Base custom exception for transport-related business rule violations.

---

## `VehicleFullError`

Specialized exception raised when an attempt is made to board a learner onto a full vehicle.

---

## `Learner`

Represents a learner registered for school transportation.

### Main attributes

* `learner_id`
* `name`
* `grade`
* `contact`

### Main behaviors

* Validate learner information.
* Provide formatted learner information.

---

## `TransportVehicle`

Abstract parent class for all transport vehicles.

### Main attributes

* Registration
* Capacity
* Passenger list
* Assigned route

### Main behaviors

* Board learner.
* Remove learner.
* Calculate available seats.
* Assign route.
* Calculate operating cost.
* Calculate transport charge.

---

## `Bus`

Concrete transport vehicle with bus-specific:

* Capacity range.
* Fuel cost.
* Driver cost.
* Conductor cost.
* Transport pricing.

---

## `Minibus`

Concrete transport vehicle with minibus-specific:

* Capacity range.
* Fuel cost.
* Driver cost.
* Maintenance cost.
* Transport pricing.

---

## `Van`

Concrete transport vehicle with van-specific:

* Capacity range.
* Fuel cost.
* Driver cost.
* Maintenance cost.
* Transport pricing.

---

## `Route`

Represents a school transport route.

### Main attributes

* Route ID
* Route name
* Stops
* Distance
* Assigned vehicles

### Main behaviors

* Add vehicles.
* Calculate seat usage.
* Validate route information.

---

## `Subscription`

Represents the relationship between:

```text
Learner
    +
Route
    +
Vehicle
```

It also stores the monthly transport charge and whether the subscription is active.

---

## `TransportSystem`

Acts as the central coordinator of the application.

It manages:

* Learners.
* Vehicles.
* Routes.
* Subscriptions.

It also performs operations such as:

* Registering learners.
* Adding vehicles.
* Creating routes.
* Assigning vehicles.
* Subscribing learners.
* Unsubscribing learners.
* Searching learners.
* Generating financial information.

---

## `TransportMenu`

Responsible for the console interface.

It handles:

* Displaying menus.
* Collecting input.
* Calling system operations.
* Displaying results.
* Handling expected user errors.

The menu does not contain the core transport business rules.

---

# System Components

The application can be viewed through the following relationships:

```text
Learner
   │
   │ subscribes through
   ▼
Subscription
   │
   ├──────────────► Route
   │
   └──────────────► Vehicle
                         │
                         ▼
                  TransportVehicle
                    /     |     \
                   /      |      \
                 Bus   Minibus    Van
```

This structure represents the relationships between the major objects in the system.

---

# Business Rules and Validation

The system contains validation rules designed to prevent invalid data and inconsistent states.

## Learner Validation

* Name cannot be empty.
* Name must contain valid characters.
* Grade/class cannot be empty.
* Guardian contact must follow the expected Ugandan phone-number format.

---

## Vehicle Validation

Vehicle registrations must contain valid alphanumeric characters.

Vehicle capacities are restricted according to vehicle type.

### Bus

```text
31–70 seats
```

### Minibus

```text
15–30 seats
```

### Van

```text
8–14 seats
```

---

## Passenger Validation

A learner cannot:

* Board a full vehicle.
* Board the same vehicle twice.
* Be subscribed to multiple active vehicles.

A learner must first be removed from the existing subscription before being assigned to another vehicle.

---

## Route Validation

A route must:

* Have a name of at least three characters.
* Contain at least two stops.
* Have a positive distance.
* Have a maximum distance of 200 km.

---

## Vehicle-Route Validation

A vehicle can only be assigned to one route in the current system.

A vehicle cannot be assigned to another route once it already serves a route.

---

## Subscription Validation

A subscription requires:

```text
Valid learner
        +
Valid route
        +
Valid vehicle
        +
Vehicle serves route
        +
Available seat
        +
No existing active subscription
```

Only when all these conditions are satisfied is the learner boarded and the subscription created.

---

# Transport Cost Model

The project uses simplified assumptions to demonstrate financial calculations.

These values are **academic modelling assumptions**, not official commercial transport rates.

The system assumes:

```text
22 school days per month
2 × one-way distance per day
```

---

## Bus

### Operating Cost

```text
Monthly fuel cost
+
Driver cost
+
Conductor cost
```

Fuel cost is calculated using:

```text
Distance × 2 × 22 × fuel cost per kilometre
```

### Transport Charge

```text
60,000 + (1,500 × distance)
```

---

## Minibus

### Operating Cost

```text
Monthly fuel cost
+
Driver cost
+
Maintenance cost
```

### Transport Charge

```text
80,000 + (2,000 × distance)
```

---

## Van

### Operating Cost

```text
Monthly fuel cost
+
Driver cost
+
Maintenance cost
```

### Transport Charge

```text
100,000 + (2,500 × distance)
```

---

# Example Workflow

A typical system workflow is:

```text
1. Register learner
        ↓
2. Register vehicle
        ↓
3. Create route
        ↓
4. Assign vehicle to route
        ↓
5. Assign learner to vehicle
        ↓
6. Create subscription
        ↓
7. Monitor passengers
        ↓
8. Calculate charges and costs
        ↓
9. Remove learner when required
```

For example:

```text
Learner:
Namukasa Grace

Vehicle:
UBA 101A

Vehicle Type:
Van

Route:
Ntinda - Kampala Road

Distance:
9.5 km
```

The system verifies that the van serves the selected route and has available capacity before creating the subscription.

---

# Sample Data

The application contains a `load_sample_data()` function for demonstration and testing.

The sample data includes:

### Learners

12 sample learners.

### Vehicles

```text
UBA 101A → Van → 8 seats
UBE 202B → Bus → 40 seats
UBF 303C → Minibus → 18 seats
```

### Routes

```text
R01 → Ntinda - Kampala Road → 9.5 km

R02 → Kireka - Kyambogo → 14 km
```

### Sample subscriptions

The sample data assigns:

```text
8 learners → Van UBA 101A
2 learners → Bus UBE 202B
```

The van therefore reaches full capacity.

---

# Error Handling

The application uses custom exceptions and validation to handle expected errors cleanly.

The base exception is:

```python
class TransportError(Exception):
    ...
```

A specialized exception is:

```python
class VehicleFullError(TransportError):
    ...
```

Example:

```python
if self.available_seats <= 0:
    raise VehicleFullError(
        "Vehicle is full."
    )
```

The menu catches expected application errors:

```python
except (ValueError, TransportError) as error:
    print(f"REJECTED: {error}")
```

This allows the program to reject invalid operations without terminating unexpectedly.

---

# Project Structure

The current academic implementation is intentionally kept in a single Python file so that the OOP concepts and program flow can easily be inspected.

```text
School-Transport-Management-System/
│
├── README.md
│
└── transport_system.py
```

A larger production-oriented version could later be organized as:

```text
School-Transport-Management-System/
│
├── README.md
├── main.py
├── requirements.txt
│
├── src/
│   ├── __init__.py
│   ├── exceptions.py
│   ├── learner.py
│   ├── vehicle.py
│   ├── route.py
│   ├── subscription.py
│   ├── transport_system.py
│   └── menu.py
│
├── data/
│   └── sample_data.py
│
└── tests/
    ├── test_learner.py
    ├── test_vehicle.py
    ├── test_route.py
    └── test_transport_system.py
```

The modular structure is recommended as the system grows, but the single-file implementation is appropriate for the current academic project.

---

# Installation and Setup

## Requirements

The project requires:

* Python 3.10 or later
* A terminal or command prompt
* A code editor such as Visual Studio Code

No external Python packages are required for the current version.

The application uses Python's standard library, including:

```python
abc
re
```

---

# Running the Application

Clone the repository or download the project files.

Navigate to the project directory:

```bash
cd School-Transport-Management-System
```

Run:

```bash
python transport_system.py
```

On systems where Python is accessed through `py`, use:

```bash
py transport_system.py
```

The application will display the main menu.

---

# Main Menu

The system provides options for:

```text
1. Register learner
2. Add vehicle
3. Create route
4. Assign vehicle to route
5. Assign learner to route and vehicle
6. Remove learner from transport
7. Display passengers
8. Search for a learner
9. Display vehicles and routes
10. Transport charges and operating costs
11. Occupancy summary
12. Load sample data
0. Exit
```

---

# Technologies Used

| Technology        | Purpose                             |
| ----------------- | ----------------------------------- |
| Python            | Core programming language           |
| Python ABC        | Abstract classes and abstraction    |
| Python Properties | Encapsulation and controlled access |
| Python `re`       | Input validation                    |
| Python Exceptions | Error handling                      |
| Git               | Version control                     |
| GitHub            | Repository and collaboration        |

---

# Testing

The implementation was tested against several functional and validation scenarios.

## Syntax Testing

The Python file was compiled to confirm that the source code contains no syntax errors.

---

## Functional Testing

The system was tested for:

* Learner registration.
* Vehicle creation.
* Route creation.
* Vehicle-route assignment.
* Learner subscriptions.
* Passenger capacity.
* Learner removal.
* Learner reassignment.
* Vehicle-specific transport charges.
* Vehicle-specific operating costs.
* Search functionality.
* Occupancy calculations.

---

## Validation Testing

Invalid scenarios tested include:

* Invalid vehicle type.
* Invalid vehicle capacity.
* Invalid route name.
* Invalid route distance.
* Duplicate vehicle registration.
* Duplicate passenger assignment.
* Boarding a full vehicle.
* Assigning a learner to an incompatible vehicle-route combination.
* Assigning a learner who already has an active subscription.
* Removing a learner who has no active subscription.

---

# Design Decisions

Several design decisions were made deliberately.

## 1. Abstract `TransportVehicle`

Rather than creating unrelated vehicle classes, `Bus`, `Minibus`, and `Van` inherit from a common abstraction.

This reflects the real-world relationship:

```text
Every Bus is a Vehicle.
Every Minibus is a Vehicle.
Every Van is a Vehicle.
```

---

## 2. Private Passenger Collection

The passenger list is private:

```python
self.__passengers
```

This prevents other objects from directly changing passenger assignments.

Passenger changes must go through controlled operations.

---

## 3. Properties for Validation

Properties are used where values require validation.

For example:

```python
vehicle.capacity = 40
```

is controlled by the `capacity` setter.

This keeps validation close to the data it protects.

---

## 4. Dedicated ID Counters

The system uses counters such as:

```python
self._next_learner_id
self._next_route_id
self._next_subscription_id
```

instead of relying on the number of objects currently stored.

This prevents ID reuse when objects are removed.

---

## 5. Separate Menu and Business Logic

`TransportMenu` handles interaction with the user.

`TransportSystem` handles system operations.

This prevents user-interface code from becoming mixed with the core business logic.

---

## 6. Polymorphic Vehicle Calculations

The system does not need code such as:

```python
if vehicle_type == "bus":
    ...
elif vehicle_type == "minibus":
    ...
elif vehicle_type == "van":
    ...
```

for every financial calculation.

Instead, it delegates the calculation to the object:

```python
vehicle.transport_charge(distance)
```

This makes the design easier to extend with additional vehicle types.

---

# Current Limitations

The current version is intentionally focused on demonstrating OOP concepts rather than implementing a full production transport platform.

Current limitations include:

### No Database

All data is stored in memory and is lost when the program terminates.

### Console Interface

The application currently uses a command-line interface rather than a graphical or web interface.

### No Authentication

There are no administrator, driver, parent, or learner accounts.

### Simplified Financial Model

Fuel, maintenance, driver costs, and transport charges are based on predefined academic assumptions.

### One Route per Vehicle

The current model assumes that a vehicle serves one route.

### No Driver Management

Drivers are represented indirectly through operating costs rather than as independent system objects.

### No Scheduling

The system does not currently manage pickup times, departure times, or daily schedules.

---

# Future Improvements

Possible future improvements include:

## Database Integration

Replace in-memory dictionaries with a relational database such as:

```text
MySQL
PostgreSQL
SQLite
```

This would allow data to persist between program sessions.

---

## Web Application

Develop a web-based interface using technologies such as:

```text
Flask
Django
FastAPI
React
```

---

## User Authentication

Introduce role-based access for:

* Administrators.
* Transport managers.
* Drivers.
* Parents.
* Learners.

---

## Driver Management

Create a dedicated `Driver` class containing:

* Driver ID.
* Name.
* Contact.
* Licence information.
* Assigned vehicle.

---

## Payment Management

Add:

* Payment records.
* Payment dates.
* Outstanding balances.
* Payment history.
* Receipts.

---

## Transport Scheduling

Introduce:

* Pickup times.
* Drop-off times.
* Morning routes.
* Afternoon routes.
* Daily schedules.

---

## GPS and Tracking

A future version could integrate GPS functionality to allow administrators and parents to monitor vehicle locations.

---

## Reporting Dashboard

The system could generate dashboards showing:

* Fleet utilization.
* Route profitability.
* Vehicle occupancy.
* Monthly revenue.
* Operating expenses.
* Outstanding payments.

---

## Automated Testing

The project can be expanded with a dedicated test suite using Python's:

```text
unittest
```

or:

```text
pytest
```

---

# Academic Purpose

This project was developed to demonstrate practical application of **Object-Oriented Programming using Python**.

The implementation specifically demonstrates:

```text
ENCAPSULATION
       ↓
ABSTRACTION
       ↓
INHERITANCE
       ↓
POLYMORPHISM
```

Rather than demonstrating these concepts through isolated examples, the project combines them into a single practical system.

For example:

```text
Encapsulation
    ↓
Protect vehicle passenger data

Abstraction
    ↓
Define common vehicle behavior

Inheritance
    ↓
Create Bus, Minibus and Van

Polymorphism
    ↓
Allow each vehicle to calculate
charges and operating costs differently
```

This makes the project both an academic OOP demonstration and a foundation for a more complete school transport management application.

---

# Author

**Timothy Mugisha**

Data Science & Analytics Student
Uganda Christian University

### Interests

* Data Science
* Machine Learning
* Software Development
* Business Intelligence
* Object-Oriented Programming

---

# Project Status

**Current Status:** Functional academic prototype

**Primary Focus:** Object-Oriented Programming

**Interface:** Console-based

**Data Storage:** In-memory

**External Dependencies:** None

---

## Key Takeaway

The School Transport Management System demonstrates how object-oriented programming can be used to model a real-world problem using interacting objects.

The core relationship is:

```text
TransportVehicle
       │
       ├── Bus
       ├── Minibus
       └── Van
              │
              ▼
        TransportSystem
              │
       ┌──────┼──────┐
       ▼      ▼      ▼
   Learner  Route  Vehicle
       │      │      │
       └──────┼──────┘
              ▼
        Subscription
```

The result is a structured Python application that demonstrates **encapsulation, abstraction, inheritance, and polymorphism** while solving a practical school transportation problem.
