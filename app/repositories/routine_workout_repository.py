from sqlmodel import Session, select
from app.models.routine_workout import RoutineWorkout
from app.models.workout import Workout
from app.schemas.workout import RoutineWorkoutAdd, RoutineWorkoutUpdate
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)


class RoutineWorkoutRepository:
    def __init__(self, db: Session):
        self.db = db

    def add(self, routine_id: int, data: RoutineWorkoutAdd) -> RoutineWorkout:
        try:
            rw = RoutineWorkout(
                routine_id=routine_id,
                workout_id=data.workout_id,
                position=data.position,
                sets=data.sets,
                reps=data.reps,
            )
            self.db.add(rw)
            self.db.commit()
            self.db.refresh(rw)
            return rw
        except Exception as e:
            logger.error(f"Error adding workout to routine: {e}")
            self.db.rollback()
            raise

    def get_by_id(self, rw_id: int) -> Optional[RoutineWorkout]:
        return self.db.get(RoutineWorkout, rw_id)

    def get_by_routine(self, routine_id: int) -> List[RoutineWorkout]:
        return self.db.exec(
            select(RoutineWorkout)
            .where(RoutineWorkout.routine_id == routine_id)
            .order_by(RoutineWorkout.position)
        ).all()

    def get_by_routine_and_workout(self, routine_id: int, workout_id: int) -> Optional[RoutineWorkout]:
        return self.db.exec(
            select(RoutineWorkout).where(
                RoutineWorkout.routine_id == routine_id,
                RoutineWorkout.workout_id == workout_id,
            )
        ).first()

    def update(self, rw_id: int, data: RoutineWorkoutUpdate) -> Optional[RoutineWorkout]:
        rw = self.db.get(RoutineWorkout, rw_id)
        if not rw:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(rw, key, value)
        try:
            self.db.add(rw)
            self.db.commit()
            self.db.refresh(rw)
            return rw
        except Exception as e:
            logger.error(f"Error updating routine workout: {e}")
            self.db.rollback()
            raise

    def remix(self, routine_id: int, old_workout_id: int, new_workout_id: int) -> RoutineWorkout:
        """Swap old_workout_id for new_workout_id, preserving sets/reps/position."""
        rw = self.get_by_routine_and_workout(routine_id, old_workout_id)
        if not rw:
            raise Exception("Workout not found in this routine")

        old_workout = self.db.get(Workout, old_workout_id)
        new_workout = self.db.get(Workout, new_workout_id)

        if not new_workout:
            raise Exception("Replacement workout not found")
        if old_workout.muscle_group != new_workout.muscle_group:
            raise Exception(
                f"Replacement must target the same muscle group ({old_workout.muscle_group})"
            )

        rw.workout_id = new_workout_id
        try:
            self.db.add(rw)
            self.db.commit()
            self.db.refresh(rw)
            return rw
        except Exception as e:
            logger.error(f"Error remixing routine: {e}")
            self.db.rollback()
            raise

    def remove(self, rw_id: int):
        rw = self.db.get(RoutineWorkout, rw_id)
        if not rw:
            raise Exception("Entry not found")
        try:
            self.db.delete(rw)
            self.db.commit()
        except Exception as e:
            logger.error(f"Error removing workout from routine: {e}")
            self.db.rollback()
            raise