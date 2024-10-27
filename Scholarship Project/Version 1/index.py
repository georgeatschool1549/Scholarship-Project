'''
Financial Assistant Application | Version 1
George R
'''
from tkinter import * 
from tkinter import ttk 
from tkcalendar import Calendar # Calendar widget for date selection
import os # For operating system interactions
import tkinter as tk 
from tkinter import PhotoImage # For image display
from PIL import Image, ImageTk 
import google.generativeai as genai # For integrating Generative AI

'''
All of the above imports neccassary modules to use external functions. 
'''

# calling the main window
root = Tk()
root.geometry("800x500") # Set the window size
root.title("xCel Finance | Financial Assistant") # Set the window title
bg_color = "#F3E4F6" # Background colour

def home():
    for widget in root.winfo_children(): # Clear all existing widgets - this is so when the user goes back and fourth to the home screen, it appears appropriatly
        widget.destroy() # Destroy each widget

    spend_tracker = SpendTracker() # Initialize SpendTracker instance

    # Frame for the logo
    frame1a = tk.Frame(root, width=200, height=100, bg=bg_color)
    frame1a.grid(row=0, column=0, columnspan=3, sticky="NSEW")
    frame1a.grid_propagate(False)

    # Load and display logo
    logo = Image.open("Version 1/diplogo.png") # Load the logo image
    logoresized = logo.resize((400,171))  # Resize the image
    logotest = ImageTk.PhotoImage(logoresized) # converting image to PhotoImage

    logo_label = tk.Label(frame1a, image=logotest, bg=bg_color)
    logo_label.pack(expand=True, fill=BOTH) # Display logo

    logo_label.image = logotest # Keep a reference for the logo image

    # Frame for the first button - will go to the spending tracker
    frame2a = tk.Frame(root, width=100, height=100, bg=bg_color)
    frame2a.grid(row=1, column=0, sticky="NSEW")
    frame2a.grid_propagate(False)

    # Load and display button image
    image = Image.open("Version 1/spend.jpeg") 
    imagetest = ImageTk.PhotoImage(image) 

    button_qwer = tk.Button(frame2a, text="", image=imagetest, command=spend_tracker.add_item) # command sets the button to take the user to the corresponding frames/classes/functions
    button_qwer.pack(expand=True, fill=BOTH) #

    button_qwer.image = imagetest 

    # Frame for the second button - will go to the finance school
    frame3a = tk.Frame(root, width=100, height=100, bg=bg_color)
    frame3a.grid(row=1, column=1, sticky="NSEW")
    frame3a.grid_propagate(False) #sets the grid geometry for propagation. assists in making the window resizable without effecting usability 

    
    image2 = Image.open("Version 1/school.jpg") 
    imagetest2 = ImageTk.PhotoImage(image2)

    button_qwer2 = tk.Button(frame3a, text="", image=imagetest2, command=school_frame)
    button_qwer2.pack(expand=True, fill=BOTH) 

    button_qwer2.image = imagetest2 

    # Frame for the third button
    frame4a = tk.Frame(root, width=100, height=100, bg=bg_color)
    frame4a.grid(row=1, column=2, sticky="NSEW")
    frame4a.grid_propagate(False)

    
    image3 = Image.open("Version 1/a.jpeg") 
    imagetest3 = ImageTk.PhotoImage(image3) 

    button_qwer3 = tk.Button(frame4a, text="", image=imagetest3, command=ai_chat)
    button_qwer3.pack(expand=True, fill=BOTH) 

    button_qwer3.image = imagetest3 

    
    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.grid_columnconfigure(2, weight=1)

class SpendTracker:
    def __init__(self):
        self.cat_list = [ # List of categories for tracking expenses
            "Food", "Technology", "Entertainment", "Groceries", "Medical",
            "Petrol", "Travel", "Clothing", "Utilities", "Education", 
            "Fitness", "Subscriptions", "Gifts", "Personal Care", 
            "Other (wants)", "Other (needs)"
        ]
        self.items = [] # List to store items entered by the user

    def add_item(self):
        for widget in root.winfo_children():  # Clear the home screen widgets
            widget.destroy()

        # Modernize the background color and font styles
        modern_bg_color = "#D6CDE2"  # Lighter variation of the pink/blue palette for a clean, modern look
        modern_font = ("Helvetica", 12, "bold")  # More modern font for labels and entries

        frame1 = ttk.Frame(root, padding=10, style="Modern.TFrame")  # Apply modern style to the frame
        frame1.grid(row=0, column=0, columnspan=4, sticky="NSEW")
            
        # Modernize the labels and entries
        ttk.Label(frame1, text="Item Name:", font=modern_font).grid(row=0, column=0, padx=5, pady=5, sticky=E)
        self.p_name = ttk.Entry(frame1, width=15)
        self.p_name.grid(row=0, column=1, padx=5, pady=5)
            
        # Dropdown for category
        ttk.Label(frame1, text="Category:", font=modern_font).grid(row=0, column=2, padx=5, pady=5, sticky=E)
        self.p_cat = ttk.Combobox(frame1, values=self.cat_list, width=15)
        self.p_cat.grid(row=0, column=3, padx=5, pady=5)
            
        # Spinbox for price
        ttk.Label(frame1, text="Price:", font=modern_font).grid(row=1, column=0, padx=5, pady=5, sticky=E)
        self.p_price = ttk.Spinbox(frame1, from_=0.00, to=100000, increment=1.00, width=10)
        self.p_price.grid(row=1, column=1, padx=5, pady=5)
            
        # Submit button with updated background color
        self.p_submit = ttk.Button(frame1, text="Submit", command=self.submit_item)
        self.p_submit.grid(row=1, column=3, padx=5, pady=5)
            
        # Update the Calendar styling
        ttk.Label(root, text="Select Date:", font=modern_font, background=modern_bg_color).grid(row=1, column=0, sticky=W)
        self.p_date = Calendar(root, selectmode="day", year=2024, foreground="black", selectforeground="blue")
        self.p_date.grid(row=2, column=0)
            
        # Text area for spending history with modernized background color and font
        ttk.Label(root, text="Spending History:", font=modern_font, background=modern_bg_color).grid(row=3, column=0, pady=5, sticky='nesw')
        self.display_area = Text(root, height=10, width=50, bg=modern_bg_color, font=("Helvetica", 10))
        self.display_area.grid(row=4, column=0, pady=5)
            
        self.display_text()  # Load and display spending history

        # Back button with modern styling
        back_button = ttk.Button(root, text="Back to Home", command=home)
        back_button.grid(row=5, column=0, pady=10)


    def submit_item(self):
        name = self.p_name.get() # Get item name
        category = self.p_cat.get() # Get selected category
        price = self.p_price.get() # Get price
        date = self.p_date.get_date() # Get selected date
        new_item = [name, category, price, date] # Create a new item list
        self.items.append(new_item) # Add to items list
        self.save_items(new_item) # Save the new item
        self.display_text() # Refresh displayed text

    def save_items(self, item):  
        with open("Version 1/spending.txt", "a") as file:  # Append new item to text file
            file.write(f"{item[0]},{item[1]},${item[2]},{item[3]}\n") # writes the appropriate information to the file - not the unessacary details
    
    def display_text(self):
        self.display_area.delete('1.0', END) # Clear the text area
        with open("Version 1/spending.txt", "r") as file:
            content = file.read() # Read content from file
            self.display_area.insert(END, content) # Display content


def ai_chat():
    # Clear the root window
    for widget in root.winfo_children():
        widget.destroy()


    os.environ["GENERATIVE_AI_KEY"] = "REDACTED ---- PLEASE SEE README.TXT" # API key
    genai.configure(api_key=os.environ["GENERATIVE_AI_KEY"]) # Set API configuration

    # Create the model
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash", # chose the specific model of choice from the Gemini
        generation_config=generation_config,
    )

    chat_session = model.start_chat(history=[])

    # Frame for chat interface
    frame = ttk.Frame(root, padding=10)
    frame.grid(row=0, column=0, sticky=(N, W, E, S))
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # Entry for user question
    ttk.Label(frame, text="Enter your question:").grid(row=0, column=0, pady=(0, 5), sticky=W)
    question_entry = ttk.Entry(frame, width=50)
    question_entry.grid(row=1, column=0, pady=(0, 10), padx=(0, 10), sticky=(W, E))

    def send_question():
        question = question_entry.get() # Get user question
        if question:
            response = chat_session.send_message(question) # Send question and get response
            response_text.insert(END, f"Q: {question}\n\nA: {response.text}\n\n") # show response
            question_entry.delete(0, END) # Clear entry box

    # Submit button for sending questions
    submit_button = ttk.Button(frame, text="Submit", command=send_question)
    submit_button.grid(row=1, column=1, pady=(0, 10))

    # Text area for history
    ttk.Label(frame, text="Chat History:").grid(row=2, column=0, pady=(0, 5), sticky=W)
    response_text = Text(frame, height=20, width=70, bg=bg_color)  
    response_text.grid(row=3, column=0, columnspan=2, pady=(0, 10), sticky=(N, W, E, S))

    # Back button to return to home screen
    back_button = ttk.Button(frame, text="Back to Home", command=home)
    back_button.grid(row=4, column=0, columnspan=2, pady=10)

    frame.grid_rowconfigure(3, weight=1)
    frame.grid_columnconfigure(0, weight=1)

def school_frame():
    for widget in root.winfo_children(): # Clear the home screen widgets
        widget.destroy()

    # Main frame for school content
    main_frame = ttk.Frame(root, padding=10)
    main_frame.grid(row=0, column=0, sticky=(N, W, E, S))
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # Sidebar for navigation
    sidebar_frame = ttk.Frame(main_frame, width=200, padding=10)
    sidebar_frame.grid(row=0, column=0, sticky=(N, S))
    sidebar_frame.grid_propagate(False)

    # Content frame for displaying selected topic
    content_frame = ttk.Frame(main_frame, padding=10)
    content_frame.grid(row=0, column=1, sticky=(N, W, E, S))
    main_frame.grid_columnconfigure(1, weight=1)

    content_text = Text(content_frame, wrap=WORD, width=60, height=20)
    content_text.grid(row=0, column=0, sticky=(N, W, E, S))
    content_frame.grid_rowconfigure(0, weight=1)
    content_frame.grid_columnconfigure(0, weight=1)

    def show_content(topic):
        content_text.delete(1.0, END) # Clear existing content
        file_path = ""
        # file path based on topic
        if topic == "Learn about budgeting":
            file_path = "Version 1/scl1.txt"
        elif topic == "When to save/spend":
            file_path = "Version 1/scl2.txt"
        elif topic == "What is investing?":
            file_path = "Version 1/scl3.txt"
        elif topic == "How to track spending?":
            file_path = "Version 1/scl4.txt"
        elif topic == "Summary":
            file_path = "Version 1/scl5.txt"
        
        if file_path:
            try:
                with open(file_path, "r") as file:
                    content = file.read() # Read content from file
                    content_text.insert(END, content) # Display content
            except FileNotFoundError:
                content_text.insert(END, "error") # error message if file not found
        else:
            content_text.insert(END, "error") # error message if no content

    button_width = 16 # Width of all buttons
    
    # sidebar buttons
    ttk.Button(sidebar_frame, text="Learn about budgeting", command=lambda: show_content("Learn about budgeting"), width=button_width).grid(row=0, column=0, pady=5, sticky=W)
    ttk.Button(sidebar_frame, text="When to save/spend", command=lambda: show_content("When to save/spend"), width=button_width).grid(row=1, column=0, pady=5, sticky=W)
    ttk.Button(sidebar_frame, text="What is investing?", command=lambda: show_content("What is investing?"), width=button_width).grid(row=2, column=0, pady=5, sticky=W)
    ttk.Button(sidebar_frame, text="How to track spending?", command=lambda: show_content("How to track spending?"), width=button_width).grid(row=3, column=0, pady=5, sticky=W)
    ttk.Button(sidebar_frame, text="Summary", command=lambda: show_content("Summary"), width=button_width).grid(row=4, column=0, pady=5, sticky=W)

    # Back button to return to home screen
    ttk.Button(sidebar_frame, text="Back to Home", command=home, width=button_width).grid(row=10, column=0, pady=20, sticky=W)

    show_content("Learn all about budgeting") # Display default content

def main():
    home() # show home screen
    root.mainloop() # start the tkinter event loop

if __name__ == "__main__":
    main() # Run the main function
