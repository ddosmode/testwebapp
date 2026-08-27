from app.infrastructure.database.models.locations import CityModel
from app.infrastructure.database.repositories.base import SQLAlchemyRepository


class CityRepository(SQLAlchemyRepository[CityModel]):
    def __init__(self, session):
        super().__init__(session, CityModel)
