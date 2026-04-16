import logging
from sqlmodel import SQLModel, Session, create_engine, select
from app.config import get_settings
from contextlib import contextmanager

#from app.dependencies import session
from app.utilities.security import encrypt_password

from app.utilities.security import encrypt_password
#from app.dependencies import session


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

    def seed_users(session: Session):
        from app.models.user import User

        # Seed Bob (Admin)
        if not session.exec(select(User).where(User.username == "bob")).one_or_none():
            bob = User(
                username="bob",
                email="bob@mail.com",
                password=encrypt_password("bobpass"),
                role="admin"
            )
            session.add(bob)
            logger.info("Admin user bob seeded")

        # Seed John (Regular User)
        if not session.exec(select(User).where(User.username == "john")).one_or_none():
            john = User(
                username="john",
                email="john@mail.com",
                password=encrypt_password("johnpass"),
                role="regular_user"
            )
            session.add(john)
            logger.info("Regular user john seeded")
    
    session.commit()

def seed_workouts(session: Session):
    from app.models.workout import Workout

    if session.exec(select(Workout)).first():
        logger.info("Workouts already exist, skipping seed")
        return

    workouts = [
        Workout(name="Squats", description="Lower body compound movement", muscle_group="legs", difficulty="beginner", equipment="barbell", demo_img_url="https://media1.tenor.com/m/jAjshaoXrewAAAAd/sumo-squat-exercise.gif"),
        Workout(name="Lunges", description="Unilateral leg exercise", muscle_group="legs", difficulty="beginner", equipment="none", demo_img_url="https://media1.tenor.com/m/-YiEMDDCOwoAAAAd/afundo.gif"),
        Workout(name="Deadlifts", description="Full body posterior chain", muscle_group="legs", difficulty="intermediate", equipment="barbell", demo_img_url="https://media1.tenor.com/m/NgtmNzYYAzYAAAAd/deadlift-james-smith.gif"),
        Workout(name="Bench Press", description="Upper body pushing movement", muscle_group="chest", difficulty="intermediate", equipment="barbell", demo_img_url="https://media1.tenor.com/m/FxBO7P1kj6kAAAAd/gym.gif"),
        Workout(name="Push Ups", description="Bodyweight chest exercise", muscle_group="chest", difficulty="beginner", equipment="none", demo_img_url="https://media1.tenor.com/m/0PnchcCC_0QAAAAd/push-up.gif"),
        Workout(name="Pull Ups", description="Bodyweight back exercise", muscle_group="back", difficulty="intermediate", equipment="bar", demo_img_url="https://media1.tenor.com/m/G-a7AMKpQugAAAAd/pull-ups-nigel-sylvester.gif"),
        Workout(name="Bent Over Row", description="Compound back movement", muscle_group="back", difficulty="intermediate", equipment="barbell", demo_img_url="https://media1.tenor.com/m/-Z-hLGN30WAAAAAC/bentover-row.gif"),
        Workout(name="Shoulder Press", description="Overhead pressing movement", muscle_group="shoulders", difficulty="intermediate", equipment="dumbbells", demo_img_url="https://media1.tenor.com/m/uhxIEHzn7moAAAAd/shoulder-press-machine.gif"),
        Workout(name="Bicep Curls", description="Isolated bicep exercise", muscle_group="arms", difficulty="beginner", equipment="dumbbells", demo_img_url="https://media.tenor.com/EYrynVOuaZQAAAA1/supernaturalwriter-supernaturalwritertwitch.webp"),
        Workout(name="Tricep Dips", description="Bodyweight tricep exercise", muscle_group="arms", difficulty="beginner", equipment="bench", demo_img_url="https://media1.tenor.com/m/b5xcjuJpdi4AAAAC/brazosms.gif"),
        Workout(name="Plank", description="Core stability exercise", muscle_group="core", difficulty="beginner", equipment="none", demo_img_url="https://media1.tenor.com/m/7O6JimICFLoAAAAd/plank.gif"),
        Workout(name="Crunches", description="Abdominal exercise", muscle_group="core", difficulty="beginner", equipment="none", demo_img_url="https://media1.tenor.com/m/26blyZDE4a0AAAAd/exercise-twist.gif"),
    ]

    for workout in workouts:
        session.add(workout)
    
    session.commit()
    logger.info(f"Seeded {len(workouts)} workouts with image URLs")

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