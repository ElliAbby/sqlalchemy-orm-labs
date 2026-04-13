import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], ".."))

# императивный подход
from queries.core import SyncCore

# декларативный подход
from queries.orm import SyncOrm


def main():
    if "--core" in sys.argv and "--sync" in sys.argv:
        # создание и вставка
        SyncCore.create_tables()
        SyncCore.insert_workers()
        SyncCore.select_workers()
        SyncCore.insert_resumes()
        SyncCore.select_resumes()
        # сложные запросы
        SyncCore.select_resumes_avg_salary(like_language="Python")
        SyncCore.get_resumes_salary_deviation()
        # обноление
        SyncCore.update_worker(worker_id=1, new_username="Superman")
        SyncCore.update_resume(resume_id=1, new_salary=100_000)
        # удаление
        SyncCore.delete_resume(resume_id=1)
        SyncCore.delete_worker(worker_id=2)
        SyncCore.select_workers()
        SyncCore.select_resumes()

    if "--orm" in sys.argv and "--sync" in sys.argv:
        # создание и вставка
        SyncOrm.create_tables()
        SyncOrm.insert_workers()
        SyncOrm.select_workers()
        SyncOrm.insert_resumes()
        SyncOrm.select_resumes()
        # сложные запросы
        SyncOrm.select_resumes_avg_salary(like_language="Python")
        SyncOrm.get_resumes_salary_deviation()
        # обноление
        SyncOrm.update_worker(worker_id=1, new_username="Superman")
        SyncOrm.select_workers()
        SyncOrm.update_resume(resume_id=1, new_salary=100_000)
        SyncOrm.select_resumes()
        # удаление
        SyncOrm.delete_resume(resume_id=1)
        SyncOrm.select_resumes()
        SyncOrm.delete_worker(worker_id=2)
        SyncOrm.select_workers()


if __name__ == "__main__":
    main()
