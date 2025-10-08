from config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    settings.db.sync_url,
    echo=settings.db.echo,
)

Session = sessionmaker(
    bind=engine,
)


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
