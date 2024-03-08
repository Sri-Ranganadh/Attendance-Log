import sqlite3

# Connect to the database
conn = sqlite3.connect("attendance.db")
cursor = conn.cursor()

# Get a list of all tables in the database
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# Iterate over the tables and print their names and data
for table in tables:
    table_name = table[0]
    print(f"Table: {table_name}")
    # Retrieve data from the table
    cursor.execute(f"SELECT * FROM {table_name};")
    rows = cursor.fetchall()
    # Print the column names
    column_names = [description[0] for description in cursor.description]
    print(" | ".join(column_names))
    # Print the data
    for row in rows:
        print(" | ".join(map(str, row)))

    print()  # Add an empty line between tables

# Close the connection
conn.close()
