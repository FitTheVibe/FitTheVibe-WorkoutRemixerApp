from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from app.models.routineworkout import RoutineWorkout

class Routine(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    name: str
    description: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    workouts: List["RoutineWorkout"] = Relationship(back_populates="routine")

