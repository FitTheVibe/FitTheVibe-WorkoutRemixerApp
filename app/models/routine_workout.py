from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.workout import Workout
    from app.models.routine import Routine

class RoutineWorkoutBase(SQLModel):
    position: int = Field(default=0)
    sets: int = Field(default=3)
    reps: int = Field(default=10)

class RoutineWorkout(RoutineWorkoutBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    routine_id: Optional[int] = Field(default=None, foreign_key="routine.id")
    workout_id: Optional[int] = Field(default=None, foreign_key="workout.id")

    routine: Optional["Routine"] = Relationship(back_populates="routine_workouts")
    workout: Optional["Workout"] = Relationship(back_populates="routine_workouts")