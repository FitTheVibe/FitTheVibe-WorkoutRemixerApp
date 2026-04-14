import typer
from sqlmodel import select
from app.database import create_db_and_tables, get_cli_session, drop_all
from app.models.user import User
from app.models.workout import Workout
from app.models.routine import Routine
from app.models.routine_workout import RoutineWorkout
from app.utilities.security import encrypt_password

cli = typer.Typer()

@cli.command()
def initialize():
    with get_cli_session() as db:
        drop_all()
        create_db_and_tables()

        # seed users
        bob = User(username='bob', email='bob@mail.com', password=encrypt_password('bobpass'), role='admin')
        john = User(username='john', email='john@mail.com', password=encrypt_password('johnpass'), role='regular_user')
        db.add_all([bob, john])
        db.commit()

        # seed workouts
        workouts = [
            Workout(name="Squats", description="Lower body compound movement", muscle_group="legs", difficulty="beginner", equipment="barbell",demo_img_url="https://media1.tenor.com/m/jAjshaoXrewAAAAd/sumo-squat-exercise.gif"    ),
            Workout(name="Lunges", description="Unilateral leg exercise", muscle_group="legs", difficulty="beginner", equipment="none", demo_img_url="https://media1.tenor.com/m/-YiEMDDCOwoAAAAd/afundo.gif"    ),
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
        db.add_all(workouts)
        db.commit()
        print("Database initialized successfully")

if __name__ == "__main__":
    cli()