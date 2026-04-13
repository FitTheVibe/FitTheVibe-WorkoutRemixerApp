from app.repositories.routine_repository import RoutineRepository
from app.repositories.routine_workout_repository import RoutineWorkoutRepository
from app.schemas.workout_routines_schemas import RoutineCreate, RoutineUpdate, RoutineWorkoutAdd, RoutineWorkoutUpdate
from app.models.routine import Routine
from app.models.routine_workout import RoutineWorkout
from typing import Optional


class RoutineService:
    def __init__(self, routine_repo: RoutineRepository, rw_repo: RoutineWorkoutRepository):
        self.routine_repo = routine_repo
        self.rw_repo = rw_repo

    def get_user_routines(self, user_id: int, page=1, limit=20):
        routines, pagination = self.routine_repo.get_by_user(user_id, page=page, limit=limit)
        return routines, pagination

    def get_routine(self, routine_id: int) -> Optional[Routine]:
        return self.routine_repo.get_by_id(routine_id)

    def get_routine_workouts(self, routine_id: int):
        return self.rw_repo.get_by_routine(routine_id)

    def create_routine(self, data: RoutineCreate, user_id: int) -> Routine:
        return self.routine_repo.create(data, user_id)

    def update_routine(self, routine_id: int, data: RoutineUpdate) -> Optional[Routine]:
        return self.routine_repo.update(routine_id, data)

    def delete_routine(self, routine_id: int):
        self.routine_repo.delete(routine_id)

    def add_workout(self, routine_id: int, data: RoutineWorkoutAdd) -> RoutineWorkout:
        return self.rw_repo.add(routine_id, data)

    def update_routine_workout(self, rw_id: int, data: RoutineWorkoutUpdate) -> Optional[RoutineWorkout]:
        return self.rw_repo.update(rw_id, data)

    def remove_workout(self, rw_id: int):
        self.rw_repo.remove(rw_id)

    def remix(self, routine_id: int, old_workout_id: int, new_workout_id: int) -> RoutineWorkout:
        return self.rw_repo.remix(routine_id, old_workout_id, new_workout_id)