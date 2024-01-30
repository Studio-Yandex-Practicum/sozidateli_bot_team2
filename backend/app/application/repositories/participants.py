from app.application.protocols.repository import SQLAlchemyRepository
from app.domain.models.participants import Participant
from sqlalchemy import select


class ParticipantRepository(SQLAlchemyRepository):
    model = Participant

    async def check_user_exists(self, **filter_by) -> bool:
        stmt = select(self.model).filter_by(**filter_by).exists()
        return await self.session.scalar(select(stmt))
