from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String, Text

from app.database import Base


class ContactMessage(Base):
    """A single contact-form submission saved to Postgres."""

    __tablename__ = "contact_messages"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    email = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )


class VisitCounter(Base):
    """A single-row table holding the total visit count."""

    __tablename__ = "visit_counter"

    id = Column(Integer, primary_key=True, index=True)
    count = Column(Integer, nullable=False, default=0)
