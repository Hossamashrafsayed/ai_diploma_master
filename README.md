# 🏥 Hospital Management System

A simple and structured **Hospital Management System** built using **Python (OOP principles)**.  
The system manages hospitals, departments, patients, and staff with proper validation and clear separation of responsibilities.

---

## Features

- Create and manage a hospital
- Add multiple departments
- Add patients and staff to specific departments
- Check-in and check-out patients and staff
- Diagnose patients and prescribe treatments
- View complete hospital information
- Input validation and logical flow control
- UML-based design (Object-Oriented)

---

## Project Structure

Project_1(Hospital_system)/
│
├── core/
│   ├── __init__.py
│   ├── hospital.py
│   └── department.py
│
├── models/
│   ├── __init__.py
│   ├── person.py
│   ├── patient.py
│   └── staff.py
│
├── docs/
│   └── hospital_uml.png
│
├── main.py
└── README.md

---

## Design Rules

- A hospital must be created before any operation
- At least one department must exist before adding patients or staff
- Patients and staff must be checked-in to perform any operation
- Medical records cannot be empty
- Input validation is applied for:
  - Dates
  - Menu choices

---

## Technologies Used

- Python
- Object-Oriented Programming (OOP)
- UML (Class Diagram)
- Command Line Interface (CLI)

---

## Future Improvements

- Graphical User Interface (GUI)
- Database integration
- User authentication (Admin / Doctor)
- Export medical records to files

---

## Authors

[Github Repo](https://github.com/Hashem-Rashed/Project_1)

- Randa Hamada El Nagar
- Enas Essam Mohamed
- Hashem Abdelrahman Abdelkhalek
- Ahmed Magdy Morad
- Hossam Ashraf Saed
