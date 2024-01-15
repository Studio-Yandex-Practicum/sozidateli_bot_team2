from src.application.protocols.repository import SQLAlchemyRepository
from src.domain.models.users import User


class UserRepository(SQLAlchemyRepository):
    model = User
