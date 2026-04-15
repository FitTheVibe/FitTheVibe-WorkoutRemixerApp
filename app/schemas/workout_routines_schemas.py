from sqlmodel import SQLModel
from typing import Optional
from datetime import datetime


#Workout Schemas
class WorkoutCreate(SQLModel):
    name: str
    description: str
    muscle_group: str
    difficulty: str
    equipment: str
    demo_img_url: Optional[str] = None

class WorkoutUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
    muscle_group: Optional[str] = None
    difficulty: Optional[str] = None
    equipment: Optional[str] = None
    demo_img_url: Optional[str] = None


class WorkoutResponse(SQLModel):
    id: int
    name: str
    description: str
    muscle_group: str
    difficulty: str
    equipment: str
    created_by: Optional[int]
    demo_img_url: Optional[str]


#Routine Schemas
class RoutineCreate(SQLModel):
    name: str
    description: str

class RoutineUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None

class RoutineResponse(SQLModel):
    id: int
    name: str
    description: str
    created_at: datetime
    user_id: Optional[int]


#RoutineWorkout Schemas
class RoutineWorkoutAdd(SQLModel):
    workout_id: int
    position: int = 0
    sets: int = 3
    reps: int = 10

class RoutineWorkoutUpdate(SQLModel):
    position: Optional[int] = None
    sets: Optional[int] = None
    reps: Optional[int] = None

class RoutineWorkoutResponse(SQLModel):
    id: int
    workout_id: int
    position: int
    sets: int
    reps: int
    workout: Optional[WorkoutResponse] = None

class RoutineDetailResponse(RoutineResponse):
    routine_workouts: list[RoutineWorkoutResponse] = []

#Remix Schema
class RemixRequest(SQLModel):
    old_workout_id: int
    new_workout_id: int