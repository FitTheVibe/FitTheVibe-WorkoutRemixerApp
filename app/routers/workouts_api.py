from fastapi import Request, HTTPException, status, Query, UploadFile, File, Depends
from fastapi.responses import JSONResponse
from typing import Optional
from app.dependencies import SessionDep, AuthDep, AdminDep
from app.repositories.workout_repository import WorkoutRepository
from app.services.workout_service import WorkoutService
from app.schemas.workout_routines_schemas import WorkoutCreate, WorkoutUpdate, WorkoutResponse
from . import api_router
import uuid
from pathlib import Path


# ── Browse workouts (any authenticated user) ──────────────────────────────────

@api_router.get("/workouts", response_model=list[WorkoutResponse])
async def list_workouts(
    request: Request,
    db: SessionDep,
    user: AuthDep,
    muscle_group: Optional[str] = Query(default=None),
    difficulty: Optional[str] = Query(default=None),
    equipment: Optional[str] = Query(default=None),
    search: Optional[str] = Query(default=None),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, le=200),
):
    service = WorkoutService(WorkoutRepository(db))
    workouts, _ = service.get_all_workouts(
        page=page, limit=limit,
        muscle_group=muscle_group, difficulty=difficulty,
        equipment=equipment, search=search,
    )
    return workouts


@api_router.get("/workouts/{workout_id}", response_model=WorkoutResponse)
async def get_workout(request: Request, workout_id: int, db: SessionDep, user: AuthDep):
    service = WorkoutService(WorkoutRepository(db))
    workout = service.get_workout(workout_id)
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    return workout


@api_router.get("/workouts/{workout_id}/alternatives", response_model=list[WorkoutResponse])
async def get_workout_alternatives(request: Request, workout_id: int, db: SessionDep, user: AuthDep):
    """Returns workouts in the same muscle group — used to power the remix picker."""
    service = WorkoutService(WorkoutRepository(db))
    if not service.get_workout(workout_id):
        raise HTTPException(status_code=404, detail="Workout not found")
    return service.get_alternatives(workout_id)


# ── Admin-only: create, update, delete ───────────────────────────────────────

@api_router.post("/workouts", response_model=WorkoutResponse, status_code=status.HTTP_201_CREATED)
async def create_workout(request: Request, data: WorkoutCreate, db: SessionDep, user: AdminDep):
    service = WorkoutService(WorkoutRepository(db))
    return service.create_workout(data, created_by=user.id)


@api_router.patch("/workouts/{workout_id}", response_model=WorkoutResponse)
async def update_workout(request: Request, workout_id: int, data: WorkoutUpdate, db: SessionDep, user: AdminDep):
    service = WorkoutService(WorkoutRepository(db))
    workout = service.update_workout(workout_id, data)
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    return workout


@api_router.delete("/workouts/{workout_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_workout(request: Request, workout_id: int, db: SessionDep, user: AdminDep):
    service = WorkoutService(WorkoutRepository(db))
    if not service.get_workout(workout_id):
        raise HTTPException(status_code=404, detail="Workout not found")
    service.delete_workout(workout_id)


# ── File upload endpoint ─────────────────────────────────────────────────────

@api_router.post("/workouts/upload")
async def upload_workout_image(user: AdminDep, file: UploadFile = File(...)):
    """Upload a workout exercise image. Returns the URL to be stored in demo_img_url."""
    try:
        # Validate file type
        allowed_types = {"image/jpeg", "image/png", "image/webp", "image/gif"}
        if file.content_type not in allowed_types:
            raise HTTPException(status_code=400, detail="Invalid file type. Only JPEG, PNG, WebP, and GIF are allowed.")

        # Validate file size (max 5MB)
        contents = await file.read()
        if len(contents) > 5 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="File size exceeds 5MB limit.")

        # Create uploads directory if it doesn't exist
        uploads_dir = Path("app/static/uploads")
        uploads_dir.mkdir(parents=True, exist_ok=True)

        # Generate unique filename
        file_ext = Path(file.filename).suffix
        unique_filename = f"{uuid.uuid4()}{file_ext}"
        file_path = uploads_dir / unique_filename

        # Save file
        with open(file_path, "wb") as f:
            f.write(contents)

        # Return URL path for storage in database
        url = f"static/uploads/{unique_filename}"
        return JSONResponse(content={"url": url}, status_code=200)

    except HTTPException:
        raise
    except Exception as e:
        print(f"Upload error: {e}")
        raise HTTPException(status_code=500, detail="Failed to upload file")