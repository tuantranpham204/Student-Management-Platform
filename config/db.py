import os
from dotenv import load_dotenv
import mysql.connector as connector
load_dotenv()

conn = connector.connect(
        host = os.getenv('DB_HOST'),
        user = os.getenv('DB_USER'),
        password = os.getenv('DB_PASSWORD'),
        database = os.getenv('DB_NAME'),
        port = int(os.getenv('DB_PORT')),
)

cursor = conn.cursor(dictionary=True)





