import sqlite3

def execute_sql_script(script_path, database_path):
    with open(script_path, 'r') as script_file:
        script = script_file.read()

    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    try:
        cursor.executescript(script)
        connection.commit()
        print(f"{script_path} executed successfully.")
    except Exception as e:
        print(f"Error executing {script_path}: {e}")
    finally:
        connection.close()

def setup_database(database_path):
    setup_script_path = "DBsetup.sql"
    execute_sql_script(setup_script_path, database_path)

def fill_database(database_path):
    fill_script_path = "DBfill.sql"
    execute_sql_script(fill_script_path, database_path)

def clear_database(database_path):
    clear_script_path = "DBclear.sql"
    execute_sql_script(clear_script_path, database_path)

def view_database(database_path):
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    try:
        # Fetch and print data from each table
        tables = ['Storage', 'Calendar', 'Operations', 'Operation_Storage_map', 'Orders']
        for table in tables:
            print(f"\n{table} Table:")
            cursor.execute(f"SELECT * FROM {table}")
            table_data = cursor.fetchall()
            for row in table_data:
                print(row)

    except Exception as e:
        print(f"Error viewing data: {e}")
    finally:
        connection.close()

if __name__ == "__main__":
    database_path = "Storage_solution_DB.db"

    clear_database(database_path)

    setup_database(database_path)

    fill_database(database_path)

    view_database(database_path)
