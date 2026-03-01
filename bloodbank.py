import tkinter as tk
from tkinter import messagebox, scrolledtext
import mysql.connector
from datetime import date

# ================= THEME =================
BG       = "#0d0f14"
CARD     = "#161920"
ACCENT   = "#c0392b"
ACCENT2  = "#922b21"
SUCCESS  = "#1e8449"
DARK_RED = "#7b241c"
ORANGE   = "#d35400"
TEXT     = "#eaecee"
MUTED    = "#626567"
BORDER   = "#252930"
ENTRY_BG = "#1e2128"
ENTRY_FG = "#eaecee"
FONT_HEADER = ("Georgia", 14, "bold")
FONT_LABEL  = ("Trebuchet MS", 10)
FONT_BODY   = ("Trebuchet MS", 10)
FONT_BTN    = ("Trebuchet MS", 10, "bold")
FONT_SMALL  = ("Trebuchet MS", 9)
FONT_MONO   = ("Courier New", 9)

# ================= HELPERS =================
def make_window(title, w=440, h=520, bar=None):
    win = tk.Toplevel(root)
    win.title(title)
    win.geometry(f"{w}x{h}")
    win.configure(bg=BG)
    win.resizable(False, False)
    tk.Frame(win, bg=bar or ACCENT, height=4).pack(fill="x")
    return win

def win_title(parent, heading, sub=""):
    tk.Label(parent, text=heading, font=FONT_HEADER, fg=TEXT, bg=BG).pack(pady=(18, 2))
    if sub:
        tk.Label(parent, text=sub, font=FONT_SMALL, fg=MUTED, bg=BG).pack(pady=(0, 10))

def form_card(parent):
    f = tk.Frame(parent, bg=CARD)
    f.pack(fill="x", padx=28, pady=4)
    tk.Frame(parent, bg=BORDER, height=1).pack(fill="x", padx=28)
    return f

def lbl_entry(parent, label, show=None):
    tk.Label(parent, text=label, font=FONT_LABEL, fg=MUTED, bg=CARD).pack(anchor="w", padx=14, pady=(10,2))
    e = tk.Entry(parent, font=FONT_BODY, bg=ENTRY_BG, fg=ENTRY_FG,
                 insertbackground=ACCENT, relief="flat", bd=0,
                 highlightthickness=1, highlightcolor=ACCENT,
                 highlightbackground=BORDER, show=show or "")
    e.pack(fill="x", padx=14, pady=(0,4), ipady=7)
    return e

def primary_btn(parent, text, cmd, color=None):
    b = tk.Button(parent, text=text, command=cmd,
                  font=FONT_BTN, bg=color or ACCENT, fg="white",
                  activebackground=DARK_RED, activeforeground="white",
                  relief="flat", bd=0, cursor="hand2", padx=20, pady=10)
    b.pack(fill="x", padx=14, pady=(12,4))
    return b

def rbox_widget(parent, h=12):
    frame = tk.Frame(parent, bg=ENTRY_BG, highlightbackground=BORDER, highlightthickness=1)
    frame.pack(fill="both", expand=True, padx=28, pady=8)
    sb = tk.Scrollbar(frame, bg=CARD, troughcolor=ENTRY_BG)
    sb.pack(side="right", fill="y")
    t = tk.Text(frame, font=FONT_MONO, bg=ENTRY_BG, fg=TEXT,
                relief="flat", bd=0, height=h,
                yscrollcommand=sb.set, padx=10, pady=8, spacing1=3)
    t.pack(fill="both", expand=True)
    sb.config(command=t.yview)
    return t

def sidebar_entry(parent, label, width=19):
    tk.Label(parent, text=label, font=FONT_LABEL, fg=MUTED, bg=CARD).pack(anchor="w", padx=10, pady=(8,2))
    e = tk.Entry(parent, font=FONT_BODY, bg=ENTRY_BG, fg=ENTRY_FG,
                 insertbackground=ACCENT, relief="flat", bd=0,
                 highlightthickness=1, highlightcolor=ACCENT,
                 highlightbackground=BORDER, width=width)
    e.pack(padx=10, pady=(0,2), ipady=6)
    return e

def sidebar_btn(parent, text, color, cmd):
    tk.Button(parent, text=text, command=cmd,
              font=("Trebuchet MS", 9, "bold"),
              bg=color, fg="white",
              activebackground=ACCENT, activeforeground="white",
              relief="flat", bd=0, cursor="hand2",
              pady=8).pack(fill="x", padx=10, pady=3)

def role_card(parent, label, sublabel, color, cmd, row, col):
    card = tk.Frame(parent, bg=CARD, cursor="hand2",
                    highlightbackground=color, highlightthickness=1)
    card.grid(row=row, column=col, padx=8, pady=6, sticky="nsew", ipadx=6, ipady=6)
    parent.columnconfigure(col, weight=1)
    tk.Frame(card, bg=color, height=3).pack(fill="x")
    tk.Label(card, text=label, font=("Georgia",12,"bold"), fg=TEXT, bg=CARD).pack(pady=(10,2))
    tk.Label(card, text=sublabel, font=("Trebuchet MS",8), fg=MUTED, bg=CARD).pack(pady=(0,8))
    card.bind("<Button-1>", lambda e: cmd())
    for c in card.winfo_children():
        c.bind("<Button-1>", lambda e: cmd())

# ================= DATABASE =================
def connect_db():
    return mysql.connector.connect(
        host="localhost", port=3306,
        user="root", password="bnl@5481",
        database="BloodBankDB"
    )

# ================= GLOBAL =================
current_admin_id = None

# ================= MAIN WINDOW =================
root = tk.Tk()
root.title("BloodBank — Management System")
root.geometry("540x660")
root.configure(bg=BG)
root.resizable(False, False)

tk.Frame(root, bg=ACCENT, height=5).pack(fill="x")

# Logo
title_f = tk.Frame(root, bg=BG)
title_f.pack(pady=(22,4))
tk.Label(title_f, text="🩸  BLOOD BANK", font=("Georgia", 32, "bold"), fg=ACCENT, bg=BG).pack()
tk.Label(title_f, text="Management System", font=("Trebuchet MS", 11), fg=MUTED, bg=BG).pack()

tk.Frame(root, bg=BORDER, height=1).pack(fill="x", padx=36, pady=(14,18))

btn_area = tk.Frame(root, bg=BG)
btn_area.pack(fill="x", padx=36)

# ════════════════════════════════════════════
#  DONOR
# ════════════════════════════════════════════
tk.Label(btn_area, text="DONOR", font=("Trebuchet MS",9,"bold"),
         fg=MUTED, bg=BG).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0,4))

def register_donor():
    win = make_window("Register Donor", 420, 520)
    win_title(win, "Register as Donor", "Join our blood donor community")
    cf = form_card(win)
    name    = lbl_entry(cf, "Full Name")
    gender  = lbl_entry(cf, "Gender")
    age     = lbl_entry(cf, "Age")
    phone   = lbl_entry(cf, "Phone")
    address = lbl_entry(cf, "Address")
    bg      = lbl_entry(cf, "Blood Group ID  (1=A+  2=A-  3=B+  4=B-  5=AB+  6=AB-  7=O+  8=O-)")

    def save():
        db = connect_db(); cursor = db.cursor()
        cursor.execute("""INSERT INTO Donor
            (name,gender,age,phone,address,blood_group_id)
            VALUES (%s,%s,%s,%s,%s,%s)""",
            (name.get(), gender.get(), age.get(),
             phone.get(), address.get(), bg.get()))
        db.commit(); db.close()
        messagebox.showinfo("Success", "Donor Registered!")
        win.destroy()

    primary_btn(cf, "✓  Register Donor", save)

def donor_login():
    win = make_window("Donor Login", 400, 260)
    win_title(win, "Donor Login", "Enter your registered phone number")
    cf = form_card(win)
    phone = lbl_entry(cf, "Phone Number")

    def login():
        db = connect_db(); cursor = db.cursor()
        cursor.execute("SELECT donor_id, status FROM Donor WHERE phone=%s", (phone.get(),))
        result = cursor.fetchone(); db.close()
        if result:
            donor_dashboard(result[0], result[1])
            win.destroy()
        else:
            messagebox.showerror("Not Found", "No donor found with this phone.")

    primary_btn(cf, "→  Login", login)

def donor_dashboard(donor_id, status):
    dash = tk.Toplevel(root)
    dash.title("Donor Dashboard")
    dash.geometry("560x320")
    dash.configure(bg=BG)
    tk.Frame(dash, bg=ACCENT, height=4).pack(fill="x")

    top = tk.Frame(dash, bg=CARD)
    top.pack(fill="x")
    tk.Label(top, text="  Donor Dashboard", font=("Georgia",14,"bold"), fg=TEXT, bg=CARD).pack(side="left", padx=16, pady=12)
    status_color = SUCCESS if status == "Active" else MUTED
    tk.Label(top, text=f"●  {status}", font=("Trebuchet MS",10,"bold"),
             fg=status_color, bg=CARD).pack(side="right", padx=16)

    body = tk.Frame(dash, bg=BG)
    body.pack(fill="both", expand=True, padx=24, pady=16)

    info = tk.Frame(body, bg=CARD, highlightbackground=BORDER, highlightthickness=1)
    info.pack(fill="x", pady=(0,12), ipadx=10, ipady=10)
    tk.Label(info, text=f"Donor ID: {donor_id}", font=FONT_SMALL, fg=MUTED, bg=CARD).pack(anchor="w", padx=12)

    btn_row = tk.Frame(body, bg=BG)
    btn_row.pack(fill="x")

    def donate():
        db = connect_db(); cursor = db.cursor()
        try:
            cursor.execute("INSERT INTO Donation (donor_id,units,donation_date) VALUES (%s,1,%s)",
                           (donor_id, date.today()))
            db.commit()
            messagebox.showinfo("Thank You!", "Blood Donated Successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        db.close()

    def update_status():
        db = connect_db(); cursor = db.cursor()
        cursor.execute("UPDATE Donor SET status='Inactive' WHERE donor_id=%s", (donor_id,))
        db.commit(); db.close()
        messagebox.showinfo("Updated", "Status set to Inactive")

    def set_active():
        db = connect_db(); cursor = db.cursor()
        cursor.execute("UPDATE Donor SET status='Active' WHERE donor_id=%s", (donor_id,))
        db.commit(); db.close()
        messagebox.showinfo("Updated", "Status set to Active")

    def make_btn(parent, text, color, cmd):
        tk.Button(parent, text=text, command=cmd,
                  font=("Trebuchet MS",9,"bold"), bg=color, fg="white",
                  activebackground=DARK_RED, activeforeground="white",
                  relief="flat", bd=0, cursor="hand2",
                  padx=14, pady=10).pack(side="left", padx=6)

    make_btn(btn_row, "🩸  Donate Blood",  ACCENT,   donate)
    make_btn(btn_row, "Set Inactive",      DARK_RED, update_status)
    make_btn(btn_row, "Set Active",        SUCCESS,  set_active)

role_card(btn_area, "Register", "Become a donor", SUCCESS, register_donor, 1, 0)
role_card(btn_area, "Login",    "Donor portal",   ACCENT,  donor_login,    1, 1)

# ════════════════════════════════════════════
#  PATIENT
# ════════════════════════════════════════════
tk.Label(btn_area, text="PATIENT", font=("Trebuchet MS",9,"bold"),
         fg=MUTED, bg=BG).grid(row=2, column=0, columnspan=2, sticky="w", pady=(14,4))

def register_patient():
    win = make_window("Register Patient", 420, 460)
    win_title(win, "Patient Registration", "Register to request blood")
    cf = form_card(win)
    name     = lbl_entry(cf, "Full Name")
    phone    = lbl_entry(cf, "Phone")
    hospital = lbl_entry(cf, "Hospital Name")
    bg       = lbl_entry(cf, "Blood Group ID  (1=A+  2=A-  3=B+  4=B-  5=AB+  6=AB-  7=O+  8=O-)")

    def save():
        db = connect_db(); cursor = db.cursor()
        cursor.execute("INSERT INTO Patient (name,phone,hospital_name,blood_group_id) VALUES (%s,%s,%s,%s)",
                       (name.get(), phone.get(), hospital.get(), bg.get()))
        db.commit(); db.close()
        messagebox.showinfo("Success", "Patient Registered!")
        win.destroy()

    primary_btn(cf, "✓  Register Patient", save)

def patient_login():
    win = make_window("Patient Login", 400, 260)
    win_title(win, "Patient Login", "Enter your registered phone number")
    cf = form_card(win)
    phone = lbl_entry(cf, "Phone Number")

    def login():
        db = connect_db(); cursor = db.cursor()
        cursor.execute("SELECT patient_id FROM Patient WHERE phone=%s", (phone.get(),))
        result = cursor.fetchone(); db.close()
        if result:
            patient_dashboard(result[0])
            win.destroy()
        else:
            messagebox.showerror("Not Found", "No patient found with this phone.")

    primary_btn(cf, "→  Login", login)

def patient_dashboard(patient_id):
    dash = tk.Toplevel(root)
    dash.title("Patient Dashboard")
    dash.geometry("680x560")
    dash.configure(bg=BG)
    tk.Frame(dash, bg=ORANGE, height=4).pack(fill="x")

    top = tk.Frame(dash, bg=CARD)
    top.pack(fill="x")
    tk.Label(top, text="  Patient Dashboard", font=("Georgia",14,"bold"), fg=TEXT, bg=CARD).pack(side="left", padx=16, pady=12)
    tk.Label(top, text=f"ID: {patient_id}", font=FONT_SMALL, fg=MUTED, bg=CARD).pack(side="right", padx=16)

    body = tk.Frame(dash, bg=BG)
    body.pack(fill="both", expand=True, padx=20, pady=10)

    left = tk.Frame(body, bg=CARD, highlightbackground=BORDER, highlightthickness=1)
    left.pack(side="left", fill="y", padx=(0,12), ipadx=6, ipady=6)
    right = tk.Frame(body, bg=BG)
    right.pack(side="left", fill="both", expand=True)

    rbox = rbox_widget(right, h=20)

    tk.Label(left, text="REQUEST BLOOD", font=("Trebuchet MS",8,"bold"), fg=MUTED, bg=CARD).pack(anchor="w", padx=10, pady=(12,4))

    def request_blood():
        db = connect_db(); cursor = db.cursor()
        cursor.execute("INSERT INTO Request (patient_id,units_requested,request_date) VALUES (%s,1,%s)",
                       (patient_id, date.today()))
        db.commit(); db.close()
        messagebox.showinfo("Submitted", "Blood Request Sent!")

    sidebar_btn(left, "🩸  Request Blood", ACCENT, request_blood)

    tk.Label(left, text="SEARCH DONORS", font=("Trebuchet MS",8,"bold"), fg=MUTED, bg=CARD).pack(anchor="w", padx=10, pady=(16,4))
    bg_e   = sidebar_entry(left, "Blood Group ID")
    area_e = sidebar_entry(left, "Area / Address")

    def search_donor():
        db = connect_db(); cursor = db.cursor()
        query = "SELECT name, phone, address FROM Donor WHERE status='Active'"
        values = []
        if bg_e.get():
            query += " AND blood_group_id=%s"; values.append(bg_e.get())
        if area_e.get():
            query += " AND address LIKE %s"; values.append("%" + area_e.get() + "%")
        cursor.execute(query, values)
        results = cursor.fetchall(); db.close()
        rbox.delete("1.0", tk.END)
        if results:
            rbox.insert(tk.END, f"── Active Donors Found: {len(results)} ──────────────────\n")
            for r in results:
                rbox.insert(tk.END, f"  Name   : {r[0]}\n  Phone  : {r[1]}\n  Address: {r[2]}\n  {'─'*42}\n")
        else:
            rbox.insert(tk.END, "  No active donors found matching criteria.\n")

    sidebar_btn(left, "Search Donors", ORANGE, search_donor)

role_card(btn_area, "Register", "Patient intake",   SUCCESS, register_patient, 3, 0)
role_card(btn_area, "Login",    "Patient portal",   ORANGE,  patient_login,    3, 1)

# ════════════════════════════════════════════
#  ADMIN
# ════════════════════════════════════════════
tk.Label(btn_area, text="ADMINISTRATOR", font=("Trebuchet MS",9,"bold"),
         fg=MUTED, bg=BG).grid(row=4, column=0, columnspan=2, sticky="w", pady=(14,4))

def register_admin():
    win = make_window("Register Admin", 400, 300, "#8e44ad")
    win_title(win, "Admin Registration", "Register as a blood bank administrator")
    cf = form_card(win)
    name  = lbl_entry(cf, "Full Name")
    phone = lbl_entry(cf, "Phone Number")

    def save():
        db = connect_db(); cursor = db.cursor()
        cursor.execute("INSERT INTO Admin (name,phone) VALUES (%s,%s)", (name.get(), phone.get()))
        db.commit(); db.close()
        messagebox.showinfo("Success", "Admin Registered!")
        win.destroy()

    primary_btn(cf, "✓  Register Admin", save, "#8e44ad")

def admin_login():
    global current_admin_id
    win = make_window("Admin Login", 400, 260, "#8e44ad")
    win_title(win, "Admin Login", "Blood bank control panel")
    cf = form_card(win)
    phone = lbl_entry(cf, "Phone Number")

    def login():
        global current_admin_id
        db = connect_db(); cursor = db.cursor()
        cursor.execute("SELECT admin_id FROM Admin WHERE phone=%s", (phone.get(),))
        result = cursor.fetchone(); db.close()
        if result:
            current_admin_id = result[0]
            admin_dashboard(current_admin_id)
            win.destroy()
        else:
            messagebox.showerror("Not Found", "Admin not found.")

    primary_btn(cf, "→  Login", login, "#8e44ad")

def admin_dashboard(admin_id):
    dash = tk.Toplevel(root)
    dash.title("Admin Dashboard")
    dash.geometry("820x600")
    dash.configure(bg=BG)
    tk.Frame(dash, bg="#8e44ad", height=4).pack(fill="x")

    top = tk.Frame(dash, bg=CARD)
    top.pack(fill="x")
    tk.Label(top, text="  Admin Dashboard", font=("Georgia",14,"bold"), fg=TEXT, bg=CARD).pack(side="left", padx=16, pady=12)
    tk.Label(top, text=f"Admin ID: {admin_id}", font=FONT_SMALL, fg=MUTED, bg=CARD).pack(side="right", padx=16)

    body = tk.Frame(dash, bg=BG)
    body.pack(fill="both", expand=True, padx=20, pady=10)

    left = tk.Frame(body, bg=CARD, highlightbackground=BORDER, highlightthickness=1)
    left.pack(side="left", fill="y", padx=(0,12), ipadx=6, ipady=6)
    right = tk.Frame(body, bg=BG)
    right.pack(side="left", fill="both", expand=True)

    rbox = rbox_widget(right, h=22)

    tk.Label(left, text="PENDING REQUESTS", font=("Trebuchet MS",8,"bold"), fg=MUTED, bg=CARD).pack(anchor="w", padx=10, pady=(12,4))

    def load_requests():
        db = connect_db(); cursor = db.cursor()
        cursor.execute("""
            SELECT r.request_id, r.units_requested, r.request_date,
                   p.name, p.phone, p.hospital_name, bg.group_name
            FROM Request r
            JOIN Patient p ON r.patient_id = p.patient_id
            JOIN Blood_Group bg ON p.blood_group_id = bg.blood_group_id
            WHERE r.status='Pending'
        """)
        results = cursor.fetchall(); db.close()
        rbox.delete("1.0", tk.END)
        if results:
            rbox.insert(tk.END, f"── Pending Requests: {len(results)} ─────────────────────────────────\n")
            for r in results:
                rbox.insert(tk.END,
                    f"  Request ID : {r[0]}\n"
                    f"  Units      : {r[1]}   Date: {r[2]}\n"
                    f"  Patient    : {r[3]}   Phone: {r[4]}\n"
                    f"  Hospital   : {r[5]}   Blood: {r[6]}\n"
                    f"  {'─'*55}\n")
        else:
            rbox.insert(tk.END, "  ✓  No pending requests.\n")

    sidebar_btn(left, "↻  Load Requests", "#8e44ad", load_requests)

    tk.Label(left, text="APPROVE REQUEST", font=("Trebuchet MS",8,"bold"), fg=MUTED, bg=CARD).pack(anchor="w", padx=10, pady=(16,4))
    approve_e = sidebar_entry(left, "Request ID")

    def approve_request():
        db = connect_db(); cursor = db.cursor()
        try:
            cursor.execute("""UPDATE Request SET status='Approved', admin_id=%s
                              WHERE request_id=%s""", (admin_id, approve_e.get()))
            db.commit()
            messagebox.showinfo("Approved", "Request Approved Successfully!")
        except mysql.connector.Error as e:
            messagebox.showerror("Error", e.msg)
        finally:
            db.close()
            load_requests()

    sidebar_btn(left, "✓  Approve Request", SUCCESS, approve_request)

    # auto-load on open
    load_requests()

role_card(btn_area, "Register", "Create admin account", SUCCESS,   register_admin, 5, 0)
role_card(btn_area, "Login",    "Admin control panel",  "#8e44ad", admin_login,    5, 1)

# ── bottom bar ──
tk.Frame(root, bg=BORDER, height=1).pack(fill="x", padx=30, pady=(16,8))
tk.Label(root, text="🩸  Save Lives — Donate Blood",
         font=("Trebuchet MS", 9), fg=DARK_RED, bg=BG).pack(pady=(0,10))

root.mainloop()