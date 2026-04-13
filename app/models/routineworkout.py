from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.routine import Routine
    from app.models.workout import Workout

class RoutineWorkout(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    routine_id: Optional[int] = Field(default=None, foreign_key="routine.id")
    workout_id: Optional[int] = Field(default=None, foreign_key="workout.id")
    position: int 
    sets: Optional[int] = None
    reps: Optional[int] = None

    routine: Optional["Routine"] = Relationship(back_populates="workouts")
    workout: Optional["Workout"] = Relationship(back_populates="workout_entries")
    
    