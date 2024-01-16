from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "user" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "email" VARCHAR(255) NOT NULL UNIQUE,
    "password" VARCHAR(100) NOT NULL,
    "last_name" VARCHAR(30) NOT NULL,
    "first_name" VARCHAR(30) NOT NULL,
    "surname" VARCHAR(30),
    "join_date" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "is_active" BOOL NOT NULL  DEFAULT True,
    "is_staff" BOOL NOT NULL  DEFAULT False,
    "is_superuser" BOOL NOT NULL  DEFAULT False,
    "comments" TEXT
);
COMMENT ON COLUMN "user"."id" IS 'Идентификатор';
COMMENT ON COLUMN "user"."email" IS 'Адрес электронной почты';
COMMENT ON COLUMN "user"."password" IS 'Пароль';
COMMENT ON COLUMN "user"."last_name" IS 'Фамилия';
COMMENT ON COLUMN "user"."first_name" IS 'Имя';
COMMENT ON COLUMN "user"."surname" IS 'Отчество';
COMMENT ON COLUMN "user"."join_date" IS 'Дата регистрации';
COMMENT ON COLUMN "user"."is_active" IS 'Признак активности';
COMMENT ON COLUMN "user"."is_staff" IS 'Признак персонала';
COMMENT ON COLUMN "user"."is_superuser" IS 'Признак администратора';
COMMENT ON COLUMN "user"."comments" IS 'Информация о пользователе';
COMMENT ON TABLE "user" IS 'Модель пользователя ';
CREATE TABLE IF NOT EXISTS "file" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(50) NOT NULL,
    "size" INT NOT NULL,
    "content_type" VARCHAR(30) NOT NULL,
    "filename" VARCHAR(30) NOT NULL UNIQUE,
    "status" VARCHAR(12) NOT NULL  DEFAULT 'under_review',
    "upload_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "owner_id" INT REFERENCES "user" ("id") ON DELETE SET NULL
);
COMMENT ON COLUMN "file"."id" IS 'Идентификатор';
COMMENT ON COLUMN "file"."name" IS 'Имя файла';
COMMENT ON COLUMN "file"."size" IS 'Размер файла';
COMMENT ON COLUMN "file"."content_type" IS 'Тип файла';
COMMENT ON COLUMN "file"."filename" IS 'Имя файла на диске';
COMMENT ON COLUMN "file"."status" IS 'Статус файла';
COMMENT ON COLUMN "file"."upload_at" IS 'Дата и время загрузки файла';
COMMENT ON COLUMN "file"."owner_id" IS 'Владелец';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
