import logging
from sqlmodel import SQLModel, Session, create_engine, select
from app.config import get_settings
from contextlib import contextmanager

logger = logging.getLogger(__name__)

engine = create_engine(
    get_settings().database_uri, 
    echo=get_settings().env.lower() in ["dev", "development", "test", "testing", "staging"],
    pool_size=get_settings().db_pool_size,
    max_overflow=get_settings().db_additional_overflow,
    pool_timeout=get_settings().db_pool_timeout,
    pool_recycle=get_settings().db_pool_recycle,
)

def create_db_and_tables():
    from app.models.user import User
    from app.models.workout import Workout
    from app.models.routine import Routine
    from app.models.routine_workout import RoutineWorkout

    SQLModel.metadata.create_all(engine)
    
    with Session(engine) as session:
        seed_admin(session)
        seed_workouts(session)
        seed_users(session)

def seed_admin(session: Session):
    from app.models.user import User
    from app.utilities.security import encrypt_password

    existing = session.exec(select(User).where(User.username == "bob")).one_or_none()
    if not existing:
        admin = User(
            username="bob",
            email="bob@mail.com",
            password=encrypt_password("bobpass"),
            role="admin"
        )
        session.add(admin)
        session.commit()
        logger.info("Admin user bob seeded successfully")
    else:
        logger.info("Admin user bob already exists, skipping seed")


def seed_users(session: Session):
    from app.models.user import User
    from app.utilities.security import encrypt_password

    existing = session.exec(select(User).where(User.username == "john")).one_or_none()
    if not existing:
        user = User(
            username="john",
            email="john@mail.com",
            password=encrypt_password("johnpass"),
            role="regular_user"
        )
        session.add(user)
        session.commit()
        logger.info("User john seeded successfully")
    else:
        logger.info("User john already exists, skipping seed")


def seed_workouts(session: Session):
    from app.models.workout import Workout
    from app.models.user import User

    bob = session.exec(select(User).where(User.username == "bob")).one_or_none()
    if not bob:
        logger.error("Admin user bob not found, cannot seed workouts")
        return
    
 
    existing = session.exec(select(Workout)).first()
    if existing:
        logger.info("Workouts already seeded, skipping")
        return

    workouts = [
       
        Workout(name="Squats", created_by= bob.id, description="Lower body compound movement", muscle_group="legs", difficulty="beginner", equipment="barbell",demo_img_url="https://media1.tenor.com/m/jAjshaoXrewAAAAd/sumo-squat-exercise.gif"    ),
            Workout(name="Lunges", created_by= bob.id, description="Unilateral leg exercise", muscle_group="legs", difficulty="beginner", equipment="none", demo_img_url="https://media1.tenor.com/m/-YiEMDDCOwoAAAAd/afundo.gif"    ),
            Workout(name="Deadlifts", created_by= bob.id, description="Full body posterior chain", muscle_group="legs", difficulty="intermediate", equipment="barbell", demo_img_url="https://media1.tenor.com/m/NgtmNzYYAzYAAAAd/deadlift-james-smith.gif"),
            Workout(name="Bench Press", created_by= bob.id, description="Upper body pushing movement", muscle_group="chest", difficulty="intermediate", equipment="barbell", demo_img_url="https://media1.tenor.com/m/FxBO7P1kj6kAAAAd/gym.gif"),
            Workout(name="Push Ups", created_by= bob.id, description="Bodyweight chest exercise", muscle_group="chest", difficulty="beginner", equipment="none", demo_img_url="https://media1.tenor.com/m/0PnchcCC_0QAAAAd/push-up.gif"),
            Workout(name="Pull Ups", created_by= bob.id, description="Bodyweight back exercise", muscle_group="back", difficulty="intermediate", equipment="bar", demo_img_url="https://media1.tenor.com/m/G-a7AMKpQugAAAAd/pull-ups-nigel-sylvester.gif"),
            Workout(name="Bent Over Row", created_by= bob.id, description="Compound back movement", muscle_group="back", difficulty="intermediate", equipment="barbell", demo_img_url="https://media1.tenor.com/m/-Z-hLGN30WAAAAAC/bentover-row.gif"),
            Workout(name="Shoulder Press", created_by= bob.id, description="Overhead pressing movement", muscle_group="shoulders", difficulty="intermediate", equipment="dumbbells", demo_img_url="https://media1.tenor.com/m/uhxIEHzn7moAAAAd/shoulder-press-machine.gif"),
            Workout(name="Bicep Curls", created_by= bob.id, description="Isolated bicep exercise", muscle_group="arms", difficulty="beginner", equipment="dumbbells", demo_img_url="https://media.tenor.com/EYrynVOuaZQAAAA1/supernaturalwriter-supernaturalwritertwitch.webp"),
            Workout(name="Tricep Dips", created_by= bob.id, description="Bodyweight tricep exercise", muscle_group="arms", difficulty="beginner", equipment="bench", demo_img_url="https://media1.tenor.com/m/b5xcjuJpdi4AAAAC/brazosms.gif"),
            Workout(name="Plank", created_by= bob.id, description="Core stability exercise", muscle_group="core", difficulty="beginner", equipment="none", demo_img_url="https://media1.tenor.com/m/7O6JimICFLoAAAAd/plank.gif"),
            Workout(name="Crunches", created_by= bob.id, description="Abdominal exercise", muscle_group="core", difficulty="beginner", equipment="none", demo_img_url="https://media1.tenor.com/m/26blyZDE4a0AAAAd/exercise-twist.gif"),
    ]

    for workout in workouts:
        session.add(workout)
    session.commit()
    logger.info(f"Seeded {len(workouts)} workouts successfully")

def drop_all():
    SQLModel.metadata.drop_all(bind=engine)
    
def _session_generator():
    with Session(engine) as session:
        try:
            yield session
        except Exception as e:
            logger.error(f"Database session error: {e}")
            raise
        finally:
            session.close()

def get_session():
    yield from _session_generator()

@contextmanager
def get_cli_session():
    yield from _session_generator()