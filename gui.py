# =====================================================================
# HOW TO RUN THIS PROJECT:
# 1. Ensure you have Python installed on your system.
# 2. Open VS Code or any terminal window in the directory of this file.
# 3. Execute the command: python gui.py
# 4. The main GUI window will launch automatically.
# =====================================================================

import tkinter as tk
from tkinter import messagebox
import json
import os
import csv
from tkinter import filedialog

# ==========================================
# DATA HANDLING
# ==========================================
DATA_FILE = "employees_data.json"

def load_data():
    """Load employee data dictionary from the JSON file."""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_data(data):
    """Save the updated employee data dictionary back to the JSON file."""
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save data: {e}")

# ==========================================
# MAIN APPLICATION CONTROLLER
# ==========================================
class OfficeAutomationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Office Automation Suite")
        self.root.geometry("1000x650")
        
        # Load database records
        self.employees = load_data()
        
        # Base Layout: Left sidebar (navigation) and Right container (content area)
        sidebar = tk.Frame(root, width=200, bg="lightgray")
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        
        self.container = tk.Frame(root, bg="white")
        self.container.pack(side="right", fill="both", expand=True)
        
        # Create different pages overlaying each other inside the main container
        self.frames = {}
        for name in ["Dashboard", "Employee", "Attendance", "Performance", "Payroll", "Reports"]:
            frame = tk.Frame(self.container, bg="white")
            frame.grid(row=0, column=0, sticky="nsew")
            self.frames[name] = frame
            
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        # Sidebar Title and Navigation Buttons
        tk.Label(sidebar, text="Suite Modules", font=("Arial", 14, "bold"), bg="lightgray").pack(pady=20)
        
        tk.Button(sidebar, text="Dashboard", width=18, command=lambda: self.show_page("Dashboard")).pack(pady=5)
        tk.Button(sidebar, text="Employee Management", width=18, command=lambda: self.show_page("Employee")).pack(pady=5)
        tk.Button(sidebar, text="Attendance Tracker", width=18, command=lambda: self.show_page("Attendance")).pack(pady=5)
        tk.Button(sidebar, text="Performance Rating", width=18, command=lambda: self.show_page("Performance")).pack(pady=5)
        tk.Button(sidebar, text="Payroll Calculator", width=18, command=lambda: self.show_page("Payroll")).pack(pady=5)
        tk.Button(sidebar, text="Reports & Export", width=18, command=lambda: self.show_page("Reports")).pack(pady=5)
        
        # Build views for each page frame
        self.build_dashboard()
        self.build_employee()
        self.build_attendance()
        self.build_performance()
        self.build_payroll()
        self.build_reports()
        
        # Show Dashboard by default on launch
        self.show_page("Dashboard")
        
    def show_page(self, name):
        """Switches display frame and refreshes dynamic database fields."""
        if name == "Dashboard":
            self.refresh_dashboard()
        elif name == "Reports":
            self.refresh_reports()
            
        frame = self.frames[name]
        frame.tkraise()

    # ==========================================
    # DASHBOARD
    # ==========================================
    def build_dashboard(self):
        frame = self.frames["Dashboard"]
        tk.Label(frame, text="Office Dashboard Overview", font=("Arial", 18, "bold"), bg="white").pack(pady=20)
        
        self.db_panel = tk.Frame(frame, bg="white")
        self.db_panel.pack(pady=10)
        
        self.lbl_total = tk.Label(self.db_panel, text="Total Employees: --", font=("Arial", 12), bg="white")
        self.lbl_total.pack(pady=8, anchor="w")
        
        self.lbl_avg_att = tk.Label(self.db_panel, text="Average Attendance: --", font=("Arial", 12), bg="white")
        self.lbl_avg_att.pack(pady=8, anchor="w")
        
        self.lbl_avg_perf = tk.Label(self.db_panel, text="Average Performance: --", font=("Arial", 12), bg="white")
        self.lbl_avg_perf.pack(pady=8, anchor="w")
        
        self.lbl_max_pay = tk.Label(self.db_panel, text="Highest Paid Employee: --", font=("Arial", 12), bg="white")
        self.lbl_max_pay.pack(pady=8, anchor="w")
        
        self.lbl_best_perf = tk.Label(self.db_panel, text="Best Performer: --", font=("Arial", 12), bg="white")
        self.lbl_best_perf.pack(pady=8, anchor="w")

    def refresh_dashboard(self):
        """Calculates and refreshes all summary statistics for the dashboard view."""
        total_emp = len(self.employees)
        
        # Average Attendance
        att_pcts = [emp["attendance"]["percentage"] for emp in self.employees.values() if emp["attendance"]["status"] != "N/A"]
        avg_att = sum(att_pcts) / len(att_pcts) if att_pcts else 0.0
        
        # Average Performance Evaluation
        perf_scores = [emp["performance"]["score"] for emp in self.employees.values() if emp["performance"]["rating"] != "N/A"]
        avg_perf = sum(perf_scores) / len(perf_scores) if perf_scores else 0.0
        
        # Highest Paid Employee
        max_pay_name = "N/A"
        max_pay_val = 0.0
        if self.employees:
            best_salary_emp = max(self.employees.values(), key=lambda e: e["payroll"]["net_salary"])
            if best_salary_emp["payroll"]["net_salary"] > 0:
                max_pay_name = best_salary_emp["name"]
                max_pay_val = best_salary_emp["payroll"]["net_salary"]
            else:
                # Fallback to basic salary if payroll basic was not calculated
                best_salary_emp = max(self.employees.values(), key=lambda e: e["salary"])
                max_pay_name = best_salary_emp["name"]
                max_pay_val = best_salary_emp["salary"]
                
        # Best Performer
        best_perf_name = "N/A"
        best_perf_score = 0.0
        if perf_scores:
            best_perf_emp = max((emp for emp in self.employees.values() if emp["performance"]["rating"] != "N/A"), key=lambda e: e["performance"]["score"])
            best_perf_name = best_perf_emp["name"]
            best_perf_score = best_perf_emp["performance"]["score"]
            
        self.lbl_total.config(text=f"Total Employees: {total_emp}")
        self.lbl_avg_att.config(text=f"Average Attendance: {avg_att:.1f}%")
        self.lbl_avg_perf.config(text=f"Average Performance: {avg_perf:.1f}/100")
        self.lbl_max_pay.config(text=f"Highest Paid Employee: {max_pay_name} (${max_pay_val:,.2f})")
        self.lbl_best_perf.config(text=f"Best Performer: {best_perf_name} ({best_perf_score:.1f}/100)")

    # ==========================================
    # EMPLOYEE MANAGEMENT
    # ==========================================
    def build_employee(self):
        frame = self.frames["Employee"]
        tk.Label(frame, text="Employee Database Management", font=("Arial", 18, "bold"), bg="white").pack(pady=10)
        
        # Split workspace frame into left controls form and right text box display
        main_split = tk.Frame(frame, bg="white")
        main_split.pack(fill="both", expand=True, padx=10, pady=10)
        
        left_input = tk.Frame(main_split, bg="white")
        left_input.pack(side="left", fill="y", padx=10)
        
        right_display = tk.Frame(main_split, bg="white")
        right_display.pack(side="right", fill="both", expand=True, padx=10)
        
        # Form details entry fields
        tk.Label(left_input, text="Employee ID:", bg="white").pack(anchor="w")
        self.emp_id_entry = tk.Entry(left_input, width=25)
        self.emp_id_entry.pack(pady=2)
        
        tk.Label(left_input, text="Full Name:", bg="white").pack(anchor="w")
        self.emp_name_entry = tk.Entry(left_input, width=25)
        self.emp_name_entry.pack(pady=2)
        
        tk.Label(left_input, text="Department:", bg="white").pack(anchor="w")
        self.emp_dept_entry = tk.Entry(left_input, width=25)
        self.emp_dept_entry.pack(pady=2)
        
        tk.Label(left_input, text="Designation:", bg="white").pack(anchor="w")
        self.emp_desig_entry = tk.Entry(left_input, width=25)
        self.emp_desig_entry.pack(pady=2)
        
        tk.Label(left_input, text="Basic Salary:", bg="white").pack(anchor="w")
        self.emp_sal_entry = tk.Entry(left_input, width=25)
        self.emp_sal_entry.pack(pady=2)
        
        # Action execution buttons
        tk.Button(left_input, text="Add Employee", width=20, bg="lightblue", command=self.add_employee).pack(pady=5)
        tk.Button(left_input, text="Update Employee", width=20, bg="lightgreen", command=self.update_employee).pack(pady=5)
        tk.Button(left_input, text="Delete Employee", width=20, bg="salmon", command=self.delete_employee).pack(pady=5)
        tk.Button(left_input, text="Clear Entry Fields", width=20, command=self.clear_employee_fields).pack(pady=5)
        tk.Button(
            left_input,
            text="Import Employees (CSV)",
            width=20,
            bg="lightyellow",
            command=self.import_employees_csv
        ).pack(pady=5)
        tk.Button(
            left_input,
            text="Export Employees (CSV)",
            width=20,
            bg="lightgreen",
            command=self.export_employees_csv
        ).pack(pady=5)
        
        # Search panel controls
        search_frame = tk.Frame(right_display, bg="white")
        search_frame.pack(fill="x", pady=5)
        
        tk.Label(search_frame, text="Search ID/Name:", bg="white").pack(side="left")
        self.emp_search_entry = tk.Entry(search_frame, width=20)
        self.emp_search_entry.pack(side="left", padx=5)
        tk.Button(search_frame, text="Search", command=self.search_employee).pack(side="left", padx=5)
        tk.Button(search_frame, text="Reset / View All", command=self.view_employees).pack(side="left", padx=5)
        
        # Scrollable Employee Textbox display
        text_frame = tk.Frame(right_display)
        text_frame.pack(fill="both", expand=True, pady=5)
        
        self.emp_textbox = tk.Text(text_frame, wrap="none", height=15)
        scrollbar = tk.Scrollbar(text_frame, command=self.emp_textbox.yview)
        self.emp_textbox.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        self.emp_textbox.pack(side="left", fill="both", expand=True)
        
        # Populate listing initially on launch
        self.view_employees()

    def clear_employee_fields(self):
        self.emp_id_entry.delete(0, tk.END)
        self.emp_name_entry.delete(0, tk.END)
        self.emp_dept_entry.delete(0, tk.END)
        self.emp_desig_entry.delete(0, tk.END)
        self.emp_sal_entry.delete(0, tk.END)

    def add_employee(self):
        emp_id = self.emp_id_entry.get().strip()
        if not emp_id:
            messagebox.showerror("Error", "Employee ID is required.")
            return
            
        if emp_id in self.employees:
            messagebox.showerror("Error", "Employee ID already exists.")
            return
            
        name = self.emp_name_entry.get().strip()
        dept = self.emp_dept_entry.get().strip()
        desig = self.emp_desig_entry.get().strip()
        salary_str = self.emp_sal_entry.get().strip()
        
        if not name or not dept or not desig or not salary_str:
            messagebox.showerror("Error", "All inputs must be filled.")
            return
            
        try:
            salary = float(salary_str)
            if salary < 0: raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Salary must be a positive number.")
            return
            
        self.employees[emp_id] = {
            "id": emp_id,
            "name": name,
            "dept": dept,
            "designation": desig,
            "salary": salary,
            "attendance": {
                "working_days": 0,
                "present_days": 0,
                "percentage": 0.0,
                "status": "N/A"
            },
            "performance": {
                "score": 0.0,
                "rating": "N/A"
            },
            "payroll": {
                "basic": salary,
                "bonus": 0.0,
                "allowance": 0.0,
                "tax": 0.0,
                "net_salary": salary
            }
        }
        
        save_data(self.employees)
        messagebox.showinfo("Success", f"Employee '{name}' added successfully.")
        self.view_employees()
        self.clear_employee_fields()

    def import_employees_csv(self):
        """Import employee records from a CSV file."""
        file_path = filedialog.askopenfilename(
            title="Select Employee CSV File",
            filetypes=[("CSV Files", "*.csv")]
        )

        if not file_path:
            return

        imported = 0
        skipped = 0

        try:
            with open(file_path, "r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)

                for row in reader:
                    emp_id = row["ID"].strip()

                    if emp_id in self.employees:
                        skipped += 1
                        continue

                    salary = float(row["Salary"])

                    self.employees[emp_id] = {
                        "id": emp_id,
                        "name": row["Name"].strip(),
                        "dept": row["Department"].strip(),
                        "designation": row["Designation"].strip(),
                        "salary": salary,
                        "attendance": {
                            "working_days": 0,
                            "present_days": 0,
                            "percentage": 0.0,
                            "status": "N/A"
                        },
                        "performance": {
                            "score": 0.0,
                            "rating": "N/A"
                        },
                        "payroll": {
                            "basic": salary,
                            "bonus": 0.0,
                            "allowance": 0.0,
                            "tax": 0.0,
                            "net_salary": salary
                        }
                    }

                    imported += 1

            save_data(self.employees)
            self.view_employees()

            messagebox.showinfo(
                "Import Complete",
                f"Imported: {imported}\nSkipped (Duplicate IDs): {skipped}"
            )

        except Exception as e:
            messagebox.showerror("Error", f"Failed to import CSV.\n\n{e}")

    def export_employees_csv(self):
        """Export employee records to a CSV file."""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")],
            title="Save Employee CSV"
        )

        if not file_path:
            return

        try:
            with open(file_path, "w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)

                # Header
                writer.writerow([
                    "ID",
                    "Name",
                    "Department",
                    "Designation",
                    "Salary"
                ])

                # Employee Data
                for emp in self.employees.values():
                    writer.writerow([
                        emp["id"],
                        emp["name"],
                        emp["dept"],
                        emp["designation"],
                        emp["salary"]
                    ])

            messagebox.showinfo(
                "Success",
                "Employees exported successfully."
            )

        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Failed to export CSV.\n\n{e}"
            )

    def update_employee(self):
        emp_id = self.emp_id_entry.get().strip()
        if not emp_id or emp_id not in self.employees:
            messagebox.showerror("Error", "Please enter a valid existing Employee ID.")
            return
            
        name = self.emp_name_entry.get().strip()
        dept = self.emp_dept_entry.get().strip()
        desig = self.emp_desig_entry.get().strip()
        salary_str = self.emp_sal_entry.get().strip()
        
        if not name or not dept or not desig or not salary_str:
            messagebox.showerror("Error", "All inputs must be filled.")
            return
            
        try:
            salary = float(salary_str)
            if salary < 0: raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Salary must be a positive number.")
            return
            
        emp = self.employees[emp_id]
        emp["name"] = name
        emp["dept"] = dept
        emp["designation"] = desig
        
        if emp["salary"] != salary:
            emp["salary"] = salary
            emp["payroll"]["basic"] = salary
            p = emp["payroll"]
            p["net_salary"] = salary + p["bonus"] + p["allowance"] - p["tax"]
            
        save_data(self.employees)
        messagebox.showinfo("Success", f"Employee '{name}' updated successfully.")
        self.view_employees()
        self.clear_employee_fields()

    def delete_employee(self):
        emp_id = self.emp_id_entry.get().strip()
        if not emp_id or emp_id not in self.employees:
            messagebox.showerror("Error", "Please enter a valid existing Employee ID.")
            return
            
        name = self.employees[emp_id]["name"]
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {name}?"):
            del self.employees[emp_id]
            save_data(self.employees)
            messagebox.showinfo("Success", "Employee deleted successfully.")
            self.view_employees()
            self.clear_employee_fields()

    def view_employees(self):
        """Displays all employee database records inside the scrollable Textbox."""
        self.emp_textbox.config(state="normal")
        self.emp_textbox.delete("1.0", tk.END)
        
        if not self.employees:
            self.emp_textbox.insert(tk.END, "No records found.")
        else:
            header = f"{'ID':<10}{'Name':<20}{'Department':<15}{'Designation':<20}{'Salary':<12}\n"
            self.emp_textbox.insert(tk.END, header + "-" * 77 + "\n")
            for emp in self.employees.values():
                line = f"{emp['id']:<10}{emp['name']:<20}{emp['dept']:<15}{emp['designation']:<20}${emp['salary']:<12,.2f}\n"
                self.emp_textbox.insert(tk.END, line)
                
        self.emp_textbox.config(state="disabled")

    def search_employee(self):
        """Filters employee view inside the Textbox by Name or ID matching."""
        q = self.emp_search_entry.get().strip().lower()
        if not q:
            messagebox.showerror("Error", "Please enter a query to search.")
            return
            
        self.emp_textbox.config(state="normal")
        self.emp_textbox.delete("1.0", tk.END)
        
        header = f"{'ID':<10}{'Name':<20}{'Department':<15}{'Designation':<20}{'Salary':<12}\n"
        self.emp_textbox.insert(tk.END, header + "-" * 77 + "\n")
        
        found = False
        for emp in self.employees.values():
            if q in emp["id"].lower() or q in emp["name"].lower():
                line = f"{emp['id']:<10}{emp['name']:<20}{emp['dept']:<15}{emp['designation']:<20}${emp['salary']:<12,.2f}\n"
                self.emp_textbox.insert(tk.END, line)
                found = True
                
        if not found:
            self.emp_textbox.insert(tk.END, "No matching records found.")
            
        self.emp_textbox.config(state="disabled")

    # ==========================================
    # ATTENDANCE
    # ==========================================
    def build_attendance(self):
        frame = self.frames["Attendance"]
        tk.Label(frame, text="Attendance Management", font=("Arial", 18, "bold"), bg="white").pack(pady=10)
        
        box = tk.Frame(frame, bg="white", padx=20, pady=20)
        box.pack(pady=10)
        
        # ID selector layout
        load_frame = tk.Frame(box, bg="white")
        load_frame.pack(fill="x", pady=10)
        tk.Label(load_frame, text="Employee ID:", bg="white").pack(side="left")
        self.att_id_entry = tk.Entry(load_frame, width=15)
        self.att_id_entry.pack(side="left", padx=5)
        tk.Button(load_frame, text="Load Profile", command=self.load_att_profile).pack(side="left", padx=5)
        
        # Details display
        self.att_info_label = tk.Label(box, text="Name: -- | Current Stats: --", font=("Arial", 11), bg="white")
        self.att_info_label.pack(pady=10)
        
        # Inputs Form
        inputs_frame = tk.Frame(box, bg="white")
        inputs_frame.pack(pady=10)
        
        tk.Label(inputs_frame, text="Total Working Days:", bg="white").grid(row=0, column=0, sticky="w", pady=5)
        self.att_working_entry = tk.Entry(inputs_frame, width=15)
        self.att_working_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(inputs_frame, text="Total Present Days:", bg="white").grid(row=1, column=0, sticky="w", pady=5)
        self.att_present_entry = tk.Entry(inputs_frame, width=15)
        self.att_present_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Action button
        tk.Button(box, text="Calculate & Save Attendance", bg="lightgreen", command=self.save_attendance).pack(pady=10)
        self.att_status_label = tk.Label(box, text="", font=("Arial", 12, "bold"), bg="white")
        self.att_status_label.pack(pady=5)

    def load_att_profile(self):
        """Loads employee profile details for attendance calculations."""
        emp_id = self.att_id_entry.get().strip()
        if not emp_id or emp_id not in self.employees:
            messagebox.showerror("Error", f"Employee ID '{emp_id}' not found.")
            return
            
        emp = self.employees[emp_id]
        att = emp["attendance"]
        self.att_info_label.config(text=f"Name: {emp['name']} | Current: {att['present_days']}/{att['working_days']} ({att['percentage']:.1f}%) [{att['status']}]")
        
        self.att_working_entry.delete(0, tk.END)
        self.att_working_entry.insert(0, str(att["working_days"]))
        self.att_present_entry.delete(0, tk.END)
        self.att_present_entry.insert(0, str(att["present_days"]))
        self.att_status_label.config(text="")

    def save_attendance(self):
        emp_id = self.att_id_entry.get().strip()
        if not emp_id or emp_id not in self.employees:
            messagebox.showerror("Error", "Please load a valid employee profile first.")
            return
            
        try:
            working = int(self.att_working_entry.get())
            present = int(self.att_present_entry.get())
            if working <= 0 or present < 0 or present > working:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Invalid inputs. Present days cannot exceed working days (which must be > 0).")
            return
            
        pct = (present / working) * 100.0
        
        # Map percentage to status categories
        if pct >= 95.0:
            status = "Excellent"
        elif pct >= 85.0:
            status = "Good"
        elif pct >= 75.0:
            status = "Average"
        else:
            status = "Poor"
            
        emp = self.employees[emp_id]
        emp["attendance"]["working_days"] = working
        emp["attendance"]["present_days"] = present
        emp["attendance"]["percentage"] = pct
        emp["attendance"]["status"] = status
        
        save_data(self.employees)
        self.att_status_label.config(text=f"Percentage: {pct:.1f}% | Category: {status}")
        self.load_att_profile()
        messagebox.showinfo("Success", "Attendance updated successfully.")
        
        self.att_working_entry.delete(0, tk.END)
        self.att_present_entry.delete(0, tk.END)
        self.att_id_entry.delete(0, tk.END)

    # ==========================================
    # PERFORMANCE
    # ==========================================
    def build_performance(self):
        frame = self.frames["Performance"]
        tk.Label(frame, text="Performance Evaluation", font=("Arial", 18, "bold"), bg="white").pack(pady=10)
        
        box = tk.Frame(frame, bg="white", padx=20, pady=20)
        box.pack(pady=10)
        
        # Load employee
        load_frame = tk.Frame(box, bg="white")
        load_frame.pack(fill="x", pady=10)
        tk.Label(load_frame, text="Employee ID:", bg="white").pack(side="left")
        self.perf_id_entry = tk.Entry(load_frame, width=15)
        self.perf_id_entry.pack(side="left", padx=5)
        tk.Button(load_frame, text="Load Profile", command=self.load_perf_profile).pack(side="left", padx=5)
        
        # Info display
        self.perf_info_label = tk.Label(box, text="Name: -- | Current Evaluation: --", font=("Arial", 11), bg="white")
        self.perf_info_label.pack(pady=10)
        
        # Inputs Form
        inputs_frame = tk.Frame(box, bg="white")
        inputs_frame.pack(pady=10)
        tk.Label(inputs_frame, text="Performance Score (0-100):", bg="white").grid(row=0, column=0, sticky="w")
        self.perf_score_entry = tk.Entry(inputs_frame, width=15)
        self.perf_score_entry.grid(row=0, column=1, padx=5)
        
        # Action button
        tk.Button(box, text="Calculate & Save Rating", bg="lightgreen", command=self.save_performance).pack(pady=10)
        self.perf_status_label = tk.Label(box, text="", font=("Arial", 12, "bold"), bg="white")
        self.perf_status_label.pack(pady=5)

    def load_perf_profile(self):
        """Loads employee profile details for performance calculations."""
        emp_id = self.perf_id_entry.get().strip()
        if not emp_id or emp_id not in self.employees:
            messagebox.showerror("Error", f"Employee ID '{emp_id}' not found.")
            return
            
        emp = self.employees[emp_id]
        perf = emp["performance"]
        self.perf_info_label.config(text=f"Name: {emp['name']} | Score: {perf['score']:.1f}/100 [{perf['rating']}]")
        self.perf_score_entry.delete(0, tk.END)
        self.perf_score_entry.insert(0, str(perf["score"]))
        self.perf_status_label.config(text="")

    def save_performance(self):
        emp_id = self.perf_id_entry.get().strip()
        if not emp_id or emp_id not in self.employees:
            messagebox.showerror("Error", "Please load a valid employee profile first.")
            return
            
        try:
            score = float(self.perf_score_entry.get())
            if score < 0 or score > 100: raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Score must be a number between 0 and 100.")
            return
            
        # Rating categories mapping
        if score >= 90.0:
            rating = "Excellent"
        elif score >= 80.0:
            rating = "Very Good"
        elif score >= 70.0:
            rating = "Good"
        elif score >= 60.0:
            rating = "Average"
        else:
            rating = "Needs Improvement"
            
        emp = self.employees[emp_id]
        emp["performance"]["score"] = score
        emp["performance"]["rating"] = rating
        
        save_data(self.employees)
        self.perf_status_label.config(text=f"Score: {score:.1f} | Category: {rating}")
        self.load_perf_profile()
        messagebox.showinfo("Success", "Performance evaluation rating saved.")
        
        self.perf_score_entry.delete(0, tk.END)
        self.perf_id_entry.delete(0, tk.END)

    # ==========================================
    # PAYROLL
    # ==========================================
    def build_payroll(self):
        frame = self.frames["Payroll"]
        tk.Label(frame, text="Salary & Payroll Management", font=("Arial", 18, "bold"), bg="white").pack(pady=10)
        
        box = tk.Frame(frame, bg="white", padx=20, pady=15)
        box.pack(pady=10)
        
        # Load employee
        load_frame = tk.Frame(box, bg="white")
        load_frame.pack(fill="x", pady=10)
        tk.Label(load_frame, text="Employee ID:", bg="white").pack(side="left")
        self.pay_id_entry = tk.Entry(load_frame, width=15)
        self.pay_id_entry.pack(side="left", padx=5)
        tk.Button(load_frame, text="Load Profile", command=self.load_payroll_profile).pack(side="left", padx=5)
        
        # Profile display details
        self.pay_info_label = tk.Label(box, text="Name: -- | Current Net Salary: --", font=("Arial", 11), bg="white")
        self.pay_info_label.pack(pady=10)
        
        # Inputs Form
        inputs_frame = tk.Frame(box, bg="white")
        inputs_frame.pack(pady=5)
        
        tk.Label(inputs_frame, text="Basic Salary:", bg="white").grid(row=0, column=0, sticky="w", pady=5)
        self.pay_basic_entry = tk.Entry(inputs_frame, width=15)
        self.pay_basic_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(inputs_frame, text="Bonus Benefits:", bg="white").grid(row=1, column=0, sticky="w", pady=5)
        self.pay_bonus_entry = tk.Entry(inputs_frame, width=15)
        self.pay_bonus_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(inputs_frame, text="Allowance Perks:", bg="white").grid(row=2, column=0, sticky="w", pady=5)
        self.pay_allow_entry = tk.Entry(inputs_frame, width=15)
        self.pay_allow_entry.grid(row=2, column=1, padx=5, pady=5)
        
        tk.Label(inputs_frame, text="Tax Deductions:", bg="white").grid(row=3, column=0, sticky="w", pady=5)
        self.pay_tax_entry = tk.Entry(inputs_frame, width=15)
        self.pay_tax_entry.grid(row=3, column=1, padx=5, pady=5)
        
        # Action button
        tk.Button(box, text="Calculate & Save Net Salary", bg="lightgreen", command=self.save_payroll).pack(pady=10)
        self.pay_status_label = tk.Label(box, text="", font=("Arial", 12, "bold"), bg="white")
        self.pay_status_label.pack(pady=5)

    def load_payroll_profile(self):
        """Loads employee profile details for payroll salary calculations."""
        emp_id = self.pay_id_entry.get().strip()
        if not emp_id or emp_id not in self.employees:
            messagebox.showerror("Error", f"Employee ID '{emp_id}' not found.")
            return
            
        emp = self.employees[emp_id]
        pay = emp["payroll"]
        self.pay_info_label.config(text=f"Name: {emp['name']} | Net Salary: ${pay['net_salary']:,.2f}")
        
        self.pay_basic_entry.delete(0, tk.END)
        self.pay_basic_entry.insert(0, str(pay["basic"]))
        self.pay_bonus_entry.delete(0, tk.END)
        self.pay_bonus_entry.insert(0, str(pay["bonus"]))
        self.pay_allow_entry.delete(0, tk.END)
        self.pay_allow_entry.insert(0, str(pay["allowance"]))
        self.pay_tax_entry.delete(0, tk.END)
        self.pay_tax_entry.insert(0, str(pay["tax"]))
        self.pay_status_label.config(text="")

    def save_payroll(self):
        emp_id = self.pay_id_entry.get().strip()
        if not emp_id or emp_id not in self.employees:
            messagebox.showerror("Error", "Please load a valid employee first.")
            return
            
        try:
            basic = float(self.pay_basic_entry.get())
            bonus = float(self.pay_bonus_entry.get())
            allowance = float(self.pay_allow_entry.get())
            tax = float(self.pay_tax_entry.get())
            if basic < 0 or bonus < 0 or allowance < 0 or tax < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "All inputs must be valid positive numbers.")
            return
            
        # Computation logic
        net_salary = basic + bonus + allowance - tax
        if net_salary < 0:
            messagebox.showerror("Error", "Tax deduction cannot exceed total basic + bonus + allowances earnings.")
            return
            
        emp = self.employees[emp_id]
        emp["payroll"]["basic"] = basic
        emp["payroll"]["bonus"] = bonus
        emp["payroll"]["allowance"] = allowance
        emp["payroll"]["tax"] = tax
        emp["payroll"]["net_salary"] = net_salary
        
        # Sync back basic salary base pay
        emp["salary"] = basic
        
        save_data(self.employees)
        self.pay_status_label.config(text=f"Monthly Net Pay: ${net_salary:,.2f}")
        self.load_payroll_profile()
        messagebox.showinfo("Success", "Salary payroll data saved successfully.")
        
        self.pay_basic_entry.delete(0, tk.END)
        self.pay_bonus_entry.delete(0, tk.END)
        self.pay_allow_entry.delete(0, tk.END)
        self.pay_tax_entry.delete(0, tk.END)
        self.pay_id_entry.delete(0, tk.END)

    # ==========================================
    # REPORTS
    # ==========================================
    def build_reports(self):
        frame = self.frames["Reports"]
        tk.Label(frame, text="Office Reports Desk", font=("Arial", 18, "bold"), bg="white").pack(pady=10)
        
        controls = tk.Frame(frame, bg="white")
        controls.pack(pady=10)
        
        tk.Label(controls, text="Employee ID (Optional):", bg="white").pack(side="left")
        self.rep_id_entry = tk.Entry(controls, width=12)
        self.rep_id_entry.pack(side="left", padx=5)
        
        # Controls buttons
        tk.Button(controls, text="Single Profile Report", command=self.generate_single_report).pack(side="left", padx=5)
        tk.Button(controls, text="Office Summary Report", command=self.refresh_reports).pack(side="left", padx=5)
        tk.Button(controls, text="Save Report to File", bg="lightyellow", command=self.save_report_to_file).pack(side="left", padx=5)
        
        # Display Text and Scrollbar area
        text_frame = tk.Frame(frame)
        text_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.rep_textbox = tk.Text(text_frame, wrap="none", font=("Courier New", 10))
        scrollbar = tk.Scrollbar(text_frame, command=self.rep_textbox.yview)
        self.rep_textbox.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        self.rep_textbox.pack(side="left", fill="both", expand=True)
        
        # Populate reports default summary on build load
        self.refresh_reports()

    def generate_single_report(self):
        """Formats and displays a single employee metrics profile report."""
        emp_id = self.rep_id_entry.get().strip()
        if not emp_id or emp_id not in self.employees:
            messagebox.showerror("Error", f"Employee ID '{emp_id}' not found.")
            return
            
        emp = self.employees[emp_id]
        self.rep_textbox.config(state="normal")
        self.rep_textbox.delete("1.0", tk.END)
        
        rep = f"========================================\n"
        rep += f"            EMPLOYEE REPORT\n"
        rep += f"========================================\n"
        rep += f"Employee ID  : {emp['id']}\n"
        rep += f"Name         : {emp['name']}\n"
        rep += f"Department   : {emp['dept']}\n"
        rep += f"Designation  : {emp['designation']}\n"
        rep += f"Salary (Basic): ${emp['salary']:,.2f}\n"
        rep += "----------------------------------------\n"
        rep += "Attendance Info:\n"
        att = emp["attendance"]
        if att["status"] != "N/A":
            rep += f"  Working Days: {att['working_days']} days\n"
            rep += f"  Present Days: {att['present_days']} days\n"
            rep += f"  Percentage  : {att['percentage']:.1f}%\n"
            rep += f"  Status      : {att['status']}\n"
        else:
            rep += "  No attendance logs recorded.\n"
        rep += "----------------------------------------\n"
        rep += "Performance Info:\n"
        perf = emp["performance"]
        if perf["rating"] != "N/A":
            rep += f"  Score       : {perf['score']:.1f}/100\n"
            rep += f"  Rating      : {perf['rating']}\n"
        else:
            rep += "  No evaluation log recorded.\n"
        rep += "----------------------------------------\n"
        rep += "Payroll Details:\n"
        p = emp["payroll"]
        rep += f"  Basic Salary: ${p['basic']:,.2f}\n"
        rep += f"  Bonus       : ${p['bonus']:,.2f}\n"
        rep += f"  Allowance   : ${p['allowance']:,.2f}\n"
        rep += f"  Tax Deduction: ${p['tax']:,.2f}\n"
        rep += f"  Net Salary  : ${p['net_salary']:,.2f}\n"
        rep += f"========================================\n"
        
        self.rep_textbox.insert(tk.END, rep)
        self.rep_textbox.config(state="disabled")

    def refresh_reports(self):
        """Formats and displays a grid overview report of all employees in the database."""
        self.rep_textbox.config(state="normal")
        self.rep_textbox.delete("1.0", tk.END)
        
        if not self.employees:
            self.rep_textbox.insert(tk.END, "No employee database records found.")
        else:
            rep = f"========================================================================================\n"
            rep += f"                            OFFICE SUMMARY REPORT\n"
            rep += f"========================================================================================\n"
            rep += f"{'ID':<10}{'Name':<20}{'Department':<15}{'Attendance':<15}{'Performance':<15}{'Net Salary':<15}\n"
            rep += f"----------------------------------------------------------------------------------------\n"
            for emp in self.employees.values():
                att = f"{emp['attendance']['percentage']:.1f}%" if emp['attendance']['status'] != "N/A" else "N/A"
                perf = emp['performance']['rating'] if emp['performance']['rating'] != "N/A" else "N/A"
                sal = f"${emp['payroll']['net_salary']:,.2f}"
                rep += f"{emp['id']:<10}{emp['name']:<20}{emp['dept']:<15}{att:<15}{perf:<15}{sal:<15}\n"
            rep += f"========================================================================================\n"
            rep += f"Total Office Size: {len(self.employees)}\n"
            self.rep_textbox.insert(tk.END, rep)
            
        self.rep_textbox.config(state="disabled")

    def save_report_to_file(self):
        """Exports the displayed summary text to a flat local file."""
        text = self.rep_textbox.get("1.0", tk.END).strip()
        if not text or text.startswith("No employee database records"):
            messagebox.showerror("Error", "There are no reports to export.")
            return
            
        try:
            with open("employee_report.txt", "w") as f:
                f.write(text)
            messagebox.showinfo("Success", "Report exported successfully to 'employee_report.txt'.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save text file: {e}")

# ==========================================
# WINDOW LAUNCH ENVIRONMENT
# ==========================================
if __name__ == "__main__":
    root = tk.Tk()
    app = OfficeAutomationApp(root)
    root.mainloop()