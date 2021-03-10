from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from database.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    items = relationship("Item", back_populates="owner")

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

