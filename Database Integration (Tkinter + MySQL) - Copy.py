import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import mysql.connector
import hashlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Hash Function
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

#Database Connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",             
        database="online_learning_experience_survey"
    )


# For Registration 
def open_registration():     #Opens a new window for new users
    reg = tk.Toplevel()      #Opens a child window
    reg.title("User Registration")
    reg.geometry("400x400")

    tk.Label(reg, text="Username").grid(row=0, column=0, padx=10, pady=10)
    reg_username = tk.Entry(reg)
    reg_username.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(reg, text="Email").grid(row=1, column=0, padx=10, pady=10)
    reg_email = tk.Entry(reg)
    reg_email.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(reg, text="Password").grid(row=2, column=0, padx=10, pady=10)
    reg_password = tk.Entry(reg, show="*")
    reg_password.grid(row=2, column=1, padx=10, pady=10)

    tk.Label(reg, text="Confirm Password").grid(row=3, column=0, padx=10, pady=10)
    reg_confirm_password = tk.Entry(reg, show="*")
    reg_confirm_password.grid(row=3, column=1, padx=10, pady=10)

    def register_user():      #This runs when Register button is clicked
        username = reg_username.get()
        email = reg_email.get()
        password = reg_password.get()
        confirm_password = reg_confirm_password.get()

        if username == "" or email == "" or password == "":
            messagebox.showerror("Error", "All fields are required")
            return
        
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return 
        
        hashed_password = hash_password(password)

        try:                # insert into MySQL
            conn = get_db_connection()
            cursor = conn.cursor()

            query = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
            cursor.execute(query, (username, email, hashed_password))
            conn.commit()

            cursor.close()
            conn.close()

            messagebox.showinfo("Success", "Registration Successful!")
            reg.destroy()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(reg, text="Register", font=("Segoe UI", 10, "bold"), 
            bg="blue", fg="white", command=register_user).grid(row=4, column=1, columnspan=2, pady=20)


# For Login
def login_user():
    username = login_username.get()     #Read Inputs
    password = login_password.get() 

    if username == "" or password == "":
        messagebox.showerror("Error", "All fields are required")
        return

    hashed_password = hash_password(password)

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = "SELECT * FROM users WHERE username=%s AND password=%s"
        cursor.execute(query, (username, hashed_password))
        result = cursor.fetchone()      #Get single matching row

        cursor.close()
        conn.close()

        if result:

            role=result[4]

            messagebox.showinfo("Success","Login Successful")

            login.destroy()

            if role=="admin":
                open_admin_dashboard()
            else:
                open_survey()

        else:
            messagebox.showerror("Error","Invalid Login")

    except Exception as e:
        messagebox.showerror("Database Error", str(e))

# User Survey

def open_survey():  
    root = tk.Tk()
    root.title("Online Learning Experience Survey")
    root.geometry("600x1000")

    respondent_count = 1  

    title_label = tk.Label(root, text="ONLINE LEARNING EXPERIENCE SURVEY", 
                        font=("Helvetica", 16, "bold"), fg="#1E3A8A", bg="white")
    title_label.pack(pady=20)

    question_label = tk.Label(root,text="1. How would you rate your Online Learning Experience? *",font=("Times New Roman", 13))
    question_label.pack(pady=10, padx=20, anchor="w")

    experience_var = tk.StringVar()

    options = ["Excellent", "Good", "Average", "Poor"]
    for opt in options:
        tk.Radiobutton(root,
            text=opt, font=("Times New Roman", 12),
            variable=experience_var,
            value=opt).pack(anchor="w", padx=60)


    # Age Group
    age_label = tk.Label(root, text="2. Age Group (Optional)", font=("Times New Roman", 13))
    age_label.pack(pady=10, padx=20, anchor='w')

    age_var = tk.StringVar()

    age_dropdown = tk.OptionMenu(root, age_var,
        "School Student",
        "College Student",
        "Working Professional",
        "Others")
    age_dropdown.pack(padx=60, anchor='w')


    # Devise Used
    device_label = tk.Label(root, text="3. Which device do you use for online learning?", font=("Times New Roman", 13))
    device_label.pack(anchor="w", padx=20, pady=10)

    device_var = tk.StringVar()

    devices_dropdown = tk.OptionMenu(root, device_var,
        "Mobile Phone", 
        "Laptop", 
        "Tablet", 
        "Desktop Computer")
    devices_dropdown.pack(padx=60, anchor='w')


    # Time details
    time_label = tk.Label(root, text="4. How many hours do you spend on Online Learning per day?", font=("Times New Roman", 13))
    time_label.pack(anchor="w", padx=20, pady=10)

    time_var = tk.StringVar()

    time_dropdown = tk.OptionMenu(root, time_var,
        "Less than 1 hour", 
        "1-2 hours", 
        "2-4 hours", 
        "More than 4 hours")
    time_dropdown.pack(padx=60, anchor='w')


    # internet details
    internet_label = tk.Label(root, text="5. How is your internet connection during online learning?", font=("Times New Roman", 13))
    internet_label.pack(anchor="w", padx=20, pady=10)

    internet_var = tk.StringVar()

    internet_dropdown = tk.OptionMenu(root, internet_var,
        "Excellent", 
        "Good", 
        "Average", 
        "Poor")
    internet_dropdown.pack(padx=60, anchor='w')


    # Learning mode
    learning_label = tk.Label(root, text="6. Which learning mode do you prefer?", font=("Times New Roman", 13))
    learning_label.pack(anchor="w", padx=20, pady=10)

    learning_var = tk.StringVar()

    learning_dropdown = tk.OptionMenu(root, learning_var,
        "Online", 
        "Offline", 
        "Hybrid")
    learning_dropdown.pack(padx=60, anchor='w')


    def submit_response():  # This function runs when Submit is clicked.
        nonlocal respondent_count

        experience = experience_var.get()  # gets selected values
        age = age_var.get()
        device = device_var.get()
        time = time_var.get()
        internet = internet_var.get()
        learning = learning_var.get()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if experience == "":
            messagebox.showerror("Error", "Please select your Experience!")
            return  #Checks if user selected an option, If not, shows error popup
        
        respondent_id = f"RESP_{respondent_count}"
        respondent_count += 1   #Generates unique ID for each user

        
        try:   #risky code (database connection, insert query)
            conn = get_db_connection()
            cursor = conn.cursor()  #Connects to database
                                    #Cursor executes SQL queries

            query = """
            INSERT INTO response
            (response_id, poll_option, age_group, device_used, learning_time, internet_quality, learning_mode, timestamp)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """

            values = (respondent_id, experience, age, device, time, internet, learning, timestamp)  

            cursor.execute(query, values)   #Sends data to database
            conn.commit()   #saves the data permanently

            cursor.close()
            conn.close()

            messagebox.showinfo(
                "Submission Successful",
                f"Respondent ID: {respondent_id}\nExperience: {experience}\nAge Group: {age}\nDevice Used: {device}\nDaily Time Spent: {time}\nInternet Quality: {internet}\nLearning Mode: {learning}\nCurrent Time: {timestamp}"
            )  #Shows confirmation popup

            clear_response()

        except Exception as e:
            messagebox.showerror("Database Error", str(e))  #Exception Handling. It is used to handle errors so that: The program does not crash The user gets a clear error message

    #Clear Function
    def clear_response():
        experience_var.set("")
        age_var.set("")
        device_var.set("")
        time_var.set("")
        internet_var.set("")
        learning_var.set("")

    #Buttons
    button_frame = tk.Frame(root)
    button_frame.pack(pady=25)

    tk.Button(button_frame, text="Submit", font=("Segoe UI", 10, "bold"), 
            bg="blue", fg="white", width=7, cursor="hand2", 
            command=submit_response).grid(row=0, column=0, padx=10)

    tk.Button(button_frame, text="Clear", font=("Segoe UI", 10, "bold"), 
            bg="orange", fg="white", width=7, cursor="hand2",
            command=clear_response).grid(row=0, column=1, padx=10)

    tk.Button(button_frame, text="Exit", font=("Segoe UI", 10, "bold"), 
            bg="red", fg="white", width=7, cursor="hand2",
            command=root.quit).grid(row=0, column=2, padx=10)

    root.mainloop()


# Admin Dashboard

def open_admin_dashboard():

    admin = tk.Tk()
    admin.title("Admin Analytics Dashboard")
    admin.geometry("1000x1200")

    admin_label = tk.Label(admin,
        text="ADMIN ANALYTICS DASHBOARD",
        font=("Helvetica",16,"bold"),
        fg="#1E3A8A")
    admin_label.pack(pady=10)

    try:

        conn = get_db_connection()
        cursor = conn.cursor()

        # EXPERIENCE DATA 
        cursor.execute("""
        SELECT poll_option, COUNT(*)
        FROM response
        GROUP BY poll_option
        """)
        exp_data = cursor.fetchall()

        exp_labels = [row[0] for row in exp_data]
        exp_counts = [row[1] for row in exp_data]

        #  PROFESSION DATA
        cursor.execute("""
        SELECT age_group, COUNT(*)
        FROM response
        GROUP BY age_group
        """)
        prof_data = cursor.fetchall()

        prof_labels = [row[0] for row in prof_data]
        prof_counts = [row[1] for row in prof_data]

        #  DEVICE USED 
        cursor.execute("""
        SELECT device_used, COUNT(*)
        FROM response
        GROUP BY device_used
        """)
        dev_data = cursor.fetchall()

        dev_labels = [row[0] for row in dev_data]
        dev_counts = [row[1] for row in dev_data]

        # LEARNING TIME 
        cursor.execute("""
        SELECT learning_time, COUNT(*)
        FROM response
        GROUP BY learning_time
        """)
        time_data = cursor.fetchall()

        time_labels = [row[0] for row in time_data]
        time_counts = [row[1] for row in time_data]

        # INTERNET QUALITY 
        cursor.execute("""
        SELECT internet_quality, COUNT(*)
        FROM response
        GROUP BY internet_quality
        """)
        net_data = cursor.fetchall()

        net_labels = [row[0] for row in net_data]
        net_counts = [row[1] for row in net_data]

        # LEARNING MODE 
        cursor.execute("""
        SELECT learning_mode, COUNT(*)
        FROM response
        GROUP BY learning_mode
        """)
        mode_data = cursor.fetchall()

        mode_labels = [row[0] for row in mode_data]
        mode_counts = [row[1] for row in mode_data]

        cursor.close()
        conn.close()

        # CREATE CHARTS 
        fig, ax = plt.subplots(3,2, figsize=(12,12))

        # Experience Chart
        bars1 = ax[0,0].bar(exp_labels, exp_counts)
        ax[0,0].set_title("Learning Experience Rating")

        for bar in bars1:
            height = bar.get_height()
            ax[0,0].text(bar.get_x() + bar.get_width()/2, height,
                        str(height), ha='center', va='bottom')

        # Profession Chart
        ax[0,1].pie(prof_counts, labels=prof_labels, autopct='%1f%%')
        ax[0,1].set_title("Profession Distribution")

        # Device Used
        bars2 = ax[1,0].bar(dev_labels, dev_counts)
        ax[1,0].set_title("Device Used")

        for bar in bars2:
            height = bar.get_height()
            ax[1,0].text(bar.get_x() + bar.get_width()/2, height,
                        str(height), ha='center', va='bottom')

        # Learning Time
        ax[1,1].pie(time_counts, labels=time_labels, autopct='%1f%%')
        ax[1,1].set_title("Learning Time")

        # Internet Quality
        bars3 = ax[2,0].bar(net_labels, net_counts)
        ax[2,0].set_title("Internet Quality")

        for bar in bars3:
            height = bar.get_height()
            ax[2,0].text(bar.get_x() + bar.get_width()/2, height,
                        str(height), ha='center', va='bottom')

        # Learning Mode
        ax[2,1].pie(mode_counts, labels=mode_labels, autopct='%1f%%')
        ax[2,1].set_title("Learning Mode")

        plt.tight_layout()
        # Increase spacing
        plt.subplots_adjust(hspace=0.6, wspace=0.4)

        # Embed in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=admin)
        canvas.draw()
        canvas.get_tk_widget().pack()

    except Exception as e:
        messagebox.showerror("Database Error", str(e))

    admin.mainloop()


#Main Login Page
login = tk.Tk()
login.title("Login")
login.geometry("300x250")

tk.Label(login, text="Username").grid(row=0, column=0, padx=10, pady=10)
login_username = tk.Entry(login)
login_username.grid(row=0, column=1, padx=10, pady=10)

tk.Label(login, text="Password").grid(row=1, column=0, padx=10, pady=10)
login_password = tk.Entry(login, show="*")
login_password.grid(row=1, column=1, padx=10, pady=10)

tk.Button(login, text="Login",font=("Segoe UI", 10, "bold"), 
            bg="blue", fg="white", command=login_user).grid(row=3, column=1, columnspan=2, pady=20)
tk.Button(login, text="Register", font=("Segoe UI", 10, "bold"), 
            bg="orange", command=open_registration).grid(row=4, column=1, columnspan=2)

login.mainloop()