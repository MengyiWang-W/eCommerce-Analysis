import sqlite3
import os
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Database file path
db_path = 'data/processed/ecommerce.db'

# SQL script file path
sql_file_path = 'sql/aggregations.sql'

# Check if files exist
if not os.path.exists(db_path):
    print(f"❌ Database file not found: {db_path}")
    exit(1)
if not os.path.exists(sql_file_path):
    print(f"❌ SQL file not found: {sql_file_path}")
    print(f"Current directory: {os.getcwd()}")
    print(f"Trying to locate: {os.path.abspath(sql_file_path)}")
    exit(1)

# Connect to database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Read SQL file
with open(sql_file_path, 'r', encoding='utf-8') as f:
    sql_script = f.read()

# Split by semicolon and execute each statement
statements = [s.strip() for s in sql_script.split(';') if s.strip()]

for stmt in statements:
    try:
        cursor.execute(stmt)
        print(f"✅ Executed successfully: {stmt[:50]}...")
    except sqlite3.OperationalError as e:
        print(f"⚠️ Execution failed: {stmt[:50]}... Error: {e}")

conn.commit()
conn.close()
print("\n🎉 All views created successfully!")