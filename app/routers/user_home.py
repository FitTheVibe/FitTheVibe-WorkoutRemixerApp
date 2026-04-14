from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import status
from app.dependencies.session import SessionDep
from app.dependencies.auth import AuthDep, IsUserLoggedIn, get_current_user, is_admin
from app.repositories.workout_repository import WorkoutRepository
from app.repositories.routine_repository import RoutineRepository
from app.services.workout_service import WorkoutService
from app.services.routine_service import RoutineService
from . import router, templates
import json


@router.get("/app", response_class=HTMLResponse)
async def user_home_view(
    request: Request,
    user: AuthDep,
    db: SessionDep
):
    exercise_id = request.query_params.get('id')

    # Fetch workouts from database
    workout_service = WorkoutService(WorkoutRepository(db))
    workouts, _ = workout_service.get_all_workouts(page=1, limit=100)

    # Fetch user routines from database
    routine_service = RoutineService(
        RoutineRepository(db),
        None  # We'll fetch routine_workouts separately if needed
    )
    routines, _ = routine_service.get_user_routines(user.id, page=1, limit=100)

    # Convert to dictionaries for JSON serialization
    workouts_data = [
        {
            "id": str(w.id),
            "name": w.name,
            "category": w.muscle_group.capitalize(),
            "muscleGroups": [w.muscle_group.capitalize()],
            "difficulty": w.difficulty.capitalize(),
            "description": w.description,
            "equipment": w.equipment,
        }
        for w in workouts
    ]

    routines_data = [
        {
            "id": str(r.id),
            "name": r.name,
            "description": r.description,
            "createdAt": r.created_at.isoformat(),
        }
        for r in routines
    ]

    return templates.TemplateResponse(
        request=request,
        name="app.html",
        context={
            "user": user,
            "exercise_detail": bool(exercise_id),
            "exercise_id": exercise_id,
            "workouts_json": json.dumps(workouts_data),
            "routines_json": json.dumps(routines_data),
        }
    )