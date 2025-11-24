from dotenv import load_dotenv
import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

load_dotenv()

# engine = create_async_engine(
#     f"postgresql+asyncpg://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}/{os.getenv('POSTGRES_DB')}",
# )
engine = create_async_engine(
    "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres",
)

new_session = async_sessionmaker(bind=engine, expire_on_commit=False)
