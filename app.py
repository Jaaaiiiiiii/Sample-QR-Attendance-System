Import os
import time
import datetime
import mysql.connector
import serial
import keyboard
import gspread
import qrcode
from google.oauth2.service_account import Credentials
from config import *

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
QR_FOLDER = "qrcodes"




def init_mysql():
    return mysql.connector.connect(**MYSQL_CONFIG)


def init_google_sheets():
    creds = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=SCOPES
    )
    client = gspread.authorize(creds)
    return client.open_by_key(SPREADSHEET_ID).sheet1


def init_arduino():
    board = serial.Serial(ARDUINO_PORT, BAUD_RATE)
    time.sleep(2)
    return board




def generate_qr_codes(cursor):
    os.makedirs(QR_FOLDER, exist_ok=True)
    cursor.execute("SELECT name, barcode FROM students")

    for name, barcode in cursor.fetchall():
        qr = qrcode.make(barcode)
        qr.save(f"{QR_FOLDER}/{name}.png")

    print("QR codes generated successfully.")



def mark_attendance(barcode, cursor, connection, sheet, arduino):

    today = datetime.date.today()
    now = datetime.datetime.now()
    time_now = now.strftime("%H:%M:%S")
    status = "On Time" if now.hour < 13 else "Late"


    cursor.execute(
        "SELECT name FROM students WHERE barcode=%s",
        (barcode,)
    )
    result = cursor.fetchone()

    if not result:
        arduino.write(b"Not Found,Error\n")
        print("QR Not Found")
        return

    name = result[0]


    cursor.execute(
        "SELECT 1 FROM attendance WHERE barcode=%s AND date=%s",
        (barcode, today)
    )

    if cursor.fetchone():
        arduino.write(b"Already Used,Today\n")
        print("Duplicate attendance blocked.")
        return


    cursor.execute(
        "INSERT INTO attendance (barcode, name, date, time, status) "
        "VALUES (%s,%s,%s,%s,%s)",
        (barcode, name, today, time_now, status)
    )
    connection.commit()

 
    sheet.append_row([
        barcode,
        name,
        str(today),
        time_now,
        status
    ])

    arduino.write(f"{name},{status}\n".encode())

    print(f"Attendance recorded: {name} - {status}")




def start_scanner(cursor, connection, sheet, arduino):

    print("System Ready. Scan QR Code...\n")

    while True:
        event = keyboard.read_event()

        if event.event_type == keyboard.KEY_DOWN and event.name == "enter":
            barcode = input("Scan QR Code: ").strip()

            if barcode:
                mark_attendance(
                    barcode,
                    cursor,
                    connection,
                    sheet,
                    arduino
                )




def main():

    connection = init_mysql()
    cursor = connection.cursor()

    sheet = init_google_sheets()
    arduino = init_arduino()

    start_scanner(cursor, connection, sheet, arduino)


if __name__ == "__main__":
    main()
