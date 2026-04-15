from sqlmodel import Session, select, func
from app.models.routine import Routine
from app.schemas.workout_routines_schemas import RoutineCreate, RoutineUpdate
from typing import Optional, Tuple, List
from app.utilities.pagination import Pagination
import logging

logger = logging.getLogger(__name__)


class RoutineRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, routine_data: RoutineCreate, user_id: int) -> Routine:
        try:
            routine = Routine(**routine_data.model_dump(), user_id=user_id)
            self.db.add(routine)
            self.db.commit()
            self.db.refresh(routine)
            return routine
        except Exception as e:
            logger.error(f"Error creating routine: {e}")
            self.db.rollback()
            raise

    def get_by_id(self, routine_id: int) -> Optional[Routine]:
        return self.db.get(Routine, routine_id)

    def get_by_user(self, user_id: int, page: int = 1, limit: int = 20) -> Tuple[List[Routine], Pagination]:
        offset = (page - 1) * limit
        query = select(Routine).where(Routine.user_id == user_id)
        count = self.db.exec(select(func.count()).select_from(query.subquery())).one()
        routines = self.db.exec(query.offset(offset).limit(limit)).all()
        pagination = Pagination(total_count=count, current_page=page, limit=limit)
        return routines, pagination

    def update(self, routine_id: int, routine_data: RoutineUpdate) -> Optional[Routine]:
        routine = self.db.get(Routine, routine_id)
        if not routine:
            return None
        for key, value in routine_data.model_dump(exclude_unset=True).items():
            setattr(routine, key, value)
        try:
            self.db.add(routine)
            self.db.commit()
            self.db.refresh(routine)
            return routine
        except Exception as e:
            logger.error(f"Error updating routine: {e}")
            self.db.rollback()
            raise

    def delete(self, routine_id: int):
        routine = self.db.get(Routine, routine_id)
        if not routine:
            raise Exception("Routine not found")
        try:
            self.db.delete(routine)
            self.db.commit()
        except Exception as e:
            logger.error(f"Error deleting routine: {e}")
            self.db.rollback()
            raise