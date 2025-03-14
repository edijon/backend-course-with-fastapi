from sqlmodel import Session, select, SQLModel, Field
from typing import List
from src.main.domain.promotion import IPromotionRepository, Promotion as DomainPromotion, PromotionId
from src.main.domain.base import BaseRepository
import uuid


class Promotion(SQLModel, table=True):
    __tablename__ = "promotions"
    __table_args__ = {"extend_existing": True}
    id: str = Field(primary_key=True)
    study_year: int
    diploma: str
    name: str


class PromotionRepository(BaseRepository, IPromotionRepository):
    def __init__(self, session: Session):
        self.session = session

    def find_all(self) -> List[DomainPromotion]:
        statement = select(Promotion)
        results = self.session.exec(statement)
        return [self._to_domain(promotion) for promotion in results.all()]

    def find_by_id(self, id: PromotionId) -> DomainPromotion:
        statement = select(Promotion).where(Promotion.id == id.id)
        result = self.session.exec(statement).first()
        if not result:
            raise ValueError("Promotion not found")
        return self._to_domain(result)

    def add(self, promotion: DomainPromotion) -> None:
        db_promotion = Promotion(
            id=promotion.id.id,
            study_year=promotion.study_year,
            diploma=promotion.diploma,
            name=promotion.name
        )
        self.session.add(db_promotion)
        self.session.commit()

    def update(self, promotion: DomainPromotion) -> None:
        db_promotion = Promotion(
            id=promotion.id.id,
            study_year=promotion.study_year,
            diploma=promotion.diploma,
            name=promotion.name
        )
        self.session.merge(db_promotion)
        self.session.commit()

    def delete(self, id: PromotionId) -> None:
        promotion = self.find_by_id(id)
        db_promotion = self.session.get(Promotion, id.id)
        self.session.delete(db_promotion)
        self.session.commit()

    def _to_domain(self, promotion: Promotion) -> DomainPromotion:
        return DomainPromotion(
            id=PromotionId(id=promotion.id),
            study_year=promotion.study_year,
            diploma=promotion.diploma,
            name=promotion.name
        )
