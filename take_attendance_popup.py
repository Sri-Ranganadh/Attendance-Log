import tkinter as tk
from tkinter import messagebox
import sys

def close_window():
    # Return 0 when window is closed
    root.quit()

def ok_clicked():
    # Return 1 when OK button is clicked
    root.quit()

def no_clicked():
    # Return 0 when No button is clicked
    root.quit()

# Get the message from the command-line arguments
message = " ".join(sys.argv[1:])

# Create the main window
root = tk.Tk()
root.title("Message Box")
root.geometry("400x200")

# Create a frame to hold the message label
frame = tk.Frame(root)
frame.pack(expand=True)

# Display the message
message_label = tk.Label(frame, text=message)
message_label.pack(pady=(50, 20))

# Create a button frame
button_frame = tk.Frame(root)
button_frame.pack(expand=True, anchor="se", padx=20, pady=20)

# Create buttons to close the window
ok_button = tk.Button(button_frame, text="OK", command=ok_clicked, bg="blue", fg="white", width=10, height=2)
ok_button.pack(side="right", padx=(0, 10))

no_button = tk.Button(button_frame, text="No", command=no_clicked, bg="red", fg="white", width=10, height=2)
no_button.pack(side="right")

# Run the Tkinter event loop
root.mainloop()

# Return 1 if OK button is clicked, otherwise return 0
if root._windowingsystem == 'x11':
    sys.exit(1)  # Exit with status code 1 when OK button is clicked
else:
    sys.exit(0)  # Exit with status code 0 when No button is clicked or window is closed
