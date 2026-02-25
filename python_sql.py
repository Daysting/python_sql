# Erick Hofer
# CIS261
# Python SQL

def create_connection(db_path: str = 'example.db'):
    """Create a SQLite database connection.

    Args:
        db_path: Path to the SQLite database file. Use ':memory:' for an in-memory database.

    Returns:
        sqlite3.Connection: A connection object to the database.
    """
    import sqlite3
    connection = sqlite3.connect(db_path)
    return connection

def create_table(connection):
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                      (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)''')
    connection.commit()

def select_us_numbers(connection):
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM users')
    return cursor.fetchall()

def update_phone_types(connection):
    cursor = connection.cursor()
    cursor.execute('ALTER TABLE users ADD COLUMN phone_type TEXT')
    connection.commit() 

def delete_xx_records(connection):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM users WHERE name LIKE 'XX%'")
    connection.commit()

def drop_phone_table(connection):
    cursor = connection.cursor()
    cursor.execute('ALTER TABLE users DROP COLUMN phone_type')
    connection.commit()

def main():
    # create a connection and ensure the table exists
    connection = create_connection()
    create_table(connection)

    # add some sample data (clean slate each run)
    cursor = connection.cursor()
    cursor.execute("DELETE FROM users")
    cursor.execute("INSERT INTO users (name, age) VALUES ('Alice', 30)")
    cursor.execute("INSERT INTO users (name, age) VALUES ('Bob', 25)")
    cursor.execute("INSERT INTO users (name, age) VALUES ('XXCharlie', 35)")
    connection.commit()

    # --- sequence of operations with basic checks ---
    users = select_us_numbers(connection)
    print("initial rows:", users)

    # 1. add phone_type column
    update_phone_types(connection)
    users = select_us_numbers(connection)
    print("after adding phone_type:", users)
    assert all(len(row) == 4 for row in users), "phone_type column not added"

    # 2. delete records beginning with XX
    delete_xx_records(connection)
    users = select_us_numbers(connection)
    print("after deleting XX rows:", users)
    assert not any(row[1].startswith('XX') for row in users), "XX records remain"

    # 3. attempt to drop the phone_type column
    try:
        drop_phone_table(connection)
        users = select_us_numbers(connection)
        print("after dropping phone_type:", users)
        assert all(len(row) == 3 for row in users), "phone_type column not removed"
    except Exception as exc:  # sqlite3.OperationalError usually
        print(f"could not drop column: {exc}")

    connection.close()
    print("sequence completed")

if __name__ == "__main__":
    main()
