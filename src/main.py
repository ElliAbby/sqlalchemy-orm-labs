import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from queries.core import create_tables


try:
    print("Creating tables...")
    create_tables()
    print("Tables created successfully")
except Exception as e:
    print(f"Error creating tables: {e}")