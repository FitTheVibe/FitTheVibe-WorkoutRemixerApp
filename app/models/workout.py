from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.routineworkout import RoutineWorkout

class Workout(SQLModel, table=True):
    id : Optional[int] = Field(default=None, primary_key=True)
    created_by: Optional[int] = Field(default=None, foreign_key="user.id")
    name: str
    description: str
    muscle_group: str
    difficulty: str
    equipment: str
    workout_entries: List["RoutineWorkout"] = Relationship(back_populates="workout")