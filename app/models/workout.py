from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.routine_workout import RoutineWorkout

class WorkoutBase(SQLModel):
    name: str
    description: str
    muscle_group: str   # e.g. "chest", "legs", "back"
    difficulty: str     # e.g. "beginner", "intermediate", "advanced"
    equipment: str      # e.g. "none", "dumbbells", "barbell"
    demo_img_url: str

class Workout(WorkoutBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_by: Optional[int] = Field(default=None, foreign_key="user.id")

    routine_workouts: List["RoutineWorkout"] = Relationship(back_populates="workout")