from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.orm import relationship

from database.database import Base


class Item(Base):
	__tablename__ = "items"
	id = Column(Integer, primary_key=True, index=True, autoincrement=True)
	title = Column(String(64), unique=True, nullable=False, comment="标题名称")
	description = Column(String(128), nullable=False, comment="标题内容")
	owner_id = Column(Integer, ForeignKey("users.id"))
	owner = relationship("User", back_populates="items")
	created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
	updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")

	def to_dict(self):
		return {c.name: getattr(self, c.name) for c in self.__table__.columns}

	class Config:
		schema_extra = {
			"example": {
				"title": "this is title",
				"description": "this is description"
			}
		}
