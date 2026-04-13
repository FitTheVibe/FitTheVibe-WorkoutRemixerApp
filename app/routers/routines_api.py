from fastapi import Request, HTTPException, status, Query
from app.dependencies import SessionDep, AuthDep
from app.repositories.routine_repository import RoutineRepository
from app.repositories.routine_workout_repository import RoutineWorkoutRepository
from app.services.routine_service import RoutineService
from app.schemas.workout_routines_schemas import (
    RoutineCreate, RoutineUpdate, RoutineResponse, RoutineDetailResponse,
    RoutineWorkoutAdd, RoutineWorkoutUpdate, RoutineWorkoutResponse,
    RemixRequest,
)
from . import api_router


def _get_service(db) -> RoutineService:
    return RoutineService(RoutineRepository(db), RoutineWorkoutRepository(db))

def _assert_owner(routine, user):
    if routine.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not your routine")


# ── Routines CRUD ─────────────────────────────────────────────────────────────

@api_router.get("/routines", response_model=list[RoutineResponse])
async def list_routines(
    request: Request,
    db: SessionDep,
    user: AuthDep,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, le=100),
):
    service = _get_service(db)
    routines, _ = service.get_user_routines(user.id, page=page, limit=limit)
    return routines


@api_router.get("/routines/{routine_id}", response_model=RoutineDetailResponse)
async def get_routine(request: Request, routine_id: int, db: SessionDep, user: AuthDep):
    service = _get_service(db)
    routine = service.get_routine(routine_id)
    if not routine:
        raise HTTPException(status_code=404, detail="Routine not found")
    _assert_owner(routine, user)

    rws = service.get_routine_workouts(routine_id)
    result = RoutineDetailResponse.model_validate(routine)
    result.routine_workouts = [
        RoutineWorkoutResponse(
            id=rw.id,
            workout_id=rw.workout_id,
            position=rw.position,
            sets=rw.sets,
            reps=rw.reps,
            workout=rw.workout,
        )
        for rw in rws
    ]
    return result


@api_router.post("/routines", response_model=RoutineResponse, status_code=status.HTTP_201_CREATED)
async def create_routine(request: Request, data: RoutineCreate, db: SessionDep, user: AuthDep):
    service = _get_service(db)
    return service.create_routine(data, user_id=user.id)


@api_router.patch("/routines/{routine_id}", response_model=RoutineResponse)
async def update_routine(request: Request, routine_id: int, data: RoutineUpdate, db: SessionDep, user: AuthDep):
    service = _get_service(db)
    routine = service.get_routine(routine_id)
    if not routine:
        raise HTTPException(status_code=404, detail="Routine not found")
    _assert_owner(routine, user)
    return service.update_routine(routine_id, data)


@api_router.delete("/routines/{routine_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_routine(request: Request, routine_id: int, db: SessionDep, user: AuthDep):
    service = _get_service(db)
    routine = service.get_routine(routine_id)
    if not routine:
        raise HTTPException(status_code=404, detail="Routine not found")
    _assert_owner(routine, user)
    service.delete_routine(routine_id)


# ── Workout entries within a routine ─────────────────────────────────────────

@api_router.post("/routines/{routine_id}/workouts", response_model=RoutineWorkoutResponse, status_code=status.HTTP_201_CREATED)
async def add_workout_to_routine(request: Request, routine_id: int, data: RoutineWorkoutAdd, db: SessionDep, user: AuthDep):
    service = _get_service(db)
    routine = service.get_routine(routine_id)
    if not routine:
        raise HTTPException(status_code=404, detail="Routine not found")
    _assert_owner(routine, user)
    try:
        rw = service.add_workout(routine_id, data)
        return RoutineWorkoutResponse(
            id=rw.id, workout_id=rw.workout_id,
            position=rw.position, sets=rw.sets, reps=rw.reps,
            workout=rw.workout,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@api_router.patch("/routines/{routine_id}/workouts/{rw_id}", response_model=RoutineWorkoutResponse)
async def update_routine_workout(request: Request, routine_id: int, rw_id: int, data: RoutineWorkoutUpdate, db: SessionDep, user: AuthDep):
    service = _get_service(db)
    routine = service.get_routine(routine_id)
    if not routine:
        raise HTTPException(status_code=404, detail="Routine not found")
    _assert_owner(routine, user)
    rw = service.update_routine_workout(rw_id, data)
    if not rw:
        raise HTTPException(status_code=404, detail="Entry not found")
    return RoutineWorkoutResponse(
        id=rw.id, workout_id=rw.workout_id,
        position=rw.position, sets=rw.sets, reps=rw.reps,
        workout=rw.workout,
    )


@api_router.delete("/routines/{routine_id}/workouts/{rw_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_workout_from_routine(request: Request, routine_id: int, rw_id: int, db: SessionDep, user: AuthDep):
    service = _get_service(db)
    routine = service.get_routine(routine_id)
    if not routine:
        raise HTTPException(status_code=404, detail="Routine not found")
    _assert_owner(routine, user)
    try:
        service.remove_workout(rw_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


# ── Remix ─────────────────────────────────────────────────────────────────────

@api_router.post("/routines/{routine_id}/remix", response_model=RoutineWorkoutResponse)
async def remix_routine(request: Request, routine_id: int, payload: RemixRequest, db: SessionDep, user: AuthDep):
    """Swap one workout for another in a routine. Muscle group must match."""
    service = _get_service(db)
    routine = service.get_routine(routine_id)
    if not routine:
        raise HTTPException(status_code=404, detail="Routine not found")
    _assert_owner(routine, user)
    try:
        rw = service.remix(routine_id, payload.old_workout_id, payload.new_workout_id)
        return RoutineWorkoutResponse(
            id=rw.id, workout_id=rw.workout_id,
            position=rw.position, sets=rw.sets, reps=rw.reps,
            workout=rw.workout,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))