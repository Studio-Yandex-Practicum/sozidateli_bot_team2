from src.application.protocols.repository import SQLAlchemyRepository
from src.domain.models import Meeting


class MeetingRepository(SQLAlchemyRepository):
    model = Meeting
