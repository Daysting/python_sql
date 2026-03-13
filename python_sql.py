# Erick Hofer
# CIS261
# Python SQL

import sqlite3

# Connect to the database
conn = sqlite3.connect('phone.db')
cursor = conn.cursor()

def create_table():
    """Create the phone table based on the SQL statement."""
    sql = """
    CREATE TABLE phone (
        phone_id INT,
        country_code INT NOT NULL,
        phone_number INT NOT NULL,
        phone_type VARCHAR(12),
        PRIMARY KEY(phone_id)
    );
    """
    cursor.execute(sql)
    conn.commit()
    print("Table 'phone' created successfully.")

def select_phones():
    """Select phone_number from phone where country_code = 'US'."""
    sql = """
    SELECT phone_number
    FROM phone
    WHERE country_code = ?
    """
    cursor.execute(sql, ("US",))
    results = cursor.fetchall()
    print("Selected phone numbers:")
    for row in results:
        print(row[0])

def update_phones():
    """Update phone_type from 'CELLULAR' to 'MOBILE'."""
    sql = """
    UPDATE phone
    SET phone_type = ?
    WHERE phone_type = ?
    """
    cursor.execute(sql, ("MOBILE", "CELLULAR"))
    conn.commit()
    print("Updated phone types from 'CELLULAR' to 'MOBILE'.")

def delete_phones():
    """Delete rows where country_code = 'XX'."""
    sql = """
    DELETE FROM phone
    WHERE country_code = ?
    """
    cursor.execute(sql, ("XX",))
    conn.commit()
    print("Deleted rows where country_code = 'XX'.")

def drop_table():
    """Drop the phone table."""
    sql = "DROP TABLE phone"
    cursor.execute(sql)
    conn.commit()
    print("Table 'phone' dropped successfully.")

# Close the connection
conn.close()
