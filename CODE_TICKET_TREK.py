import tkinter as tk
from tkinter import Canvas, ttk, messagebox, filedialog, PhotoImage, font  
from PIL import ImageTk, Image
import sqlite3
from datetime import datetime
from ttkthemes import ThemedStyle
from plyer import notification
import time
import threading
from threading import Thread
import itertools
import pygame

def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
def play_notification_sound():
    pygame.mixer.init()
    pygame.mixer.music.load(r"C:\Users\arun1\Downloads\WhatsApp Audio 2023-12-10 at 8.43.15 PM.mpeg") 
    pygame.mixer.music.play()
#intialization
def initialize_database():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, username TEXT NOT NULL, password TEXT NOT NULL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS trains (train_id INTEGER PRIMARY KEY, train_name TEXT NOT NULL, arrival_time TEXT NOT NULL, departure_time TEXT NOT NULL, date TEXT NOT NULL,
            total_seats INTEGER NOT NULL, available_seats INTEGER NOT NULL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS user_profile (profile_id INTEGER PRIMARY KEY, user_id INTEGER UNIQUE, phone_number TEXT, email TEXT, address TEXT,
                      FOREIGN KEY (user_id) REFERENCES users (user_id))''')
    cursor.execute(''' CREATE TABLE IF NOT EXISTS bookings (booking_id INTEGER PRIMARY KEY, train_id INTEGER, user_id INTEGER, user_name TEXT NOT NULL, phone_number TEXT NOT NULL, num_seats INTEGER NOT NULL,
            seat_numbers TEXT, booking_time TEXT NOT NULL, FOREIGN KEY (train_id) REFERENCES trains (train_id), FOREIGN KEY (user_id) REFERENCES users (user_id))''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS user_logins (login_id INTEGER PRIMARY KEY, user_id INTEGER, username TEXT NOT NULL,
            login_time TEXT NOT NULL,FOREIGN KEY (user_id) REFERENCES users (user_id))''')
    cursor.executemany('''INSERT INTO users (username, password) VALUES (?, ?)''', [('admin', 'admin123'), ('pes', 'pes123'),('Rachana','123') ])
    cursor.executemany('''INSERT INTO trains (train_id, train_name, arrival_time, departure_time, date, total_seats, available_seats) VALUES ( ?, ?, ?, ?, ?, ?, ?)ON CONFLICT(train_id) DO UPDATE SET
  train_name = excluded.train_name,
  arrival_time = excluded.arrival_time,
  departure_time = excluded.departure_time,
  date = excluded.date,
  total_seats = excluded.total_seats,
  available_seats = excluded.available_seats''', [
           ('12267' ,'MUMBAI CENTRAL-AHMEDABAD AC DURONTO EXP', '05:55', '23:25', '2023-12-10', 50, 50),
        ('12268' ,'AHMEDABAD-MUMBAI CENT AC DURONTO EXP', '06:00', '23:40', '2023-12-10', 42, 42),
        ('22201' ,'KOLKATA SEALDAH-PURI DURONTO EXPRESS', '04:00', '20:00', '2023-12-10', 30, 30),
        ('22204' ,'SECUNDERABAD-VISHAKAPATNAM AC DURONTO EXPRESS', '06:35', '20:15', '2023-12-10', 45, 45),
        ('22206' ,'MADURAI-CHENNAI CENTRAL AC DURONTO EXPRESS', '07:20', '22:40', '2023-12-10', 60, 60),
        ('12426' ,'JAMMU TAWI-NEW DELHI RAJDHANI EXPRESS', '05:05', '19:40', '2023-12-10', 56, 56),
        ('12430' ,'NEW DELHI-LUCKNOW AC SF EXPRESS', '06:40', '20:50', '2023-12-10', 58, 58),
        ('12437' ,'SECUNDERABAD-HAZRAT NIZAMUDDIN RAJDHANI EXPRESS', '10:25', '12:45', '2023-12-10', 63, 63),
        ('12951' ,'MUMBAI CENTRAL-NEW DELHI RAJDHANI EXPRESS', '08:35', '16:35', '2023-12-10', 30, 30),
        ('12953' ,'MUMBAI CENT-HAZRAT NIZAMUDDIN AUGUST KRANTI RAJ EXP', '10:55', '17:40', '2023-12-10', 65, 65),
        ('12019' ,'HOWRAH RANCHI SHATABDI EXPRESS', '13:15', '06:05', '2023-12-10', 32, 32),
        ('12038' ,'LUDHIANA NEWDELHI SHATABDI EXPRESS', '22:10', '16:40', '2023-12-10', 68, 68),
        ('12048' ,'FIROZPUR NEWDELHI SHATABDI EXPRESS', '21:10', '04:00', '2023-12-10', 43, 43),
        ('12049' ,'AGRA CANTT-DELHI NIZAMUDDIN GATIMANN EXPRESS', '19:30', '17:50', '2023-12-11', 59, 59),
        ('12050' ,'DELHI NIZAMUDDIN-AGRA CANTT GATIMANN EXPRESS', '09:50', '08:10', '2023-12-11', 28, 28),
        ('11077' ,'PUNE-JAMMU TAWI JHELUM EXPRESS', '10:10', '17:20', '2023-12-11', 39, 39),
        ('12138' ,'FIROZPUR CANTT-MUMBAI CST PUNJAB MAIL SF EXP', '07:35', '21:40', '2023-12-11', 44, 44),
        ('12295' ,'BANGALORE CITY-DANAPUR SANGHAMITRA SF EXP', '09:20', '09:00', '2023-12-11', 32, 32),
        ('12307' ,'HOWRAH-JODHPUR SF EXPRESS', '08:30', '23:30', '2023-12-011', 40, 40),
        ('12424' ,'NEW DELHI-DIBRUGARH TOWN RAJDHANI EXPRESS', '07:00', '13:55', '2023-12-11', 18, 18),
        ('12506' ,'DELHI ANAND VIHAR-GUWAHATI NORTH EAST EXPRESS', '16:50', '06:45', '2023-12-11', 22, 22),
        ('12801' ,'PURI-NEW DELHI PURUSHOTTAM SF EXPRESS', '04:50', '21:45', '2023-12-11', 25, 25),
        ('12802' ,'NEW DELHI-PURI PURUSHOTTAM SF EXPRESS', '05:25', '22:15', '2023-12-11', 30, 30),
        ('12833' ,'AHMEDABAD-HOWRAH SF EXPRESS', '13:30', '06:00', '2023-12-11', 14, 14),
        ('12859' ,'MUMBAI CST-HOWRAH GITANJALI SF EXPRESS', '12:30', '06:00', '2023-12-11', 18, 18),
        ('12864' ,'YESVANTPUR-HOWRAH SF EXPRESS', '06:25', '19:35', '2023-12-11', 19, 19),
        ('12426' ,'JAMMU TAWI-NEW DELHI RAJDHANI EXPRESS', '05:05', '19:40', '2023-12-12', 25, 25),
        ('12430' ,'NEW DELHI-LUCKNOW AC SF EXPRESS', '06:40', '20:50', '2023-12-12', 33, 33),
	('12437' ,'SECUNDERABAD-HAZRAT NIZAMUDDIN RAJDHANI EXPRESS', '10:45', '12:45', '2023-12-12', 28, 28),
	('12951' ,'MUMBAI CENTRAL-NEW DELHI RAJDHANI EXPRESS', '08:35', '16:35', '2023-12-12', 25, 25),
	('12953' ,'MUMBAI CENT-HAZRAT NIZAMUDDIN AUGUST KRANTI RAJ EXP', '10:55', '17:40', '2023-12-12', 39, 39),
	('12019' ,'HOWRAH-RANCHI SHATABDI EXPRESS', '13:15', '16:05', '2023-12-12', 42, 42),
	('12038' ,'LUDHIANA-NEW DELHI SHATABDI EXPRESS', '22:10', '16:40', '2023-12-12', 19, 19),
	('12048' ,'FIROZPUR-NEW DELHI SHATABDI EXPRESS', '21:10', '04:00', '2023-12-12', 14, 14),
	('12049' ,'AGRA CANTT-DELHI H NIZAMUDDIN GATIMANN EXPRESS', '19:30', '17:50', '2023-12-12', 22, 22),
	('12050' ,'DELHI H NIZAMUDDIN AGRA CANTT GATIMANN EXPRESS', '09:50', '08:10', '2023-12-12', 38, 38),
	('11077' ,'PUNE-JAMMU TAWI JHELUM EXPRESS', '10:00', '10:10', '2023-12-12', 17, 17),
	('12138' ,'FIROZPUR CANTT-MUMBAI CST PUNJAB MAIL SF EXP', '07:35', '21:40', '2023-12-12', 34, 34),
	('12296' ,'BANGALORE CITY-DANAPUR SANGHAMITRA SF EXP', '09:20', '09:00', '2023-12-12', 22, 22),
	('12307' ,'HOWRAH-JODHPUR SF EXPRESS', '08:30', '23:30', '2023-12-12', 14, 14),
        ('12424' ,'NEW DELHI-DIBRUNGARH TOWN RAJDHANI EXPESS', '07:00', '13:55', '2023-12-12', 30, 30), ])
    conn.commit()
    return conn, cursor

def get_user_id(cursor, username, password):
    result = cursor.execute('''SELECT user_id FROM users WHERE username = ? AND password = ?''', (username, password)).fetchone()
    return result[0] if result else None

def get_reserved_seats(cursor, train_id):
    result = cursor.execute(''' SELECT seat_numbers FROM bookings WHERE train_id = ?''', (train_id,)).fetchall()
    reserved_seats = set()
    for row in result:
        seats = map(int, row[0].split(','))
        reserved_seats.update(seats)

    return reserved_seats

def create_treeview(root, columns, headings):
    tree = ttk.Treeview(root, columns=columns, show="headings", height="100")
    for col, heading in zip(columns, headings):
        tree.heading(col, text=heading)
    return tree
def create_label(root, text, font=None):
    label = tk.Label(root, text=text, font=font)
    return label

def create_entry(root):
    entry = tk.Entry(root)
    return entry

def create_button(root, text, command):
    button = tk.Button(root, text=text, command=command)
    return button
def show_notification(title, message):
        notification.notify(
            title=title,
            message=message,
            timeout=20,)


def book_seats(conn, cursor, user_id, user_name, phone_number, train_id, num_seats, selected_seats):
    if len(phone_number) != 10:
        result_message = "Invalid phone number. Phone number must be exactly 10 digits."
        notification_message = result_message
    else:
        reserved_seats = get_reserved_seats(cursor, train_id)

        available_seats = cursor.execute('''SELECT available_seats FROM trains WHERE train_id = ?''', (train_id,)).fetchone()[0]

        if available_seats < int(num_seats) or any(seat in reserved_seats for seat in selected_seats):
            result_message = f"Seats{reserved_seats}are reserved and are not available for booking."
            notification_message = result_message
        else:
            booking_time = get_current_time()
            seat_numbers = ','.join(map(str, selected_seats))

            cursor.execute('''
                INSERT INTO bookings (train_id, user_id, user_name, phone_number, num_seats, seat_numbers, booking_time)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (train_id, user_id, user_name, phone_number, num_seats, seat_numbers, booking_time))

            available_seats -= int(num_seats)
            cursor.execute('''
                UPDATE trains SET available_seats = ? WHERE train_id = ?
            ''', (available_seats, train_id))

            result_message = f"Booking successful! {num_seats} seat(s) booked for Train ID {train_id}."
            notification_message = f"Seats booked for Train ID {train_id}"
            messagebox.showinfo("Booking Result", result_message)
            show_notification("Booking Result", notification_message)
           
    return result_message, notification_message


def railway_management_system_gui(root, conn, cursor, user_id, username):
    root.title("Railway Management System")
    root.geometry("1540x800")
    try:
        image = Image.open(r"C:/Users/arun1/Downloads/WhatsApp Image 2023-12-09 at 6.56.54 PM (1).jpeg")
        background_image = ImageTk.PhotoImage(image)
    except FileNotFoundError:
        print("Background image file not found. Please check the file path.")
        return
    canvas = Canvas(root, width=1280, height=660)
    canvas.pack(fill="both", expand=True)
    
    canvas.create_image(0, 0, anchor="nw", image=background_image)


    email_var = tk.StringVar(value="")
    phone_var = tk.StringVar(value="")
    address_var = tk.StringVar(value="")
    def show_notification(title, message):
        notification.notify(
        title=title,
        message=message,
        timeout=20,)

# Adding a running notification for the main menu window
    show_notification("Welcome", "Hello! Welcome to TICKET TREK. Experience seamless railway journey planning and booking with our intuitive Railway Management System, offering easy login, real-time seat reservations, and personalized user profiles through a user-friendly interface.")

    def on_profile_click():
        profile_window = tk.Toplevel(root)
        profile_window.title("Profile")
        profile_window.geometry("1540x600")
        background_image = Image.open(r"C:\Users\arun1\OneDrive\Pictures\WhatsApp Image 2023-12-15 at 5.02.36 PM.png")  
        photo = ImageTk.PhotoImage(background_image)
        background_label = tk.Label(profile_window, image=photo)
        background_label.image = photo
        background_label.place(relwidth=1, relheight=1)

       
        label_font = font.Font(family="Lucida Calligraphy", size=22)
        headline_label = create_label(profile_window, "PROFILE",font=label_font)
        headline_label.place(x=650, y=50)

        email_label = create_label(profile_window, "Email:", font=label_font)
        email_label.place(x=550,y=160)
       
        email_entry = create_entry(profile_window)
        email_entry.config(textvariable=email_var)
        email_entry.place(x=550,y=195)

        name_label = create_label(profile_window, "Name:", font=label_font)
        name_label.place(x=550,y=230)
        
        name_entry = create_entry(profile_window)
        name_entry.insert(0, username)  
        name_entry.place(x=550,y=270)


        phone_label = create_label(profile_window, "Phone Number:", font=label_font)
        phone_label.place(x=550,y=300)
        

        phone_entry = create_entry(profile_window)
        phone_entry.config(textvariable=phone_var)
        phone_entry.place(x=550,y=340)


        address_label = create_label(profile_window, "Address:", font=label_font)
        address_label.place(x=550,y=370)
        

        address_entry = create_entry(profile_window)
        address_entry.config(textvariable=address_var)
        address_entry.place(x=550,y=415)
                
        update_profile_button = create_button(profile_window, "Update Profile", lambda: update_profile())
        update_profile_button.place(x=650,y=460)

        email_var.set(email_entry.get())
        phone_var.set(phone_entry.get())
        address_var.set(address_entry.get())

        def update_profile():
           
            email = email_entry.get()
            phone_number = phone_entry.get()
            address = address_entry.get()

            if len(phone_number) != 10:
               messagebox.showerror("Error", "Phone number must be exactly 10 digits.")
               return

            cursor.execute('''
                INSERT OR REPLACE INTO user_profile (user_id, phone_number, email, address)
                VALUES (?, ?, ?, ?)
            ''', (user_id, phone_number, email, address))
            conn.commit()
            updated_details = f"Email: {email}\nName: {username}\nPhone Number: {phone_number}\nAddress: {address}"
            messagebox.showinfo("Profile Updated", f"Your profile has been updated!\n\n{updated_details}")

            email_var.set(email)
            phone_var.set(phone_number)
            address_var.set(address)
    def create_treeview_with_custom_style(root, columns, headings):
        style_name = "Custom.Treeview"

        style = ttk.Style()
        style.configure(style_name, font=('Lucida Calligraphy', 10))  
        style.layout(style_name, [('Treeview.treearea', {'sticky': 'nswe'})]) 

        tree = ttk.Treeview(root, columns=columns, show="headings", height="200", style=style_name)
        for col, heading in zip(columns, headings):
            tree.heading(col, text=heading)
        return tree

    def display_train_schedule_gui():
        train_schedule_window = tk.Toplevel(root)
        train_schedule_window.title("Train Schedule")
        train_schedule_window.geometry("1540x300")
        
        train_schedule_tree = create_treeview_with_custom_style(train_schedule_window, (1, 2, 3, 4, 5, 6, 7), ("Train ID", "Train Name", "Arrival Time", "Departure Time", "Date", "Total Seats", "Available Seats"))
        train_schedule = cursor.execute('''
            SELECT train_id, train_name, arrival_time, departure_time, date, total_seats, available_seats FROM trains
        ''').fetchall()

        for row in train_schedule:
            train_schedule_tree.insert("", "end", values=row)

        train_schedule_tree.pack()

    def bookings_gui():
        bookings_window = tk.Toplevel(root)
        bookings_window.title("Book Seats")
        bookings_window.geometry("1540x600")
        background_image = Image.open(r"C:\Users\arun1\Downloads\WhatsApp Image 2023-12-10 at 1.05.14 AM (5).jpeg") 
        photo = ImageTk.PhotoImage(background_image)
        background_label = tk.Label(bookings_window, image=photo)
        background_label.image = photo
        background_label.place(relwidth=1, relheight=1)

        label_font = font.Font(family="Lucida Calligraphy", size=18)
        user_name_label = create_label(bookings_window, f"Welcome, {username}!Enter your name:",font=label_font)
        user_name_label.place(x=550,y=50)

        user_name_entry = create_entry(bookings_window)
        user_name_entry.insert(0, username) 
        user_name_entry.place(x=550,y=90)

        phone_number_label = create_label(bookings_window, "Enter your phone number:",font=label_font)
        phone_number_label.place(x=550,y=130)

        phone_number_entry = create_entry(bookings_window)
        phone_number_entry.place(x=550,y=160)

        train_id_label = create_label(bookings_window, "Select Train ID:",font=label_font)
        train_id_label.place(x=550,y=200)

        train_ids = [str(row[0]) for row in cursor.execute('''SELECT train_id FROM trains''').fetchall()]
        train_id_var = tk.StringVar()
        train_id_var.set(train_ids[0])  
        train_id_dropdown = tk.OptionMenu(bookings_window, train_id_var, *train_ids)
        train_id_dropdown.place(x=550,y=240)

        num_seats_label = create_label(bookings_window, "Enter the number of seats:",font=label_font)
        num_seats_label.place(x=550,y=280)

        num_seats_entry = create_entry(bookings_window)
        num_seats_entry.place(x=550,y=315)
        
        seat_numbers_label = create_label(bookings_window, "Enter seat numbers (comma-separated):",font=label_font)
        seat_numbers_label.place(x=550,y=350)

        seat_numbers_entry = create_entry(bookings_window)
        seat_numbers_entry.place(x=550,y=390)

        
        def book_seats_button_click():
            user_name = user_name_entry.get()
            phone_number = phone_number_entry.get()
            train_id = train_id_var.get()
            num_seats = num_seats_entry.get()
            seat_numbers = seat_numbers_entry.get()
            

            if not all([user_name, phone_number, train_id, num_seats, seat_numbers]):
                messagebox.showerror("Error", "Please fill in all the details.")
                return
            selected_seats = list(map(int, seat_numbers.split(',')))

            result = book_seats(conn, cursor, user_id, user_name, phone_number, train_id, num_seats, selected_seats)
            messagebox.showinfo("Booking Result", result)
            booking_details = [train_id, result['booking_id'], train_name, num_seats, seat_numbers, result['booking_time'], user_name, phone_number]
            save_booking_to_file(booking_details)
            bookings_window.destroy()
       
        book_seats_button = create_button(bookings_window, "Book Seats", book_seats_button_click)
        book_seats_button.place(x=550,y=450)
        def save_booking_to_file(booking_details):
            filename = 'bookings.txt'

            with open(filename, 'a') as file:
                booking_string = ', '.join(map(str, booking_details)) + '\n'
                file.write(booking_string)
    def display_user_bookings_gui():
      display_bookings_window = tk.Toplevel(root)
      display_bookings_window.title("Display Booking Details")
      display_bookings_window.geometry("1540x300")
    
      user_bookings_tree = create_treeview_with_custom_style(display_bookings_window, (1, 2, 3, 4, 5, 6, 7, 8), ("Train ID", "Booking ID", "Train Name", "Num Seats", "Seat Numbers", "Booking Date and Time", "User Name", "Phone Number"))
      user_bookings_tree.pack()

      user_bookings = cursor.execute('''SELECT b.train_id, b.booking_id, t.train_name, b.num_seats, b.seat_numbers, b.booking_time, b.user_name, b.phone_number
        FROM bookings b
        JOIN trains t ON b.train_id = t.train_id
        WHERE b.user_id = ? 
    ''', (user_id,)).fetchall()

      for row in user_bookings:
        user_bookings_tree.insert("", "end", values=row)
      
    def display_login_details():
        login_details_window = tk.Toplevel(root)
        login_details_window.title("Login Details")
        login_details_window.geometry("1000x300")
       
        user_details_label = create_label(login_details_window, f"Logged in as: {username}")
        user_details_label.pack()

        user_logins_tree = create_treeview_with_custom_style(login_details_window, (1, 2, 3, 4), ("Login ID", "User ID", "Username", "Login Time"))
        user_logins_tree.pack()

        user_logins = cursor.execute('''
            SELECT login_id, user_id, username, login_time
            FROM user_logins
            WHERE user_id = ?
        ''', (user_id,)).fetchall()

        for item in user_logins_tree.get_children():
            user_logins_tree.delete(item)

        for row in user_logins:
            user_logins_tree.insert("", "end", values=row)
   
    def on_logout_click():
        confirm_logout = messagebox.askquestion("Logout", "Do you really want to log out?")
        if confirm_logout == 'yes':
            root.destroy()
    def create_button(root, text, command, font_size=12, relief="raised", bg="black", fg="white"):
        button = tk.Button(root, text=text, command=command, font=("Lucida Calligraphy", font_size),
                       relief=relief, bg=bg, fg=fg, borderwidth=3, highlightthickness=2)
        return button
           
    train_schedule_button = create_button(root, "Train Schedule", display_train_schedule_gui, font_size=30)
    train_schedule_button.place(x=900,y=100)

    bookings_button = create_button(root, "Book Seats", bookings_gui, font_size=30)
    bookings_button.place(x=900, y=200)

    display_booking_details_button = create_button(root, "Display Booking Details", display_user_bookings_gui, font_size=30)
    display_booking_details_button.place(x=900, y=300)

    login_details_button = create_button(root, "Login Details", display_login_details, font_size=30)
    login_details_button.place(x=900, y=400)

    profile_button = create_button(root, "Profile", on_profile_click, font_size=30)
    profile_button.place(x=900, y=500)

    logout_button = create_button(root, "Logout", on_logout_click, font_size=30)
    logout_button.place(x=900, y=600)

    
    
    running_message_var = tk.StringVar()
    running_message_label = tk.Label(root, textvariable=running_message_var, font=("Lucida Calligraphy", 22),bg="white")
    running_message_label.place(x=15, y=40, anchor="w")

    def update_running_message():
        messages = itertools.cycle([
        "🚆 Introducing TICKET TREK: Your Ultimate Railway Management System! 🚄","🎟 Book Seats Effortlessly","📅 Stay Informed with Train Schedules","👤 Personalized User Profiles","🔐 Secure and Reliable",
        "📈 Check Seat Availability","🌐 User-Friendly Interface","🎉 Join Us on TICKET TREK Today! 🚉","🌐 Visit us now! 🚄","📣 Follow us on social media for updates and promotions:","@Facebook: facebook.com/TRAINTREK",
        "@Twitter: twitter.com/TICKETTREK","@Instagram: instagram.com/TICKETTREK","🚆 TICKET TREK - Redefining Railway Travel! 🌟"
    ])

        def update_message():
          message = next(messages)
          running_message_var.set(message)
          root.after(3000, update_message)  
        update_message()
    update_running_message()

    root.mainloop()
def on_login_click(username_entry, password_entry, conn, cursor):
    username = username_entry.get()
    password = password_entry.get()

    user_id = get_user_id(cursor, username, password)

    if user_id is not None:
        cursor.execute('''
            INSERT INTO user_logins(user_id, username, login_time)
            VALUES (?, ?, ?)
        ''', (user_id, username, get_current_time()))
        
        conn.commit()
        messagebox.showinfo("Success", "Logged in successfully!")
        play_notification_sound()
        login_window.destroy()
        root = tk.Tk()
        railway_management_system_gui(root, conn, cursor, user_id, username)
        
        root.mainloop()
    else:
        messagebox.showerror("Error", "Invalid username or password")
def on_register_click(register_username_entry, register_password_entry, phone_entry, email_entry, conn, cursor):
    username = register_username_entry.get()
    password = register_password_entry.get()
    phone_number = phone_entry.get()
    email = email_entry.get()

    if len(phone_number) != 10:
        messagebox.showerror("Error", "Phone number must be exactly 10 digits.")
        return

    if not all([username, password, phone_number, email]):
        messagebox.showerror("Error", "Please enter all details.")
        return
    existing_user_id = get_user_id(cursor, username, password)
    if existing_user_id:
        messagebox.showinfo("Success", "You're already registered! Please log in.")
        return

    cursor.execute('''
        INSERT INTO users (username, password) VALUES (?, ?)
    ''', (username, password))
    user_id = cursor.lastrowid

    cursor.execute('''
        INSERT INTO user_profile (user_id, phone_number, email) VALUES (?, ?, ?)
    ''', (user_id, phone_number, email))

    conn.commit()

    messagebox.showinfo("Success", "Registered successfully!please LoG IN ")
def login_gui():
    global login_window
    login_window = tk.Tk()
    login_window.title("Login / Register")
    login_window.geometry("1540x800")
    
    image_path = ImageTk.PhotoImage(file=r"C:\Users\arun1\OneDrive\Pictures\WhatsApp Image 2023-12-10 at 8.43.20 PM.jpg")
    bg_image = tk.Label(login_window, image=image_path)
    bg_image.place(relwidth=1, relheight=1)  

    notebook = ttk.Notebook(login_window)
    style = ThemedStyle(login_window)
    style.set_theme("plastik")
    style.configure("TNotebook", background="#f2f2f2") 
    style.configure("TNotebook.Tab", background="#4CAF50", foreground="black", padding=[10, 5]) 
    style = ThemedStyle(login_window)
    style.set_theme("plastik")
    style = ttk.Style()
    style.configure("TNotebook", tabposition='n')  

    frame = tk.Frame(login_window)
    frame.place(relx=0.5, rely=0.70, anchor="center")

    notebook = ttk.Notebook(frame)

    login_tab = ttk.Frame(notebook)
    notebook.add(login_tab, text='Login')

    username_label = create_label(login_tab, "Username:")
    username_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")

    username_entry = create_entry(login_tab)
    username_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    password_label = create_label(login_tab, "Password:")
    password_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")

    password_entry = create_entry(login_tab)
    password_entry.config(show="*")
    password_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

    login_button = create_button(login_tab, "Login", lambda: on_login_click(username_entry, password_entry, conn, cursor))
    login_button.grid(row=2, column=0, columnspan=2, pady=10)

# Register Tab
    register_tab = ttk.Frame(notebook)
    notebook.add(register_tab, text='Register')

    register_username_label = create_label(register_tab, "Username:")
    register_username_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")

    register_username_entry = create_entry(register_tab)
    register_username_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    register_password_label = create_label(register_tab, "Password:")
    register_password_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")

    register_password_entry = create_entry(register_tab)
    register_password_entry.config(show="*")
    register_password_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

    phone_label = create_label(register_tab, "Phone Number:")
    phone_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")

    phone_entry = create_entry(register_tab)
    phone_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

    email_label = create_label(register_tab, "Email:")
    email_label.grid(row=3, column=0, padx=10, pady=10, sticky="e")

    email_entry = create_entry(register_tab)
    email_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")
    def on_register_click_wrapper():
        on_register_click(register_username_entry, register_password_entry, phone_entry, email_entry, conn, cursor)
        register_username_entry.delete(0, tk.END)
        register_password_entry.delete(0, tk.END)
        phone_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)

    register_button = create_button(register_tab, "Register",
                                    lambda: on_register_click(register_username_entry, register_password_entry, phone_entry, email_entry, conn, cursor))
    register_button.grid(row=4, column=0, columnspan=2, pady=10)

    notebook.pack(fill='both', expand=True)

    login_window.update_idletasks()
    width = login_window.winfo_width()
    height = login_window.winfo_height()
    x = (login_window.winfo_screenwidth() - width) // 2
    y = (login_window.winfo_screenheight() - height) // 2
    login_window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    login_window.mainloop()

# Main program

conn, cursor = initialize_database()
login_gui()
