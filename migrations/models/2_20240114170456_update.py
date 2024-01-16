from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "file" ALTER COLUMN "is_public" TYPE BOOL USING "is_public"::BOOL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "file" ALTER COLUMN "is_public" TYPE BOOL USING "is_public"::BOOL;"""
