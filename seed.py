"""Seed the database with a demo user and sample items."""

import asyncio

from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.auth.service import hash_password
from app.config import settings
from app.database import Base
from app.models.item import Item
from app.models.user import User

DEMO_EMAIL = "demo@example.com"
DEMO_PASSWORD = "demo1234"

SAMPLE_ITEMS = [
    ("Integrate Stripe payments", "Set up Stripe checkout for subscription billing"),
    ("Design landing page", "Mobile-first landing page with hero, features, and CTA"),
    ("Set up monitoring", "Configure Prometheus + Grafana for API metrics"),
    ("Write API documentation", "OpenAPI spec review and usage examples for clients"),
    ("Database optimization", "Add indexes and query tuning for the reports endpoint"),
]


async def seed():
    engine = create_async_engine(settings.database_url)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    async with session_factory() as db:
        result = await db.execute(select(User).where(User.email == DEMO_EMAIL))
        if result.scalar_one_or_none():
            print(f"Demo user ({DEMO_EMAIL}) already exists, skipping seed.")
            await engine.dispose()
            return

        user = User(
            email=DEMO_EMAIL,
            hashed_password=hash_password(DEMO_PASSWORD),
        )
        db.add(user)
        await db.flush()

        for title, description in SAMPLE_ITEMS:
            db.add(Item(title=title, description=description, owner_id=user.id))

        await db.commit()

    await engine.dispose()
    print(f"Seeded demo user ({DEMO_EMAIL} / {DEMO_PASSWORD}) with {len(SAMPLE_ITEMS)} items.")


if __name__ == "__main__":
    asyncio.run(seed())
