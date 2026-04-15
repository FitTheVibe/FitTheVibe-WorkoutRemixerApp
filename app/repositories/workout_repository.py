from sqlmodel import Session, select, func
from app.models.workout import Workout, WorkoutBase
from app.schemas.workout_routines_schemas import WorkoutCreate, WorkoutUpdate
from typing import Optional, Tuple, List
from app.utilities.pagination import Pagination
import logging

logger = logging.getLogger(__name__)


class WorkoutRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, workout_data: WorkoutCreate, created_by: int) -> Workout:
        try:
            workout = Workout(**workout_data.model_dump(), created_by=created_by)
            self.db.add(workout)
            self.db.commit()
            self.db.refresh(workout)
            return workout
        except Exception as e:
            logger.error(f"Error creating workout: {e}")
            self.db.rollback()
            raise

    def get_by_id(self, workout_id: int) -> Optional[Workout]:
        return self.db.get(Workout, workout_id)

    def get_all(
        self,
        page: int = 1,
        limit: int = 20,
        muscle_group: Optional[str] = None,
        difficulty: Optional[str] = None,
        equipment: Optional[str] = None,
        search: Optional[str] = None,
    ) -> Tuple[List[Workout], Pagination]:
        offset = (page - 1) * limit
        query = select(Workout)

        if muscle_group:
            query = query.where(Workout.muscle_group == muscle_group)
        if difficulty:
            query = query.where(Workout.difficulty == difficulty)
        if equipment:
            query = query.where(Workout.equipment == equipment)
        if search:
            query = query.where(Workout.name.ilike(f"%{search}%"))

        count = self.db.exec(select(func.count()).select_from(query.subquery())).one()
        workouts = self.db.exec(query.offset(offset).limit(limit)).all()
        pagination = Pagination(total_count=count, current_page=page, limit=limit)
        return workouts, pagination

    def get_alternatives(self, workout_id: int) -> List[Workout]:
        """Return workouts in the same muscle group — used by the remix feature."""
        workout = self.get_by_id(workout_id)
        if not workout:
            return []
        return self.db.exec(
            select(Workout).where(
                Workout.muscle_group == workout.muscle_group,
                Workout.id != workout_id,
            )
        ).all()

    def update(self, workout_id: int, workout_data: WorkoutUpdate) -> Optional[Workout]:
        workout = self.db.get(Workout, workout_id)
        if not workout:
            return None
        for key, value in workout_data.model_dump(exclude_unset=True).items():
            setattr(workout, key, value)
        try:
            self.db.add(workout)
            self.db.commit()
            self.db.refresh(workout)
            return workout
        except Exception as e:
            logger.error(f"Error updating workout: {e}")
            self.db.rollback()
            raise

    def delete(self, workout_id: int):
        workout = self.db.get(Workout, workout_id)
        if not workout:
            raise Exception("Workout not found")
        try:
            self.db.delete(workout)
            self.db.commit()
        except Exception as e:
            logger.error(f"Error deleting workout: {e}")
            self.db.rollback()
            raise