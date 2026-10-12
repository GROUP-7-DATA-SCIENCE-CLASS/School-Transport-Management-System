
# School Transport Management System

A Python-based, object-oriented application for managing school transportation operations, including learners, vehicles, routes, subscriptions, passenger capacity, and transport cost analysis.

Built as part of **CSC2105: Object-Oriented Programming Using Python**, this project demonstrates how the four pillars of OOP can be integrated into a practical software solution.

<p align="center">
  <strong>Python • Object-Oriented Design • Validation • Business Logic</strong>
</p>

---

## Table of Contents

- [Overview](#overview)
- [Problem Statement](#problem-statement)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Object-Oriented Programming](#object-oriented-programming)
- [Business Rules and Validation](#business-rules-and-validation)
- [Transport Cost Model](#transport-cost-model)
- [Getting Started](#getting-started)
- [Usage Workflow](#usage-workflow)
- [Technology Stack](#technology-stack)
- [Testing](#testing)
- [Limitations](#limitations)
- [Future Enhancements](#future-enhancements)
- [Learning Outcomes](#learning-outcomes)
- [Contributors and Acknowledgements](#contributors-and-acknowledgements)
- [Author](#author)

---

## Overview

The School Transport Management System is a console-based Python application that models the core operations of a school's transportation service.

It brings together multiple interacting objects to manage learners, transport vehicles, routes, and subscriptions while enforcing business rules that help maintain consistent system data.

Rather than demonstrating Object-Oriented Programming concepts through isolated examples, the project integrates them into one application.

### The problem it addresses

Manual school transport management can make it difficult to track learner assignments, monitor seating capacity, manage routes, calculate transport charges, and estimate operating expenses.

This project provides a structured approach to these tasks using Python classes, object interactions, validation, and exception handling.

## Features

### Learner Management
- Register learners with identification, name, grade/class, and guardian contact details.
- Validate learner information.
- Search by learner ID or name.
- View current transport assignments.
- Remove learners from transport and manage reassignment.

### Fleet Management
- Register buses, minibuses, and vans.
- Validate vehicle registration details and seating capacity.
- Assign vehicles to transport routes.
- Track passengers and available seats.
- Prevent duplicate passenger assignments and boarding beyond capacity.

### Route and Subscription Management
- Create routes with names, stops, and distances.
- Associate vehicles with routes.
- Subscribe eligible learners to transport services.
- Track subscription status and monthly transport charges.
- Validate learner, vehicle, route, and seat availability before subscription.

### Financial Analysis
- Calculate monthly transport charges according to vehicle type.
- Estimate monthly vehicle operating costs.
- Compare estimated transport income with operating expenses.
- Review vehicle and route occupancy.

### Reliability and Validation
- Apply input validation to important data fields.
- Enforce transport business rules.
- Use custom exceptions for transport-related errors.
- Provide a menu-driven interface for interacting with the application.

## System Architecture

The application separates its core domain objects, business operations, and console interface.

```text
                  TransportMenu
                       |
                       v
                 TransportSystem
                       |
          +------------+------------+
          |            |            |
          v            v            v
       Learner        Route     Subscription
                       |
                       v
                TransportVehicle
                       |
             +---------+---------+
             |         |         |
             v         v         v
            Bus     Minibus      Van
```

### Core components

| Component | Responsibility |
|---|---|
| `Learner` | Represents a learner using school transport. |
| `TransportVehicle` | Defines shared vehicle attributes and behavior. |
| `Bus` | Implements bus-specific behavior and cost calculations. |
| `Minibus` | Implements minibus-specific behavior and cost calculations. |
| `Van` | Implements van-specific behavior and cost calculations. |
| `Route` | Represents a transport route, its stops, and distance. |
| `Subscription` | Connects a learner to a route and vehicle. |
| `TransportSystem` | Coordinates domain objects and business operations. |
| `TransportMenu` | Handles user interaction through the console. |
| `TransportError` | Base exception for transport business-rule violations. |
| `VehicleFullError` | Represents attempts to board a full vehicle. |

## Object-Oriented Programming

The project demonstrates all four fundamental pillars of OOP.

### 1. Encapsulation

Encapsulation protects an object's internal state and controls how it is accessed or modified.

The vehicle class uses a private passenger collection and controlled methods for boarding and removing learners. Properties and validation help prevent invalid state changes.

### 2. Abstraction

Abstraction exposes essential behavior while hiding implementation details.

`TransportVehicle` is an abstract base class that defines a common contract for vehicle behavior, including transport charge and operating cost calculations.

### 3. Inheritance

Inheritance allows specialized classes to reuse and extend common functionality.

`Bus`, `Minibus`, and `Van` inherit shared vehicle behavior from `TransportVehicle`, reducing unnecessary duplication.

### 4. Polymorphism

Polymorphism allows different vehicle types to respond differently to the same method call.

For example:

```python
vehicle.transport_charge(distance)
```

The appropriate implementation is selected according to the actual vehicle object. Each vehicle type can therefore apply its own transport pricing model without requiring separate calling code for every type.

## Business Rules and Validation

The application enforces rules designed to preserve consistent transport assignments.

Examples include:

- A vehicle must have a valid registration and an acceptable seating capacity.
- A route must have valid stops and a positive distance within the application's permitted range.
- A vehicle must be assigned to the selected route before a learner can subscribe to it.
- A learner cannot hold multiple active transport subscriptions.
- A learner cannot be boarded twice on the same vehicle.
- A full vehicle must reject additional passengers.
- Invalid assignments must be rejected before a subscription is completed.

Custom exceptions and validation checks help communicate expected errors without unnecessarily terminating the application.

## Transport Cost Model

The project includes a simplified financial model for demonstrating object-specific calculations.

The current model assumes 22 school days per month and two one-way journeys per day when estimating monthly fuel usage.

The illustrative transport charge formulas are:

| Vehicle type | Monthly charge formula |
|---|---|
| Bus | 60,000 + (1,500 × route distance) |
| Minibus | 80,000 + (2,000 × route distance) |
| Van | 100,000 + (2,500 × route distance) |

The distance is measured in kilometres. Monetary values are illustrative amounts in Ugandan shillings (UGX).

Operating cost estimates account for relevant expenses such as fuel, driver costs, and applicable conductor or maintenance costs.

**Important:** These are academic modelling assumptions, not official commercial transport tariffs or financial forecasts.

## Getting Started

### Prerequisites

- Python 3.10 or later
- Git (optional, for cloning the repository)
- A terminal or code editor such as Visual Studio Code

The current implementation uses Python's standard library and requires no external packages.

### 1. Clone the repository

```bash
git clone https://github.com/GROUP-7-DATA-SCIENCE-CLASS/School-Transport-Management-System.git
```

### 2. Enter the project directory

```bash
cd School-Transport-Management-System
```

### 3. Run the application

```bash
python transport_system.py
```

On Windows, you can alternatively use:

```bash
py transport_system.py
```

The application opens a console menu through which you can perform the available operations.

## Usage Workflow

A typical workflow is:

1. Register learners.
2. Register transport vehicles.
3. Create transport routes.
4. Assign vehicles to routes.
5. Subscribe learners to eligible vehicle-route combinations.
6. Monitor passengers and available seats.
7. Search for learners or remove existing assignments.
8. Review transport charges, operating costs, and occupancy summaries.

A sample-data loading option is also available for demonstration.

## Technology Stack

| Technology | Application |
|---|---|
| Python | Core implementation |
| `abc` | Abstract base classes |
| Python properties | Controlled attribute access |
| `re` | Input validation |
| Custom exceptions | Application-level error handling |
| Git and GitHub | Version control and project collaboration |

## Testing

The project has been exercised against syntax, functional, and validation scenarios, as documented during development.

Areas covered include:

- Learner registration and search.
- Vehicle and route creation.
- Vehicle-to-route assignment.
- Subscription creation and removal.
- Capacity and duplicate-assignment restrictions.
- Vehicle-specific charges and operating costs.
- Occupancy calculations.
- Rejection of invalid vehicle, route, and subscription operations.

This describes the development checks performed; it does not imply a formal automated test suite or continuous integration pipeline.

## Limitations

The current implementation is an academic prototype rather than a production-ready transport platform.

- **In-memory storage:** Data is not persisted between program sessions.
- **Console interface:** There is no graphical or web-based interface.
- **No authentication:** Role-based access and user accounts are not implemented.
- **Simplified financial model:** Cost and pricing values use predefined assumptions.
- **Single-route assignment:** A vehicle is restricted to one route in the current model.
- **No scheduling or live tracking:** Pickup schedules, GPS tracking, and real-time notifications are outside the current scope.

## Future Enhancements

Potential improvements include:

- Database integration using MySQL, PostgreSQL, or SQLite.
- Automated unit and integration tests using `unittest` or `pytest`.
- A web interface using Flask, Django, or FastAPI.
- Role-based authentication for administrators, drivers, and parents.
- Driver and payment management modules.
- Transport scheduling and route optimization.
- Reporting dashboards for fleet utilization, occupancy, revenue, and expenses.

These are proposed enhancements, not existing features.

## Learning Outcomes

Through this project, the team applied:

- Object-oriented modelling of a practical domain.
- Encapsulation, abstraction, inheritance, and polymorphism.
- Class relationships and object collaboration.
- Input validation and business-rule enforcement.
- Custom exception handling.
- Separation of business logic from user-interface code.
- Version control and collaborative development practices.

## Contributors and Acknowledgements

Developed as part of **CSC2105: Object-Oriented Programming Using Python** at Uganda Christian University.

This is a collaborative academic project maintained in the `GROUP-7-DATA-SCIENCE-CLASS` GitHub organization.

Credit for individual contributions should be attributed according to the work each team member completed.

## Author

**Timothy Mugisha**  
Data Science & Analytics Student | Python | Software Development | Machine Learning

- GitHub: [@timomugishan8-ai](https://github.com/timomugishan8-ai)
- LinkedIn: [Timothy Mugisha](https://www.linkedin.com/in/timothy-mugisha-39ba2a2b/)

## Project Status

**Status:** Functional academic prototype  
**Interface:** Console-based  
**Storage:** In-memory  
**Primary objective:** Practical demonstration of Object-Oriented Programming in Python

---

*This project demonstrates how structured object-oriented design can turn a real-world management problem into a maintainable software application.*