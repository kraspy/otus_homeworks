from sqlalchemy import select
from sqlalchemy.orm import Session as SessionType

from .models import User


# ========================================
# CRUD: Users
# ========================================
def get_all_users(session: SessionType):
    with session:
        stmt = select(User)
        return session.scalars(stmt).all()


def add_user(session: SessionType, user: dict[str, str]):
    user = User(**user)
    with session:
        session.add(user)
        session.commit()
