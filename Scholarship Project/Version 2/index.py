'''
Financial Assistant Application | Version 2
George R
'''
import customtkinter as ctk # replacement for tkinter - custom version provides more customization, better GUI
import json # json file imported to be able to write/read for passwords an usernames
from PIL import Image # for the use of images in my code
import os # used to restart the application when user clicks log out
from tkcalendar import Calendar # external module to display the calnendar, user can select date
import google.generativeai as genai # google gemini API used for the AI section of my app
from CTkSpinbox import * # custom tikinter spin box 
import sys # used to restart the application when user clicks log out
import matplotlib.pyplot as plt # imporitng for GUI graph for spending tracker
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg# imporitng for GUI graph for spending tracker
from datetime import datetime, timedelta# imporitng for GUI graph for spending tracker
import calendar# imporitng for GUI graph for spending tracker
import tkinter as tk
import smtplib
import random

reset_codes = {}  # Dictionary to store reset codes for each email

def send_reset_email(to_email):
    reset_code = str(random.randint(100000, 999999))  # Generate 6-digit reset code
    reset_codes[to_email] = reset_code  # Store the reset code with the email
    subject = "Password Reset"
    body = f"Your reset code: {reset_code}. Enter the correct code into the prompt on screen."
    message = f"Subject: {subject}\n\n{body}"

    # Set up Gmail SMTP
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login("REDACTED --- PLEASE SEE README.TXT", "REDACTED --- PLEASE SEE README.TXT")  # Your app password here
            smtp.sendmail("REDACTED --- PLEASE SEE README.TXT", to_email, message)
    except Exception as e:
        print(f"Failed to send email: {e}")

def load_users(): # function to open and read the jason file for passwords
    with open("Version 2/users.json", "r") as file:
        return json.load(file)

def save_users(users):# function to open and write the jason file for passwords
    with open("Version 2/users.json", "w") as file:
        json.dump(users, file) # writing the username and password to the json

def login(): # log in function
    username = username_entry.get() # Get the username
    password = password_entry.get() # Get the password
    users = load_users() # Load users from the JSON file
    
    # Check if the username exists and the password matches
    if users.get(username) and users[username].get('password') == password:
        login_frame.grid_forget()  # Hide the login frame
        show_spend_tracker()  # Show the spending tracker frame
    else:
        error_label.configure(text="Invalid username or password. Please try again.")

def show_create_account(): # function for if the user creates a new account 
    login_content.grid_forget() # hide the log in page 
    create_account_content.grid(row=1, column=0, sticky="ns") # sets the layout

def create_account():
    new_username = new_username_entry.get()  # Get the username input
    new_password = new_password_entry.get()  # Get the password input
    new_email = new_email_entry.get()  # Get the email input
    users = load_users()

    # Check if the fields are empty
    if not new_username or not new_password or not new_email:
        create_account_error_label.configure(text="Please enter a username, password, and email.")
        return

    # Check if the username already exists
    if new_username in users:
        create_account_error_label.configure(text="Username already exists. Please choose another.")
        return

    # Store the new user data with email
    users[new_username] = {"password": new_password, "email": new_email}
    save_users(users)

    create_account_content.grid_forget()  # Hide the account creation form
    login_content.grid(row=1, column=0, sticky="ns")  # Show the login form

    error_label.configure(text="Account created successfully. Please log in.")  # Success message
def show_email_popup():
    # Create a pop-up window for entering the email address
    email_popup = ctk.CTkToplevel()
    email_popup.title("Password Reset")
    email_popup.geometry("400x200")

    email_label = ctk.CTkLabel(email_popup, text="Enter your email to receive a reset code:", text_color="black")
    email_label.pack(pady=(20, 10))

    email_entry = ctk.CTkEntry(email_popup, width=300)
    email_entry.pack(pady=(0, 20))

    def send_reset():
        email = email_entry.get()
        users = load_users()

        # Loop through the users and find the matching email
        for username, user_data in users.items():
            if isinstance(user_data, dict) and user_data.get('email') == email:
                send_reset_email(email)  # This sends the reset code via email
                show_reset_code_popup(email, username, email_popup)  # Pass username and email
                break
        else:
            email_label.configure(text="Email not found. Please try again.", text_color="red")


    
    send_code_button = ctk.CTkButton(email_popup, text="Send Reset Code", command=send_reset)
    send_code_button.pack(pady=(10, 20))
def show_reset_code_popup(email, username, email_popup):
    email_popup.destroy()  # Close the email input popup

    reset_popup = ctk.CTkToplevel()
    reset_popup.title("Enter Reset Code")
    reset_popup.geometry("400x250")

    reset_code_label = ctk.CTkLabel(reset_popup, text="Enter the reset code sent to your email:", text_color="black")
    reset_code_label.pack(pady=(20, 10))

    reset_code_entry = ctk.CTkEntry(reset_popup, width=300)
    reset_code_entry.pack(pady=(0, 20))

    def validate_reset_code():
        entered_code = reset_code_entry.get()
        # Compare the entered reset code with the actual reset code from reset_codes dictionary
        if reset_codes.get(email) == entered_code:
            show_reset_password_popup(email, username, reset_popup)  # Pass the username for updating the password
        else:
            reset_code_label.configure(text="Invalid reset code. Please try again.", text_color="red")
    
    submit_code_button = ctk.CTkButton(reset_popup, text="Submit Code", command=validate_reset_code)
    submit_code_button.pack(pady=(10, 20))


def show_reset_password_popup(email, username, reset_popup):
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
        
        # Update the password for the correct user
        if username in users and users[username]['email'] == email:
            users[username]['password'] = new_password
            save_users(users)
            new_password_label.configure(text="Password reset successfully.", text_color="green")
        
        password_popup.after(2000, password_popup.destroy)  # Close after 2 seconds
    
    reset_button = ctk.CTkButton(password_popup, text="Reset Password", command=update_password)
    reset_button.pack(pady=(10, 20))

# Window setup
window = ctk.CTk() # sets the first window as a custom tkinter set up
window.title("xCel Finance | Financial Application") # name of application
window.geometry("1920x1080") # window size
window.configure(fg_color="#F3E4F6") #colour of background

# Configure the grid
window.grid_columnconfigure(0, weight=2) # sets how many coloums and the weight of this
window.grid_columnconfigure(1, weight=1) # same as above
window.grid_rowconfigure(0, weight=1) # same for rows

# Image frame
image_frame = ctk.CTkFrame(window, fg_color="white", corner_radius=20)# frame for the left hand side of the log in screen, contains the  
image_frame.grid(row=0, column=0, padx=(20, 10), pady=20, sticky="nsew")

# Load and display image
image = ctk.CTkImage(Image.open("Version 2/diplogo.png"), size=(800, 342))
image_label = ctk.CTkLabel(image_frame, image=image, text="")
image_label.pack(fill="both", expand=True, padx=10, pady=10) # expands to the whole screen size


login_frame = ctk.CTkFrame(window, fg_color="#d096dc", corner_radius=20) # background of the log in screeen
login_frame.grid(row=0, column=1, padx=(10, 20), pady=20, sticky="nsew") # sticks to all corners, north south east west

login_frame.grid_rowconfigure(0, weight=1) # sets how many rows and the weight of this
login_frame.grid_rowconfigure(6, weight=1) # same as above
login_frame.grid_columnconfigure(0, weight=1)  # sets how many coloums and the weight of this

# Login content
login_content = ctk.CTkFrame(login_frame, fg_color="transparent")
login_content.grid(row=1, column=0, sticky="ns") # expands to north and south side

title_label = ctk.CTkLabel(login_content, text="Ready to accelerate your\npersonal finance story?", font=("Arial", 24, "bold"), text_color="white") # label to act as title for the lgoin page 
title_label.pack(pady=(0, 30))

username_label = ctk.CTkLabel(login_content, text="Username:", text_color="white") # Username title
username_label.pack(pady=(0, 5))
username_entry = ctk.CTkEntry(login_content, width=200) # entry box to get the users entry
username_entry.pack(pady=(0, 20))

password_label = ctk.CTkLabel(login_content, text="Password:", text_color="white") # label for password - telling user they need to enter it
password_label.pack(pady=(0, 5))
password_entry = ctk.CTkEntry(login_content, width=200, show="*") # entry box to get the entry
password_entry.pack(pady=(0, 20))

login_button = ctk.CTkButton(login_content, text="Log In", text_color="#208ad6", hover_color="#CFCFCF", fg_color="white", command=login) # log in button activates the login funciton - hover colour is included in this line of code
login_button.pack(pady=(0, 20))

create_account_button = ctk.CTkButton(login_content, text="Create Account", command=show_create_account) # if the user does not have an account, they can create it by clicking this buttom, then sends it to the create account funciton 
create_account_button.pack()

forgot_password_button = ctk.CTkButton(login_content, text="Forgot Password?", command=show_email_popup)
forgot_password_button.pack(pady=(0, 10))

error_label = ctk.CTkLabel(login_content, text="", text_color="red") # this is what is configured if there is some sort of error
error_label.pack(pady=(10, 0))

# Create account content
create_account_content = ctk.CTkFrame(login_frame, fg_color="transparent")

create_account_title = ctk.CTkLabel(create_account_content, text="Create a new account", font=("Arial", 24, "bold"), text_color="white") # create account title
create_account_title.pack(pady=(0, 30))

new_username_label = ctk.CTkLabel(create_account_content, text="New Username:", text_color="white") # username title
new_username_label.pack(pady=(0, 5))
new_username_entry = ctk.CTkEntry(create_account_content, width=200) # username entry box
new_username_entry.pack(pady=(0, 20))

new_password_label = ctk.CTkLabel(create_account_content, text="New Password:", text_color="white") # Pasword title
new_password_label.pack(pady=(0, 5))
new_password_entry = ctk.CTkEntry(create_account_content, width=200, show="*") # password entry box
new_password_entry.pack(pady=(0, 20))

new_email_label = ctk.CTkLabel(create_account_content, text="New Email:", text_color="white")  # Email title
new_email_label.pack(pady=(0, 5))
new_email_entry = ctk.CTkEntry(create_account_content, width=200)  # Email entry box
new_email_entry.pack(pady=(0, 20))

create_button = ctk.CTkButton(create_account_content, text="Create Account", command=create_account) #button that runs the create account function
create_button.pack(pady=(0, 20))

back_to_login_button = ctk.CTkButton(create_account_content, text="Back to Login", command=lambda: (create_account_content.grid_forget(), login_content.grid(row=1, column=0, sticky="ns")))  # This line creates a back to login button within the 'create_account_content' container. it starts a function that hides the current content by grid forget
back_to_login_button.pack()  #makes the button visible within its parent container


create_account_error_label = ctk.CTkLabel(create_account_content, text="", text_color="red") # label that can be configured later 
create_account_error_label.pack(pady=(10, 0))

def restart_app(): # function to restart application 
    python = sys.executable
    os.execl(python, python, *sys.argv)

def logout():
    window.destroy() # close the current window
    restart_app() # runs the above restart app function

def create_top_bar(parent):  # setting up top bar 
    top_bar = ctk.CTkFrame(parent, height=60, fg_color="#d096dc")  # frame as top bar 
    top_bar.pack(fill="x", pady=(0, 10))  # This ensures the top bar stretches across the width of the window 
    top_bar.pack_propagate(False)  # Keeps the top bar at the intended height

    logo = ctk.CTkImage(Image.open("Version 2/diplogo.png"), size=(140, 60))  # Loading the logo image to be displayed on the top bar
    logo_label = ctk.CTkLabel(top_bar, image=logo, text="")  # Assigning the logo to a label
    logo_label.pack(side="left", padx=10)  

    logout_button = ctk.CTkButton(top_bar, text="Log Out", command=logout, fg_color="red", text_color="white", width=100)  # log out button runs log out function
    logout_button.pack(side="right", padx=10, pady=10)  

def create_navigation_bar(parent, active_frame):
    nav_bar = ctk.CTkFrame(parent, fg_color="#CFCFCF") # nav bar frame
    nav_bar.pack(side="bottom", fill="x") #fills across width/x-axis of the window

    button_color = "#F3E4F6"  # colour of button that is not selectted
    active_color = "#d096dc"  # colour of button that is selectted

    # button clolours and size 
    button_height = 40
    button_text_color = "black"
    button_hover_color = "#d9b1e0"

    # creates Spend Tracker button
    spend_button = ctk.CTkButton(master=nav_bar,text="Spend Tracker",text_color=button_text_color,command=show_spend_tracker,height=button_height,hover_color=button_hover_color)
    spend_button.pack(side="left", expand=True, fill="x")

    # Set the color of the button based on what frame it is on
    if active_frame == "spend_tracker":
        spend_button.configure(fg_color=active_color)
    else:
        spend_button.configure(fg_color=button_color)    

    # Create Finance School button
    school_button = ctk.CTkButton(master=nav_bar,text="Finance School",text_color=button_text_color,command=show_school_frame,height=button_height,hover_color=button_hover_color)
    school_button.pack(side="left", expand=True, fill="x")

    # Set the color of the button based on what frame it is on
    if active_frame == "finance_school":
        school_button.configure(fg_color=active_color)
    else:
        school_button.configure(fg_color=button_color)

    # Create xCel AI Assistant button
    ai_button = ctk.CTkButton(master=nav_bar,text="xCel AI Assistant",text_color=button_text_color,command=show_ai_chat, height=button_height, hover_color=button_hover_color)
    ai_button.pack(side="left", expand=True, fill="x")

     # Set the color of the button based on what frame it is on
    if active_frame == "ai_chat":
        ai_button.configure(fg_color=active_color)
    else:
        ai_button.configure(fg_color=button_color)
    

def show_spend_tracker():
    for widget in window.winfo_children():
        widget.destroy()  # clear all widgets from main window

    container = ctk.CTkFrame(window)  # make a new container frame
    container.pack(fill="both", expand=True)

    create_top_bar(container)  # add the top bar

    content_frame = ctk.CTkFrame(container)  # frame for main content
    content_frame.pack(fill="both", expand=True, padx=10, pady=10)

    spend_tracker = SpendTracker()  # create SpendTracker instance
    spend_tracker.add_item(content_frame)  # add spend tracker interface

    create_navigation_bar(container, "spend_tracker")  # add nav bar, highlight spend tracker button

def show_school_frame():
    for widget in window.winfo_children():
        widget.destroy()  # Clear all existing widgets from the main window

    container = ctk.CTkFrame(window)  # Create a new container frame
    container.pack(fill="both", expand=True)  # Make the container fill the entire window

    create_top_bar(container)  # Add the top bar to the container

    content_frame = ctk.CTkFrame(container)  # Create a frame for the main content
    content_frame.pack(fill="both", expand=True, padx=10, pady=10)  # Pack the content frame with padding

    school_frame(content_frame)  # Add the school frame content to the content frame

    create_navigation_bar(container, "finance_school")  # Add the navigation bar, highlighting the finance school button

def show_ai_chat():
    for widget in window.winfo_children():
        widget.destroy()  # clear all widgets from main window

    container = ctk.CTkFrame(window)  # new container frame
    container.pack(fill="both", expand=True)

    create_top_bar(container)  # add top bar

    content_frame = ctk.CTkFrame(container)  # frame for main content
    content_frame.pack(fill="both", expand=True, padx=10, pady=10)

    ai_chat(content_frame)  # add AI chat interface

    create_navigation_bar(container, "ai_chat")  # add nav bar, highlight AI chat button

class SpendTracker:
    def __init__(self):
        # List of spending categories
        self.cat_list = [
            "Food", "Technology", "Entertainment", "Groceries", "Medical",
            "Petrol", "Travel", "Clothing", "Utilities", "Education", 
            "Fitness", "Subscriptions", "Gifts", "Personal Care", 
            "Other (wants)", "Other (needs)"
        ]
        self.items = []  # list to store spending items

    def add_item(self, parent_frame):
        frame1 = ctk.CTkFrame(parent_frame, fg_color="white")  # main frame for spend tracker
        frame1.pack(fill="both", expand=True, padx=10, pady=10)

        # Configure grid layout
        frame1.grid_columnconfigure((0, 1, 2), weight=1)
        frame1.grid_rowconfigure((0,1), weight=1)

        # Left column - Item input fields
        left_frame = ctk.CTkFrame(frame1, fg_color="white")
        left_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        ctk.CTkLabel(left_frame, text="Item Name:").pack(anchor="w", padx=5, pady=5)
        self.p_name = ctk.CTkEntry(left_frame, width=150)  # entry for item name
        self.p_name.pack(anchor="w", padx=5, pady=5)

        ctk.CTkLabel(left_frame, text="Category:").pack(anchor="w", padx=5, pady=5)
        self.p_cat = ctk.CTkComboBox(left_frame, values=self.cat_list, width=150)  # dropdown for category
        self.p_cat.pack(anchor="w", padx=5, pady=5)

        ctk.CTkLabel(left_frame, text="Price:").pack(anchor="w", padx=5, pady=5)
        self.p_price = tk.Spinbox(left_frame, from_=0, to=100000, increment=1.0, width=18)  # Standard Tkinter Spinbox for price
        self.p_price.pack(anchor="w", padx=5, pady=5)


        # Middle column - Calendar for date selection
        middle_frame = ctk.CTkFrame(frame1, fg_color="white")
        middle_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        ctk.CTkLabel(middle_frame, text="Select Date:").pack(anchor="n", padx=5, pady=5)
        self.p_date = Calendar(middle_frame, selectmode="day", year=2024, foreground="black", selectforeground="blue")  # calendar widget
        self.p_date.pack(padx=5, pady=5)

        self.p_submit = ctk.CTkButton(middle_frame, text="Submit", command=self.submit_item)  # submit button
        self.p_submit.pack(padx=5, pady=5)

        # Right column - Spending History display
        right_frame = ctk.CTkFrame(frame1, fg_color="white")
        right_frame.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)

        ctk.CTkLabel(right_frame, text="Spending History:").pack(anchor="w", padx=5, pady=5)
        self.display_area = ctk.CTkTextbox(right_frame, height=250, width=300)  # textbox for spending history
        self.display_area.pack(fill="both", padx=5, pady=5)

        self.display_text()  # show initial spending history

        # Bottom frame - Spending Chart
        bottom_frame = ctk.CTkFrame(frame1, fg_color="white")
        bottom_frame.grid(row=1, columnspan=3, sticky="nsew", padx=5, pady=5)

        ctk.CTkLabel(bottom_frame, text="Spending History (Last 12 Months):").pack(anchor="w", padx=5, pady=5)

        # Create and display the spending chart
        self.create_spending_chart(bottom_frame)

    def submit_item(self):
        # collect item details from input fields
        name = self.p_name.get()
        category = self.p_cat.get()
        price = float(self.p_price.get())  
        date = self.p_date.get_date()
        new_item = [name, category, price, date]
        self.items.append(new_item)
        self.save_items(new_item)  # save new item to file
        self.display_text()  # update displayed spending history

    def save_items(self, item):

        date_obj = datetime.strptime(item[3], "%m/%d/%y")  
        formatted_date = date_obj.strftime("%m/%d/%Y")  
        with open("Version 2/spending.txt", "a") as file:
            file.write(f"{item[0]},{item[1]},{item[2]},{formatted_date}\n")

    def display_text(self):
        # show spending history in textbox
        self.display_area.delete('1.0', "end")  # clear existing text
        with open("Version 2/spending.txt", "r") as file:
            content = file.read()
            self.display_area.insert("end", content)  # put file contents in textbox

    def create_spending_chart(self, parent_frame):
        spending_data = self.read_spending_data()  # get spending data from file

        fig, ax = plt.subplots(figsize=(10, 3))  # make figure and axis for chart

        if spending_data:
            # set up dict for monthly spending
            monthly_spending = {month: 0 for month in range(1, 13)}

            # add up spending for each month
            for date, amount in spending_data:
                monthly_spending[date.month] += amount

            # get data  for plotting
            months = list(calendar.month_abbr)[1:]  # month abbreviations
            spending_values = [monthly_spending[month] for month in range(1, 13)]

            # make the bar plot
            bars = ax.bar(months, spending_values)

            # format axis
            ax.set_xlabel("Month")
            ax.set_ylabel("Amount Spent ($)")
            ax.set_title("Monthly Spending")

            # add labels on top of each bar
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height, f"${height:.2f}", ha="center", va="bottom")

            # rotate x-axis labels so they're easier to read
            plt.xticks(rotation=45)

        else:
            # show message if no spending data
            ax.text(0.5, 0.5, "No spending data",  horizontalalignment="center", verticalalignment="center")

        plt.tight_layout()

        # make a canvas to show the chart in the tkinter window
        canvas = FigureCanvasTkAgg(fig, master=parent_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill="both", expand=True)

    def read_spending_data(self):
        spending_data = []  # list to store our spending data
        today = datetime.now()  # get current date
        start_of_year = datetime(today.year, 1, 1)  # set start date to the beginning of this year

        try:
            # open and read spending file
            with open("Version 2/spending.txt", "r") as file:
                for line in file:
                    try:
                        # split each line into 4 parts
                        parts = line.strip().split(',')

                        # getting the parts of the data
                        name, category, price, date_str = parts[:4]

                        price = float(price.strip())

                        # convert date string to actual date object
                        date = datetime.strptime(date_str.strip(), "%m/%d/%Y")  # Read date in 'dmy' format

                        # Filter data to include all months of the current year
                        if date.year == today.year:
                            spending_data.append((date, price))

                    except ValueError as e:
                        print("Error")  # Debugging line for errors
                    except Exception as e:
                        print("Error")  # Debugging line for errors
                    
        except FileNotFoundError:
            print("error")
        except Exception as e:
            print("Error") 
        # sort our data by date, oldest first
        spending_data.sort(key=lambda x: x[0])
        return spending_data

def ai_chat(parent_frame):
    frame = ctk.CTkFrame(parent_frame)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    os.environ["GENERATIVE_AI_KEY"] = "REDACTED --- PLEASE SEE README.TXT"  
    genai.configure(api_key=os.getenv("GENERATIVE_AI_KEY"))

    # Configure the AI model
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.0-pro",
        generation_config=generation_config,
    )

    chat_session = model.start_chat(history=[])  # start new chat session with AI

    ctk.CTkLabel(frame, text="Enter your question:").pack(anchor="w", pady=(0, 5))
    question_entry = ctk.CTkEntry(frame, width=500)  # entry field for questions
    question_entry.pack(fill="x", pady=(0, 10), padx=(0, 10))

    def send_question():
        question = question_entry.get()  # get user's question
        if question:
            response = chat_session.send_message(question)  # send question to AI and get response
            response_text.insert("end", f"Q: {question}\n\nA: {response.text}\n\n")  # show Q&A in text area
            question_entry.delete(0, "end")  # clear question entry field

    submit_button = ctk.CTkButton(frame, text="Submit", command=send_question)  # submit button
    submit_button.pack(pady=(0, 10))

    ctk.CTkLabel(frame, text="Chat History:").pack(anchor="w", pady=(0, 5))
    response_text = ctk.CTkTextbox(frame, height=400, width=700)  # text area for chat history
    response_text.pack(fill="both", expand=True, pady=(0, 10))

def school_frame(parent_frame):
    main_frame = ctk.CTkFrame(parent_frame)
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)

    button_frame = ctk.CTkFrame(main_frame)  # frame for topic buttons
    button_frame.pack(fill="x", padx=10, pady=(10, 5))

    content_frame = ctk.CTkFrame(main_frame)  # frame for content display
    content_frame.pack(fill="both", expand=True, padx=10, pady=(5, 10))

    content_text = ctk.CTkTextbox(content_frame, wrap="word", width=600, height=400)  # text area for displaying content
    content_text.pack(fill="both", expand=True, padx=10, pady=10)

    def show_content(topic):
        content_text.delete("1.0", "end")  # clear previous content
        file_path = "Version 2/scl1.txt"
        try:
            with open(file_path, "r") as file:
                all_content = file.read().split('\n\n\n\n')  # split content into sections
                topic_dict = {"Learn about budgeting": 0, "When to save/spend": 1, "What is investing?": 2, "How to track spending?": 3, "Summary": 4}
                if topic in topic_dict:
                    content_text.insert("end", all_content[topic_dict[topic]])  # show content for selected topic
                else:
                    content_text.insert("end", "Topic not found")
        except FileNotFoundError:
            content_text.insert("end", "File not found")

    button_width = 180
    topics = ["Learn about budgeting", "When to save/spend", "What is investing?", "How to track spending?", "Summary"]

    # make buttons for each topic
    for topic in topics:
        ctk.CTkButton(button_frame, text=topic, command=lambda t=topic: show_content(t), width=button_width).pack(side="left", padx=5)

    show_content("Learn about budgeting")  # show initial content

# Start the application
if __name__ == "__main__":
    window.mainloop()
