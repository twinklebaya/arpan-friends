from sqlmodel import SQLModel, Session, create_engine
from sqlalchemy.pool import NullPool

from .config import get_settings

settings = get_settings()

# SQLAlchemy dropped support for the bare "postgres://" scheme that Supabase
# (and Heroku, etc.) hand out -- normalize it so a re-copied connection
# string doesn't silently break the app.
_db_url = settings.database_url
if _db_url.startswith("postgres://"):
    _db_url = _db_url.replace("postgres://", "postgresql://", 1)

_is_sqlite = _db_url.startswith("sqlite")
connect_args = {"check_same_thread": False} if _is_sqlite else {}

# On serverless (Vercel), each invocation is a short-lived process -- a
# persistent SQLAlchemy connection pool doesn't carry over between
# invocations and just risks handing out stale/dead connections. NullPool
# opens a fresh connection per request instead, and pairs with Supabase's
# own PgBouncer pooler (use the pooled connection string, port 6543, not
# the direct one) to avoid exhausting Postgres's connection limit.
engine = create_engine(
    _db_url,
    connect_args=connect_args,
    poolclass=None if _is_sqlite else NullPool,
)


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
