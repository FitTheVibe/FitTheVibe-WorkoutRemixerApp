from app.repositories.workout_repository import WorkoutRepository
from app.schemas.workout import WorkoutCreate, WorkoutUpdate
from app.models.workout import Workout
from typing import Optional, List


class WorkoutService:
    def __init__(self, workout_repo: WorkoutRepository):
        self.workout_repo = workout_repo

    def get_all_workouts(self, page=1, limit=20, muscle_group=None, difficulty=None, equipment=None, search=None):
        workouts, pagination = self.workout_repo.get_all(
            page=page, limit=limit,
            muscle_group=muscle_group, difficulty=difficulty,
            equipment=equipment, search=search,
        )
        return workouts, pagination

    def get_workout(self, workout_id: int) -> Optional[Workout]:
        return self.workout_repo.get_by_id(workout_id)

    def get_alternatives(self, workout_id: int) -> List[Workout]:
        return self.workout_repo.get_alternatives(workout_id)

    def create_workout(self, data: WorkoutCreate, created_by: int) -> Workout:
        return self.workout_repo.create(data, created_by)

    def update_workout(self, workout_id: int, data: WorkoutUpdate) -> Optional[Workout]:
        return self.workout_repo.update(workout_id, data)

    def delete_workout(self, workout_id: int):
        self.workout_repo.delete(workout_id)