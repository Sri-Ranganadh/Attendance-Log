import tkinter as tk
from tkinter import messagebox
import sys

def close_window():
    root.destroy()

# Get the message from the command-line arguments
message = " ".join(sys.argv[1:])

# Create the main window
root = tk.Tk()
root.title("Message Box")
root.geometry("400x150")

# Create a frame to hold the message label
frame = tk.Frame(root)
frame.pack(expand=True)

# Display the message
message_label = tk.Label(frame, text=message)
message_label.pack(pady=(50, 20))

# Create a button frame
button_frame = tk.Frame(root)
button_frame.pack(expand=True, anchor="se", padx=20, pady=20)

# Create a button to close the window
close_button = tk.Button(button_frame, text="OK", command=close_window, bg="blue", fg="white", width=10, height=2)
close_button.pack(side="right")

# Run the Tkinter event loop
root.mainloop()
