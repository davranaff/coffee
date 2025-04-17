import asyncio
import logging

from datetime import datetime, timedelta
from sqlalchemy import select

from app.core.celery_app import celery_app
from app.db.base import async_session
from app.db.models.user import User


@celery_app.task
def send_verification_email(user_id: int, verification_code: str):
    """
    Sends email with verification code.
    """
    # In a real application, there would be email sending logic through SMTP here
    logging.info(f"Sending verification code {verification_code} to user {user_id}")

    return True


@celery_app.task
def clean_unverified_users():
    """
    Cleans up unverified users registered more than 7 days ago.
    """
    async def _clean_users():
        async with async_session() as db:
            # Calculate the date up to which to delete users
            cutoff_date = datetime.utcnow() - timedelta(days=7)

            # Find users for deletion
            query = select(User).where(
                (User.is_verified == False) &
                (User.created_at < cutoff_date)
            )

            result = await db.execute(query)
            users_to_delete = result.scalars().all()

            # Delete users
            count = 0
            for user in users_to_delete:
                await db.delete(user)
                count += 1

            if count > 0:
                await db.commit()
                logging.info(f"Deleted {count} unverified users")

            return count

    return asyncio.run(_clean_users())
