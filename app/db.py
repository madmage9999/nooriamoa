from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=".env", override=True)

DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL is None:
    raise ValueError("DATABASE_URL environment variable not set")

engine = create_async_engine(DATABASE_URL, echo=True)

# Create session factory for async sessions
# expire_on_commit=False prevents expired object errors after commit
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()

async def get_db():
    """
    Dependency that yields database sessions.
    
    Usage:
        @app.get("/")
        async def root(db: AsyncSession = Depends(get_db)):
            ...
    
    Yields:
        AsyncSession: Database session that is automatically closed after use
    """
    async with async_session() as session:
        yield session
