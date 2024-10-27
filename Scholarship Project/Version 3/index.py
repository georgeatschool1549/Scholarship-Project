'''
Financial Assistant Application | Version 3
George R
'''
import customtkinter as ctk# replacement for tkinter - custom version provides more customization, better GUI
import json # json file imported to be able to write/read for passwords an usernames
from PIL import Image # for the use of images in my code
import os # used to restart the application when user clicks log out
from CTkSpinbox import * # custom tikinter spin box 
import sys# used to restart the application when user clicks log out
import matplotlib.pyplot as plt# imporitng for GUI graph for spending tracker
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg# imporitng for GUI graph for spending tracker
from datetime import datetime, timedelta# imporitng for GUI graph for spending tracker
import calendar # imporitng for GUI graph for spending tracker
import google.generativeai as genai # google gemini API used for the AI section of my app
import tkinter as tk # used for gui 
import awesometkinter # used for progress bar
import ttkbootstrap as ttkb # used for my calendar
from tkvideo import tkvideo  # Import tkVideoPlayer
import smtplib # for the email service that sends a reset password number
import random # sets the random number. This is used for the reset code if the user forgot their password
from PIL import Image, ImageDraw, ImageTk 

logged_in_user = None  # keeps track of the currently logged in user
reset_codes = {}  # This dictionary stores the reset codes for each email

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def send_reset_email(to_email): # function to send the email
    reset_code = str(random.randint(100000, 999999))  # Generate random six digit code
    reset_codes[to_email] = reset_code  # Stores the reset code with the email
    subject = "Password Reset" #subject of the email
    body = f"Your reset code: {reset_code}. Enter the correct code into the prompt on screen." # body text
    message = f"Subject: {subject}\n\n{body}"

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp: # This line of code calls the SMTP to send the email. smtp.gmail.com is Gmails outgoing server name, 465 is the secure port (SSL)
            smtp.login("REDACTED --- PLEASE SEE README.TXT", "REDACTED --- PLEASE SEE README.TXT")  # Username and app password to be able to send the message 
            smtp.sendmail("REDACTED --- PLEASE SEE README.TXT", to_email, message) # sends the email from the email adress, to the already assigned variable, with the already assigned body text variable.
    except Exception: # if it fails, it will except it and then print the failed text
        print("Failed")

def load_users():# Load users from a json file
    with open(resource_path("users.json"), "r") as file:
        return json.load(file)

def save_users(users):# save user data back into the json file
    with open(resource_path("users.json"), "w") as file:
        json.dump(users, file, indent=4) # indent ensures appropriate spacing

def login():  # function to deal with the user login
    username = username_entry.get()  # gets username from the entry field
    password = password_entry.get()  # get password from entry field
    users = load_users()

    # make sure that the passwords are correct and load the spend tracker on successful login
    if username in users and users[username]["password"] == password:
        global logged_in_user # global ensures that it can be used within the entire program, not just the function
        logged_in_user = username #sets logged in user variable as the username
        login_frame.grid_forget()  # forget hides widget temporarly
        show_spend_tracker() # call the function for showing the spend tracker class
        
        window.after(100, show_spend_tracker)  # refreshes the window after 100 milleseconds. This is because the TK boostrap was messing with my application on the first load.
    else:
        error_label.configure(text="Invalid username or password. Please try again.")# show error if login fails due to wrong username or password

def play_video_in_image_frame():# Function to play the video in the left hand rectangle within the log in and create account page
    video_label = tk.Label(image_frame)# Create a label in the image frame for the video
    video_label.pack(fill="both", expand=True, padx=10, pady=10) # expand to fill the entire rectangle
   
    video_path = resource_path("better.mp4") #  path to video file

    if os.path.exists(video_path):    # ensures that the video exists
        def resize_video_label():# Function to resize the video label to fit the frame
            width = 920
            height = 780
            video_label.config(width=width, height=height)

        player = tkvideo(video_path, video_label, loop=1, size=(1386, 780))# runs the video and resizes it to fit
        player.play()

        window.after(100, resize_video_label)#resests the video after the videos is finished playing
    else:
        print(f"Video file not found at: {video_path}") # if the video cannot be found, the error will come up


def show_login_screen():# updates show_login_screen to play the video in the image frame
    login_content.grid(row=1, column=0, sticky="ns")
    play_video_in_image_frame()  # Plays the video in the image frame when the login screen is displayed

# show the account creation screen
def show_create_account():
    login_content.grid_forget() # temproaraly forget the displayed frame
    create_account_content.grid(row=1, column=0, sticky="ns") # stick to the corners of both north and south

def create_account():  # handle the account creation process
    new_username = new_username_entry.get()  # get the username entered by the user in create account
    new_password = new_password_entry.get()  # get the new password 
    new_email = new_email_entry.get()  # get the new email
    salary = salary_entry.get()  # get yearly salary
    users = load_users()  # load the users from json

    # Ensures that all fields are filled in
    if not new_username or not new_password or not new_email:
        create_account_error_label.configure(text="Please enter username, password, and email.")
        return

    # checks if the username already exists
    if new_username in users:
        create_account_error_label.configure(text="Username already exists.")
        return

    # checks to see if the email adress entered is valid. 
    if "@" not in new_email or "." not in new_email:
        create_account_error_label.configure(text="Enter a valid email address.")
        return

    try:  # Ensures that the salary input is a number
        salary = float(salary) if salary else 0  # store salary if (else default to 0)
    except ValueError:
        create_account_error_label.configure(text="Enter a valid number for salary.")
        return

    # Save the new user data
    users[new_username] = {"password": new_password, "email": new_email, "spending_history": [], "saving_goal": 0, "progress": 0, "salary": salary}

    save_users(users)

    create_account_content.grid_forget()  # switch to login screen after account creation
    login_content.grid(row=1, column=0, sticky="ns")
    success_label.configure(text="Account created successfully. Please log in.")  # success message

def show_email_popup():
    # Create a pop up window for entering the email address
    email_popup = ctk.CTkToplevel()
    email_popup.title("Reset password")
    email_popup.geometry("400x200")

    email_label = ctk.CTkLabel(email_popup, text="Enter your email adress to receive a reset code:", text_color="black")
    email_label.pack(pady=(20, 10))

    email_entry = ctk.CTkEntry(email_popup, width=300)
    email_entry.pack(pady=(0, 20))

    def send_reset():
        email = email_entry.get()
        users = load_users()

        # Loops through each user to find the matching email
        for username, user_data in users.items():
            if isinstance(user_data, dict) and user_data.get('email') == email:
                send_reset_email(email)  # runs the send reset code function to send the email
                show_reset_code_popup(email, username, email_popup)  # calls function to run the reset code pop up.
                break
        else:
            email_label.configure(text="Email Invalid. Please try again.", text_color="red")

    
    send_code_button = ctk.CTkButton(email_popup, text="Send Reset Code", command=send_reset)
    send_code_button.pack(pady=(10, 20))

def show_reset_code_popup(email, username, email_popup):
    email_popup.destroy()  # Close the email input popup

    reset_popup = ctk.CTkToplevel()
    reset_popup.title("Enter Reset Code")
    reset_popup.geometry("400x250")

    reset_code_label = ctk.CTkLabel(reset_popup, text="Enter the reset code from email:", text_color="black")
    reset_code_label.pack(pady=(20, 10))

    reset_code_entry = ctk.CTkEntry(reset_popup, width=300)
    reset_code_entry.pack(pady=(0, 20))

    def validate_reset_code(): # function to make sure that the number entered is acccurate. 
        entered_code = reset_code_entry.get()
        if reset_codes.get(email) == entered_code:# Compares the entered reset code with correct reset code from reset_codes dictionary
            show_reset_password_popup(email, username, reset_popup)  # Pass the username to updating the password
        else:
            reset_code_label.configure(text="Invalid code. Please try again.", text_color="red") # if incorrect, the user must try again.
    
    submit_code_button = ctk.CTkButton(reset_popup, text="Submit Code", command=validate_reset_code)
    submit_code_button.pack(pady=(10, 20))


def show_reset_password_popup(email, username, reset_popup):# function to allow the user to change their password
    reset_popup.destroy()  # Close the reset code popup

    password_popup = ctk.CTkToplevel()
    password_popup.title("Reset Password")
    password_popup.geometry("400x250")

    new_password_label = ctk.CTkLabel(password_popup, text="Enter New Password:", text_color="black")
    new_password_label.pack(pady=(20, 10))

    new_password_entry = ctk.CTkEntry(password_popup, width=300, show="*")
    new_password_entry.pack(pady=(0, 20))

    def update_password():
        new_password = new_password_entry.get()
        users = load_users()
        
        # Update the passwords
        if username in users and users[username]['email'] == email:
            users[username]['password'] = new_password
            save_users(users)
            new_password_label.configure(text="Password reset!", text_color="green")
        
        password_popup.destroy()  # closes the window
    
    reset_button = ctk.CTkButton(password_popup, text="Reset Password", command=update_password)
    reset_button.pack(pady=(10, 20))


def save_goal(goal_amount):# Save the user's financial goal in the json file
    users = load_users() # load the file
    if logged_in_user not in users:# set to deafult config if there is no information given (means its new account)
        users[logged_in_user] = {"spending_history": [], "saving_goal": 0, "progress": 0}
    users[logged_in_user]["saving_goal"] = goal_amount # sets the goal ammount variable to that from the json file
    users[logged_in_user]["progress"] = 0  # reset progress when a new goal is set
    save_users(users)

def update_progress(saved_amount):# Update saving progress in the json file and return the percentage of progress
    users = load_users()
    goal = users[logged_in_user].get("saving_goal", 0) # get the goal from the external file
    if goal > 0: # if it is greater than 0
        progress = (saved_amount / goal) * 100 # it turns it into a percentage 
        users[logged_in_user]["progress"] = progress # sets the variable, progress, as the progress from the json file of the logged in user
        save_users(users) # save it to the file
        return progress
    return 0 # if it equels to 0, then return to window frane

window = ctk.CTk()#  main window of the application
window.title("xCel Finance | Financial Application") #name of application
window.geometry("1920x1080") # size
window.configure(fg_color="#F3E4F6") # color 

window.grid_columnconfigure(0, weight=2)# Grid configuration for window layout before calling the object =
window.grid_columnconfigure(1, weight=1) # here too
window.grid_rowconfigure(0, weight=1) # 

image_frame = ctk.CTkFrame(window, fg_color="white", corner_radius=20)# image frame for displaying logo
image_frame.grid(row=0, column=0, padx=(20, 10), pady=20, sticky="nsew") # positioning and padding

login_frame = ctk.CTkFrame(window, fg_color="#d096dc", corner_radius=20)# Frame for the login GU Interface
login_frame.grid(row=0, column=1, padx=(10, 20), pady=20, sticky="nsew")
login_frame.grid_rowconfigure(0, weight=1) # configure the layout
login_frame.grid_rowconfigure(6, weight=1) 
login_frame.grid_columnconfigure(0, weight=1)

login_content = ctk.CTkFrame(login_frame, fg_color="transparent")# content for the login form
login_content.grid(row=1, column=0, sticky="ns")

title_label = ctk.CTkLabel(login_content, text="Ready to accelerate your\npersonal finance story?", font=("Arial", 24, "bold"), text_color="white")# title for the login section
title_label.pack(pady=(0, 30))

username_label = ctk.CTkLabel(login_content, text="Username:", text_color="white")# Username and password entry
username_label.pack(pady=(0, 5))
username_entry = ctk.CTkEntry(login_content, width=200)
username_entry.pack(pady=(0, 20))

password_label = ctk.CTkLabel(login_content, text="Password:", text_color="white")
password_label.pack(pady=(0, 5))
password_entry = ctk.CTkEntry(login_content, width=200, show="*")
password_entry.pack(pady=(0, 20))

# log in and account creation buttons
login_button = ctk.CTkButton(login_content, text="Log In", text_color="#208ad6", hover_color="#CFCFCF", fg_color="white", command=login)
login_button.pack(pady=(0, 20))

create_account_button = ctk.CTkButton(login_content, text="Create Account", command=show_create_account)
create_account_button.pack()

forgot_password_button = ctk.CTkButton(login_content, text="Forgot Password?", command=show_email_popup)  # Add the forgot password button
forgot_password_button.pack(pady=(10, 10))

# labels for displaying error or success messages
error_label = ctk.CTkLabel(login_content, text="", text_color="red")
error_label.pack(pady=(10, 0))

success_label = ctk.CTkLabel(login_content, text="", text_color="white")
success_label.pack(pady=(10, 0))

create_account_content = ctk.CTkFrame(login_frame, fg_color="transparent")# main content for creating a new account

create_account_title = ctk.CTkLabel(create_account_content, text="Create a new account", font=("Arial", 24, "bold"), text_color="white")
create_account_title.pack(pady=(0, 30))

new_username_label = ctk.CTkLabel(create_account_content, text="New Username:", text_color="white")
new_username_label.pack(pady=(0, 5))
new_username_entry = ctk.CTkEntry(create_account_content, width=200)
new_username_entry.pack(pady=(0, 20))

new_password_label = ctk.CTkLabel(create_account_content, text="New Password:", text_color="white")
new_password_label.pack(pady=(0, 5))
new_password_entry = ctk.CTkEntry(create_account_content, width=200, show="*")
new_password_entry.pack(pady=(0, 20))

new_email_label = ctk.CTkLabel(create_account_content, text="Email:", text_color="white")
new_email_label.pack(pady=(0, 5))
new_email_entry = ctk.CTkEntry(create_account_content, width=200)
new_email_entry.pack(pady=(0, 20))

salary_label = ctk.CTkLabel(create_account_content, text="Salary (optional):", text_color="white")
salary_label.pack(pady=(0, 5))
salary_entry = ctk.CTkEntry(create_account_content, width=200)
salary_entry.pack(pady=(0, 20))

# Button to activate for tbe new account
create_button = ctk.CTkButton(create_account_content, text="Create Account", command=create_account)
create_button.pack(pady=(0, 20))

# back button to log in screen
back_to_login_button = ctk.CTkButton(create_account_content, text="Back to Login", command=lambda: (create_account_content.grid_forget(), login_content.grid(row=1, column=0, sticky="ns")))
back_to_login_button.pack()

# error label   
create_account_error_label = ctk.CTkLabel(create_account_content, text="", text_color="red")
create_account_error_label.pack(pady=(10, 0))

# function to restart the app when called
def restart_app():
    python = sys.executable
    os.execl(python, python, *sys.argv)

# Log out function that destroys the window and restarts the app
def logout():
    window.destroy()
    restart_app()

# Function to quit the app
def quitapp():
    quit()

# Settings function for changing options such as changing theme or deleting account
def settings():
    def confirm_deletion(): # delete account function
        users = load_users()
        if logged_in_user in users:
            del users[logged_in_user]  # remove user from the list
            save_users(users)
            delete_window.destroy()  # close the settings
            logout()  # log out after deletion

    def switch_theme(): # toggle between light and dark mode
        current_mode = ctk.get_appearance_mode()
        if current_mode == "Dark":
            ctk.set_appearance_mode("Light")
        else:
            ctk.set_appearance_mode("Dark") 
    
    def remove_salary():# func to remove salary information
        users = load_users()
        if logged_in_user in users:
            users[logged_in_user]["salary"] = 0  # Remove salary by jsut setting it to 0
            save_users(users)
            salary_label.configure(text="Salary information removed.") # tell the user the action completed
    
    def add_salary():  # Func to add salary information
        new_salary = salary_entry.get()
        try:
            new_salary = float(new_salary)  # Validate to see if salary is numeric
        except ValueError:
            salary_label.configure(text="Please enter a valid numeric salary.")
            return

        users = load_users()
        if logged_in_user in users:
            users[logged_in_user]["salary"] = new_salary  # Update the salary in the user data
            save_users(users)
            salary_label.configure(text=f"Salary updated to ${new_salary:.2f}.") # tells the user how much the salary is updated to
    # create a pop up window for settings
    delete_window = ctk.CTkToplevel(window)
    delete_window.title("Settings") # name
    delete_window.geometry("300x600") # size

    ctk.CTkLabel(delete_window, text="Change to Dark/Light mode", wraplength=250).pack(pady=10)    # button to switch the theme of the application
    theme_button = ctk.CTkButton(delete_window, text="Switch Theme", command=switch_theme)# calls the fucntion from above
    theme_button.pack(pady=10)

    users = load_users()    # Section to add or remove salary information
    user_salary = users.get(logged_in_user, {}).get("salary", 0)

    if user_salary > 0:
        # only show the option to remove salary if the user has it already submted.
        ctk.CTkLabel(delete_window, text=f"Current Salary: ${user_salary:.2f}").pack(pady=10)
        remove_salary_button = ctk.CTkButton(delete_window, text="Remove Salary", command=remove_salary)
        remove_salary_button.pack(pady=10)
    else:
        # only show the option to add salary if they do not already have it
        ctk.CTkLabel(delete_window, text="No salary information. Add your salary below:").pack(pady=10)
        salary_entry = ctk.CTkEntry(delete_window, placeholder_text="Enter salary")
        salary_entry.pack(pady=5)
        add_salary_button = ctk.CTkButton(delete_window, text="Add Salary", command=add_salary)
        add_salary_button.pack(pady=10)

    salary_label = ctk.CTkLabel(delete_window, text="")
    salary_label.pack(pady=10)

    #label and button for confirming account deletion
    ctk.CTkLabel(delete_window, text="Delete Account", wraplength=250).pack(pady=10)
    confirm_button = ctk.CTkButton(delete_window, text="Delete", fg_color="red", text_color="white", command=confirm_deletion)
    confirm_button.pack(padx=20, pady=10)

    # button to close the settings pop up window
    cancel_button = ctk.CTkButton(delete_window, text="Close Settings", command=delete_window.destroy)
    cancel_button.pack(padx=20, pady=10)

def create_top_bar(parent):
    top_bar = ctk.CTkFrame(parent, height=60, fg_color="#d096dc") 
    top_bar.pack(side="top", fill="x")  # make top bar stretch across the entire window
    top_bar.pack_propagate(False)  # Fix the height of bar

    # fix logo to fit within the top bar
    logo = ctk.CTkImage(Image.open(resource_path("diplogo.png")), size=(150, 64))
    logo_label = ctk.CTkLabel(top_bar, image=logo, text="")
    logo_label.pack(side="left", padx=10)  # align logo to the left side

def create_sidebar(parent):# sidebar func for navigation 
    sidebar = ctk.CTkFrame(parent, fg_color="#F3E4F6", width=150)  # sidebar with fixed width
    sidebar.pack(side="left", fill="y", pady=(0, 0))  # sidebar spans the height of the window

    button_color = "#d096dc"  # sidebar button color
    button_text_color = "white"
    button_width = 140  # button width to 140px

    set_button_image = ctk.CTkImage(Image.open(resource_path("settings.png")), size=(140, 99))# settings button with an image as the button.
    set_button = ctk.CTkButton(master=sidebar, image=set_button_image, text="", fg_color="transparent", hover=False, command=settings, width=button_width)
    set_button.pack(fill="x", padx=(5, 5))  # equal padding on left and right
    # logout and quit buttons
    logout_button = ctk.CTkButton(master=sidebar, text="Log Out", command=logout, fg_color="white", text_color="black", hover_color="#d9b1e0", width=button_width)
    logout_button.pack(pady=(20, 10), fill="x", padx=(5, 5))  #equal padding on left and right

    quit_button = ctk.CTkButton(master=sidebar, text="Quit", command=quitapp, fg_color="red", text_color="black", hover_color="#d9b1e0", width=button_width)
    quit_button.pack(pady=10, fill="x", padx=(5, 5))  # equal padding on left and righ

    gap = ctk.CTkLabel(master=sidebar, text="")    # I used a label to act as a spacer between top and bottom buttons
    gap.pack(pady=25)

    spend_button = ctk.CTkButton(master=sidebar, text="Spend Tracker", command=show_spend_tracker, fg_color=button_color, text_color=button_text_color, hover_color="#d9b1e0", width=button_width)    # spend tracker button
    spend_button.pack(pady=5, fill="x", padx=(5, 5))  # equal padding on left and right

    # finance school button
    school_button = ctk.CTkButton(master=sidebar, text="Finance School", command=show_school_frame, fg_color=button_color, text_color=button_text_color, hover_color="#d9b1e0", width=button_width)
    school_button.pack(pady=5, fill="x", padx=(5, 5))  # equal padding on left and right

    # Add this in the create_sidebar function, where other buttons are added:
    salary_button = ctk.CTkButton(master=sidebar, text="Salary Tracker", command=show_salary_tracker, fg_color=button_color, text_color=button_text_color, hover_color="#d9b1e0", width=button_width)
    salary_button.pack(pady=5, fill="x", padx=(5, 5))  # padding and alignment

    # AI button
    ai_button = ctk.CTkButton(master=sidebar, text="xCel AI Assistant", command=show_ai_chat, fg_color=button_color, text_color=button_text_color, hover_color="#d9b1e0", width=button_width)
    ai_button.pack(pady=5, fill="x", padx=(5, 5)) 

def show_spend_tracker():# function shows the spending tracker screen
    for widget in window.winfo_children():
        widget.destroy()  # clears the content from the window

    create_top_bar(window)  # add the top bar
    create_sidebar(window)  # add the sidebar

    # main content area for the spend tracker
    content_frame = ctk.CTkFrame(window)
    content_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    spend_tracker = SpendTracker()  # create an instance of the spend tracker class
    spend_tracker.add_item(content_frame)  # add spend tracker elements to the content frame

# show the ai chat interface
def show_ai_chat():
    for widget in window.winfo_children():
        widget.destroy()  # clear window content
    create_top_bar(window)
    create_sidebar(window)

    # main content area for AI chat
    content_frame = ctk.CTkFrame(window)
    content_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    AIChat(content_frame)  # call the class 

# show the finance school interface
def show_school_frame():
    for widget in window.winfo_children():
        widget.destroy()  # clear window content
    create_top_bar(window)
    create_sidebar(window)

    # Main content area for finance school
    content_frame = ctk.CTkFrame(window)
    content_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    SchoolFrame(content_frame)  # finance school class

# spending tracker
class SpendTracker:
    def __init__(self):
        # list of spending categories
        self.cat_list = [
            "Food", "Technology", "Entertainment", "Groceries", "Medical",
            "Petrol", "Travel", "Clothing", "Utilities", "Education",
            "Fitness", "Subscriptions", "Gifts", "Personal Care",
            "Other (wants)", "Other (needs)"
        ]
        self.items = []  # List to store spending items

    def add_item(self, parent_frame):
        # container for the two rectangles
        container_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
        container_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Adjust grid configuration for the container
        container_frame.grid_columnconfigure(0, weight=3)
        container_frame.grid_columnconfigure(1, weight=1) 
        container_frame.grid_rowconfigure(0, weight=1)  # call the height of the content

        left_frame = ctk.CTkFrame(container_frame, fg_color="white", corner_radius=20)# Left frame for item inputs and spending history and chart
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=10)

        right_frame = ctk.CTkFrame(container_frame, fg_color="white", corner_radius=20)# Right frame for financial goals
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=10)

        left_frame.grid_rowconfigure(2, weight=1) # configure left frame rows and columns to control widget resizing
        left_frame.grid_columnconfigure(0, weight=1)

        input_frame = ctk.CTkFrame(left_frame, fg_color="transparent") # Left frame contents for input fields and calendar
        input_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        ctk.CTkLabel(input_frame, text="Item Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.p_name = ctk.CTkEntry(input_frame, width=200)
        self.p_name.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        # Category
        ctk.CTkLabel(input_frame, text="Category:").grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.p_cat = ctk.CTkComboBox(input_frame, values=self.cat_list, width=200)
        self.p_cat.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # Price
        ctk.CTkLabel(input_frame, text="Price:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.p_price = tk.Spinbox(input_frame, from_=0, to=100000, increment=1.0, width=10)
        self.p_price.grid(row=1, column=2, padx=5, pady=5, sticky="w")

        # Calendar
        ctk.CTkLabel(input_frame, text="Select Date:").grid(row=0, column=3, padx=5, pady=5, sticky="w")

        self.p_date = ttkb.DateEntry(input_frame, bootstyle="primary", dateformat="%d/%m/%Y")
        self.p_date.grid(row=1, column=3, padx=5, pady=5, sticky="w")


        # Submit button
        self.p_submit = ctk.CTkButton(input_frame, text="Submit", command=self.submit_item)
        self.p_submit.grid(row=1, column=4, padx=5, pady=5, sticky="w")

        # spending history box 
        display_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        display_frame.grid(row=2, column=0, sticky="", padx=10, pady=10)

        display_frame.grid_columnconfigure(0, weight=1)  # Add weight to center the content
        display_frame.grid_columnconfigure(1, weight=1)  # Add weight to center the content

        ctk.CTkLabel(display_frame, text="Spending History:").grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="w")
        self.display_area = ctk.CTkTextbox(display_frame, height=150, width=400)  
        self.display_area.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        self.display_text()

        self.clear_button = ctk.CTkButton(display_frame, text="Clear History", command=self.clear_history)# Button to clear history
        self.clear_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="n")

        ctk.CTkLabel(left_frame, text="Spending Chart (Last 12 Months):").grid(row=3, column=0, padx=10, pady=5, sticky="w")# monthly spending chart uisng matplot lib
        self.create_spending_chart(left_frame)

        # right frame contents for financial goals
        ctk.CTkLabel(right_frame, text="Financial Goals", font=("Arial", 18)).pack(pady=10)

        ctk.CTkLabel(right_frame, text="Enter Saving Goal:").pack(pady=5)
        self.goal_spinbox = tk.Spinbox(right_frame, from_=0, to=1000000, increment=1, width=10)
        self.goal_spinbox.pack(pady=10)

        self.set_goal_button = ctk.CTkButton(right_frame, text="Set Saving Goal", command=self.set_goal)
        self.set_goal_button.pack(pady=10)

        ctk.CTkLabel(right_frame, text="Enter Saved Amount:").pack(pady=5)
        self.saved_amount_spinbox = tk.Spinbox(right_frame, from_=0, to=1000000, increment=1, width=10)
        self.saved_amount_spinbox.pack(pady=10)

        self.update_progress_button = ctk.CTkButton(right_frame, text="Update Progress", command=self.update_saving_progress)
        self.update_progress_button.pack(pady=10)

        # progress bar that is imported from awesome tkinter. This is to show theprgress of th eusers savings goals.
        self.progressbar = awesometkinter.RadialProgressbar(right_frame, fg='green', parent_bg="white", bg="white", size=(130,130))
        self.progressbar.pack(padx=20, pady=10)

        self.goal_label = ctk.CTkLabel(right_frame, text=f"Current Saving Goal: $0.00", text_color="black")# label to display the current saving goal amount
        self.goal_label.pack(pady=5)

        users = load_users()
        user_data = users.get(logged_in_user, {})
        saved_progress = user_data.get("progress", 0)
        saving_goal = user_data.get("saving_goal", 0)
        self.progressbar.set(saved_progress)
        self.goal_label.configure(text=f"Current Saving Goal: ${saving_goal:.2f}")

    def clear_history(self):# function to clear spending history
        users = load_users()
        users[logged_in_user]["spending_history"] = []  # Clears the history
        save_users(users)
        self.display_text()  # Refresh the display area
        self.create_spending_chart(self.parent_frame)  # update the chart by refreshing it.

    def set_goal(self):# function to set the saving goal
        goal_amount = float(self.goal_spinbox.get())
        save_goal(goal_amount)
        self.progressbar.set(0)
        self.goal_label.configure(text=f"Current Saving Goal: ${goal_amount:.2f}") # displays the set savings goal through the label

    def update_saving_progress(self):# update saving progress when the user adds it
        saved_amount = float(self.saved_amount_spinbox.get())
        progress = update_progress(saved_amount) # sCES IT UNDER this varibale
        self.progressbar.set(progress)

    def submit_item(self):# function to submit a spending item within the left hand pannel
        name = self.p_name.get()
        category = self.p_cat.get()

        # Validate that the price input is numeric
        try:
            price = float(self.p_price.get())
        except ValueError:
            self.display_area.insert("end", "Please enter a valid numeric price for the product.\n")
            return

        date = self.p_date.entry.get()  # gets selected date

        new_item = {"name": name, "category": category, "price": price, "date": date}

        users = load_users()
        users[logged_in_user]["spending_history"].append(new_item)  # save to the user's spending history
        save_users(users)

        # Refresh the Spend Tracker page to update the chart
        show_spend_tracker()  # This will reload the page as well as the chart

    def display_text(self): # display spending history
        self.display_area.delete('1.0', "end")  # clear existing text
        users = load_users()
        spending_history = users.get(logged_in_user, {}).get("spending_history", [])

        for item in spending_history:
            display_str = f"{item['name']}, {item['category']}, {item['price']}, {item['date']}\n"
            self.display_area.insert("end", display_str)
    
    def create_spending_chart(self, parent_frame):# create spending chart through matplotlib
        spending_data = self.read_spending_data()  # get spending data from the logged in user

        fig, ax = plt.subplots(figsize=(6, 2.5))  #resizes the chart

        if spending_data:
            monthly_spending = {month: 0 for month in range(1, 13)}

            for date, amount in spending_data:
                monthly_spending[date.month] += amount

            months = list(calendar.month_abbr)[1:]  # month abbreviations fdor title on the axis - e.g jan etc 
            spending_values = [monthly_spending[month] for month in range(1, 13)]

            bars = ax.bar(months, spending_values)

            ax.set_xlabel("Month") # titles 
            ax.set_ylabel("Amount Spent ($)")
            ax.set_title("Monthly Spending")

            for bar in bars:
                height = bar.get_height()
                if height > 0:
                    ax.text(bar.get_x() + bar.get_width() / 2., height, f"${height:.2f}", ha="center", va="bottom")

            plt.xticks(rotation=45)

        else:
            ax.text(0.5, 0.5, "No spending data available", horizontalalignment="center", verticalalignment="center")

        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=parent_frame)# use grid for the chart canvas
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
        canvas.draw()

    def read_spending_data(self):# read spending data from the users history
        spending_data = []  # list to store spending data
        today = datetime.now()
        start_of_year = datetime(today.year, 1, 1)

        users = load_users()
        user_spending_history = users.get(logged_in_user, {}).get("spending_history", [])

        for item in user_spending_history:
            try:
                # first the programme is to try dmy
                try:
                    date = datetime.strptime(item["date"], "%d/%m/%Y")
                except ValueError:
                    # if not it wil accept mdy
                    date = datetime.strptime(item["date"], "%m/%d/%y")

                price = float(item["price"])

                if date >= start_of_year:
                    spending_data.append((date, price))

            except ValueError: # error handilling
                print("error")
            except KeyError:
                print("error")
            except Exception:
                print("error")

        spending_data.sort(key=lambda x: x[0])
        return spending_data

# class for ai chat interface
class AIChat:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.create_ai_chat_frame()

    def create_ai_chat_frame(self):
        frame = ctk.CTkFrame(self.parent_frame)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        os.environ["GENERATIVE_AI_KEY"] = "REDACTED --- PLEASE SEE README.TXT"  # google gemini key
        genai.configure(api_key=os.getenv("GENERATIVE_AI_KEY"))

        # Configure the AI model
        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
        }

        self.model = genai.GenerativeModel(
            model_name="gemini-1.0-pro",
            generation_config=generation_config,
        )
        self.chat_session = self.model.start_chat(history=[])  # start new chat with AI

        ctk.CTkLabel(frame, text="Enter your question:").pack(anchor="w", pady=(0, 5))
        self.question_entry = ctk.CTkEntry(frame, width=500)
        self.question_entry.pack(fill="x", pady=(0, 10), padx=(0, 10))

        submit_button = ctk.CTkButton(frame, text="Submit", command=self.send_question)
        submit_button.pack(pady=(0, 10))

        ctk.CTkLabel(frame, text="Disclaimer - Responses are generated by google Gemini. Some responses may not be accurate.").pack(anchor="w", pady=(0, 5))
        self.response_text = ctk.CTkTextbox(frame, height=400, width=700)
        self.response_text.pack(fill="both", expand=True, pady=(0, 10))

    def send_question(self): # function to send the question to google gemini servers
        question = self.question_entry.get()
        if question:
            response = self.chat_session.send_message(question)
            self.response_text.insert("end", f"Q: {question}\n\nA: {response.text}\n\n")
            self.question_entry.delete(0, "end")

class SalaryTracker: # SalaryTracker class for the frame to show the income of the user
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.create_salary_tracker_frame()

    def create_salary_tracker_frame(self):
        #  main frame for salary tracker content
        frame = ctk.CTkFrame(self.parent_frame)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Load user data to retrieve the salary
        users = load_users()
        user_data = users.get(logged_in_user, {})
        salary = user_data.get("salary", 0)

        if salary == 0:
            ctk.CTkLabel(frame, text="No salary information here! Head to user settings to add it.", font=("Arial", 18)).pack(pady=10) # if the user has no salary, this message will appear
            return
        
        ctk.CTkLabel(frame, text="Projected net income over next 5 Years", font=("Arial", 18)).pack(pady=10)      # title
        
        years = list(range(1, 6))# generates data for the next 5 years based on salary input
        salary_projection = [salary * year for year in years]

        fig, ax = plt.subplots(figsize=(6, 4))# Creating the line chart
        ax.plot(years, salary_projection, marker="o")
        ax.set_title("Net Income Over 5 Years")
        ax.set_xlabel("Years")
        ax.set_ylabel("Total Salary ($)")
        ax.grid(True)

        canvas = FigureCanvasTkAgg(fig, master=frame)# plot into Tkinter
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

def show_salary_tracker():# Function to show salary tracker page
    for widget in window.winfo_children():
        widget.destroy()  # clear window content
    create_top_bar(window)
    create_sidebar(window)

    # Main content area for salary tracker
    content_frame = ctk.CTkFrame(window)
    content_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    SalaryTracker(content_frame)  # calls the class to create the salary tracker page

class SchoolFrame:# class for the finance school interface
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.create_school_frame()

    def create_school_frame(self): # creating the main frame
        main_frame = ctk.CTkFrame(self.parent_frame)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        button_frame = ctk.CTkFrame(main_frame)
        button_frame.pack(fill="x", padx=10, pady=(10, 5))

        content_frame = ctk.CTkFrame(main_frame)
        content_frame.pack(fill="both", expand=True, padx=10, pady=(5, 10))

        self.content_text = ctk.CTkTextbox(content_frame, wrap="word", width=600, height=400)
        self.content_text.pack(fill="both", expand=True, padx=10, pady=10)

        topics = ["Learn about budgeting", "When to save/spend", "What is investing?", "How to track spending?", "Summary"] # topics that are the titles for each button
        for topic in topics:
            ctk.CTkButton(button_frame, text=topic, command=lambda t=topic: self.show_content(t), width=180).pack(side="left", padx=5) # creates a button for each topic provided above 

        self.show_content("Learn about budgeting") 

    def show_content(self, topic): # function to show the content based on what the user asked for
        self.content_text.delete("1.0", "end")
        file_path = resource_path("scl1.txt") # importing the text file that has the informaiton
        try:
            with open(file_path, "r") as file:
                all_content = file.read().split('\n\n\n\n')# splits the content for each topic
                topic_dict = {"Learn about budgeting": 0, "When to save/spend": 1, "What is investing?": 2, "How to track spending?": 3, "Summary": 4} # dictionary to assign the text files to each topic
                if topic in topic_dict:
                    self.content_text.insert("end", all_content[topic_dict[topic]])  # display content
                else:
                    self.content_text.insert("end", "Topic not found") # error handiling if the text file is not founf
        except FileNotFoundError:
            self.content_text.insert("end", "File not found")# error handiling if the text file is not founf

# code to start the application 
if __name__ == "__main__":
    show_login_screen()
    window.mainloop()  # Start the window loop, which is the first frame
