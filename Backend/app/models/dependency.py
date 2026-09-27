from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.card import Card


class CardDependency(Base):
    """
    Represents a dependency between two cards.
    dependent_card_id depends on upstream_card_id.
    
    Example: "Follow-up with Neurology" depends on "Complete MRI"
    """
    __tablename__ = "card_dependencies"

    id: Mapped[int] = mapped_column(primary_key=True)
    
    dependent_card_id: Mapped[int] = mapped_column(
        ForeignKey("cards.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="The card that depends on another"
    )
    
    upstream_card_id: Mapped[int] = mapped_column(
        ForeignKey("cards.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="The card that must be completed first"
    )
    
    reason: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
        comment="Why does dependent_card depend on upstream_card?"
    )
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint(
            'dependent_card_id',
            'upstream_card_id',
            name='uq_card_dependency_pair'
        ),
    )