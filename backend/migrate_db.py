import sqlite3
import os

DB_PATH = "assessment.db"

def migrate_database():
    if not os.path.exists(DB_PATH):
        print("Database doesn't exist. It will be created automatically on server start.")
        return
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute("PRAGMA table_info(employees)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'department' not in columns:
            print("Adding 'department' column to employees table...")
            cursor.execute("ALTER TABLE employees ADD COLUMN department TEXT")
            print("Added 'department' column")
        else:
            print("'department' column already exists")
        
        if 'phone' not in columns:
            print("Adding 'phone' column to employees table...")
            cursor.execute("ALTER TABLE employees ADD COLUMN phone TEXT")
            print("Added 'phone' column")
        else:
            print("'phone' column already exists")
        cursor.execute("PRAGMA table_info(tasks)")
        task_columns = [col[1] for col in cursor.fetchall()]
        
        if 'priority' not in task_columns:
            print("Adding 'priority' column to tasks table...")
            cursor.execute("ALTER TABLE tasks ADD COLUMN priority TEXT DEFAULT 'Medium'")
            print("Added 'priority' column")
        else:
            print("'priority' column already exists")
        
        if 'due_date' not in task_columns:
            print("Adding 'due_date' column to tasks table...")
            cursor.execute("ALTER TABLE tasks ADD COLUMN due_date DATE")
            print("Added 'due_date' column")
        else:
            print("'due_date' column already exists")
        
        if 'updated_at' not in task_columns:
            print("Adding 'updated_at' column to tasks table...")
            cursor.execute("ALTER TABLE tasks ADD COLUMN updated_at DATETIME")
            print("Added 'updated_at' column")
        else:
            print("'updated_at' column already exists")
        
        conn.commit()
        print("\nDatabase migration completed successfully!")
        
    except Exception as e:
        conn.rollback()
        print(f"\nError during migration: {e}")
        print("You may need to delete the database and recreate it.")
    finally:
        conn.close()

if __name__ == "__main__":
    print("Starting database migration...\n")
    migrate_database()
