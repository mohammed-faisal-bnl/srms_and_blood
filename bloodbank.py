import tkinter as tk
from tkinter import messagebox, scrolledtext
import mysql.connector
from datetime import date

# -------- DATABASE CONNECTION --------
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="bnl@5481",
        database="BloodBankDB"
    )

# -------- GLOBAL VARIABLE FOR LOGGED-IN ADMIN --------
current_admin_id = None  # will store admin ID after login

# -------- MAIN WINDOW --------
root = tk.Tk()
root.title("Blood Bank System")
root.geometry("400x400")

# -------- REGISTER DONOR --------
def register_donor():
    win = tk.Toplevel(root)
    win.title("Register Donor")

    tk.Label(win, text="Name").pack()
    name = tk.Entry(win)
    name.pack()

    tk.Label(win, text="Gender").pack()
    gender = tk.Entry(win)
    gender.pack()

    tk.Label(win, text="Age").pack()
    age = tk.Entry(win)
    age.pack()

    tk.Label(win, text="Phone").pack()
    phone = tk.Entry(win)
    phone.pack()

    tk.Label(win, text="Address").pack()
    address = tk.Entry(win)
    address.pack()

    tk.Label(win, text="Blood Group ID (1-8)").pack()
    bg = tk.Entry(win)
    bg.pack()

    def save():
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO Donor
            (name, gender, age, phone, address, blood_group_id)
            VALUES (%s,%s,%s,%s,%s,%s)
        """, (name.get(), gender.get(), age.get(),
              phone.get(), address.get(), bg.get()))
        db.commit()
        db.close()
        messagebox.showinfo("Success", "Donor Registered")

    tk.Button(win, text="Register", command=save).pack()

# -------- DONOR LOGIN --------
def donor_login():
    win = tk.Toplevel(root)
    win.title("Donor Login")

    tk.Label(win, text="Enter Phone").pack()
    phone = tk.Entry(win)
    phone.pack()

    def login():
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT donor_id, status FROM Donor WHERE phone=%s",
                       (phone.get(),))
        result = cursor.fetchone()
        db.close()

        if result:
            donor_dashboard(result[0], result[1])
        else:
            messagebox.showerror("Error", "Donor not found")

    tk.Button(win, text="Login", command=login).pack()

# -------- DONOR DASHBOARD --------
def donor_dashboard(donor_id, status):
    win = tk.Toplevel(root)
    win.title("Donor Dashboard")

    tk.Label(win, text=f"Status: {status}").pack()

    def donate():
        db = connect_db()
        cursor = db.cursor()
        try:
            cursor.execute("""
                INSERT INTO Donation
                (donor_id, units, donation_date)
                VALUES (%s,1,%s)
            """, (donor_id, date.today()))
            db.commit()
            messagebox.showinfo("Success", "Blood Donated")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        db.close()

    def update_status():
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("""
            UPDATE Donor SET status='Inactive'
            WHERE donor_id=%s
        """, (donor_id,))
        db.commit()
        db.close()
        messagebox.showinfo("Updated", "Status changed")
        
    def set_active():
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("""
            UPDATE Donor 
            SET status='Active'
            WHERE donor_id=%s
        """, (donor_id,))
        db.commit()
        db.close()
        messagebox.showinfo("Updated", "Status set to Active")   

    tk.Button(win, text="Donate Blood", command=donate).pack()
    tk.Button(win, text="Set Inactive", command=update_status).pack()
    tk.Button(win, text="Set Active", command=set_active).pack()

# -------- REGISTER PATIENT --------
def register_patient():
    win = tk.Toplevel(root)
    win.title("Register Patient")

    tk.Label(win, text="Name").pack()
    name = tk.Entry(win)
    name.pack()

    tk.Label(win, text="Phone").pack()
    phone = tk.Entry(win)
    phone.pack()

    tk.Label(win, text="Hospital").pack()
    hospital = tk.Entry(win)
    hospital.pack()

    tk.Label(win, text="Blood Group ID").pack()
    bg = tk.Entry(win)
    bg.pack()

    def save():
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO Patient
            (name, phone, hospital_name, blood_group_id)
            VALUES (%s,%s,%s,%s)
        """, (name.get(), phone.get(), hospital.get(), bg.get()))
        db.commit()
        db.close()
        messagebox.showinfo("Success", "Patient Registered")

    tk.Button(win, text="Register", command=save).pack()

# -------- PATIENT LOGIN --------
def patient_login():
    win = tk.Toplevel(root)
    win.title("Patient Login")

    tk.Label(win, text="Enter Phone").pack()
    phone = tk.Entry(win)
    phone.pack()

    def login():
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT patient_id FROM Patient WHERE phone=%s",
                       (phone.get(),))
        result = cursor.fetchone()
        db.close()

        if result:
            patient_dashboard(result[0])
        else:
            messagebox.showerror("Error", "Patient not found")

    tk.Button(win, text="Login", command=login).pack()

# -------- PATIENT DASHBOARD --------
def patient_dashboard(patient_id):
    win = tk.Toplevel(root)
    win.title("Patient Dashboard")
    win.geometry("500x500")

    # -------- REQUEST BLOOD --------
    def request_blood():
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO Request
            (patient_id, units_requested, request_date)
            VALUES (%s,1,%s)
        """, (patient_id, date.today()))
        db.commit()
        db.close()
        messagebox.showinfo("Success", "Request Sent")

    tk.Button(win, text="Request Blood", command=request_blood).pack(pady=5)

    # -------- ADVANCED SEARCH SECTION --------
    tk.Label(win, text="Search Active Donors", font=("Arial", 12, "bold")).pack(pady=5)

    tk.Label(win, text="Blood Group ID (optional)").pack()
    bg_entry = tk.Entry(win)
    bg_entry.pack()

    tk.Label(win, text="Area (optional)").pack()
    area_entry = tk.Entry(win)
    area_entry.pack()

    def search_donor():
        db = connect_db()
        cursor = db.cursor()

        query = """
            SELECT name, phone, address
            FROM Donor
            WHERE status='Active'
        """
        values = []

        if bg_entry.get():
            query += " AND blood_group_id = %s"
            values.append(bg_entry.get())

        if area_entry.get():
            query += " AND address LIKE %s"
            values.append("%" + area_entry.get() + "%")

        cursor.execute(query, values)
        results = cursor.fetchall()
        db.close()

        result_box.delete("1.0", tk.END)

        if results:
            for r in results:
                result_box.insert(tk.END, f"Name: {r[0]}\nPhone: {r[1]}\nAddress: {r[2]}\n\n")
        else:
            result_box.insert(tk.END, "No Active Donors Found")

    tk.Button(win, text="Search Donors", command=search_donor).pack(pady=5)

    result_box = scrolledtext.ScrolledText(win, height=10, width=55)
    result_box.pack(pady=10)

# -------- REGISTER ADMIN --------
def register_admin():
    win = tk.Toplevel(root)
    win.title("Register Admin")

    tk.Label(win, text="Name").pack()
    name = tk.Entry(win)
    name.pack()

    tk.Label(win, text="Phone").pack()
    phone = tk.Entry(win)
    phone.pack()

    def save():
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO Admin (name, phone)
            VALUES (%s,%s)
        """, (name.get(), phone.get()))
        db.commit()
        db.close()
        messagebox.showinfo("Success", "Admin Registered")

    tk.Button(win, text="Register", command=save).pack()
        
# -------- ADMIN LOGIN --------
def admin_login():
    global current_admin_id
    win = tk.Toplevel(root)
    win.title("Admin Login")

    tk.Label(win, text="Enter Phone").pack()
    phone = tk.Entry(win)
    phone.pack()

    def login():
        global current_admin_id
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT admin_id FROM Admin WHERE phone=%s",
                       (phone.get(),))
        result = cursor.fetchone()
        db.close()

        if result:
            current_admin_id = result[0]  # store logged-in admin
            admin_dashboard(current_admin_id)
        else:
            messagebox.showerror("Error", "Admin not found")

    tk.Button(win, text="Login", command=login).pack()  
        
# -------- ADMIN DASHBOARD --------
def admin_dashboard(admin_id):
    win = tk.Toplevel(root)
    win.title("Admin Dashboard")
    win.geometry("600x400")

    tk.Label(win, text="Pending Requests",
             font=("Arial", 12, "bold")).pack(pady=5)

    request_box = scrolledtext.ScrolledText(win, height=10, width=70)
    request_box.pack(pady=5)

    # -------- LOAD PENDING REQUESTS --------
    def load_requests():
        db = connect_db()
        cursor = db.cursor()

        cursor.execute("""
            SELECT r.request_id, r.units_requested, r.request_date,
                   p.name, p.phone, p.hospital_name,
                   bg.group_name
            FROM Request r
            JOIN Patient p ON r.patient_id = p.patient_id
            JOIN Blood_Group bg ON p.blood_group_id = bg.blood_group_id
            WHERE r.status='Pending'
        """)

        results = cursor.fetchall()
        db.close()

        request_box.delete("1.0", tk.END)

        if results:
            for r in results:
                request_box.insert(
                    tk.END,
                    f"Request ID: {r[0]} | Units: {r[1]} | Date: {r[2]}\n"
                    f"Patient Name: {r[3]} | Phone: {r[4]} | Hospital: {r[5]} | Blood Group: {r[6]}\n\n"
                )
        else:
            request_box.insert(tk.END, "No Pending Requests\n")

    load_requests()

    # -------- APPROVE SECTION --------
    tk.Label(win, text="Enter Request ID to Approve").pack(pady=5)
    approve_entry = tk.Entry(win)
    approve_entry.pack()

    # -------- APPROVE FUNCTION --------
    def approve_request():
        db = connect_db()
        cursor = db.cursor()

        try:
            request_id = approve_entry.get()
            # Use logged-in admin_id automatically
            cursor.execute("""
                UPDATE Request
                SET status='Approved',
                    admin_id=%s
                WHERE request_id=%s
            """, (admin_id, request_id))

            db.commit()
            messagebox.showinfo("Success", "Request Approved")

        except mysql.connector.Error as e:
            messagebox.showerror("Error", e.msg)

        finally:
            db.close()
            load_requests()

    tk.Button(win, text="Approve Request", command=approve_request).pack(pady=10)        

# -------- MAIN MENU --------
tk.Button(root, text="Register Donor", command=register_donor).pack(pady=5)
tk.Button(root, text="Donor Login", command=donor_login).pack(pady=5)
tk.Button(root, text="Register Patient", command=register_patient).pack(pady=5)
tk.Button(root, text="Patient Login", command=patient_login).pack(pady=5)
tk.Button(root, text="Register Admin", command=register_admin).pack(pady=5)
tk.Button(root, text="Admin Login", command=admin_login).pack(pady=5)

root.mainloop()