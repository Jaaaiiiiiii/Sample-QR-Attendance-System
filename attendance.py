import gspread
from google.oauth2.service_account import Credentials
import mysql.connector
import serial
import datetime
import time
import tkinter as tk
from tkinter import scrolledtext

# ---------------- GOOGLE SHEETS SETUP ---------------- #
SERVICE_ACCOUNT_FILE = "your-credentials.json"  # Update with your JSON key file
SCOPES = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(creds)

SPREADSHEET_ID = "1ElteDMHWtGq3SqP9aib35e2knWZc8yY_3a_4RZwc_2Q"  # Replace with your Google Sheet ID
sheet = client.open_by_key(SPREADSHEET_ID).sheet1  # Selects first sheet

# ---------------- DATABASE SETUP ---------------- #
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",  # Change this
    database="attendance_system"
)
cursor = conn.cursor()

# ---------------- ARDUINO CONNECTION ---------------- #
arduino = serial.Serial("COM3", 9600)  # Change to your Arduino port

# ---------------- GUI SETUP ---------------- #
root = tk.Tk()
root.title("QR Attendance System")

tk.Label(root, text="Scan QR Code:").pack(pady=5)

entry = tk.Entry(root, width=40, font=("Arial", 14))
entry.pack(pady=5)
entry.focus()

log_box = scrolledtext.ScrolledText(root, width=60, height=15, state="normal")
log_box.pack(pady=10)

def log_message(msg):
    log_box.insert(tk.END, f"{datetime.datetime.now().strftime('%H:%M:%S')} - {msg}\n")
    log_box.yview(tk.END)

# ---------------- ATTENDANCE FUNCTION ---------------- #
def mark_attendance(barcode_data):
    today = datetime.date.today()
    current_time = datetime.datetime.now().time()
    status = "On Time" if current_time <= datetime.time(13, 0) else "Late"

    cursor.execute("SELECT name FROM students WHERE barcode = %s", (barcode_data,))
    result = cursor.fetchone()

    if result:
        name = result[0]
        cursor.execute("SELECT * FROM attendance WHERE barcode = %s AND date = %s", (barcode_data, today))
        if cursor.fetchone() is None:
            cursor.execute(
                "INSERT INTO attendance (barcode, name, date, time, status) VALUES (%s, %s, %s, %s, %s)",
                (barcode_data, name, today, datetime.datetime.now().strftime("%H:%M:%S"), status)
            )
            conn.commit()

            # Send to Arduino
            arduino.write(f"{name},{status}\n".encode())

            # Log attendance
            log_message(f"Marked: {name} ({status})")

            # Save to Google Sheets
            sheet.append_row([str(today), str(datetime.datetime.now().strftime("%H:%M:%S")), name, status])

        else:
            log_message(f"Already Used: {name}")
            arduino.write("Already Used,Today\n".encode())

    else:
        log_message("QR Code Not Found")
        arduino.write("Not Found,Error\n".encode())

# ---------------- SCANNING FUNCTION ---------------- #
def process_scan(event=None):
    barcode_data = entry.get().strip()
    if barcode_data:
        mark_attendance(barcode_data)
        entry.delete(0, tk.END)
        time.sleep(3)  # Prevent multiple scans in a row

entry.bind("<Return>", process_scan)  # Auto-process when scanner sends data

tk.Button(root, text="Exit", command=root.quit).pack(pady=5)
log_message("System Ready. Please scan QR codes.")

root.mainloop()
