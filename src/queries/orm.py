import logging

from sqlalchemy import Integer, and_, func, select
from sqlalchemy.orm import aliased, joinedload, selectinload
from tabulate import tabulate

from database import Base, session_factory, sync_engine
from models.orm import ResumesOrm, WorkersOrm
from utils import Workload

logger = logging.getLogger(__name__)


class SyncOrm:
    @staticmethod
    def create_tables():
        sync_engine.echo = True
        Base.metadata.drop_all(sync_engine)
        Base.metadata.create_all(sync_engine)
        sync_engine.echo = True

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
                    tablefmt="psql",  # стили: "psql", "fancy_grid", "rounded_grid"
                )
            )

    @staticmethod
    def get_resumes_salary_deviation():
        """
        Описание:
        Этот SQL-запрос выполняет сложный аналитический расчет:
        он сравнивает зарплату каждого конкретного работника со средней зарплатой по его типу занятости (workload).

        SQL-скрипт:
        WITH helper2 AS (
            SELECT *, salary-avg_workload_salary AS salary_diff
            FROM
            (SELECT
                w.id,
                w.username,
                r.salary,
                r.workload,
                avg(r.salary) OVER (PARTITION BY workload)::int AS avg_workload_salary
            FROM resumes r
            JOIN workers w ON r.worker_id = w.id) helper1
        )
        SELECT * FROM helper2
        ORDER BY salary_diff DESC;
        """
        with session_factory() as session:
            r = aliased(ResumesOrm)
            w = aliased(WorkersOrm)
            # оконная функция
            avg_workload_col = (
                func.avg(r.salary)
                .over(partition_by=r.workload)
                .cast(Integer)
                .label("avg_workload_salary")
            )

            # подзапрос
            subquery = (
                select(w.id, w.username, r.salary, r.workload, avg_workload_col)
                .select_from(r)
                .join(w, w.id == r.worker_id)
                .subquery()
            )

            # Финальный запрос с вычислением разницы
            diff_salary = (subquery.c.salary - subquery.c.avg_workload_salary).label(
                "salary_diff"
            )

            stmt = select(subquery, diff_salary).order_by(diff_salary.desc())
            result = session.execute(stmt).all()
            table_data = [
                [r.username, r.workload.value, r.salary, r.salary_diff] for r in result
            ]
            print(
                tabulate(
                    table_data,
                    headers=[
                        "Имя п-ля",
                        "Тип занятости",
                        "Зарплата",
                        "Разница между средней ЗП и своей",
                    ],
                    tablefmt="psql",  # стили: "psql", "fancy_grid", "rounded_grid"
                )
            )

    @staticmethod
    def select_workers_with_lazy_relationship():
        """данный запрос демонстрирует Lazy Loading (отложенную загрузку) связанных данных в SQLAlchemy."""
        with session_factory() as session:
            query = select(WorkersOrm)

            res = session.execute(query).scalars().all()

            # в данный момент SQLAlchemy «на лету» отправляет в базу данных новый отдельный SQL-запрос, чтобы найти резюме именно для этого работника.
            worker_1_resumes = res[0].resumes
            logger.info(f"LAZY relationships: {worker_1_resumes}")
            print(f"LAZY relationships: {worker_1_resumes}")

            worker_2_resumes = res[1].resumes
            logger.info(f"LAZY relationships: {worker_2_resumes}")
            print(f"LAZY relationships: {worker_2_resumes}")

    @staticmethod
    def select_workers_with_joined_relationships():
        """Решает проблему N+1. Загружает и работников, и их резюме за один SQL-запрос"""
        with session_factory() as session:
            query = select(WorkersOrm).options(joinedload(WorkersOrm.resumes))

            res = (
                session.execute(query).unique().scalars().all()
            )  # при joinedload важно использовать unique

            worker_1_resumes = res[0].resumes
            logger.info(f"JOINED relationships: {worker_1_resumes}")
            print(f"JOINED relationships: {worker_1_resumes}")

            worker_2_resumes = res[1].resumes
            logger.info(f"JOINED relationships: {worker_2_resumes}")
            print(f"JOINED relationships: {worker_2_resumes}")

    @staticmethod
    def select_workers_with_selectin_relationships():
        """
        Самый оптимальный вариант для загрузки коллекций (связей «один-ко-многим»)
        Первый запрос: SQLAlchemy выбирает всех работников: SELECT * FROM workers.
        Второй запрос: SQLAlchemy собирает все id полученных работников и делает один отдельный запрос для резюме: SELECT * FROM resumes WHERE worker_id IN (1, 2, 3, ...).
        """
        with session_factory() as session:
            query = select(WorkersOrm).options(selectinload(WorkersOrm.resumes))

            res = (
                session.execute(query).scalars().all()
            )  # при selectinload нед дубликатов -> не надо использовать unique

            worker_1_resumes = res[0].resumes
            logger.info(f"SELECTIN relationships: {worker_1_resumes}")
            print(f"SELECTIN relationships: {worker_1_resumes}")

            worker_2_resumes = res[1].resumes
            logger.info(f"SELECTIN relationships: {worker_2_resumes}")
            print(f"SELECTIN relationships: {worker_2_resumes}")
