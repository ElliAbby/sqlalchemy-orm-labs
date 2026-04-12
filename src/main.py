import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], ".."))

# императивный подход
from queries.core import SyncCore

# декларативный подход
# from queries.orm import create_tables, insert_data, select_data


def main():
    if "--core" in sys.argv and "--sync" in sys.argv:
        SyncCore.create_tables()
        SyncCore.insert_workers()
        SyncCore.select_workers()
        SyncCore.insert_resumes()
        SyncCore.select_resumes()
        SyncCore.select_resumes_avg_salary(like_language="Python")
        SyncCore.update_worker(worker_id=1, new_username="Superman")
        SyncCore.update_resume(resume_id=1, new_salary=100_000)
        SyncCore.delete_resume(resume_id=1)
        SyncCore.delete_worker(worker_id=2)


if __name__ == "__main__":
    main()
