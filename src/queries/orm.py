import logging

from sqlalchemy import Integer, and_, func, select
from tabulate import tabulate

from database import Base, session_factory, sync_engine
from models.orm import ResumesOrm, WorkersOrm
from utils import Workload

logger = logging.getLogger(__name__)


class SyncOrm:
    @staticmethod
    def create_tables():
        sync_engine.echo = False
        Base.metadata.drop_all(sync_engine)
        Base.metadata.create_all(sync_engine)
        # sync_engine.echo = True

    @staticmethod
    def insert_workers():
        with session_factory() as session:
            try:
                workers = [
                    WorkersOrm(username="John Doe"),
                    WorkersOrm(username="Ivan Ivanov"),
                    WorkersOrm(username="Artem"),
                    WorkersOrm(username="Roman"),
                    WorkersOrm(username="Petr"),
                ]
                session.add_all(workers)
                session.flush()  # После flush каждый из работников получает первичный ключ id, который отдала БД
                session.commit()
                logger.info("Работники успешно добавлены")
                print("Работники успешно добавлены")
            except Exception as e:
                session.rollback()
                logger.warning(f"Ошибка при вставке: {e}")
                print(f"Ошибка при вставке: {e}")

    @staticmethod
    def select_workers():
        with session_factory() as session:
            stmt = select(WorkersOrm)
            workers = session.scalars(stmt).all()
            for worker in workers:
                logger.info(f"ID: {worker.id}, Name: {worker.username}")
                print(f"ID: {worker.id}, Name: {worker.username}")

    @staticmethod
    def update_worker(worker_id: int, new_username: str):
        with session_factory() as session:
            worker = session.get(WorkersOrm, worker_id)
            if worker:
                worker.username = new_username
                # refresh нужен, если мы хотим заново подгрузить данные модели из базы.
                # Подходит, если мы давно получили модель и в это время
                # данные в базе данныхмогли быть изменены
                # session.refresh(worker)
                session.commit()
                logger.info(f"Работник с ID = {worker_id} успешно обновлен")
                print(f"Работник с ID = {worker_id} успешно обновлен")
            else:
                logger.warning(f"Работник с ID = {worker_id} не найден")
                print(f"Работник с ID = {worker_id} не найден")

    @staticmethod
    def delete_worker(worker_id: int):
        with session_factory() as session:
            worker = session.get(WorkersOrm, worker_id)
            if worker:
                session.delete(worker)
                session.commit()
                logger.info(f"Работник с ID {worker_id} удален")
                print(f"Работник с ID {worker_id} удален")
            else:
                logger.warning(f"Работник с ID = {worker_id} не найден")
                print(f"Работник с ID = {worker_id} не найден")

    @staticmethod
    def insert_resumes():
        with session_factory() as session:
            resumes = [
                ResumesOrm(
                    title="Python Junior Developer",
                    salary=50000,
                    workload=Workload.FULLTIME,
                    worker_id=1,
                ),
                ResumesOrm(
                    title="Python Разработчик",
                    salary=150000,
                    workload=Workload.FULLTIME,
                    worker_id=1,
                ),
                ResumesOrm(
                    title="Python Data Engineer",
                    salary=250000,
                    workload=Workload.PARTTIME,
                    worker_id=2,
                ),
                ResumesOrm(
                    title="Data Scientist",
                    salary=300000,
                    workload=Workload.FULLTIME,
                    worker_id=2,
                ),
                ResumesOrm(
                    title="Python программист",
                    salary=60000,
                    workload=Workload.FULLTIME,
                    worker_id=3,
                ),
                ResumesOrm(
                    title="Machine Learning Engineer",
                    salary=70000,
                    workload=Workload.PARTTIME,
                    worker_id=3,
                ),
                ResumesOrm(
                    title="Python Data Scientist",
                    salary=80000,
                    workload=Workload.PARTTIME,
                    worker_id=4,
                ),
                ResumesOrm(
                    title="Python Analyst",
                    salary=90000,
                    workload=Workload.FULLTIME,
                    worker_id=4,
                ),
                ResumesOrm(
                    title="Python Junior Developer",
                    salary=100000,
                    workload=Workload.FULLTIME,
                    worker_id=5,
                ),
            ]
            session.add_all(resumes)
            session.commit()
            logger.info("Резюме успешно добавлены")
            print("Резюме успешно добавлены")

    @staticmethod
    def select_resumes():
        with session_factory() as session:
            stmt = select(ResumesOrm)
            resumes = session.scalars(stmt).all()
            for resume in resumes:
                logger.info(
                    f"ID: {resume.id}, Title: {resume.title}, Worker ID: {resume.worker_id}, Salary: {resume.salary}"
                )
                print(
                    f"ID: {resume.id}, Title: {resume.title}, Worker ID: {resume.worker_id}, Salary: {resume.salary}"
                )

    @staticmethod
    def update_resume(resume_id: int, new_salary: int):
        with session_factory() as session:
            resume = session.get(ResumesOrm, resume_id)
            if resume:
                resume.salary = new_salary
                # session.refresh(resume)
                session.commit()
                logger.info(f"Резюме с ID = {resume_id} успешно обновлено")
                print(f"Резюме с ID = {resume_id} успешно обновлено")
            else:
                logger.warning(f"Резюме с ID = {resume_id} не найдено")
                print(f"Резюме с ID = {resume_id} не найдено")

    @staticmethod
    def delete_resume(resume_id: int):
        with session_factory() as session:
            resume = session.get(ResumesOrm, resume_id)
            if resume:
                session.delete(resume)
                session.commit()
                logger.info(f"Резюме с ID {resume_id} удалено")
                print(f"Резюме с ID {resume_id} удалено")
            else:
                logger.warning(f"Резюме с ID = {resume_id} не найдено")
                print(f"Резюме с ID = {resume_id} не найдено")

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
                    ResumesOrm.workload,
                    func.avg(ResumesOrm.salary).cast(Integer).label("avg_salary"),
                )
                .select_from(ResumesOrm)
                .filter(
                    and_(
                        ResumesOrm.title.contains(like_language),
                        ResumesOrm.salary > 40000,
                    )
                )
                .group_by(ResumesOrm.workload)
                # .having(func.avg(ResumesOrm.salary) > 70000)
            )
            print(query.compile(compile_kwargs={"literal_binds": True}))
            res = conn.execute(query).all()
            table_data = [[r.workload.value, r.avg_salary] for r in res]
            print(
                tabulate(
                    table_data,
                    headers=["Тип занятости", "Средняя ЗП"],
                    tablefmt="rounded_grid",  # или "psql", "fancy_grid"
                )
            )
