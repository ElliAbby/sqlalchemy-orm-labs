import logging
import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], ".."))

# императивный подход
from queries.core import SyncCore

# декларативный подход
# from queries.orm import create_tables, insert_data, select_data

logger = logging.getLogger(__name__)

try:
    logger.info("Creating tables...")
    SyncCore.create_tables()
    logger.info("Tables created successfully")
except Exception as e:
    logger.warning(f"Error creating tables: {e}")


try:
    logger.info("Inserting data...")
    SyncCore.insert_workers()
    logger.info("Data inserted successfully")
except Exception as e:
    logger.warning(f"Error inserting data: {e}")


try:
    logger.info("Selecting data...")
    SyncCore.select_workers()
    logger.info("Data selected successfully")
except Exception as e:
    logger.warning(f"Error selecting data: {e}")


try:
    logger.info("Update worker where id=1")
    SyncCore.update_worker(worker_id=1, new_username="Superman")
    logger.info("Data updated successfuly")
except Exception as e:
    logger.warning(f"Error updating data: {e}")


try:
    logger.info("Delete worker where id=1")
    SyncCore.delete_worker(worker_id=1)
    logger.info("Data deleted successfuly")
except Exception as e:
    logger.warning(f"Error deleting data: {e}")
