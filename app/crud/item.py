from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from models.items import Item
from schemas.item import ItemCreate, ItemUpdate
from core.custom_exception import ServerException


class CrudItem():
	def get_item_by_id(self, db: Session, id: int) -> Optional[Item]:
		return db.query(Item).filter(Item.id == id).first()

	def get_multi_by_owner(self, db: Session, owner_id: int) -> List[Item]:
		return db.query(Item).filter(Item.owner_id == owner_id).all()

	def get_multi_items(self, db: Session, skip: int = 0, limit: int = 100) -> Optional[Item]:
		data = db.query(Item).offset(skip).limit(limit).all()
		print("hello" * 100)
		return data

	def create_with_owner(self, db: Session, owner_id: int, item_obj: ItemCreate) -> Item:
		try:
			item_data = jsonable_encoder(item_obj)
			db_obj = Item(**item_data, owner_id=owner_id)
			db.add(db_obj)
			db.commit()
			db.refresh(db_obj)
			return db_obj
		except Exception as e:
			db.rollback()
			raise ServerException()

	def update_item(self, db: Session, id: int, item_obj: ItemUpdate):
		try:
			item_data = jsonable_encoder(item_obj)
			db.query(Item).filter(Item.id == id).update(item_data)
			db.commit()
			return item_data
		except Exception as e:
			db.rollback()
			raise ServerException()

	def delete_item(self, db: Session, id: int):
		item = db.query(Item).get(id)
		db.delete(item)
		db.commit()
		return item.title


crud_item = CrudItem()
