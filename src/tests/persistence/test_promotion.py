from src.main.domain import BaseRepository, IPromotionRepository, Promotion as DomainPromotion, PromotionId
import pytest
from sqlmodel import Session, create_engine
from src.main.persistence import SQLModel, PromotionRepository


class PromotionRepositoryDumb(BaseRepository, IPromotionRepository):
    """Dumb implementation of IPromotionRepository."""
    def __init__(self):
        self.promotions = [
            DomainPromotion(id=PromotionId(id="1"), study_year=2, diploma="DEUST", name="Kempf"),
            DomainPromotion(id=PromotionId(id="2"), study_year=5, diploma="M2", name="Maisonnier")
        ]

    def find_all(self):
        return self.promotions

    def find_by_id(self, promotion_id: PromotionId):
        for promotion in self.promotions:
            if str(promotion.id) == str(promotion_id):
                return promotion
        raise ValueError("Promotion not found")

    def add(self, promotion: DomainPromotion) -> None:
        self.promotions.append(promotion)

    def update(self, promotion: DomainPromotion) -> None:
        for i, p in enumerate(self.promotions):
            if p.id == promotion.id:
                self.promotions[i] = promotion
                break
        else:
            raise ValueError("Promotion not found")

    def delete(self, id: PromotionId) -> None:
        for i, p in enumerate(self.promotions):
            if p.id == id:
                del self.promotions[i]
                break
        else:
            raise ValueError("Promotion not found")


class PromotionRepositoryException(PromotionRepositoryDumb):
    def find_all(self):
        raise Exception("Test exception")

    def find_by_id(self, id: PromotionId):
        raise Exception("Test exception")


DATABASE_URL = "sqlite:///test.db"
engine = create_engine(DATABASE_URL)


@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)


def test_promotion_repository(session):
    # Given
    repository = PromotionRepository(session)
    promotion_id = PromotionId(id=repository.next_identity())
    promotion = DomainPromotion(id=promotion_id, study_year=2, diploma="DEUST", name="Kempf")

    # When
    repository.add(promotion)
    assert promotion.id is not None

    fetched_promotion = repository.find_by_id(promotion.id)
    assert fetched_promotion is not None
    assert fetched_promotion.name == "Kempf"

    fetched_promotion.name = "Software Engineering"
    repository.update(fetched_promotion)
    updated_promotion = repository.find_by_id(fetched_promotion.id)
    assert updated_promotion.name == "Software Engineering"

    repository.delete(updated_promotion.id)
    with pytest.raises(ValueError):
        repository.find_by_id(updated_promotion.id)
