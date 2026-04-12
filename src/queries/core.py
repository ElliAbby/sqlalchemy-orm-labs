from sqlalchemy import Integer, and_, delete, func, insert, select, text, update

from database import sync_engine
from models.core import metadata_obj, resumes_table, workers_table
from utils import Workload


class SyncCore:
    @staticmethod
    def create_tables():
        # sync_engine.echo = False
        metadata_obj.drop_all(sync_engine)
        metadata_obj.create_all(sync_engine)
        # sync_engine.echo = True

    @staticmethod
    def insert_workers():
        with sync_engine.connect() as conn:
            # stmt = "INSERT INTO workers (username) VALUES ('John Doe'), ('Ivan Ivanov');"
            stmt = insert(workers_table).values(
                [
                    {"username": "John Doe"},
                    {"username": "Ivan Ivanov"},
                ]
            )
            conn.execute(stmt)
            conn.commit()

    @staticmethod
    def select_workers():
        with sync_engine.connect() as conn:
            # stmt = "SELECT * FROM workers;"
            stmt = select(workers_table)
            result = conn.execute(stmt)
            for row in result:
                print(row)

    @staticmethod
    def update_worker(worker_id: int, new_username: str):
        with sync_engine.connect() as conn:
            # stmt = text("UPDATE workers SET username=:username WHERE id=:id")
            # stmt = stmt.bindparams(username=new_username, id=worker_id)
            stmt = (
                update(workers_table)
                .values(username=new_username)
                .filter_by(id=worker_id)
            )
            conn.execute(stmt)
            conn.commit()

    @staticmethod
    def delete_worker(worker_id: int):
        with sync_engine.connect() as conn:
            # stmt = text("DELETE FROM workers WHERE id=:id")
            # stmt = stmt.bindparams(id=worker_id)
            stmt = delete(workers_table).filter_by(id=worker_id)
            conn.execute(stmt)
            conn.commit()

    @staticmethod
    def insert_resumes():
        with sync_engine.connect() as conn:
            resumes = [
                {
                    "title": "Python Junior Developer",
                    "salary": 50000,
                    "workload": Workload.FULLTIME,
                    "worker_id": 1,
                },
                {
                    "title": "Python Разработчик",
                    "salary": 150000,
                    "workload": Workload.FULLTIME,
                    "worker_id": 1,
                },
                {
                    "title": "Python Data Engineer",
                    "salary": 250000,
                    "workload": Workload.PARTTIME,
                    "worker_id": 2,
                },
                {
                    "title": "Data Scientist",
                    "salary": 300000,
                    "workload": Workload.FULLTIME,
                    "worker_id": 2,
                },
            ]
            stmt = insert(resumes_table).values(resumes)
            conn.execute(stmt)
            conn.commit()

    @staticmethod
    def select_resumes():
        with sync_engine.connect() as conn:
            # stmt = "SELECT * FROM resumes;"
            stmt = select(resumes_table)
            result = conn.execute(stmt)
            for row in result:
                print(row)

    @staticmethod
    def update_resume(resume_id: int, new_salary: int):
        with sync_engine.connect() as conn:
            # stmt = text("UPDATE resumes SET salary=:salary WHERE id=:id")
            # stmt = stmt.bindparams(salary=new_salary, id=resume_id)
            stmt = (
                update(resumes_table).values(salary=new_salary).filter_by(id=resume_id)
            )
            conn.execute(stmt)
            conn.commit()

    @staticmethod
    def delete_resume(resume_id: int):
        with sync_engine.connect() as conn:
            # stmt = text("DELETE FROM resumes WHERE id=:id")
            # stmt = stmt.bindparams(id=resume_id)
            stmt = delete(resumes_table).filter_by(id=resume_id)
            conn.execute(stmt)
            conn.commit()

    @staticmethod
    def select_resumes_avg_salary(like_language: str):
        """
        select workload, avg(salary)::int as avg_salary
        from resumes
        where title like '%Python%' and salary > 40000
        group by workload
        having avg(salary) > 70000
        """
        with sync_engine.connect() as conn:
            query = (
                select(
                    resumes_table.c.workload,
                    func.avg(resumes_table.c.salary).cast(Integer).label("avg_salary"),
                )
                .select_from(resumes_table)
                .filter(
                    and_(
                        resumes_table.c.title.contains(like_language),
                        resumes_table.c.salary > 40000,
                    )
                )
                .group_by(resumes_table.c.workload)
                .having(func.avg(resumes_table.c.salary) > 70000)
            )
            print(query.compile(compile_kwargs={"literal_binds": True}))
            res = conn.execute(query)
            result = res.all()
            print(result[0].avg_salary)
