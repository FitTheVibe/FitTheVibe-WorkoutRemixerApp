import typer
from sqlmodel import select
from tabulate import tabulate
from app.database import create_db_and_tables, get_cli_session, drop_all
from app.models.user import User
from app.models.workout import Workout
from app.models.routine import Routine
from app.models.routine_workout import RoutineWorkout
from app.utilities.security import encrypt_password

cli = typer.Typer()

@cli.command()
def initialize():
    print("Dropping all tables...")
    drop_all()
    
    print("Creating tables and seeding data...")
    create_db_and_tables() 
    
    print("Database initialized successfully!")

if __name__ == "__main__":
    cli()