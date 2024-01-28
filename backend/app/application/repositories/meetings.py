from app.application.protocols.repository import SQLAlchemyRepository
from app.domain.models import Meeting


class MeetingRepository(SQLAlchemyRepository):
    model = Meeting
