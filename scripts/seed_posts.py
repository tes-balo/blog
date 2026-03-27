# scripts/seed_posts.py
import asyncio
from datetime import datetime
from typing import Any

from sqlalchemy import insert, select

from app.db.database import async_engine, metadata
from app.db.tables.posts import posts  # your posts table definition

# Old posts to seed
old_posts: list[dict[str, Any]] = [
    {
        "id": 1,
        "title": "first post",
        "content": "some interesting stories",
        "published": True,
        "created_at": "2026-03-12 19:49:34+01",
    },
    {
        "id": 2,
        "title": "second post",
        "content": "yadayadayads",
        "published": True,
        "created_at": "2026-03-12 19:55:31+01",
    },
    {
        "id": 3,
        "title": "second post",
        "content": "wagwan",
        "published": True,
        "created_at": "2026-03-12 19:55:31+01",
    },
    {
        "id": 4,
        "title": "second post",
        "content": "david de gea",
        "published": True,
        "created_at": "2026-03-12 19:55:31+01",
    },
]

# Convert created_at strings to datetime objects
for post in old_posts:
    post["created_at"] = datetime.fromisoformat(str(post["created_at"]))


async def seed() -> None:
    async with async_engine.begin() as conn:
        # Ensure tables exist
        await conn.run_sync(metadata.create_all)

        # Fetch existing IDs
        result = await conn.execute(select(posts.c.id))
        existing_ids: set[Any] = {row[0] for row in result.all()}

        # Filter only posts that are missing
        posts_to_insert: list[dict[str, Any]] = [
            post for post in old_posts if post["id"] not in existing_ids
        ]

        if posts_to_insert:
            await conn.execute(insert(posts), posts_to_insert)
            print(f"✅ Inserted {len(posts_to_insert)} new post(s)")
        else:
            print("⚠️ All old posts already exist, skipping insert")


# Ensures that this block only runs when you execute the script directly,
# not when its imported as a module.
if __name__ == "__main__":
    asyncio.run(seed())
