from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime, timezone

if TYPE_CHECKING:
    from app.models.routine_workout import RoutineWorkout

class RoutineBase(SQLModel):
    name: str
    description: str

class Routine(RoutineBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    routine_workouts: List["RoutineWorkout"] = Relationship(back_populates="routine")