import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime, date
from core.hospital import Hospital
from core.department import Department
from models.patient import Patient
from models.staff import Staff

class HospitalManagementGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Hospital Management System")
        self.root.geometry("1200x700")
        
        self.hospital = None
        self.current_department = None
        self.current_doctor = None
        self.current_patient = None
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.setup_gui()
        
    def setup_gui(self):
        # Create main frame with sidebar and content area
        self.main_container = ttk.Frame(self.root)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Sidebar
        self.sidebar = ttk.Frame(self.main_container, width=200, relief=tk.RAISED)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        # Main content area
        self.content = ttk.Frame(self.main_container)
        self.content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Title
        title_label = ttk.Label(self.sidebar, text="HMS", font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)
        
        # Sidebar buttons
        buttons = [
            ("Create Hospital", self.create_hospital_window),
            ("Add Department", self.add_department_window),
            ("Add Patient", self.add_patient_window),
            ("Add Staff", self.add_staff_window),
            ("View Hospital Info", self.view_hospital_info),
            ("Check In/Out", self.check_in_out_window),
            ("Diagnose/Prescribe", self.diagnose_window),
            ("Exit", self.exit_app)
        ]
        
        for text, command in buttons:
            btn = ttk.Button(self.sidebar, text=text, command=command, width=20)
            btn.pack(pady=5, padx=10)
        
        # Status bar
        self.status_bar = ttk.Label(self.root, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Output text area
        self.output_text = scrolledtext.ScrolledText(self.content, height=30, width=80)
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Clear output button
        clear_btn = ttk.Button(self.content, text="Clear Output", command=self.clear_output)
        clear_btn.pack(pady=5)
    
    def parse_date(self, date_str):
        """Parse date string in YYYY-MM-DD format"""
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Invalid date format. Please use YYYY-MM-DD")
    
    def create_hospital_window(self):
        if self.hospital:
            messagebox.showinfo("Info", "Hospital already created.")
            return
            
        window = tk.Toplevel(self.root)
        window.title("Create Hospital")
        window.geometry("400x200")
        
        ttk.Label(window, text="Hospital Name:").pack(pady=5)
        name_entry = ttk.Entry(window, width=40)
        name_entry.pack(pady=5)
        
        ttk.Label(window, text="Location:").pack(pady=5)
        location_entry = ttk.Entry(window, width=40)
        location_entry.pack(pady=5)
        
        def create():
            name = name_entry.get().strip()
            location = location_entry.get().strip()
            if name and location:
                try:
                    self.hospital = Hospital(name, location)
                    self.update_status(f"Hospital '{name}' created at {location}")
                    self.output(f"Hospital '{name}' created at {location}.")
                    window.destroy()
                except Exception as e:
                    messagebox.showerror("Error", str(e))
            else:
                messagebox.showwarning("Warning", "Name and location cannot be empty.")
        
        ttk.Button(window, text="Create", command=create).pack(pady=10)
    
    def add_department_window(self):
        if not self.hospital:
            messagebox.showwarning("Warning", "Create a hospital first.")
            return
            
        window = tk.Toplevel(self.root)
        window.title("Add Department")
        window.geometry("400x150")
        
        ttk.Label(window, text="Department Name:").pack(pady=5)
        name_entry = ttk.Entry(window, width=40)
        name_entry.pack(pady=5)
        
        def add():
            name = name_entry.get().strip()
            if name:
                try:
                    dept = Department(name)
                    self.hospital.add_department(dept)
                    self.update_status(f"Department '{name}' added")
                    self.output(f"Department '{name}' added.")
                    window.destroy()
                except Exception as e:
                    messagebox.showerror("Error", str(e))
            else:
                messagebox.showwarning("Warning", "Department name cannot be empty.")
        
        ttk.Button(window, text="Add", command=add).pack(pady=10)
    
    def add_patient_window(self):
        if not self.hospital:
            messagebox.showwarning("Warning", "Create a hospital first.")
            return
            
        # First select department
        dept = self.select_department("Select department for patient:")
        if not dept:
            return
            
        window = tk.Toplevel(self.root)
        window.title("Add Patient")
        window.geometry("500x300")
        
        # Form fields
        ttk.Label(window, text="Name:").pack(pady=5)
        name_entry = ttk.Entry(window, width=40)
        name_entry.pack(pady=5)
        
        ttk.Label(window, text="Date of Birth (YYYY-MM-DD):").pack(pady=5)
        dob_entry = ttk.Entry(window, width=40)
        dob_entry.pack(pady=5)
        
        ttk.Label(window, text="Medical Record:").pack(pady=5)
        record_entry = ttk.Entry(window, width=40)
        record_entry.pack(pady=5)
        
        def add():
            try:
                name = name_entry.get().strip()
                dob_str = dob_entry.get().strip()
                record = record_entry.get().strip()
                
                if not name or not record:
                    messagebox.showwarning("Warning", "Name and medical record cannot be empty.")
                    return
                
                if not dob_str:
                    messagebox.showwarning("Warning", "Date of birth cannot be empty.")
                    return
                
                # Parse date
                try:
                    dob = self.parse_date(dob_str)
                except ValueError as e:
                    messagebox.showerror("Error", str(e))
                    return
                
                patient = Patient(name, dob, record)
                dept.add_patient(patient)
                self.update_status(f"Patient '{name}' added")
                self.output(f"Patient '{name}' added to {dept.name}.")
                window.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        ttk.Button(window, text="Add Patient", command=add).pack(pady=10)
    
    def add_staff_window(self):
        if not self.hospital:
            messagebox.showwarning("Warning", "Create a hospital first.")
            return
            
        dept = self.select_department("Select department for staff:")
        if not dept:
            return
            
        window = tk.Toplevel(self.root)
        window.title("Add Staff")
        window.geometry("500x250")
        
        ttk.Label(window, text="Name:").pack(pady=5)
        name_entry = ttk.Entry(window, width=40)
        name_entry.pack(pady=5)
        
        ttk.Label(window, text="Date of Birth (YYYY-MM-DD):").pack(pady=5)
        dob_entry = ttk.Entry(window, width=40)
        dob_entry.pack(pady=5)
        
        ttk.Label(window, text="Position:").pack(pady=5)
        position_entry = ttk.Entry(window, width=40)
        position_entry.pack(pady=5)
        
        def add():
            try:
                name = name_entry.get().strip()
                dob_str = dob_entry.get().strip()
                position = position_entry.get().strip()
                
                if not name or not position:
                    messagebox.showwarning("Warning", "Name and position cannot be empty.")
                    return
                
                if not dob_str:
                    messagebox.showwarning("Warning", "Date of birth cannot be empty.")
                    return
                
                # Parse date
                try:
                    dob = self.parse_date(dob_str)
                except ValueError as e:
                    messagebox.showerror("Error", str(e))
                    return
                
                staff = Staff(name, dob, position)
                dept.add_staff(staff)
                self.update_status(f"Staff '{name}' added")
                self.output(f"Staff '{name}' added to {dept.name}.")
                window.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        ttk.Button(window, text="Add Staff", command=add).pack(pady=10)
    
    def view_hospital_info(self):
        if not self.hospital:
            messagebox.showwarning("Warning", "Create a hospital first.")
            return
            
        self.output("\n" + "="*60)
        self.output(f"HOSPITAL: {self.hospital.name}")
        self.output(f"Location: {self.hospital.location}")
        self.output(f"Total Departments: {len(self.hospital.departments)}")
        self.output(f"Total Patients: {self.hospital.get_total_patients()}")
        self.output(f"Total Staff: {self.hospital.get_total_staff()}")
        
        for dept in self.hospital.departments:
            self.output(f"\nDepartment: {dept.name}")
            self.output(f"  Staff: {len(dept.staff)} | Patients: {len(dept.patients)}")
            
            if dept.patients:
                self.output("  Patients:")
                for p in dept.patients:
                    self.output(f"    - {p.view_record()}")
            
            if dept.staff:
                self.output("  Staff:")
                for s in dept.staff:
                    self.output(f"    - {s.view_info()}")
        
        self.output("="*60)
        self.update_status("Hospital info displayed")
    
    def check_in_out_window(self):
        if not self.hospital:
            messagebox.showwarning("Warning", "Create a hospital first.")
            return
            
        window = tk.Toplevel(self.root)
        window.title("Check In/Out")
        window.geometry("400x250")
        
        ttk.Label(window, text="Select Action:", font=('Arial', 10, 'bold')).pack(pady=10)
        
        def patient_check_in():
            self.check_in_out_action("patient", "in")
            window.destroy()
        
        def patient_check_out():
            self.check_in_out_action("patient", "out")
            window.destroy()
        
        def staff_check_in():
            self.check_in_out_action("staff", "in")
            window.destroy()
        
        def staff_check_out():
            self.check_in_out_action("staff", "out")
            window.destroy()
        
        ttk.Button(window, text="Patient Check-in", command=patient_check_in, width=25).pack(pady=5)
        ttk.Button(window, text="Patient Check-out", command=patient_check_out, width=25).pack(pady=5)
        ttk.Button(window, text="Staff Check-in", command=staff_check_in, width=25).pack(pady=5)
        ttk.Button(window, text="Staff Check-out", command=staff_check_out, width=25).pack(pady=5)
    
    def diagnose_window(self):
        if not self.hospital:
            messagebox.showwarning("Warning", "Create a hospital first.")
            return
            
        # Select department, doctor, and patient
        dept = self.select_department("Select department:")
        if not dept:
            return
            
        doctors = [s for s in dept.staff if "Dr" in s.name or "doctor" in s.position.lower()]
        if not doctors:
            messagebox.showinfo("Info", "No doctors available in this department.")
            return
            
        doctor = self.select_member(doctors, "doctor")
        if not doctor:
            return
            
        if not dept.patients:
            messagebox.showinfo("Info", "No patients available in this department.")
            return
            
        patient = self.select_member(dept.patients, "patient")
        if not patient:
            return
        
        window = tk.Toplevel(self.root)
        window.title("Diagnose & Prescribe")
        window.geometry("500x300")
        
        ttk.Label(window, text=f"Doctor: {doctor.name}", font=('Arial', 10, 'bold')).pack(pady=5)
        ttk.Label(window, text=f"Patient: {patient.name}", font=('Arial', 10, 'bold')).pack(pady=5)
        
        ttk.Label(window, text="Diagnosis:").pack(pady=5)
        diag_entry = scrolledtext.ScrolledText(window, height=3, width=50)
        diag_entry.pack(pady=5)
        
        ttk.Label(window, text="Treatment:").pack(pady=5)
        treat_entry = scrolledtext.ScrolledText(window, height=3, width=50)
        treat_entry.pack(pady=5)
        
        def process():
            diagnosis = diag_entry.get("1.0", tk.END).strip()
            treatment = treat_entry.get("1.0", tk.END).strip()
            
            if diagnosis:
                result = doctor.diagnose_patient(patient, diagnosis)
                self.output(result)
                patient.medical_record += f" | Diagnosis: {diagnosis}"
            
            if treatment:
                result = doctor.prescribe_treatment(patient, treatment)
                self.output(result)
                patient.medical_record += f", Treatment: {treatment}"
            
            if diagnosis or treatment:
                self.update_status(f"{doctor.name} treated {patient.name}")
                window.destroy()
            else:
                messagebox.showwarning("Warning", "Please enter diagnosis or treatment.")
        
        ttk.Button(window, text="Submit", command=process).pack(pady=10)
    
    def check_in_out_action(self, member_type, action):
        dept = self.select_department(f"Select department for {member_type} {action}:")
        if not dept:
            return
            
        if member_type == "patient":
            members = dept.patients
            label = "patient"
        else:
            members = dept.staff
            label = "staff"
            
        if not members:
            messagebox.showinfo("Info", f"No {label}s available.")
            return
            
        member = self.select_member(members, label)
        if not member:
            return
            
        if action == "in":
            result = member.check_in()
        else:
            result = member.check_out()
            
        self.output(result)
        self.update_status(f"{member.name} checked {action}")
    
    def select_department(self, title):
        if not self.hospital or not self.hospital.departments:
            messagebox.showinfo("Info", "No departments available.")
            return None
            
        window = tk.Toplevel(self.root)
        window.title(title)
        window.geometry("300x200")
        
        ttk.Label(window, text="Select Department:", font=('Arial', 10, 'bold')).pack(pady=10)
        
        selected_dept = tk.StringVar()
        
        for i, dept in enumerate(self.hospital.departments):
            rb = ttk.Radiobutton(window, text=dept.name, variable=selected_dept, value=dept.name)
            rb.pack(pady=2, padx=20, anchor=tk.W)
        
        def confirm():
            if selected_dept.get():
                window.destroy()
            else:
                messagebox.showwarning("Warning", "Please select a department.")
        
        ttk.Button(window, text="Select", command=confirm).pack(pady=10)
        
        # Make window modal
        window.transient(self.root)
        window.grab_set()
        self.root.wait_window(window)
        
        if selected_dept.get():
            for dept in self.hospital.departments:
                if dept.name == selected_dept.get():
                    return dept
        return None
    
    def select_member(self, members, member_type):
        window = tk.Toplevel(self.root)
        window.title(f"Select {member_type.title()}")
        window.geometry("300x200")
        
        ttk.Label(window, text=f"Select {member_type}:", font=('Arial', 10, 'bold')).pack(pady=10)
        
        selected_member = tk.StringVar()
        
        for i, member in enumerate(members):
            rb = ttk.Radiobutton(window, text=member.name, variable=selected_member, value=member.name)
            rb.pack(pady=2, padx=20, anchor=tk.W)
        
        def confirm():
            if selected_member.get():
                window.destroy()
            else:
                messagebox.showwarning("Warning", f"Please select a {member_type}.")
        
        ttk.Button(window, text="Select", command=confirm).pack(pady=10)
        
        window.transient(self.root)
        window.grab_set()
        self.root.wait_window(window)
        
        if selected_member.get():
            for member in members:
                if member.name == selected_member.get():
                    return member
        return None
    
    def output(self, text):
        self.output_text.insert(tk.END, text + "\n")
        self.output_text.see(tk.END)
    
    def clear_output(self):
        self.output_text.delete(1.0, tk.END)
        self.update_status("Output cleared")
    
    def update_status(self, message):
        self.status_bar.config(text=f"Status: {message}")
    
    def exit_app(self):
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.root.quit()

def main():
    root = tk.Tk()
    app = HospitalManagementGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()