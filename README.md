# HBnB Evolution – UML Documentation

This document is part of the technical documentation of the **HBnB Evolution** project, whose objective is to design the general architecture of the system before its implementation.
Through different UML diagrams, it is described how the system components are organized, how they communicate with each other and how the main layers of the application are structured.

---

## 🧩 Diagram 0: High-Level Package Diagram

### 📘 Overview
The **High-Level Package Diagram** shows the **Three-Layer Architecture** of the **HBnB** system, organized as follows:

- **Presentation Layer**: Manages the interaction with the user and the APIs that expose the system services.
- **Business Logic Layer**: Contains the main business logic, implemented through classes and controllers that apply the system rules.
- **Data Layer**: Manages access and persistence of data in the database.

These layers communicate with each other through the **Facade design pattern**, which acts as an intermediary that simplifies communication between the presentation layer and the business logic layer.
The façade offers a single and controlled interface that avoids direct dependencies between modules, guaranteeing a modular, scalable and easy-to-maintain design.

---

### 🧱 Diagram structure

- **Presentation Layer**
- `+API`
- `+User Interface`
- **Business Logic Layer**
- `+Facade`
- `+Controllers`
- `+Services`
- **Data Layer**
- `+Models`
- `+Database Access`

---

### 🔄 Relationships between packages

- The **Presentation Layer** depends on the **Facade**, not directly on the business logic.
- The **Facade** coordinates communication between the **Presentation Layer** and the **Business Logic Layer**.
- The **Business Logic Layer** uses the **Data Layer** to access or modify persistent information.

---

📌 *This diagram provides a conceptual vision of the system, serving as a basis for the class, component and sequence diagrams that will be developed in the following phases of the project.*
