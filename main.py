from datetime import datetime
from core.hospital import Hospital
from core.department import Department
from models.patient import Patient
from models.staff import Staff
from models.person import Person





def choose_department(hospital):
    """Helper to select a department from the hospital."""
    if not hospital.departments:
        print("No departments available. Add a department first.")
        return None

    print("\nChoose a department:")
    for idx, dept in enumerate(hospital.departments, 1):
        print(f"{idx}. {dept.name}")

    choice_str = input("Enter choice number: ").strip()
    if not choice_str.isdigit():
        print("Invalid input. Enter a number.")
        return None

    choice = int(choice_str)
    if 1 <= choice <= len(hospital.departments):
        return hospital.departments[choice - 1]
    else:
        print("Choice out of range.")
        return None


def choose_member(members, member_type="Member"):
    """Helper to select a patient or staff member from a list."""
    if not members:
        print(f"No {member_type.lower()}s available.")
        return None

    print(f"\nSelect a {member_type.lower()}:")
    for idx, m in enumerate(members, 1):
        print(f"{idx}. {m.name}")

    choice_str = input(f"Enter {member_type} number: ").strip()
    if not choice_str.isdigit():
        print("Invalid input. Enter a number.")
        return None

    choice = int(choice_str)
    if 1 <= choice <= len(members):
        return members[choice - 1]
    else:
        print("Choice out of range.")
        return None


def input_date(prompt="Enter date (YYYY-MM-DD): "):
    """Helper to input and validate a date."""
    date_str = input(prompt).strip()
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        print("Invalid date format. Use YYYY-MM-DD.")
        return None


def main():
    hospital = None

    while True:
        print("\n--- Hospital Management System ---")
        print("1. Create Hospital")
        print("2. Add Department")
        print("3. Add Patient")
        print("4. Add Staff")
        print("5. View Hospital Info")
        print("6. Check-in / Check-out")
        print("7. Diagnose / Prescribe")
        print("8. Exit")

        choice = input("Enter your choice: ").strip()
        if not choice.isdigit():
            print("Invalid input. Enter a number 1-8.")
            continue

        if choice == "1":
            if hospital:
                print("Hospital already created.")
            else:
                name = input("Enter hospital name: ").strip()
                location = input("Enter hospital location: ").strip()
                if name and location:
                    hospital = Hospital(name, location)
                    print(f"Hospital '{name}' created at {location}.")
                else:
                    print("Name and location cannot be empty.")

        elif choice == "2":
            if not hospital:
                print("Create a hospital first.")
                continue
            dept_name = input("Enter department name: ").strip()
            if dept_name:
                dept = Department(dept_name)
                hospital.add_department(dept)
            else:
                print("Department name cannot be empty.")

        elif choice == "3":
            if not hospital:
                print("Create a hospital first.")
                continue
            department = choose_department(hospital)
            if department:
                name = input("Enter patient name: ").strip()
                dob = input_date("Enter date of birth (YYYY-MM-DD): ")
                if not dob:
                    continue
                record = input("Enter medical record: ").strip()
                if not name or not record:
                    print("Name and medical record cannot be empty.")
                    continue
                patient = Patient(name, dob, record)
                department.add_patient(patient)
                print(f"Patient '{name}' added to {department.name}.")

        elif choice == "4":
            if not hospital:
                print("Create a hospital first.")
                continue
            department = choose_department(hospital)
            if department:
                name = input("Enter staff name: ").strip()
                dob = input_date("Enter date of birth (YYYY-MM-DD): ")
                if not dob:
                    continue
                position = input("Enter position: ").strip()
                if not name or not position:
                    print("Name and position cannot be empty.")
                    continue
                staff_member = Staff(name, dob, position)
                department.add_staff(staff_member)
                print(f"Staff '{name}' added to {department.name}.")

        elif choice == "5":
            if not hospital:
                print("Create a hospital first.")
                continue
            hospital.view_hospital_info()
            for dept in hospital.departments:
                print(f"\nDepartment: {dept.name} | Staff: {len(dept.staff)} | Patients: {len(dept.patients)}")
                if dept.patients:
                    print("Patients:")
                    for p in dept.patients:
                        print(f"  - {p.view_record()}")
                if dept.staff:
                    print("Staff:")
                    for s in dept.staff:
                        print(f"  - {s.view_info()}")

        elif choice == "6":
            if not hospital:
                print("Create a hospital first.")
                continue
            department = choose_department(hospital)
            if department:
                print("\n1. Check-in Patient\n2. Check-out Patient\n3. Check-in Staff\n4. Check-out Staff")
                sub_choice = input("Enter choice: ").strip()
                if sub_choice == "1":
                    member = choose_member(department.patients, "Patient")
                    if member:
                        print(member.check_in())
                elif sub_choice == "2":
                    member = choose_member(department.patients, "Patient")
                    if member:
                        print(member.check_out())
                elif sub_choice == "3":
                    member = choose_member(department.staff, "Staff")
                    if member:
                        print(member.check_in())
                elif sub_choice == "4":
                    member = choose_member(department.staff, "Staff")
                    if member:
                        print(member.check_out())
                else:
                    print("Invalid choice.")

        elif choice == "7":
            if not hospital:
                print("Create a hospital first.")
                continue
            department = choose_department(hospital)
            if department and department.staff and department.patients:
                doctors = [s for s in department.staff if "Dr" in s.name or "doctor" in s.position.lower()]
                if not doctors:
                    print("No doctors available.")
                    continue
                doctor = choose_member(doctors, "Doctor")
                patient = choose_member(department.patients, "Patient")
                if doctor and patient:
                    diag = input("Enter diagnosis: ").strip()
                    treat = input("Enter treatment: ").strip()
                    if diag:
                        print(doctor.diagnose_patient(patient, diag))
                    if treat:
                        print(doctor.prescribe_treatment(patient, treat))
                    if diag or treat:
                        patient.medical_record += f" | Diagnosis: {diag}, Treatment: {treat}"

        elif choice == "8":
            print("Exiting the system. Goodbye!")
            break

        else:
            print("Invalid choice. Enter a number between 1 and 8.")


if __name__ == "__main__":
    main()
