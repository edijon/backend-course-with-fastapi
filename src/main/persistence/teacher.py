from sqlmodel import Session, select, SQLModel, Field
from typing import List
from src.main.domain.teacher import ITeacherRepository, Teacher as DomainTeacher, TeacherId
from src.main.domain.base import BaseRepository
import uuid


class Teacher(SQLModel, table=True):
    __tablename__ = "teachers"
    __table_args__ = {"extend_existing": True}
    id: str = Field(primary_key=True)
    name: str
    firstname: str


class TeacherRepository(BaseRepository, ITeacherRepository):
    def __init__(self, session: Session):
        self.session = session

    def next_identity(self) -> TeacherId:
        return TeacherId(id=str(uuid.uuid4()))

    def find_all(self) -> List[DomainTeacher]:
        statement = select(Teacher)
        results = self.session.exec(statement)
        return [self._to_domain(teacher) for teacher in results.all()]

    def find_by_id(self, id: TeacherId) -> DomainTeacher:
        statement = select(Teacher).where(Teacher.id == id.id)
        result = self.session.exec(statement).first()
        if not result:
            raise ValueError("Teacher not found")
        return self._to_domain(result)

    def add(self, teacher: DomainTeacher) -> None:
        db_teacher = Teacher(
            id=teacher.id.id,
            name=teacher.name,
            firstname=teacher.firstname
        )
        self.session.add(db_teacher)
        self.session.commit()

    def update(self, teacher: DomainTeacher) -> None:
        db_teacher = Teacher(
            id=teacher.id.id,
            name=teacher.name,
            firstname=teacher.firstname
        )
        self.session.merge(db_teacher)
        self.session.commit()

    def delete(self, id: TeacherId) -> None:
        teacher = self.find_by_id(id)
        db_teacher = self.session.get(Teacher, id.id)
        self.session.delete(db_teacher)
        self.session.commit()

    def _to_domain(self, teacher: Teacher) -> DomainTeacher:
        return DomainTeacher(
            id=TeacherId(id=teacher.id),
            name=teacher.name,
            firstname=teacher.firstname
        )
