import re
import csv
import mysql.connector

INPUT_FILE = "employees_data.txt"
CSV_FILE = "output.csv"

# ---------- STEP 1: READ & CLEAN TEXT ----------
with open(INPUT_FILE, "r") as f:
    raw_text = f.read()

# Replace newlines with spaces
raw_text = raw_text.replace("\n", " ")

# Regex to extract records
pattern = r'([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*(\d+)'
records = re.findall(pattern, raw_text)

print(f"Total records found: {len(records)}")

# ---------- STEP 2: WRITE CLEAN CSV ----------
with open(CSV_FILE, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Name", "Email", "Phone", "Address", "PostalCode"])

    for r in records:
        writer.writerow([field.strip() for field in r])

print("CSV file created successfully")

# ---------- STEP 3: INSERT INTO MYSQL ----------
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="pass123",
    database="usersdata"
)

cursor = conn.cursor()

insert_query = """
INSERT INTO users (name, email, phone, address, postal_code)
VALUES (%s, %s, %s, %s, %s)
"""

cursor.executemany(insert_query, records)
conn.commit()

print(f"{cursor.rowcount} rows inserted into MySQL")

cursor.close()
conn.close()
