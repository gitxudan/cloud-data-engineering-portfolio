
from google.cloud.sql.connector import Connector
import pymysql
import os
import dotenv

dotenv.load_dotenv()

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "keys/ba2512-gcp-key.json"


#Initialize Cloud SQL Python Connector
connector = Connector()

# Connection function for Cloud SQL database
def getconn():
    conn = connector.connect(
        "ba2512-480414:asia-southeast1:ba2512-mysql-server2",
        "pymysql",
        user = "ba25122",
        password = "19540519",
        db = "petstore"
    )
    return conn

# Insert a record
def insert_record(customerid, householdid, gender, name):
    conn = getconn()
    try:
        with conn.cursor() as cursor:
            sql = "INSERT INTO customer (customerid, householdid, gender, name) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (customerid, householdid, gender, name))
            conn.commit()
            print("Record inserted successfully.")
    finally:
        conn.close()


if __name__ == "__main__":
    # Example usage
    insert_record(12333, 345, 'Female', 'John Doe')
