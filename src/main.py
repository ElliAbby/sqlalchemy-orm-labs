import os
import sys
import logging
sys.path.insert(1, os.path.join(sys.path[0], '..'))

# императивный подход
# from queries.core import create_tables, insert_data, select_data

# декларативный подход
from queries.orm import create_tables, insert_data, select_data

logger = logging.getLogger(__name__)

try:
    logger.info("Creating tables...")
    create_tables()
    logger.info("Tables created successfully")
except Exception as e:
    logger.info(f"Error creating tables: {e}")


try:
    logger.info("Inserting data...")
    insert_data()
    logger.info("Data inserted successfully")
except Exception as e:
    logger.info(f"Error inserting data: {e}")


try:
    logger.info("Selecting data...")
    select_data()
    logger.info("Data selected successfully")
except Exception as e:
    logger.info(f"Error selecting data: {e}")