# QR Code Attendance System (Sample Demo)

A hardware-software integration mini-project that tracks student attendance using **Python**, **MySQL**, **Google Sheets API**, and an **Arduino**. 


##  How It Works
1. **Scan:** A student scans their generated QR code.
2. **Process:** Python verifies the barcode against a local **MySQL** database to check validity and prevent duplicate daily scans.
3. **Sync:** The attendance record is saved locally and instantly backed up to a **Google Sheet**.
4. **Hardware Feedback:** Python sends a serial command to the **Arduino**, which displays the student's name on an I2C LCD and triggers a Servo motor (simulating a gate).

##  Tech Stack
* **Software:** Python 3 (`mysql-connector`, `gspread`, `qrcode`, `python-dotenv`)
* **Hardware:** Arduino Uno (C++), 16x2 I2C LCD, SG90 Servo
* **Database & Cloud:** MySQL, Google Sheets API

##  Quick Setup

 **Note: This project will not run "out of the box."** You must configure your own database and API credentials for security reasons.

### Clone & Install
```bash
git clone [https://github.com/Jaaaiiiiiii/Sample-QR-Attendance-System.git](https://github.com/Jaaaiiiiiii/Sample-QR-Attendance-System.git)
cd Sample-QR-Attendance-System
pip install -r requirements.txt
