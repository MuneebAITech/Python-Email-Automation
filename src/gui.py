import customtkinter as ctk
from tkinter import filedialog
from bulk_email_sender import send_bulk_emails
import threading

selected_excel = None



ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


app = ctk.CTk()

app.title(
    "Email Automation Tool"
)

app.geometry(
    "600x400"
)


title = ctk.CTkLabel(
    app,
    text="Bulk Email Automation",
    font=("Arial", 24)
)

title.pack(
    pady=20
)

def select_excel():

    global selected_excel

    file_path = filedialog.askopenfilename(

        title="Select Excel File",

        filetypes=[
            ("Excel Files", "*.xlsx")
        ]
    )

    if file_path:

        selected_excel = file_path

        status_label.configure(
            text=file_path
        )


status_label = ctk.CTkLabel(
    app,
    text="Ready..."
)

status_label.pack(
    pady=10
)

def update_progress(value):

    progress_bar.set(value)

    app.update_idletasks()


browse_button = ctk.CTkButton(

    app,

    text="Browse Excel",

    command=select_excel

)

browse_button.pack(
    pady=20
)

print("BUTTON CLICKED")

def start_sending():

    send_button.configure(
        state="disabled"
    )

    send_bulk_emails(
        selected_excel,
        update_progress
    )

    send_button.configure(
        state="normal"
    )

    status_label.configure(
        text="Completed"
    )
    
    progress_bar.set(1)


def send_emails():

    if selected_excel:
        progress_bar.set(0)

        status_label.configure(
            text="Sending Emails..."
        )

        thread = threading.Thread(
            target=start_sending
        )

        thread.start()

    else:

        status_label.configure(
            text="Please Select Excel File"
        )

send_button = ctk.CTkButton(

    app,

    text="Send Emails",

    command=send_emails
)

send_button.pack(
    pady=10
)

progress_bar = ctk.CTkProgressBar(
    app,
    width=400
)

progress_bar.pack(
    pady=20
)

progress_bar.set(0)

app.mainloop()