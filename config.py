Import os

from dotenv import load_dotenv



load_dotenv()



MYSQL_CONFIG = {

"host": os.getenv("MYSQL_HOST"),

"user": os.getenv("MYSQL_USER"),

"password": os.getenv("MYSQL_PASSWORD"),

"database": os.getenv("MYSQL_DATABASE")

}



SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT_FILE")

SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")



ARDUINO_PORT = os.getenv("ARDUINO_PORT")

BAUD_RATE = int(os.getenv("BAUD_RATE"))
