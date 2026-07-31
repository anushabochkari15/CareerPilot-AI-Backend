"""
CareerPilot AI — History Service

Handles saving and retrieving user history from the database.
"""
from typing import Optional
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import HistoryRecord
import uuid
from datetime import datetime


async def save_history(
    db: AsyncSession,
    feature: str,
    title: str,
    summary: str,
    data: dict,
) -> HistoryRecord:
    """Save a history entry to the database."""
    record = HistoryRecord(
        id=str(uuid.uuid4()),
        feature=feature,
        title=title,
        summary=summary,
        data=data,
        created_at=datetime.utcnow(),
    )
    db.add(record)
    await db.commit()
    await db.refresh(record)
    return record


async def get_history(db: AsyncSession, feature: Optional[str] = None) -> list:
    """Retrieve history entries, optionally filtered by feature."""
    if feature:
        stmt = (
            select(HistoryRecord)
            .where(HistoryRecord.feature == feature)
            .order_by(desc(HistoryRecord.created_at))
        )
    else:
        stmt = select(HistoryRecord).order_by(desc(HistoryRecord.created_at))

    result = await db.execute(stmt)
    return result.scalars().all()


async def delete_history(db: AsyncSession, record_id: str) -> bool:
    """Delete a history entry by ID."""
    stmt = select(HistoryRecord).where(HistoryRecord.id == record_id)
    result = await db.execute(stmt)
    record = result.scalar_one_or_none()

    if record:
        await db.delete(record)
        await db.commit()
        return True
    return False
