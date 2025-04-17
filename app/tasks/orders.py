import asyncio
import logging

from datetime import datetime, timedelta
from sqlalchemy import select

from app.core.celery_app import celery_app
from app.db.base import async_session
from app.db.models.order import Order, OrderStatus


@celery_app.task
def send_order_confirmation(order_id: int, user_email: str):
    """
    Sends order confirmation to the user's email.
    """
    # In a real application, there would be email sending logic through SMTP here
    logging.info(f"Sending order {order_id} confirmation to user {user_email}")

    return True


@celery_app.task
def send_order_status_update(order_id: int, user_email: str, status: str):
    """
    Sends notification about order status change.
    """
    # In a real application, there would be email sending logic through SMTP here
    logging.info(f"Sending order {order_id} status update to user {user_email}: {status}")

    return True


@celery_app.task
def process_abandoned_orders():
    """
    Processes orders that have been in "processing" status for a long time.
    """
    async def _process_orders():
        async with async_session() as db:
            # Calculate the date up to which to check orders
            cutoff_date = datetime.utcnow() - timedelta(days=3)

            # Find orders for processing
            query = select(Order).where(
                (Order.status == OrderStatus.PROCESSING) &
                (Order.updated_at < cutoff_date)
            )

            result = await db.execute(query)
            orders = result.scalars().all()

            # Update order statuses
            count = 0
            for order in orders:
                # Send notification in a real application
                # send_order_status_update.delay(order.id, user_email, "cancelled")

                order.status = OrderStatus.CANCELLED
                db.add(order)
                count += 1

            if count > 0:
                await db.commit()
                logging.info(f"Cancelled {count} abandoned orders")

            return count

    return asyncio.run(_process_orders())
